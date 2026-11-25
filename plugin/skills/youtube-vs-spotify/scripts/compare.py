"""Compare someone's YouTube music watching with their Spotify listening.

python3 compare.py --youtube <takeout.zip|folder> --spotify <my_spotify_data.zip|folder> --work <dir> [--tz Europe/Berlin]

Writes into --work: data.json (page data), facts.md (the only source of numbers for story.json),
artists.tsv (top artists on each side with their plays on the other app, for aliases.json),
youtube_channels.tsv (top channels with the share counted as music, for labels.json).
Reads from --work if present: aliases.json, labels.json (see SKILL.md).

Units: a YouTube music play is one start of a video classified as music.
A Spotify listen is a song stream of 30 s or more; focus/sleep audio is left out.
Only the span both histories cover is compared.
"""
import argparse
import collections as C
import json
import os
import re
import sys
import unicodedata
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from takeout import load as load_yt, system_tz  # noqa: E402
from classify import category, artist  # noqa: E402
from spotify import load as load_sp  # noqa: E402

FUNCTIONAL_RX = re.compile(r'focus|concentrat|brain ?waves?|alpha waves|\bsleep(ing)?\b|meditat|binaural|white noise|brown noise|rain sounds|\bstudy|adhd|\d+\s?hz', re.I)


def norm(s):
    s = unicodedata.normalize('NFKC', s or '').casefold()
    s = re.sub(r'^[♫\W_]+', '', s)
    s = re.sub(r'\s*[(（][^)）]*[)）]\s*$', '', s)  # "中森明菜(나카모리 아키나)" -> "中森明菜"
    s = re.sub(r'vevo$|\s*-\s*topic$|official', '', s)
    return re.sub(r'[^\w]', '', s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--youtube', required=True)
    ap.add_argument('--spotify', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--tz', default=system_tz())
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    rd = lambda n: json.load(open(os.path.join(a.work, n), encoding='utf-8')) if os.path.exists(os.path.join(a.work, n)) else {}  # noqa: E731
    aliases, labels = rd('aliases.json'), rd('labels.json')
    amap = {norm(k): norm(v) for k, v in aliases.get('names', {}).items()}
    display = {norm(v): v for v in aliases.get('names', {}).values()}
    key = lambda s: amap.get(norm(s), norm(s))  # noqa: E731
    func = {x.casefold() for x in labels.get('functional', [])}
    not_func = {x.casefold() for x in labels.get('not_functional', [])}
    ytlab = {k.strip().lower(): v for k, v in labels.get('youtube_channels', {}).items()}

    yrows, _, _ = load_yt(a.youtube, a.tz)
    srows, kind = load_sp(a.spotify, a.tz)
    yt, chan = [], C.defaultdict(lambda: [0, 0, C.Counter()])
    for r in yrows:
        if r['removed']:
            continue
        music = category(r['title'], r['ch'], ytlab) == 'Music'
        if r['ch']:
            c = chan[r['ch']]
            c[0] += 1
            c[1] += music
            c[2][r['title']] += 1
        if music:
            yt.append(dict(ts=r['ts'].replace(tzinfo=None), a=artist(r['title'], r['ch']), title=r['title']))
    sp, hits, tot_a = [], C.Counter(), C.Counter()
    tracks = [r for r in srows if r['kind'] == 'track' and r['ms'] >= 30000]
    kinds = C.defaultdict(set)
    for r in tracks:  # focus/sleep audio is decided per artist, by titles, and never by a single song
        tot_a[r['artist']] += 1
        if FUNCTIONAL_RX.search(r['track']):
            hits[r['artist']] += 1
            kinds[r['artist']].add(r['track'].casefold())
    func_set = {x for x in tot_a if (x.casefold() in func or (len(kinds[x]) >= 2 and (hits[x] / tot_a[x] >= 0.6 or
                                     (FUNCTIONAL_RX.search(x) and hits[x] / tot_a[x] >= 0.3)))) and x.casefold() not in not_func}
    for r in tracks:
        if r['artist'] not in func_set:
            sp.append(dict(ts=r['start'].replace(tzinfo=None), a=r['artist'], t=r['track']))
    excluded = C.Counter(r['artist'] for r in tracks if r['artist'] in func_set)
    if not yt or not sp:
        raise SystemExit('One of the histories has no music in it.')
    t0 = max(min(x['ts'] for x in yt), min(x['ts'] for x in sp))
    t1 = min(max(x['ts'] for x in yt), max(x['ts'] for x in sp))
    if t0 >= t1:
        raise SystemExit('The two histories do not overlap in time.')
    yt = [x for x in yt if t0 <= x['ts'] <= t1]
    sp = [x for x in sp if t0 <= x['ts'] <= t1]
    # A YouTube credit like "A & B" or "A and B" matches Spotify's "A" when only "A" exists there.
    sp_keys = {key(x['a']) for x in sp}
    for x in yt:
        if x['a'] and key(x['a']) not in sp_keys:
            first = re.split(r'\s*(?:&| and | и )\s*', x['a'], maxsplit=1)[0]
            if first != x['a'] and key(first) in sp_keys:
                x['a'] = first
    D = dict(window=[str(t0.date()), str(t1.date())], yt_total=len(yt), sp_total=len(sp), spotify_export=kind, tz=a.tz)
    F = [f"## Window\n- Compared span: {t0.date()} to {t1.date()} (both histories cover it). Spotify export: {kind}. Times in {a.tz}.",
         '- Left out as focus/sleep audio (check; fix with labels.json): ' + ('; '.join(f'{x} {n:,}' for x, n in excluded.most_common(15)) or 'nothing') + '\n' +
         f"- YouTube music plays: {len(yt):,}. Spotify listens (30 s+, focus/sleep audio excluded): {len(sp):,}. "
         f"Spotify share of all music plays: {round(100 * len(sp) / (len(sp) + len(yt)))}%."]

    name = {}
    for x in yt:
        if x['a']:
            name.setdefault(key(x['a']), re.sub(r'^[♫\s]+', '', x['a']))
    for x in sp:
        name[key(x['a'])] = x['a']
    name.update(display)

    years = list(range(t0.year, t1.year + 1))
    D['years'] = [[y, sum(1 for x in yt if x['ts'].year == y), sum(1 for x in sp if x['ts'].year == y)] for y in years]
    F.append('\n## By year (YouTube plays / Spotify listens / Spotify share)\n' + '\n'.join(
        f'- {y}: {u:,} / {s:,} / {round(100 * s / (u + s)) if u + s else 0}%' for y, u, s in D['years']))

    hy, hs = C.Counter(x['ts'].hour for x in yt), C.Counter(x['ts'].hour for x in sp)
    D['hours'] = [[h, round(hy[h] / len(yt), 4), round(hs[h] / len(sp), 4)] for h in range(24)]
    D['peak'] = [hy.most_common(1)[0][0], hs.most_common(1)[0][0]]
    D['night'] = [round(sum(hy[h] for h in range(5)) / len(yt), 3), round(sum(hs[h] for h in range(5)) / len(sp), 3)]
    D['weekend'] = [round(sum(1 for x in yt if x['ts'].weekday() >= 5) / len(yt), 3), round(sum(1 for x in sp if x['ts'].weekday() >= 5) / len(sp), 3)]
    F.append(f"\n## When\n- Peak hour: YouTube {D['peak'][0]}:00, Spotify {D['peak'][1]}:00.\n"
             f"- After midnight (00–05): YouTube {round(D['night'][0] * 100)}%, Spotify {round(D['night'][1] * 100)}%.\n"
             f"- Weekends: YouTube {round(D['weekend'][0] * 100)}%, Spotify {round(D['weekend'][1] * 100)}%.")

    dy, ds = {x['ts'].date() for x in yt}, {x['ts'].date() for x in sp}
    D['days'] = dict(both=len(dy & ds), yt=len(dy - ds), sp=len(ds - dy))
    F.append(f"\n## Days\n- Days with music: {len(dy | ds):,}. Both apps: {D['days']['both']:,}. YouTube only: {D['days']['yt']:,}. Spotify only: {D['days']['sp']:,}.")

    ya, sa = C.Counter(key(x['a']) for x in yt if x['a']), C.Counter(key(x['a']) for x in sp)
    D['top50_overlap'] = len({k for k, _ in ya.most_common(50)} & {k for k, _ in sa.most_common(50)})
    shared = [k for k in set(ya) & set(sa) if ya[k] >= 20 and sa[k] >= 20]
    shared.sort(key=lambda k: -(ya[k] / len(yt) + sa[k] / len(sp)))
    D['lean'] = [[name[k], ya[k], sa[k]] for k in shared[:24]]
    lean_pct = {k: (ya[k] / len(yt)) / (ya[k] / len(yt) + sa[k] / len(sp)) for k in shared}
    F.append(f"\n## Artists\n- Top-50 artists in common: {D['top50_overlap']} of 50.\n- Biggest shared artists (YouTube plays / Spotify listens / YouTube lean, where 50% = equal share of each app's plays):\n" +
             '\n'.join(f"  - {name[k]}: {ya[k]:,} / {sa[k]:,} / {round(lean_pct[k] * 100)}% YouTube" for k in shared[:24]))
    D['yt_only'] = [[name[k], ya[k], sa[k]] for k, _ in ya.most_common() if sa[k] <= ya[k] * 0.05 and ya[k] >= 30][:8]
    D['sp_only'] = [[name[k], ya[k], sa[k]] for k, _ in sa.most_common() if ya[k] <= sa[k] * 0.03 and sa[k] >= 80][:8]
    F.append('- Mostly YouTube only: ' + '; '.join(f'{n} {u:,} vs {s:,} on Spotify' for n, u, s in D['yt_only']) +
             '\n- Mostly Spotify only: ' + '; '.join(f'{n} {s:,} vs {u:,} on YouTube' for n, u, s in D['sp_only']))

    fy, fs = {}, {}
    for x in sorted(yt, key=lambda x: x['ts']):
        if x['a']:
            fy.setdefault(key(x['a']), x['ts'])
    for x in sorted(sp, key=lambda x: x['ts']):
        fs.setdefault(key(x['a']), x['ts'])
    both = [k for k in set(ya) & set(sa) if ya[k] >= 15 and sa[k] >= 15]
    # Artists first heard in the window's first 30 days were probably known before it began: no "first" for them.
    edge = t0 + timedelta(days=30)
    early = [k for k in both if min(fy[k], fs[k]) < edge]
    both = [k for k in both if k not in early]
    first_yt = [k for k in both if fy[k].date() < fs[k].date()]
    first_sp = [k for k in both if fs[k].date() < fy[k].date()]
    same_day = [k for k in both if fs[k].date() == fy[k].date()]
    lag = sorted((fs[k] - fy[k]).days for k in first_yt)
    lag2 = sorted((fy[k] - fs[k]).days for k in first_sp)
    D['discovery'] = dict(n=len(both), yt_first=len(first_yt), sp_first=len(first_sp), same_day=len(same_day), early=len(early),
                          median_lag=lag[len(lag) // 2] if lag else None, median_lag_sp=lag2[len(lag2) // 2] if lag2 else None,
                          slow=[[name[k], str(fy[k].date()), str(fs[k].date()), (fs[k] - fy[k]).days] for k in sorted(first_yt, key=lambda k: -(fs[k] - fy[k]).days) if sa[k] >= 50][:6],
                          sp_led=[[name[k], str(fs[k].date()), str(fy[k].date()), (fy[k] - fs[k]).days] for k in sorted(first_sp, key=lambda k: -sa[k])][:6])
    dsc = D['discovery']
    F.append(f"\n## Discovery (artists with 15+ plays on each app, first heard after {edge.date()}: {dsc['n']}; {dsc['early']} more were already playing in the window's first 30 days and are left out)\n- Found first on YouTube: {dsc['yt_first']}; on Spotify: {dsc['sp_first']}; same day on both: {dsc['same_day']}."
             f"\n- Median days from first YouTube play to first Spotify listen: {dsc['median_lag']}. The other way: {dsc['median_lag_sp']}."
             '\n- Slowest moves to Spotify: ' + '; '.join(f"{n} ({u} → {s}, {d:,} day{'s' if d != 1 else ''})" for n, u, s, d in dsc['slow']) +
             '\n- Found on Spotify first: ' + '; '.join(f"{n} ({s} → {u}, {d:,} day{'s' if d != 1 else ''})" for n, s, u, d in dsc['sp_led']))

    def songkey(art, t):
        t = re.sub(r'\(.*?\)|\[.*?\]|official.*|music video|lyrics?|\baudio\b|\bhq\b|\bhd\b|\b4k\b|\s[-–]\s*live\b.*|\blive (at|from|on|in)\b.*|\bremaster(ed)?\b.*', '', (t or '').casefold())
        return key(art) + '|' + re.sub(r'[^\w]', '', t)
    ys = C.Counter()
    for x in yt:
        m = re.match(r'^\s*(.+?)\s+[-–—]\s+(.+)$', x['title'] or '')
        if m and x['a']:
            ys[songkey(x['a'], m.group(2))] += 1
    ss = C.Counter(songkey(x['a'], x['t']) for x in sp)
    st = {}
    for x in sp:
        st.setdefault(songkey(x['a'], x['t']), (x['a'], re.sub(r'\s*[-–]\s*(live|\d{4} remaster(ed)?|remaster(ed)?( \d{4})?)\b.*$|\s*\((\d{4} )?remaster(ed)?( \d{4})?\)', '', x['t'], flags=re.I)))
    common = sorted((k for k in ys if k in ss and ys[k] >= 10 and ss[k] >= 10), key=lambda k: -min(ys[k] / len(yt), ss[k] / len(sp)))
    D['songs'] = [[st[k][1], st[k][0], ys[k], ss[k]] for k in common[:10]]
    F.append('\n## Songs played on both (10+ each; YouTube plays / Spotify listens; live and remastered versions count with the song)\n' + '\n'.join(f'- “{t}” by {ar}: {u} / {s}' for t, ar, u, s in D['songs']))

    with open(os.path.join(a.work, 'artists.tsv'), 'w', encoding='utf-8') as f:
        f.write('side\tplays\tartist\tplays on the other app\n')
        for side, cnt, other in (('YouTube', ya, sa), ('Spotify', sa, ya)):
            for k, n in cnt.most_common(120):
                f.write(f"{side}\t{n}\t{name.get(k, k)}\t{other[k]}\n")
    with open(os.path.join(a.work, 'youtube_channels.tsv'), 'w', encoding='utf-8') as f:
        f.write('plays\tchannel\tshare counted as music\tsample titles\n')
        for chn, (n, m, tc) in sorted(chan.items(), key=lambda kv: -kv[1][0])[:120]:
            f.write(f"{n}\t{chn}\t{round(100 * m / n)}%\t{' || '.join(t[:60] for t, _ in tc.most_common(2))}\n")
    json.dump(D, open(os.path.join(a.work, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(a.work, 'facts.md'), 'w', encoding='utf-8').write('\n'.join(F) + '\n')
    print(f"{t0.date()} to {t1.date()}: {len(yt):,} YouTube music plays vs {len(sp):,} Spotify listens. "
          f"Top-50 overlap {D['top50_overlap']}. Wrote data.json, facts.md, artists.tsv to {a.work}")


if __name__ == '__main__':
    main()
