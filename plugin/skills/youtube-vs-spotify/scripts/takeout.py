"""Read a Google Takeout YouTube history export (zip or folder, JSON or English HTML).

Returns watch rows and search rows with timezone-aware local timestamps.
Stdlib only, so it runs on any Python 3.9+.
"""
import atexit
import html as htmlmod
import shutil
import json
import os
import re
import tempfile
import zipfile
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo


def system_tz():
    """IANA name of this machine's zone, or UTC."""
    tz = os.environ.get('TZ')
    if tz:
        return tz
    try:
        p = os.path.realpath('/etc/localtime')
        if 'zoneinfo/' in p:
            return p.split('zoneinfo/', 1)[1]
    except OSError:
        pass
    return 'UTC'


def find_history(path):
    """Return the folder holding watch-history.(json|html), extracting a zip if needed."""
    if path.endswith('.zip'):
        out = tempfile.mkdtemp(prefix='mustory-yt-')
        atexit.register(shutil.rmtree, out, True)  # never leave copies of private history behind
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if re.search(r'(watch|search)-history\.(json|html)$', n)]
            if not names:
                raise SystemExit('No watch-history.json or watch-history.html inside the zip. '
                                 'Export again with YouTube "history" included.')
            for n in names:
                z.extract(n, out)
        path = out
    for root, _, files in os.walk(path):
        if any(f.startswith('watch-history.') for f in files):
            return root
    raise SystemExit(f'No watch-history file found under {path}')


VID = re.compile(r'[?&]v=([\w-]{11})')


def _strip_prefix(items, url_key):
    """Takeout titles carry a localized prefix ("Watched ", "Вы посмотрели: ").
    Learn it from entries whose title is just prefix + URL (deleted videos), else
    from the longest common prefix of all titles."""
    for x in items:
        u, t = x.get(url_key, ''), x.get('title', '')
        if u and t.endswith(u) and len(t) > len(u):
            return t[:-len(u)]
    titles = [x.get('title', '') for x in items[:500] if x.get('title')]
    if not titles:
        return ''
    p = os.path.commonprefix(titles)
    return p[:p.rfind(' ') + 1] if ' ' in p else ''


def _is_ad(x):
    return bool(x.get('details'))  # Takeout marks ad plays with a "details" block ("From Google Ads")


def load_json(folder, tz):
    w = json.load(open(os.path.join(folder, 'watch-history.json'), encoding='utf-8'))
    ads = sum(1 for x in w if _is_ad(x))
    w = [x for x in w if not _is_ad(x)]
    pre = _strip_prefix(w, 'titleUrl')
    rows = []
    for x in w:
        m = VID.search(x.get('titleUrl', ''))
        if not m:
            continue  # posts, stories, surveys
        t = x['title'][len(pre):] if x['title'].startswith(pre) else x['title']
        sub = (x.get('subtitles') or [{}])[0]
        rows.append(_row(m.group(1), t, sub.get('name'), sub.get('url'), x['time'], tz,
                         x.get('header') == 'YouTube Music'))
    searches = []
    sp = os.path.join(folder, 'search-history.json')
    if os.path.exists(sp):
        for x in json.load(open(sp, encoding='utf-8')):
            if _is_ad(x):
                continue
            q = parse_qs(urlparse(x.get('titleUrl', '')).query).get('search_query')
            if q:
                searches.append(dict(q=q[0], ts=_ts(x['time'], tz)))
    return _finish(rows, searches, ads)


def _ts(iso, tz):
    return datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(tz)


def _row(v, title, ch, chu, iso_or_dt, tz, music):
    ts = iso_or_dt if isinstance(iso_or_dt, datetime) else _ts(iso_or_dt, tz)
    removed = title.startswith('https://') or not title.strip()
    return dict(v=v, title=title, removed=removed, ch=None if removed else ch, chu=chu, ts=ts, music=music)


CELL = re.compile(r'<div class="content-cell[^"]*body-1">(.*?)</div>', re.S)
HDATE = re.compile(r'([A-Z][a-z]{2} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s*[AP]M)\s*(GMT[+-]\d{2}:\d{2}|GMT|UTC|[A-Z]{2,5})?')

HDATE_UK = re.compile(r'(\d{1,2} [A-Z][a-z]{2,3} \d{4}, \d{1,2}:\d{2}:\d{2})\s*(GMT[+-]\d{2}:\d{2}|GMT|UTC|[A-Z]{2,5})?')


def _hdate(s, tz):
    m = HDATE.search(s.replace(' ', ' ').replace('\xa0', ' '))
    if m:
        dt = datetime.strptime(m.group(1).replace('  ', ' '), '%b %d, %Y, %I:%M:%S %p')
    else:  # UK/other English style: "24 Sept 2026, 13:20:53"
        m = HDATE_UK.search(s.replace(' ', ' ').replace('\xa0', ' '))
        if not m:
            return None
        dt = datetime.strptime(re.sub(r'\bSept\b', 'Sep', m.group(1)), '%d %b %Y, %H:%M:%S')
    off = m.group(2) or ''
    om = re.match(r'GMT([+-])(\d{2}):(\d{2})', off)
    if om:
        sign = 1 if om.group(1) == '+' else -1
        from datetime import timedelta
        dt = dt.replace(tzinfo=timezone(sign * timedelta(hours=int(om.group(2)), minutes=int(om.group(3)))))
    elif off in ('GMT', 'UTC'):
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.replace(tzinfo=tz)  # named abbreviations are ambiguous; assume the chosen zone
    return dt.astimezone(tz)


def load_html(folder, tz):
    t = open(os.path.join(folder, 'watch-history.html'), encoding='utf-8').read()
    rows, ads, bad = [], 0, 0
    for outer in t.split('<div class="outer-cell')[1:]:
        if '<b>Details:</b>' in outer:  # ad plays ("From Google Ads")
            ads += 1
            continue
        cells = CELL.findall(outer)
        if not cells:
            continue
        c = cells[0]
        links = re.findall(r'<a href="([^"]+)">([^<]*)</a>', c)
        m = VID.search(links[0][0]) if links else None
        ts = _hdate(c, tz)
        if not m or not ts:
            bad += 1
            continue
        title = htmlmod.unescape(links[0][1])
        ch = htmlmod.unescape(links[1][1]) if len(links) > 1 and '/channel/' in links[1][0] else None
        rows.append(_row(m.group(1), title, ch, links[1][0] if ch else None, ts, tz, 'YouTube Music<br>' in outer[:400]))
    if rows == [] and bad:
        raise SystemExit('Could not read dates in watch-history.html (probably a non-English export). '
                         'Export again choosing JSON as the history format.')
    searches = []
    sp = os.path.join(folder, 'search-history.html')
    if os.path.exists(sp):
        for outer in open(sp, encoding='utf-8').read().split('<div class="outer-cell')[1:]:
            cells = CELL.findall(outer)
            if '<b>Details:</b>' in outer or not cells:
                continue
            c = cells[0]
            a = re.search(r'<a href="([^"]+)">', c)
            ts = _hdate(c, tz)
            q = parse_qs(urlparse(htmlmod.unescape(a.group(1))).query).get('search_query') if a else None
            if q and ts:
                searches.append(dict(q=q[0], ts=ts))
    return _finish(rows, searches, ads)


def _finish(rows, searches, ads):
    rows.sort(key=lambda r: r['ts'])
    searches.sort(key=lambda r: r['ts'])
    return rows, searches, dict(ads_excluded=ads)


def load(path, tz_name):
    tz = ZoneInfo(tz_name)
    folder = find_history(path)
    if os.path.exists(os.path.join(folder, 'watch-history.json')):
        return load_json(folder, tz)
    return load_html(folder, tz)
