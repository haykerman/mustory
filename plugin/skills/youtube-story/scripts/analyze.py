"""Compute every statistic the YouTube story page shows.

python3 analyze.py --export <takeout.zip|folder> --work <dir> [--tz Europe/Berlin] [--today 2026-11-24] [--southern]

Writes into --work:
  data.json          everything the page draws (read by render.py)
  facts.md           a readable digest; the only source of numbers for story.json
  to_label.tsv       top channels with sample titles and the current topic guess
  artists.tsv        top artists, for mood tagging
  odd_candidates.tsv one-off watches from one-off channels, for the "odd" chapter
Reads from --work if present: labels.json, moods.json (see SKILL.md).
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
from takeout import load, system_tz  # noqa: E402
from classify import artist, category, norm  # noqa: E402

DEFAULT_QUESTS = {
    'Guitar': r'guitar lesson|how to play .*guitar|chords|fingerstyle|guitar tutorial|backing track|pentatonic',
    'Piano': r'piano tutorial|piano lesson|learn piano',
    'Singing': r'vocal (exercise|warm|lesson|technique)|singing lesson|how to sing',
    'Drawing': r'how to draw|drawing tutorial|procreate',
    'Languages': r'learn (german|spanish|french|english|italian|japanese|korean|chinese)|(german|spanish|french|japanese) lesson',
    'Cooking': r'recipe|how to cook|how to make .*(bread|pasta|cake)',
    'Fitness': r'workout|exercise routine|stretch|back pain|posture',
    'Driving test': r'driving test|road signs|parallel park|ПДД|ГАИ',
    'Coding tutorials': r'tutorial for beginners|crash course|full course|learn (python|javascript|react|swift|rust)',
    'Home & DIY': r'renovat|how to fix|repair|diy|ремонт',
    'Chess': r'\bchess\b',
}
SEASON_N = {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
SEASON_NAMES = ['Winter', 'Spring', 'Summer', 'Fall']
RITUAL_KEYWORDS = {'Christmas songs': r'christmas|xmas|jingle bell|santa|новогод|новый год',
                   'Halloween': r'halloween|spooky', 'Eurovision': r'eurovision|\besc\b|junior eurovision',
                   'World Cup': r'world cup', 'Ramadan': r'ramadan|ramazan'}


def short(t, n=70):
    return t if len(t) <= n else t[:n - 1] + '…'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--export', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--tz', default=system_tz())
    ap.add_argument('--today')
    ap.add_argument('--southern', action='store_true', help='southern hemisphere seasons')
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    tz = ZoneInfo(a.tz)
    rows, srch, meta = load(a.export, a.tz)
    if not rows:
        raise SystemExit('The export has no watch history.')
    today = datetime.fromisoformat(a.today).replace(tzinfo=tz) if a.today else datetime.now(tz)
    lab_path, mood_path = os.path.join(a.work, 'labels.json'), os.path.join(a.work, 'moods.json')
    labels = json.load(open(lab_path, encoding='utf-8')) if os.path.exists(lab_path) else {}
    ch_labels = {k.strip().lower(): v for k, v in labels.get('channels', {}).items()}
    rename = labels.get('rename', {})  # e.g. {"Tech": "Tech reviews"}: renames a built-in topic everywhere
    moods = json.load(open(mood_path, encoding='utf-8')) if os.path.exists(mood_path) else {}

    scale = max(0.1, len(rows) / 50000)  # thresholds below were tuned on ~50k plays

    def th(base, lo):
        return max(lo, round(base * scale))

    for r in rows:
        r['cat'] = 'Removed video' if r['removed'] else category(r['title'], r['ch'], ch_labels)
        r['cat'] = rename.get(r['cat'], r['cat'])
        r['art'] = artist(r['title'], r['ch']) if r['cat'] == 'Music' else None
        r['ak'] = norm(r['art']) if r['art'] else None
    live = [r for r in rows if not r['removed']]
    names = defaultdict(Counter)
    for r in live:
        if r['ak']:
            names[r['ak']][r['art']] += 1
    AN = {k: c.most_common(1)[0][0] for k, c in names.items()}
    titles = {r['v']: r['title'] for r in live}
    chan = {r['v']: r['ch'] for r in live}
    plays = defaultdict(list)
    for r in rows:
        plays[r['v']].append(r['ts'])
    d = lambda ts: ts.strftime('%Y-%m-%d')  # noqa: E731
    years = list(range(rows[0]['ts'].year, rows[-1]['ts'].year + 1))
    D, F = {}, []  # page data, facts lines

    # ---------- totals
    vc = Counter(r['v'] for r in rows)
    days = Counter(d(r['ts']) for r in rows)
    rep = sum(n for n in vc.values() if n >= 10)
    D['totals'] = dict(plays=len(rows), unique=len(vc), channels=len({r['ch'] for r in live if r['ch']}), searches=len(srch),
                       first=rows[0]['ts'].isoformat(), last=rows[-1]['ts'].isoformat(), first_title=rows[0]['title'],
                       last_title=rows[-1]['title'], removed=sum(r['removed'] for r in rows),
                       removed_unique=len({r['v'] for r in rows if r['removed']}), artists=len(AN), active_days=len(days),
                       once_share=round(sum(1 for n in vc.values() if n == 1) / len(vc), 3), videos_10plus=sum(1 for n in vc.values() if n >= 10),
                       share_to_10plus=round(rep / len(rows), 3), ads_excluded=meta['ads_excluded'])
    D['meta'] = dict(tz=a.tz, today=d(today), southern=a.southern)
    T = D['totals']
    F.append(f"## Totals\n- {T['plays']:,} plays of {T['unique']:,} different videos from {T['channels']:,} channels, {T['searches']:,} searches.")
    F.append(f"- First play: {T['first'][:16]} “{T['first_title']}”. Last: {T['last'][:16]} “{T['last_title']}”.")
    F.append(f"- {round(T['once_share']*100)}% of videos played exactly once; {T['videos_10plus']:,} videos played 10+ times take {round(T['share_to_10plus']*100)}% of all plays.")
    F.append(f"- {T['removed']:,} plays point to {T['removed_unique']:,} deleted/private videos. {T['ads_excluded']:,} ad plays excluded. Days with any play: {T['active_days']:,}.")

    # ---------- monthly + years
    mc = Counter(r['ts'].strftime('%Y-%m') for r in rows)
    mm = Counter(r['ts'].strftime('%Y-%m') for r in live if r['cat'] == 'Music')
    y, m = rows[0]['ts'].year, rows[0]['ts'].month
    D['monthly'] = []
    while (y, m) <= (rows[-1]['ts'].year, rows[-1]['ts'].month):
        k = f'{y}-{m:02d}'
        D['monthly'].append([k, mc[k], mm[k]])
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    yt = Counter(r['ts'].year for r in rows)
    yc = defaultdict(Counter)
    for r in live:
        yc[r['ts'].year][r['cat']] += 1
    peak = max(D['monthly'], key=lambda x: x[1])
    F.append('\n## By year (plays incl. deleted videos; topic shares of playable videos)')
    for yy in years:
        tot = sum(yc[yy].values()) or 1
        mix = ', '.join(f'{c} {round(100 * n / tot)}%' for c, n in yc[yy].most_common(6))
        F.append(f'- {yy}: {yt[yy]:,} plays. {mix}')
    F.append(f'- Busiest month: {peak[0]} with {peak[1]:,} plays. Busiest day: {days.most_common(1)[0][0]} with {days.most_common(1)[0][1]} plays.')
    D['year_totals'] = {yy: yt[yy] for yy in years}
    tc = Counter(r['cat'] for r in live)
    D['topics'] = tc.most_common()
    F.append('\n## Topics (all time, playable videos)\n- ' + ', '.join(f'{c} {n:,} ({round(100 * n / max(1, len(live)))}%)' for c, n in tc.most_common(25)))

    # ---------- artists
    ap_ = defaultdict(list)
    for r in live:
        if r['ak']:
            ap_[r['ak']].append(r)
    top = sorted(ap_.items(), key=lambda kv: -len(kv[1]))
    D['top_artists'] = [(AN[k], len(v)) for k, v in top[:12]]
    F.append('\n## Top artists (all time)\n' + '\n'.join(f'{i+1}. {AN[k]}: {len(v)} plays ({min(r["ts"].year for r in v)}–{max(r["ts"].year for r in v)})'
                                                   for i, (k, v) in enumerate(top[:20])))
    ya = defaultdict(Counter)
    for r in live:
        if r['ak']:
            ya[r['ts'].year][r['ak']] += 1
    F.append('\n## Top artists per year\n' + '\n'.join(f'- {yy}: ' + ', '.join(f'{AN[k]} {n}' for k, n in ya[yy].most_common(5)) for yy in years))
    ych = defaultdict(Counter)
    for r in live:
        if r['cat'] != 'Music' and r['ch']:
            ych[r['ts'].year][r['ch']] += 1
    F.append('\n## Top non-music channels per year\n' + '\n'.join(f'- {yy}: ' + ', '.join(f'{c} {n}' for c, n in ych[yy].most_common(5)) for yy in years))
    with open(os.path.join(a.work, 'artists.tsv'), 'w', encoding='utf-8') as f:
        f.write('plays\tartist\ttop songs\n')
        for k, v in top[:150]:
            songs = ' || '.join(short(t, 50) for t, _ in Counter(r['title'] for r in v).most_common(2))
            f.write(f'{len(v)}\t{AN[k]}\t{songs}\n')

    # ---------- eras (artist streaks) and obsessions (song streaks)
    def streaks(ts_list, gap):
        ts_list = sorted(ts_list)
        cur = [ts_list[0]]
        for t in ts_list[1:]:
            if (t - cur[-1]).days > gap:
                yield cur
                cur = [t]
            else:
                cur.append(t)
        yield cur
    eras = []
    for k, rs in ap_.items():
        rs = sorted(rs, key=lambda r: r['ts'])
        by_ts = {id(r): r for r in rs}
        cur = [rs[0]]
        for r in rs[1:] + [None]:
            if r is None or (r['ts'] - cur[-1]['ts']).days > 10:
                if len(cur) >= th(40, 12):
                    song = Counter(x['title'] for x in cur).most_common(1)[0][0]
                    eras.append(dict(a=AN[k], s=d(cur[0]['ts']), e=d(cur[-1]['ts']), n=len(cur), song=short(song, 60)))
                cur = [r] if r else []
            else:
                cur.append(r)
        del by_ts
    eras.sort(key=lambda e: e['s'])
    D['eras'] = eras
    obs = []
    for v, ts in plays.items():
        if v not in titles:
            continue
        for s in streaks(ts, 14):
            if len(s) >= th(10, 6):
                obs.append(dict(t=short(titles[v]), v=v, s=d(s[0]), e=d(s[-1]), n=len(s)))
    obs.sort(key=lambda o: -o['n'])
    seen, D['obsessions'] = set(), []
    for o in obs:
        if o['v'] not in seen:
            seen.add(o['v'])
            D['obsessions'].append(o)
    D['obsessions'] = D['obsessions'][:10]
    F.append(f"\n## Eras (≥{th(40,12)} plays of one artist, gaps ≤10 days): {len(eras)} in total, biggest 15 listed\n" +
             '\n'.join(f"- {e['a']}: {e['s']} to {e['e']}, {e['n']} plays, mostly “{e['song']}”" for e in sorted(eras, key=lambda e: -e['n'])[:15]))
    F.append('\n## Song obsessions (single video, gaps <2 weeks)\n' + '\n'.join(f"- “{titles[o['v']]}”: {o['n']} plays, {o['s']} to {o['e']}" for o in D['obsessions']))
    bursts = []
    for k, rs in ap_.items():
        ts = sorted(r['ts'] for r in rs)
        j, best, bi = 0, 0, 0
        for i in range(len(ts)):
            while (ts[i] - ts[j]).days > 6:
                j += 1
            if i - j + 1 > best:
                best, bi = i - j + 1, j
        if best >= th(25, 8):
            bursts.append((best, AN[k], d(ts[bi])))
    bursts.sort(reverse=True)
    F.append('\n## Biggest 7-day bursts per artist (look for anniversaries, releases, concerts)\n' +
             '\n'.join(f'- {a_}: {n} plays in 7 days starting {s}' for n, a_, s in bursts[:10]))

    # ---------- dedications, forgotten
    min_years = max(3, min(5, len(years) - 2))
    ded = []
    for v, ts in plays.items():
        if v not in titles:
            continue
        yrs = Counter(t.year for t in ts)
        if len(yrs) >= min_years:
            ded.append(dict(t=short(titles[v]), v=v, n=len(ts), years=len(yrs), y={yy: yrs.get(yy, 0) for yy in years}))
    D['dedications'] = sorted(ded, key=lambda x: -x['n'])[:12]
    D['dedications_min_years'] = min_years
    allyears = [x for x in ded if x['years'] == len(years)]
    F.append(f"\n## Dedications (played in ≥{min_years} different years)\n" + '\n'.join(f"- “{x['t']}”: {x['n']} plays over {x['years']} years" for x in D['dedications']) +
             f"\n- Played in every year {years[0]}–{years[-1]}: " + ('; '.join(f"“{x['t']}”" for x in sorted(allyears, key=lambda x: -x['n'])[:8]) or 'none'))
    fmin = th(12, 6)
    ff = []
    for v, ts in plays.items():
        if v in titles and len(ts) >= fmin and (today - max(ts)).days >= 540:
            ff.append(dict(t=short(titles[v]), v=v, n=len(ts), last=d(max(ts)), py=Counter(t.year for t in ts).most_common(1)[0][0]))
    D['forgotten'] = sorted(ff, key=lambda x: -x['n'])[:12]
    D['forgotten_min'] = fmin
    cp = defaultdict(list)
    for r in live:
        if r['ch']:
            cp[r['ch']].append(r)
    fc = [dict(ch=c, n=len(rs), last=d(max(r['ts'] for r in rs)), cat=Counter(r['cat'] for r in rs).most_common(1)[0][0])
          for c, rs in cp.items() if len(rs) >= th(60, 15) and (today - max(r['ts'] for r in rs)).days >= 540]
    D['forgotten_channels'] = sorted(fc, key=lambda x: -x['n'])[:6]
    F.append(f"\n## Forgotten favorites (≥{fmin} plays, none in 18 months)\n" + '\n'.join(f"- “{x['t']}”: {x['n']} plays, last {x['last']}" for x in D['forgotten']) +
             '\n- Channels left behind: ' + '; '.join(f"{x['ch']} ({x['n']}, last {x['last']})" for x in D['forgotten_channels']))

    # ---------- seasons
    overall = Counter(r['cat'] for r in live)
    tot = sum(overall.values())
    sc = defaultdict(list)
    for r in live:
        yy, mo = r['ts'].year, r['ts'].month
        s = SEASON_N[mo]
        if a.southern:
            s = (s + 2) % 4
        sc[(yy + 1 if mo == 12 else yy, s)].append(r)
    seasons = []
    for (yy, s), rs in sorted(sc.items()):
        if len(rs) < th(150, 30):
            continue
        c = Counter(r['cat'] for r in rs)
        n = len(rs)
        lifts = sorted([(k, c[k] / n / (overall[k] / tot)) for k in c if k not in ('Music', 'Other', 'Removed video') and c[k] >= th(25, 6)], key=lambda x: -x[1])
        arts = [AN[k] for k, _ in Counter(r['ak'] for r in rs if r['ak']).most_common(2)]
        chs = [ch for ch, _ in Counter(r['ch'] for r in rs if r['cat'] != 'Music' and r['ch']).most_common(1)]
        label = f'{SEASON_NAMES[s]} {yy - 1}–{str(yy)[2:]}' if s == 0 and not a.southern else f'{SEASON_NAMES[s]} {yy}'
        seasons.append(dict(l=label, n=n, m=round(c['Music'] / n, 2), a=arts, into=[k for k, l in lifts[:2] if l >= 1.4], ch=chs))
    D['seasons'] = seasons
    F.append('\n## Seasons\n' + '\n'.join(f"- {s['l']}: {s['n']:,} plays, {round(s['m']*100)}% music, top {', '.join(s['a'])}; unusually into {', '.join(s['into']) or '—'}" for s in seasons))

    # ---------- soundtrack per year
    D['soundtrack'] = {}
    for yy in years:
        c = Counter(r['v'] for r in live if r['ts'].year == yy and r['cat'] == 'Music')
        D['soundtrack'][yy] = [dict(t=short(titles[v], 58), n=n) for v, n in c.most_common(3)]
        F.append(('\n## Soundtrack per year' if yy == years[0] else '') + f"\n- {yy}: " + '; '.join(f"“{titles[v]}” {n}" for v, n in c.most_common(3)))

    # ---------- mood (needs moods.json)
    if moods.get('moods') and moods.get('artists'):
        am = {norm(k): v for k, v in moods['artists'].items()}
        q = defaultdict(Counter)
        tagged = 0
        for r in live:
            mo = am.get(r['ak']) if r['ak'] else None
            if mo:
                q[f"{r['ts'].year} Q{(r['ts'].month - 1) // 3 + 1}"][mo] += 1
                tagged += 1
        D['mood'] = dict(order=moods['moods'][:4], q=sorted((k, dict(v)) for k, v in q.items()), tagged=tagged, artists=len(am))
        F.append(f"\n## Mood mix per quarter ({tagged:,} plays from {len(am)} tagged artists)\n" +
                 '\n'.join(f"- {k}: " + ', '.join(f'{mm_} {round(100*n/sum(v.values()))}%' for mm_, n in sorted(v.items(), key=lambda x: -x[1])) for k, v in D['mood']['q']))

    # ---------- time of day
    hw = [[0] * 24 for _ in range(7)]
    for r in rows:
        hw[r['ts'].weekday()][r['ts'].hour] += 1
    D['heat'] = hw
    ny = {}
    for yy in years:
        rs = [r for r in rows if r['ts'].year == yy]
        ny[yy] = round(sum(1 for r in rs if r['ts'].hour < 5) / len(rs), 3) if rs else 0
    D['night_by_year'] = ny
    hours = Counter(r['ts'].hour for r in rows)
    F.append(f"\n## Time of day ({a.tz})\n- Share of plays 00:00–05:00 by year: " + ', '.join(f'{yy} {round(v*100)}%' for yy, v in ny.items()) +
             f"\n- Overall {round(sum(1 for r in rows if r['ts'].hour < 5)/len(rows)*100)}% after midnight. Busiest hour: {hours.most_common(1)[0][0]}:00.")
    nv = Counter(r['v'] for r in live if r['ts'].hour < 5)
    D['comfort'] = [dict(t=short(titles[v]), night=n, total=len(plays[v])) for v, n in nv.most_common(60)
                    if n >= th(8, 4) and n / len(plays[v]) >= 0.4][:8]
    F.append('\n## Comfort videos (≥40% of plays after midnight)\n' + '\n'.join(f"- “{x['t']}”: {x['night']} of {x['total']} plays" for x in D['comfort']))

    # ---------- taste drift
    big = [yy for yy in years if sum(ya[yy].values()) >= th(200, 40)]
    top40 = {yy: set(k for k, _ in ya[yy].most_common(40)) for yy in big}
    D['drift'] = dict(years=big, m=[[round(len(top40[p] & top40[q_]) / max(1, len(top40[p] | top40[q_])), 2) for q_ in big] for p in big])
    pairs = sorted(((D['drift']['m'][i][j], big[i], big[j]) for i in range(len(big)) for j in range(i + 1, len(big))), reverse=True)
    lifers = set.intersection(*[set(k for k, _ in ya[yy].most_common(80)) for yy in big[1:]]) if len(big) > 2 else set()
    D['lifers'] = sorted((AN[k] for k in lifers), key=lambda n: -len(ap_[norm(n)]))
    if pairs:
        F.append(f"\n## Taste drift (top-40 artist overlap)\n- Most alike: " + '; '.join(f'{p}–{q_} {round(v*100)}%' for v, p, q_ in pairs[:3]) +
                 '\n- Least alike: ' + '; '.join(f'{p}–{q_} {round(v*100)}%' for v, p, q_ in pairs[-3:]) +
                 f"\n- In the top 80 every year {big[1] if len(big) > 1 else ''}–{big[-1]}: {', '.join(D['lifers']) or 'nobody'}")

    # ---------- flings and lifers
    dd = []
    for k, rs in ap_.items():
        if len(rs) < th(30, 10):
            continue
        ts = sorted(r['ts'] for r in rs)
        j = best = 0
        for i in range(len(ts)):
            while (ts[i] - ts[j]).days > 30:
                j += 1
            best = max(best, i - j + 1)
        dd.append(dict(artist=AN[k], n=len(rs), peak30=best, peak_share=round(best / len(rs), 2), years=len({t.year for t in ts}), first=d(ts[0])))
    recent = d(today - timedelta(days=3 * 365))
    D['flings'] = sorted([x for x in dd if x['first'] >= recent], key=lambda x: -x['peak30'])[:6]
    steady_years = max(3, len(years) - 1)
    D['steady'] = sorted([x for x in dd if x['years'] >= steady_years], key=lambda x: x['peak_share'])[:6]
    D['steady_years'] = steady_years
    F.append('\n## Flings (first played in last 3 years, best 30 days)\n' + '\n'.join(f"- {x['artist']}: {x['peak30']} plays in best 30 days, {x['n']} total, first {x['first']}" for x in D['flings']) +
             f'\n## Lifers (≥{steady_years} years, most even spread)\n' + '\n'.join(f"- {x['artist']}: {x['n']} plays over {x['years']} years, busiest month {round(x['peak_share']*100)}%" for x in D['steady']))

    # ---------- gateways
    gw = []
    for k, rs in top[:14]:
        rs = sorted(rs, key=lambda r: r['ts'])
        nxt = sum(1 for r in rs if (r['ts'] - rs[0]['ts']).days <= 30)
        if nxt >= th(10, 4):
            gw.append(dict(artist=AN[k], title=short(rs[0]['title'], 80), date=d(rs[0]['ts']), next30=nxt, total=len(rs)))
    D['gateways'] = gw[:6]
    F.append('\n## Gateway videos\n' + '\n'.join(f"- {g['artist']}: first “{g['title']}” on {g['date']}, {g['next30']} plays in the next 30 days, {g['total']} total" for g in D['gateways']))

    # ---------- rabbit holes
    sess, cur = [], [rows[0]]
    for r in rows[1:]:
        if (r['ts'] - cur[-1]['ts']).total_seconds() <= 1200:
            cur.append(r)
        else:
            sess.append(cur)
            cur = [r]
    sess.append(cur)
    lens = sorted(len(s) for s in sess)
    D['rabbit'] = [dict(n=len(s), start=s[0]['ts'].strftime('%Y-%m-%dT%H:%M'), end=s[-1]['ts'].strftime('%H:%M'),
                        hours=round((s[-1]['ts'] - s[0]['ts']).total_seconds() / 3600, 1), first=short(s[0]['title'], 60), last=short(s[-1]['title'], 60),
                        cats=Counter(r['cat'] for r in s).most_common(3), shorts=sum('#short' in r['title'].lower() for r in s))
                   for s in sorted(sess, key=lambda s: -len(s))[:3]]
    D['session_median'] = lens[len(lens) // 2]
    F.append(f"\n## Rabbit holes (session = gaps ≤20 min; median session {D['session_median']} videos)\n" +
             '\n'.join(f"- {r['start']}→{r['end']} ({r['hours']} h, weekday {datetime.fromisoformat(r['start']).strftime('%A')}): {r['n']} videos, mix {r['cats']}, #shorts {r['shorts']}; from “{r['first']}” to “{r['last']}”" for r in D['rabbit']))

    # ---------- quests
    qd = dict(DEFAULT_QUESTS)
    qd.update(labels.get('quests', {}))
    D['quests'] = {}
    for name, pat in qd.items():
        rx = re.compile(pat, re.I)
        c = Counter(r['ts'].strftime('%Y-%m') for r in live if rx.search(r['title']))  # titles only: channel names would count every upload
        if sum(c.values()) >= th(15, 6):
            D['quests'][name] = dict(n=sum(c.values()), months=dict(c))
    F.append('\n## Quests (how-to topics by month)\n' + '\n'.join(f"- {k}: {v['n']} videos, {min(v['months'])} to {max(v['months'])}, peaks " +
                                                       ', '.join(f'{m_} {n}' for m_, n in Counter(v['months']).most_common(3)) for k, v in D['quests'].items()))

    # ---------- rituals: a 1–4 month window holding most plays, across ≥3 years
    groups = {f'channel: {c}': rs for c, rs in cp.items()}
    groups.update({f'artist: {AN[k]}': rs for k, rs in ap_.items()})
    for name, pat in RITUAL_KEYWORDS.items():
        rx = re.compile(pat, re.I)
        groups[f'theme: {name}'] = [r for r in live if rx.search(r['title'] + ' ' + (r['ch'] or ''))]
    rit = []
    for name, rs in groups.items():
        if len(rs) < th(40, 12):
            continue
        mo = Counter(r['ts'].month for r in rs)
        best = None
        for w in (1, 2, 3, 4):
            for s in range(1, 13):
                ms = [((s - 1 + i) % 12) + 1 for i in range(w)]
                share = sum(mo[m_] for m_ in ms) / len(rs)
                need = {1: .3, 2: .45, 3: .55, 4: .65}[w]
                yrs = {r['ts'].year for r in rs if r['ts'].month in ms}
                if share >= need and len(yrs) >= 3 and (best is None or share / w > best[0]):
                    best = (share / w, ms, share, sorted(yrs))
        if best:
            rit.append(dict(name=name, n=len(rs), months=[mo.get(i, 0) for i in range(1, 13)], window=best[1], share=round(best[2], 2), years=best[3]))
    rit.sort(key=lambda x: -x['n'] * x['share'])
    D['rituals'] = rit[:8]
    F.append('\n## Yearly rituals (chart one with rituals.chart_index; "theme" = keyword group across all channels)\n' + '\n'.join(
        f"{i}. {x['name']}: {x['n']} plays, {round(x['share']*100)}% in months {x['window']}, years {x['years'][0]}–{x['years'][-1]} ({len(x['years'])} years)" for i, x in enumerate(D['rituals'])))

    # ---------- on this day
    otd = {}
    for yy in years:
        rs = [r for r in live if r['ts'].year == yy and r['ts'].month == today.month and r['ts'].day == today.day]
        if rs:
            otd[yy] = dict(n=len(rs), s=[short(r['title'], 60) for r in rs[:3]])
    D['otd'] = otd
    F.append(f"\n## On this day ({today.strftime('%d %B')})\n" + '\n'.join(f"- {yy}: {v['n']} plays, e.g. " + '; '.join(v['s']) for yy, v in otd.items()))

    # ---------- searches
    D['searches'] = Counter(s['q'].lower().strip() for s in srch).most_common(12)
    sy = Counter(s['ts'].year for s in srch)
    F.append('\n## Searches\n- Top: ' + ', '.join(f'“{q_}” {n}' for q_, n in D['searches']) + '\n- Per year: ' + ', '.join(f'{k} {v}' for k, v in sorted(sy.items())) + (f" (search history starts {d(srch[0]['ts'])}, it can predate watch history)" if srch else ''))

    # ---------- labeling helpers
    cc = Counter(r['ch'] for r in live if r['ch'])
    samp = defaultdict(Counter)
    for r in live:
        if r['ch']:
            samp[r['ch']][r['title']] += 1
    with open(os.path.join(a.work, 'to_label.tsv'), 'w', encoding='utf-8') as f:
        f.write('plays\tchannel\tcurrent guess\tsample titles\n')
        for c, n in cc.most_common(300):
            guess = Counter(r['cat'] for r in cp[c]).most_common(1)[0][0]
            f.write(f"{n}\t{c}\t{guess}\t{' || '.join(short(t, 60) for t, _ in samp[c].most_common(2))}\n")
    one = [r for r in live if vc[r['v']] == 1 and cc[r['ch']] == 1 and r['cat'] not in ('Music',)]
    random.Random(7).shuffle(one)
    with open(os.path.join(a.work, 'odd_candidates.tsv'), 'w', encoding='utf-8') as f:
        f.write('date\ttitle\tchannel\n')
        for r in sorted(one[:250], key=lambda r: r['ts']):
            f.write(f"{d(r['ts'])}\t{r['title']}\t{r['ch']}\n")
    other = sum(1 for r in live if r['cat'] == 'Other' or r['cat'].endswith('-language other')) / max(1, len(live))
    F.append(f"\n## Topic coverage\n- Unclassified ('Other' + '…-language other') share: {round(other*100)}%. Labeled channels: {len(ch_labels)}. Mood file: {'yes' if moods else 'no'}.")
    D['facts_numbers_note'] = 'Only cite numbers that appear in facts.md.'

    json.dump(D, open(os.path.join(a.work, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    open(os.path.join(a.work, 'facts.md'), 'w', encoding='utf-8').write('\n'.join(F) + '\n')
    print(f"{len(rows):,} plays, {len(srch):,} searches, {years[0]}–{years[-1]}, tz {a.tz}. Unclassified: {round(other*100)}%. Wrote data.json, facts.md, to_label.tsv, artists.tsv, odd_candidates.tsv to {a.work}")


if __name__ == '__main__':
    main()
