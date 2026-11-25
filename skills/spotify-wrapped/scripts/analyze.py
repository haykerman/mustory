"""Compute every statistic the Spotify Wrapped page shows.

python3 analyze.py --export <my_spotify_data.zip|folder> --work <dir> [--tz Europe/Berlin] [--today 2026-11-24] [--southern]

Writes into --work: data.json (page data), facts.md (the only source of numbers for story.json),
artists.tsv (top artists for labels/moods), odd_candidates.tsv (one-off listens).
Reads from --work if present: labels.json, moods.json (see SKILL.md).

Definitions used everywhere:
  listen      = a music stream of 30 seconds or more (Spotify's own threshold for a play)
  quick skip  = a stream ended by the next button before 30 seconds
  hours       = listening time with overlaps removed (two devices at once count once)
"""
import argparse
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spotify import load, system_tz  # noqa: E402

FUNCTIONAL_RX = re.compile(r'focus|concentrat|brain ?waves?|brain boost|alpha waves|theta waves|delta waves|solfeggio|\bsleep(ing)?\b|meditat|binaural|white noise|brown noise|pink noise|rain sounds|\bstudy|adhd|\d+\s?hz|'
                           r'deep work|relaxing|lullab|ambient noise|nature sounds|asmr', re.I)
PICKED = {'clickrow', 'playbtn', 'click-row', 'popup'}
COUNTRY = {'AM': 'Armenia', 'US': 'United States', 'GB': 'United Kingdom', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain',
           'NL': 'Netherlands', 'CZ': 'Czechia', 'PL': 'Poland', 'AT': 'Austria', 'CH': 'Switzerland', 'RU': 'Russia', 'UA': 'Ukraine',
           'GE': 'Georgia', 'TR': 'Türkiye', 'AE': 'UAE', 'HK': 'Hong Kong', 'JP': 'Japan', 'KR': 'South Korea', 'CN': 'China', 'TH': 'Thailand',
           'ME': 'Montenegro', 'RS': 'Serbia', 'GR': 'Greece', 'PT': 'Portugal', 'CA': 'Canada', 'MX': 'Mexico', 'BR': 'Brazil', 'AR': 'Argentina',
           'IN': 'India', 'ID': 'Indonesia', 'SG': 'Singapore', 'AU': 'Australia', 'NZ': 'New Zealand', 'EG': 'Egypt', 'IL': 'Israel', 'CY': 'Cyprus',
           'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland', 'BE': 'Belgium', 'IE': 'Ireland', 'HU': 'Hungary', 'RO': 'Romania',
           'BG': 'Bulgaria', 'HR': 'Croatia', 'KZ': 'Kazakhstan', 'BY': 'Belarus', 'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia', 'QA': 'Qatar'}
SEASON_N = {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
SEASON_NAMES = ['Winter', 'Spring', 'Summer', 'Fall']


def short(t, n=70):
    t = t or ''
    return t if len(t) <= n else t[:n - 1] + '…'


def hrs(ms):
    return round(ms / 3.6e6, 1) if ms < 3.6e7 else round(ms / 3.6e6)


def pct(a, b):
    return round(100 * a / b) if b else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--export', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--tz', default=system_tz())
    ap.add_argument('--today')
    ap.add_argument('--southern', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    tz = ZoneInfo(a.tz)
    rows, export_kind = load(a.export, a.tz)
    if not rows:
        raise SystemExit('No streams found.')
    today = datetime.fromisoformat(a.today).replace(tzinfo=tz) if a.today else datetime.now(tz)
    lp, mp = os.path.join(a.work, 'labels.json'), os.path.join(a.work, 'moods.json')
    labels = json.load(open(lp, encoding='utf-8')) if os.path.exists(lp) else {}
    moods = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}
    functional_artists = {x.lower() for x in labels.get('functional', [])}
    not_functional = {x.lower() for x in labels.get('not_functional', [])}

    music = [r for r in rows if r['kind'] == 'track']
    # Focus/sleep audio is decided per artist: labeled by hand, or most of the artist's tracks look like it.
    # One song title ("Go To Sleep", "Focus") must not pull a whole band out of the taste sections.
    hits, tot_a, kinds = Counter(), Counter(), defaultdict(set)
    for r in music:
        tot_a[r['artist']] += 1
        if FUNCTIONAL_RX.search(r['track']):
            hits[r['artist']] += 1
            kinds[r['artist']].add(r['track'].casefold())
    # Titles decide; a name like "Deep Sleep Waves" only counts when some titles agree ("Arms and Sleepers", "Sleep Token" stay music).
    # ...and it takes 2+ different focus-like titles: one song called "Sleep" doesn't make a band a sleep channel.
    func_set = {x for x in tot_a if (x.lower() in functional_artists or (len(kinds[x]) >= 2 and (hits[x] / tot_a[x] >= 0.6 or
                                     (FUNCTIONAL_RX.search(x) and hits[x] / tot_a[x] >= 0.3)))) and x.lower() not in not_functional}
    for r in music:
        # One song can have several Spotify IDs (single, album, remaster): count it as one.
        r['uri'] = r['track'].strip().casefold() + '\u241f' + r['artist'].strip().casefold()
        r['listen'] = r['ms'] >= 30000
        r['qskip'] = r['re'] == 'fwdbtn' and r['ms'] < 30000 if export_kind == 'extended' else r['ms'] < 30000
        r['func'] = r['artist'] in func_set
    listens = [r for r in music if r['listen']]
    # Taste sections (songs, eras, loops, seasons, flings, rituals, drift) leave focus/sleep audio out.
    # Totals, hours, devices, time of day and the focus chapter keep everything.
    mnf = [r for r in music if not r['func']]
    lnf = [r for r in mnf if r['listen']]
    scale = max(0.1, len(listens) / 60000)

    def pl(n, word):
        return f"{n:,} {word}{'' if n == 1 else 's'}"

    def th(base, lo):
        return max(lo, round(base * scale))
    d = lambda ts: ts.strftime('%Y-%m-%d')  # noqa: E731
    years = list(range(rows[0]['start'].year, rows[-1]['start'].year + 1))
    ext = export_kind == 'extended'
    D, F = {}, []
    D['meta'] = dict(tz=a.tz, today=d(today), export=export_kind, southern=a.southern)

    # ---------- totals
    days = Counter(r['start'].date() for r in music)
    ds = sorted(days)
    best = cur = 1
    streak_end = ds[0]
    for x, y in zip(ds, ds[1:]):
        cur = cur + 1 if (y - x).days == 1 else 1
        if cur > best:
            best, streak_end = cur, y
    tot_ms = sum(r['eff'] for r in music)
    tracks = {r['uri'] for r in listens}
    T = dict(hours=round(tot_ms / 3.6e6), days_of_music=round(tot_ms / 8.64e7, 1), streams=len(music), listens=len(listens),
             tracks=len(tracks), artists=len({r['artist'] for r in listens}), albums=len({(r['album'], r['artist']) for r in listens if r['album']}),
             active_days=len(days), streak=best, streak_end=str(streak_end), streak_start=str(streak_end - timedelta(days=best - 1)),
             first=rows[0]['start'].isoformat(), first_track=f"{rows[0]['artist']} – {rows[0]['track']}",
             last=rows[-1]['start'].isoformat(), last_track=f"{rows[-1]['artist']} – {rows[-1]['track']}",
             quick_skips=sum(r['qskip'] for r in music), incognito=sum(r['incognito'] for r in rows), offline=sum(r['offline'] for r in rows),
             episodes=sum(1 for r in rows if r['kind'] == 'episode'), episode_hours=hrs(sum(r['eff'] for r in rows if r['kind'] == 'episode')),
             videos=sum(1 for r in rows if r['kind'] == 'video'), audiobook_hours=hrs(sum(r['eff'] for r in rows if r['kind'] == 'audiobook')),
             raw_hours=round(sum(r['ms'] for r in music) / 3.6e6))
    D['totals'] = T
    F.append('## Totals')
    F.append(f"- {T['hours']:,} hours of music ({T['days_of_music']} days), {T['listens']:,} listens (30 s+) out of {T['streams']:,} streams. "
             f"{T['tracks']:,} different tracks, {T['artists']:,} artists, {T['albums']:,} albums. Export type: {export_kind}.")
    F.append(f"- Raw ms_played adds up to {T['raw_hours']:,} hours; {T['raw_hours'] - T['hours']:,} of those overlap with another stream (two devices or a stream left running) and are not counted.")
    F.append(f"- First stream: {T['first'][:16]} {T['first_track']}. Last: {T['last'][:16]} {T['last_track']}.")
    F.append(f"- Days with music: {T['active_days']:,}. Longest daily streak: {T['streak']} days ({T['streak_start']} to {T['streak_end']}).")
    F.append(f"- Quick skips (next before 30 s): {T['quick_skips']:,} ({pct(T['quick_skips'], T['streams'])}% of streams). "
             f"Offline streams: {T['offline']:,}. Private-session streams: {T['incognito']:,} (never list what they were).")
    extra = [f"Podcasts: {T['episodes']:,} episode streams, {T['episode_hours']} hours" if T['episodes'] else '',
             f"Videos: {T['videos']:,}" if T['videos'] else '', f"Audiobooks: {T['audiobook_hours']} hours" if T['audiobook_hours'] else '']
    if any(extra):
        F.append('- ' + '. '.join(x for x in extra if x) + '.')

    # ---------- monthly and yearly
    mh, mq, ms_ = Counter(), Counter(), Counter()
    for r in music:
        k = r['start'].strftime('%Y-%m')
        mh[k] += r['eff']
        ms_[k] += 1
        mq[k] += r['qskip']
    y, m = rows[0]['start'].year, rows[0]['start'].month
    D['monthly'] = []
    while (y, m) <= (rows[-1]['start'].year, rows[-1]['start'].month):
        k = f'{y}-{m:02d}'
        D['monthly'].append([k, round(mh[k] / 3.6e6, 1), round(mq[k] / ms_[k], 3) if ms_[k] else 0])
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    first_seen = {}
    for r in listens:
        first_seen.setdefault(r['artist'], r['start'].year)
    YR = {}
    F.append('\n## By year')
    for yy in years:
        rs = [r for r in music if r['start'].year == yy]
        if not rs:
            continue
        ls = [r for r in rs if r['listen']]
        h = sum(r['eff'] for r in rs)
        new_h = sum(r['eff'] for r in rs if first_seen.get(r['artist']) == yy)
        YR[yy] = dict(hours=round(h / 3.6e6), listens=len(ls), skip=round(sum(r['qskip'] for r in rs) / len(rs), 3),
                      shuffle=round(sum(bool(r['shuffle']) for r in rs) / len(rs), 3) if ext else None,
                      picked=round(sum(r['rs'] in PICKED for r in rs) / len(rs), 3) if ext else None,
                      new_artists=sum(1 for v in first_seen.values() if v == yy), new_share=round(new_h / h, 3) if h else 0,
                      func_hours=round(sum(r['eff'] for r in rs if r['func']) / 3.6e6), night=round(sum(r['eff'] for r in rs if r['start'].hour < 5) / h, 3) if h else 0)
        v = YR[yy]
        F.append(f"- {yy}: {v['hours']:,} hours, {v['listens']:,} listens, quick-skip rate {pct(v['skip'], 1)}%" +
                 (f", shuffle {pct(v['shuffle'], 1)}%, picked on purpose {round(v['picked'] * 100, 1)}%" if ext else '') +
                 (', first year (every artist is new)' if yy == years[0] else f", {v['new_artists']:,} new artists ({pct(v['new_share'], 1)}% of that year's hours)") +
                 f", focus/sleep audio {v['func_hours']} h, after midnight {pct(v['night'], 1)}%")
    D['years'] = YR
    pm = max(D['monthly'], key=lambda x: x[1])
    F.append(f"- Biggest month: {pm[0]} with {pm[1]} hours.")

    # ---------- top artists / tracks / albums
    ah, al = Counter(), Counter()
    for r in music:
        ah[r['artist']] += r['eff']
    for r in listens:
        al[r['artist']] += 1
    D['top_artists'] = [(x, round(ms / 3.6e6), al[x]) for x, ms in ah.most_common(12)]
    F.append('\n## Top artists by hours (listens in brackets)\n' + '\n'.join(f"{i+1}. {x}: {round(ms/3.6e6)} h ({al[x]:,} listens){' [focus/sleep audio]' if any(r['func'] for r in music if r['artist'] == x) and x.lower() not in not_functional and (x.lower() in functional_artists) else ''}" for i, (x, ms) in enumerate(ah.most_common(20))))
    F.append('## Top artists by listens\n' + '\n'.join(f'{i+1}. {x}: {n:,}' for i, (x, n) in enumerate(al.most_common(10))))
    th_, tl = Counter(), Counter()
    meta = {}
    for r in music:
        meta[r['uri']] = (r['track'], r['artist'])
    for r in mnf:
        th_[r['uri']] += r['eff']
    for r in lnf:
        tl[r['uri']] += 1
    # Back-to-back repeats: a listen right after a listen of the same song (within 30 min, duplicates from a second device ignored).
    loops, rep_ct, run = [], Counter(), []
    for r in [q for q in lnf if q['eff'] > 0] + [None]:
        if r is not None and run and r['uri'] == run[-1]['uri'] and (r['start'] - run[-1]['end']).total_seconds() <= 1800:
            run.append(r)
            continue
        if len(run) >= 2:
            rep_ct[run[0]['uri']] += len(run) - 1
        if len(run) >= 5:
            loops.append(dict(t=short(run[0]['track'], 60), a=run[0]['artist'], n=len(run), date=d(run[0]['start']),
                              start=run[0]['start'].strftime('%Y-%m-%d %H:%M'), end=run[-1]['end'].strftime('%Y-%m-%d %H:%M'),
                              hours=hrs(sum(q['eff'] for q in run))))
        run = [r] if r is not None else []
    rt = lambda u: f", {rep_ct[u]} of them back-to-back repeats" if rep_ct[u] >= 10 else ''  # noqa: E731
    D['top_tracks'] = [dict(t=short(meta[u][0], 60), a=meta[u][1], h=hrs(ms), n=tl[u]) for u, ms in th_.most_common(10)]
    F.append('\n## Top tracks by hours (focus/sleep audio excluded)\n' + '\n'.join(f"- “{meta[u][0]}” by {meta[u][1]}: {hrs(ms)} h, {tl[u]} listens{rt(u)}" for u, ms in th_.most_common(12)))
    F.append('## Top tracks by listens\n' + '\n'.join(f"- “{meta[u][0]}” by {meta[u][1]}: {n} listens{rt(u)}" for u, n in tl.most_common(12)))
    albh = Counter()
    for r in mnf:
        if r['album']:
            albh[(r['album'], r['artist'])] += r['eff']
    D['top_albums'] = [dict(t=short(al_, 50), a=ar, h=hrs(ms)) for (al_, ar), ms in albh.most_common(8)]
    if albh:
        F.append('## Top albums by hours\n' + '\n'.join(f'- “{al_}” by {ar}: {hrs(ms)} h' for (al_, ar), ms in albh.most_common(8)))
    ya = defaultdict(Counter)
    for r in mnf:
        ya[r['start'].year][r['artist']] += r['eff']
    F.append('\n## Top artists per year (hours, focus/sleep audio excluded)\n' + '\n'.join(f'- {yy}: ' + ', '.join(f'{x} {round(ms/3.6e6)}' for x, ms in ya[yy].most_common(5)) for yy in years if ya[yy]))
    with open(os.path.join(a.work, 'artists.tsv'), 'w', encoding='utf-8') as f:
        f.write('hours\tlistens\tartist\tauto focus/sleep guess\ttop tracks\n')
        for x, ms in ah.most_common(200):
            rs = [r for r in music if r['artist'] == x]
            fun = 'yes' if x in func_set else ''
            tops = ' || '.join(short(t, 45) for t, _ in Counter(r['track'] for r in rs).most_common(2))
            f.write(f'{round(ms/3.6e6)}\t{al[x]}\t{x}\t{fun}\t{tops}\n')

    # ---------- eras and obsessions (listens)
    byart = defaultdict(list)
    for r in lnf:
        byart[r['artist']].append(r)
    eras = []
    for x, rs in byart.items():
        cur = [rs[0]]
        for r in rs[1:] + [None]:
            if r is None or (r['start'] - cur[-1]['start']).days > 10:
                if len(cur) >= th(60, 15):
                    song = Counter(q['track'] for q in cur).most_common(1)[0][0]
                    eras.append(dict(a=x, s=d(cur[0]['start']), e=d(cur[-1]['start']), n=len(cur), song=short(song, 60)))
                cur = [r] if r else []
            else:
                cur.append(r)
    eras.sort(key=lambda e: e['s'])
    D['eras'] = eras
    span = lambda e: (datetime.fromisoformat(e['e']) - datetime.fromisoformat(e['s'])).days + 1  # noqa: E731
    line = lambda e: f"- {e['a']}: {e['s']} to {e['e']} ({span(e)} days), {e['n']} listens, mostly “{e['song']}”"  # noqa: E731
    F.append(f"\n## Eras (≥{th(60,15)} listens of one artist, gaps ≤10 days): {len(eras)} in total\nBiggest 15:\n" +
             '\n'.join(line(e) for e in sorted(eras, key=lambda e: -e['n'])[:15]) +
             '\nLongest-lasting 3:\n' + '\n'.join(line(e) for e in sorted(eras, key=span, reverse=True)[:3]) +
             '\nMost recent 3:\n' + '\n'.join(line(e) for e in eras[-3:]))
    bytrack = defaultdict(list)
    for r in lnf:
        bytrack[r['uri']].append(r['start'])
    obs = []
    for u, ts in bytrack.items():
        cur = [ts[0]]
        for t in ts[1:] + [None]:
            if t is None or (t - cur[-1]).days > 14:
                if len(cur) >= th(20, 8):
                    obs.append(dict(t=short(meta[u][0], 60), a=meta[u][1], s=d(cur[0]), e=d(cur[-1]), n=len(cur), u=u))
                cur = [t] if t else []
            else:
                cur.append(t)
    obs.sort(key=lambda o: -o['n'])
    seen, D['obsessions'] = set(), []
    for o in obs:
        if o['u'] not in seen:
            seen.add(o['u'])
            D['obsessions'].append(o)
    D['obsessions'] = D['obsessions'][:10]
    F.append('## Song obsessions (listens of one track, gaps <2 weeks)\n' + '\n'.join(f"- “{meta[o['u']][0]}” by {o['a']}: {o['n']} listens, {o['s']} to {o['e']}{rt(o['u'])} (all-time)" for o in D['obsessions']))

    # ---------- loops (computed with top tracks above)
    loops.sort(key=lambda x: -x['n'])
    D['loops'] = loops[:6]
    F.append('\n## Loops (the same song listened to back to back, 5+ times, gaps ≤30 min, second-device duplicates ignored)\n' +
             '\n'.join(f"- “{x['t']}” by {x['a']}: {x['n']} listens in a row, {x['start']} to {x['end']} ({x['hours']} h)" for x in D['loops']) +
             f'\n- Loops of 5+ in total: {len(loops):,}.')

    # ---------- dedications and forgotten
    min_years = max(3, min(5, len(years) - 2))
    ded = []
    for u, ts in bytrack.items():
        yrs = Counter(t.year for t in ts)
        if len(yrs) >= min_years:
            ded.append(dict(t=short(meta[u][0], 60), a=meta[u][1], n=len(ts), years=len(yrs), y={yy: yrs.get(yy, 0) for yy in years}))
    D['dedications'] = sorted(ded, key=lambda x: -x['n'])[:12]
    allyears = [x for x in ded if x['years'] == len(years)]
    F.append(f"\n## Dedications (listened in ≥{min_years} different years)\n" + '\n'.join(f"- “{x['t']}” by {x['a']}: {x['n']} listens over {x['years']} years" for x in D['dedications']) +
             f"\n- In every year {years[0]}–{years[-1]}: " + ('; '.join(f"“{x['t']}” by {x['a']}" for x in sorted(allyears, key=lambda x: -x['n'])[:8]) or 'none'))
    fmin = th(25, 8)
    ff = [dict(t=short(meta[u][0], 60), a=meta[u][1], n=len(ts), last=d(max(ts)), py=Counter(t.year for t in ts).most_common(1)[0][0])
          for u, ts in bytrack.items() if len(ts) >= fmin and (today - max(ts)).days >= 540]
    D['forgotten'] = sorted(ff, key=lambda x: -x['n'])[:12]
    fa = [dict(a=x, n=len(rs), last=d(rs[-1]['start'])) for x, rs in byart.items() if len(rs) >= th(150, 30) and (today - rs[-1]['start']).days >= 540]
    D['forgotten_artists'] = sorted(fa, key=lambda x: -x['n'])[:6]
    F.append(f"\n## Forgotten favorites (≥{fmin} listens, none in 18 months)\n" + '\n'.join(f"- “{x['t']}” by {x['a']}: {x['n']} listens, last {x['last']}" for x in D['forgotten']) +
             ('\n- Artists left behind: ' + '; '.join(f"{x['a']} ({x['n']:,}, last {x['last']})" for x in D['forgotten_artists']) if D['forgotten_artists'] else ''))

    # ---------- skips
    sk = []
    for u in {r['uri'] for r in music}:
        pass
    st, sq = Counter(), Counter()
    for r in music:
        st[r['uri']] += 1
        sq[r['uri']] += r['qskip']
    sk = [(u, sq[u], st[u]) for u in st if st[u] >= th(30, 10)]
    most_skipped = sorted(sk, key=lambda z: (-z[1] / z[2], -z[2]))[:8]
    untouch = sorted([z for z in sk if z[1] / z[2] <= 0.03 and tl[z[0]] >= th(30, 10)], key=lambda z: -tl[z[0]])[:8]
    D['skipped'] = [dict(t=short(meta[u][0], 60), a=meta[u][1], s=s, n=n) for u, s, n in most_skipped]
    D['untouchable'] = [dict(t=short(meta[u][0], 60), a=meta[u][1], n=tl[u]) for u, s, n in untouch]
    qs = [r['ms'] for r in music if r['qskip']]
    qs.sort()
    D['skip_median_s'] = round(qs[len(qs) // 2] / 1000, 1) if qs else None
    ask = Counter()
    asn = Counter()
    for r in music:
        asn[r['artist']] += 1
        ask[r['artist']] += r['qskip']
    skart = sorted([(x, ask[x], asn[x]) for x in asn if asn[x] >= th(200, 40)], key=lambda z: -z[1] / z[2])[:5]
    F.append(f"\n## Skips\n- Median time before a quick skip: {D['skip_median_s']} s.\n- Most-skipped tracks you still kept getting (quick skips / streams):\n" +
             '\n'.join(f"  - “{meta[u][0]}” by {meta[u][1]}: skipped {s} of {n}" for u, s, n in most_skipped) +
             '\n- Untouchables (≤3% skipped, most listens):\n' + '\n'.join(f"  - “{meta[u][0]}” by {meta[u][1]}: {tl[u]} listens, skipped {s}" for u, s, n in untouch) +
             '\n- Most-skipped artists: ' + '; '.join(f'{x} {pct(s, n)}% of {n:,}' for x, s, n in skart))

    # ---------- autopilot vs on purpose (extended only)
    if ext:
        cat = lambda rs_: 'Picked a song' if rs_ in PICKED else {'trackdone': 'Previous song ended', 'fwdbtn': 'Skipped to it', 'backbtn': 'Went back to it'}.get(rs_, 'Other (app start, remote, error)')  # noqa: E731
        sc = Counter(cat(r['rs']) for r in music)
        D['starts'] = sc.most_common()
        pk = Counter(r['uri'] for r in music if r['rs'] in PICKED)
        D['picked'] = [dict(t=short(meta[u][0], 60), a=meta[u][1], n=n) for u, n in pk.most_common(8)]
        F.append('\n## How songs started\n' + '\n'.join(f'- {k}: {n:,} ({round(100*n/len(music),1)}%)' for k, n in sc.most_common()) +
                 '\n- Songs you picked on purpose most often: ' + '; '.join(f"“{meta[u][0]}” by {meta[u][1]} {n}" for u, n in pk.most_common(8)))

    # ---------- time of day
    hw = [[0] * 24 for _ in range(7)]
    for r in music:
        hw[r['start'].weekday()][r['start'].hour] += r['eff']
    D['heat'] = [[round(v / 3.6e6, 1) for v in row] for row in hw]
    hours_c = Counter()
    for r in music:
        hours_c[r['start'].hour] += r['eff']
    D['night_by_year'] = {yy: YR[yy]['night'] for yy in YR}
    F.append(f"\n## Time of day ({a.tz})\n- After midnight (00–05) share of hours by year: " + ', '.join(f'{yy} {pct(v, 1)}%' for yy, v in D['night_by_year'].items()) +
             f"\n- Busiest hour: {hours_c.most_common(1)[0][0]}:00. Weekday vs weekend hours: {round(sum(sum(r) for r in hw[:5]) / 3.6e6):,} vs {round(sum(sum(r) for r in hw[5:]) / 3.6e6):,}.")

    # ---------- focus / sleep audio
    fr = [r for r in music if r['func']]
    if fr:
        ft = Counter()
        for r in fr:
            ft[r['uri']] += r['eff']
        D['functional'] = dict(hours=round(sum(r['eff'] for r in fr) / 3.6e6), share=round(sum(r['eff'] for r in fr) / tot_ms, 3),
                               tracks=[dict(t=short(meta[u][0], 60), a=meta[u][1], h=hrs(ms)) for u, ms in ft.most_common(6)],
                               by_year={yy: YR[yy]['func_hours'] for yy in YR},
                               hours_of_day=[round(sum(r['eff'] for r in fr if r['start'].hour == h) / 3.6e6, 1) for h in range(24)])
        fa = Counter()
        for r in fr:
            fa[r['artist']] += 1
        F.append('\n## Left out of taste sections as focus/sleep audio (check this list; fix with labels.json)\n- ' + '; '.join(f'{x} {n:,} streams' for x, n in fa.most_common(20)))
        F.append(f"\n## Focus and sleep audio (labels.json functional + artists whose tracks mostly look like it)\n- {D['functional']['hours']} hours, {pct(D['functional']['share'], 1)}% of all listening. Top: " +
                 '; '.join(f"“{meta[u][0]}” by {meta[u][1]} {hrs(ms)} h" for u, ms in ft.most_common(6)) +
                 f"\n- Busiest hour for it: {max(range(24), key=lambda h: D['functional']['hours_of_day'][h])}:00")

    # ---------- devices
    dev = defaultdict(Counter)
    for r in music:
        dev[r['start'].year][r['platform']] += r['eff']
    devs = [p for p, _ in Counter({p: sum(dev[yy][p] for yy in dev) for yy in dev for p in dev[yy]}).most_common()]
    allp = Counter()
    for yy in dev:
        allp.update(dev[yy])
    devs = [p for p, _ in allp.most_common(6)]
    D['devices'] = dict(order=devs, years={yy: {p: round(dev[yy][p] / 3.6e6) for p in devs} for yy in sorted(dev)}) if ext else dict(order=[], years={})
    if ext:
        F.append('\n## Devices (hours per year)\n' + '\n'.join(f'- {yy}: ' + ', '.join(f'{p} {round(ms/3.6e6)}' for p, ms in dev[yy].most_common(4) if ms >= 3.6e6) for yy in sorted(dev)))

    # ---------- travel
    cc = Counter(r['country'] for r in music if r['country'] and r['country'] != 'ZZ')
    trips = []
    if cc:
        home = cc.most_common(1)[0][0]
        cur = None
        for r in music:
            c = r['country']
            if not c or c in ('ZZ', home):
                continue
            if cur and cur['c'] == c and (r['start'] - cur['last']).days <= 3:
                cur['last'] = r['start']
                cur['rs'].append(r)
            else:
                cur = dict(c=c, first=r['start'], last=r['start'], rs=[r])
                trips.append(cur)
        trips = [t for t in trips if len(t['rs']) >= 3]
        journeys = []  # runs abroad less than 3 days apart are one journey (UAE → Hong Kong → UAE)
        for t in trips:
            if journeys and (t['first'] - journeys[-1]['last']).days <= 3:
                journeys[-1]['last'] = t['last']
                journeys[-1]['rs'] += t['rs']
                if t['c'] not in journeys[-1]['cs']:
                    journeys[-1]['cs'].append(t['c'])
            else:
                journeys.append(dict(cs=[t['c']], first=t['first'], last=t['last'], rs=list(t['rs'])))
        D['travel'] = dict(home=COUNTRY.get(home, home), trips=[dict(c=' → '.join(COUNTRY.get(c, c) for c in j['cs']), s=d(j['first']), e=d(j['last']), n=len(j['rs']),
                                                                       days=(j['last'].date() - j['first'].date()).days + 1,
                                                                       top=Counter(f"{q['artist']} – {q['track']}" for q in j['rs']).most_common(1)[0][0],
                                                                       first=f"{j['rs'][0]['artist']} – {j['rs'][0]['track']}",
                                                                       maybe_vpn=len(j['rs']) < 30 and j['first'].date() == j['last'].date()) for j in journeys])
        F.append(f"\n## Travel (home: {COUNTRY.get(home, home)}; journeys = streams from other countries, 3+ streams, gaps <3 days merged)\n" +
                 '\n'.join(f"- {x['c']}: {x['s']} to {x['e']} ({pl(x['days'], 'day')}), {x['n']} streams; first “{x['first']}”, most played “{x['top']}”" +
                            (' [one day, few streams: maybe a VPN or layover]' if x['maybe_vpn'] else '') for x in D['travel']['trips']) +
                 f"\n- Unknown-country streams (ZZ): {sum(1 for r in music if r['country'] == 'ZZ'):,}")

    # ---------- discovery
    D['discovery'] = {yy: dict(new=YR[yy]['new_artists'], share=YR[yy]['new_share']) for yy in YR}

    # ---------- seasons
    sc_ = defaultdict(list)
    for r in music:
        yy, mo = r['start'].year, r['start'].month
        s = SEASON_N[mo]
        if a.southern:
            s = (s + 2) % 4
        sc_[(yy + 1 if mo == 12 else yy, s)].append(r)
    seasons = []
    for (yy, s), rs in sorted(sc_.items()):
        h = sum(r['eff'] for r in rs)
        if h < 3.6e6 * max(2, 8 * scale):
            continue
        ac = Counter()
        for r in rs:
            if not r['func']:
                ac[r['artist']] += r['eff']
        newc = Counter()
        for r in rs:
            if r['listen'] and not r['func'] and r['artist'] in byart and (r['start'] - byart[r['artist']][0]['start']).days <= 92:
                newc[r['artist']] += 1
        label = f'{SEASON_NAMES[s]} {yy - 1}–{str(yy)[2:]}' if s == 0 and not a.southern else f'{SEASON_NAMES[s]} {yy}'
        seasons.append(dict(l=label, h=round(h / 3.6e6), a=[x for x, _ in ac.most_common(2)], new=[x for x, _ in newc.most_common(1)],
                            skip=round(sum(r['qskip'] for r in rs) / len(rs), 2)))
    D['seasons'] = seasons
    F.append('\n## Seasons\n' + '\n'.join(f"- {s['l']}: {s['h']} h, top {', '.join(s['a'])}; best new find {', '.join(s['new']) or '—'}; quick-skip rate {pct(s['skip'], 1)}%" for s in seasons))

    # ---------- soundtrack per year
    D['soundtrack'] = {}
    for yy in years:
        c = Counter(r['uri'] for r in listens if r['start'].year == yy and not r['func'])
        D['soundtrack'][yy] = [dict(t=short(meta[u][0], 50), a=meta[u][1], n=n) for u, n in c.most_common(3)]
        F.append(('\n## Soundtrack per year (listens, focus audio excluded)' if yy == years[0] else '') + f"\n- {yy}: " +
                 '; '.join(f"“{meta[u][0]}” by {meta[u][1]} {n}" for u, n in c.most_common(3)))

    # ---------- moods
    if moods.get('moods') and moods.get('artists'):
        am = {k.lower(): v for k, v in moods['artists'].items()}
        q = defaultdict(Counter)
        tagged = 0
        for r in music:
            mo = am.get(r['artist'].lower())
            if mo:
                q[f"{r['start'].year} Q{(r['start'].month - 1) // 3 + 1}"][mo] += r['eff']
                tagged += r['eff']
        D['mood'] = dict(order=moods['moods'][:4], q=sorted((k, {m_: round(v / 3.6e6, 1) for m_, v in c.items()}) for k, c in q.items()), artists=len(am))
        F.append(f"\n## Mood mix per quarter (share of hours; {round(tagged/3.6e6):,} hours from {len(am)} tagged artists)\n" +
                 '\n'.join(f"- {k}: " + ', '.join(f'{m_} {pct(v, sum(c.values()))}%' for m_, v in sorted(c.items(), key=lambda z: -z[1]) if pct(v, sum(c.values())) > 0) for k, c in D['mood']['q'] if sum(c.values()) > 0))

    # ---------- drift, flings, lifers, gateways
    big = [yy for yy in years if sum(ya[yy].values()) >= 3.6e6 * max(5, 40 * scale)]
    top40 = {yy: {x for x, _ in ya[yy].most_common(40)} for yy in big}
    D['drift'] = dict(years=big, m=[[round(len(top40[p] & top40[q_]) / max(1, len(top40[p] | top40[q_])), 2) for q_ in big] for p in big])
    pairs = sorted(((D['drift']['m'][i][j], big[i], big[j]) for i in range(len(big)) for j in range(i + 1, len(big))), reverse=True)
    lifers = set.intersection(*[{x for x, _ in ya[yy].most_common(80)} for yy in big[1:]]) if len(big) > 2 else set()
    D['lifers'] = sorted(lifers, key=lambda x: -ah[x])
    if pairs:
        F.append('\n## Taste drift (top-40 artists by hours)\n- Most alike: ' + '; '.join(f'{p}–{q_} {pct(v, 1)}%' for v, p, q_ in pairs[:3]) +
                 '\n- Least alike: ' + '; '.join(f'{p}–{q_} {pct(v, 1)}%' for v, p, q_ in pairs[-3:]) +
                 f"\n- In the top 80 (by hours) of every year {big[1] if len(big) > 1 else ''}–{big[-1]}: {', '.join(D['lifers']) or 'nobody'}")
    dd = []
    for x, rs in byart.items():
        if len(rs) < th(60, 15):
            continue
        ts = [r['start'] for r in rs]
        j = b_ = 0
        for i in range(len(ts)):
            while (ts[i] - ts[j]).days > 30:
                j += 1
            b_ = max(b_, i - j + 1)
        dd.append(dict(artist=x, n=len(rs), peak30=b_, peak_share=round(b_ / len(rs), 2), years=len({t.year for t in ts}), first=d(ts[0])))
    recent = d(today - timedelta(days=3 * 365))
    D['flings'] = sorted([z for z in dd if z['first'] >= recent], key=lambda z: -z['peak30'])[:6]
    D['steady_years'] = max(3, len(years) - 1)
    D['steady'] = sorted([z for z in dd if z['years'] >= D['steady_years']], key=lambda z: z['peak_share'])[:6]
    F.append('\n## Flings (first heard in last 3 years, best 30 days)\n' + '\n'.join(f"- {z['artist']}: {z['peak30']} listens in best 30 days, {z['n']} total, first {z['first']}" for z in D['flings']) +
             f"\n## Lifers (≥{D['steady_years']} years, most even)\n" + '\n'.join(f"- {z['artist']}: {z['n']} listens over {z['years']} years, busiest month {pct(z['peak_share'], 1)}%" for z in D['steady']))
    gw = []
    for x, _ in ah.most_common(14):
        rs = byart.get(x)
        if not rs:
            continue
        nxt = sum(1 for r in rs if (r['start'] - rs[0]['start']).days <= 30)
        if nxt >= th(15, 5):
            gw.append(dict(artist=x, title=short(rs[0]['track'], 70), date=d(rs[0]['start']), next30=nxt, total=len(rs)))
    D['gateways'] = gw[:6]
    F.append('\n## Gateway tracks\n' + '\n'.join(f"- {g['artist']}: first “{g['title']}” on {g['date']}, {g['next30']} listens in 30 days, {g['total']} total" for g in D['gateways']))

    # ---------- biggest days and marathons
    dh = defaultdict(list)
    for r in music:
        dh[r['start'].date()].append(r)
    bd = sorted(dh.items(), key=lambda kv: -sum(r['eff'] for r in kv[1]))[:3]
    D['big_days'] = [dict(date=str(k), h=hrs(sum(r['eff'] for r in v)), top=Counter(f"{r['artist']} – {r['track']}" for r in v if r['listen']).most_common(1)[0][0] if any(r['listen'] for r in v) else '',
                          artists=len({r['artist'] for r in v})) for k, v in bd]
    sess, cur = [], [music[0]]
    for r in music[1:]:
        if (r['start'] - (cur[-1]['start'] + timedelta(milliseconds=cur[-1]['eff']))).total_seconds() <= 1800:
            cur.append(r)
        else:
            sess.append(cur)
            cur = [r]
    sess.append(cur)
    lens = sorted(sum(r['eff'] for r in s) for s in sess)
    D['session_median_min'] = round(lens[len(lens) // 2] / 60000)
    D['marathons'] = [dict(start=s[0]['start'].strftime('%Y-%m-%dT%H:%M'), end=s[-1]['end'].strftime('%Y-%m-%dT%H:%M'), h=hrs(sum(r['eff'] for r in s)), n=len(s),
                           first=f"{s[0]['artist']} – {short(s[0]['track'], 50)}", last=f"{s[-1]['artist']} – {short(s[-1]['track'], 50)}",
                           top=Counter(r['artist'] for r in s).most_common(1)[0][0], func=pct(sum(r['eff'] for r in s if r['func']), sum(r['eff'] for r in s)))
                      for s in sorted(sess, key=lambda s: -sum(r['eff'] for r in s))[:3]]
    F.append('\n## Biggest days\n' + '\n'.join(f"- {x['date']}: {x['h']} h, {pl(x['artists'], 'artist')}, most played “{x['top']}”" + (' [16+ h: music was almost certainly left running]' if x['h'] >= 16 else '') for x in D['big_days']) +
             f"\n## Marathons (session = gaps ≤30 min; median session {D['session_median_min']} min; one artist for many hours often means a loop left running)\n" +
             '\n'.join(f"- {x['start']} → {x['end']}: {x['h']} h, {x['n']} streams, mostly {x['top']} ({x['func']}% focus/sleep audio); from “{x['first']}” to “{x['last']}”" for x in D['marathons']))

    # ---------- rituals
    rit = []
    for x, rs in byart.items():
        if len(rs) < th(80, 20):
            continue
        mo = Counter(r['start'].month for r in rs)
        best_ = None
        for w in (1, 2, 3):
            for s in range(1, 13):
                ms3 = [((s - 1 + i) % 12) + 1 for i in range(w)]
                share = sum(mo[m_] for m_ in ms3) / len(rs)
                yrs = {r['start'].year for r in rs if r['start'].month in ms3}
                if share >= {1: .3, 2: .45, 3: .55}[w] and len(yrs) >= 3 and (best_ is None or share / w > best_[0]):
                    best_ = (share / w, ms3, share, sorted(yrs))
        if best_:
            rit.append(dict(name=x, n=len(rs), months=[mo.get(i, 0) for i in range(1, 13)], window=best_[1], share=round(best_[2], 2), years=best_[3]))
    xm = [r for r in listens if re.search(r'christmas|xmas|jingle|santa|новогод|navidad|noël|weihnacht', r['track'] + ' ' + (r['album'] or ''), re.I)]
    if len(xm) >= th(30, 10):
        mo = Counter(r['start'].month for r in xm)
        rit.append(dict(name='theme: Christmas music', n=len(xm), months=[mo.get(i, 0) for i in range(1, 13)], window=[12], share=round(mo[12] / len(xm), 2),
                        years=sorted({r['start'].year for r in xm})))
    rit.sort(key=lambda z: -z['n'] * z['share'])
    D['rituals'] = rit[:6]
    F.append('\n## Yearly rituals (chart one with rituals.chart_index)\n' + '\n'.join(f"{i}. {z['name']}: {z['n']} listens, {pct(z['share'], 1)}% in months {z['window']}, {len(z['years'])} different years with listens in those months" for i, z in enumerate(D['rituals'])))

    # ---------- on this day, podcasts
    otd = {}
    for yy in years:
        rs = [r for r in listens if r['start'].year == yy and r['start'].month == today.month and r['start'].day == today.day]
        if rs:
            uniq = list(dict.fromkeys(f"{r['artist']} – {short(r['track'], 50)}" for r in rs))
            otd[yy] = dict(n=len(rs), s=uniq[:3])
    D['otd'] = otd
    F.append(f"\n## On this day ({today.strftime('%d %B')})\n" + '\n'.join(f"- {yy}: {v['n']} listens, e.g. " + '; '.join(v['s']) for yy, v in otd.items()))
    eps = [r for r in rows if r['kind'] == 'episode']
    if eps:
        sh = Counter()
        for r in eps:
            sh[r['artist']] += r['eff']
        D['podcasts'] = [dict(show=x, h=hrs(ms)) for x, ms in sh.most_common(5)]
        F.append('\n## Podcasts\n' + '\n'.join(f"- {x['show']}: {x['h']} h" for x in D['podcasts']))

    # ---------- odd candidates: one listen of an artist heard only once
    once = [r for r in listens if al[r['artist']] == 1 and not r['func']]
    random.Random(7).shuffle(once)
    with open(os.path.join(a.work, 'odd_candidates.tsv'), 'w', encoding='utf-8') as f:
        f.write('date\tartist\ttrack\talbum\n')
        for r in sorted(once[:250], key=lambda r: r['start']):
            f.write(f"{d(r['start'])}\t{r['artist']}\t{r['track']}\t{r['album'] or ''}\n")
    json.dump(D, open(os.path.join(a.work, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    open(os.path.join(a.work, 'facts.md'), 'w', encoding='utf-8').write('\n'.join(F) + '\n')
    print(f"{T['hours']:,} hours, {T['listens']:,} listens, {years[0]}–{years[-1]}, {export_kind} export, tz {a.tz}. Focus/sleep audio: "
          f"{D.get('functional', {}).get('hours', 0)} h. Wrote data.json, facts.md, artists.tsv, odd_candidates.tsv to {a.work}")


if __name__ == '__main__':
    main()
