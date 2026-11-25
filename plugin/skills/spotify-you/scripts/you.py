"""Turn analyze.py's output plus genres.json into traits, taste directions and clues.

python3 you.py --work <dir>

Reads data.json, facts.md and artists.tsv (from analyze.py) and genres.json (written by Claude).
Writes you_data.json (for the page) and you_facts.md (every number the page may quote).
Every trait is scored 0-100 from fixed thresholds, so the same history always gets the same traits
and friends' pages can be compared.
"""
import argparse
import json
import os
import re
import sys

# Genre -> weights on the five taste directions (Rentfrow & Gosling's MUSIC model:
# Mellow, Unpretentious, Sophisticated, Intense, Contemporary). Loose by design.
GENRES = {
    'pop':               dict(C=1.0),
    'k-pop / j-pop':     dict(C=1.0),
    'dance / edm':       dict(C=1.0),
    'hip-hop / rap':     dict(C=0.8, I=0.2),
    'r&b / soul':        dict(M=0.5, C=0.5),
    'latin':             dict(C=0.7, U=0.3),
    'reggae':            dict(U=0.5, C=0.5),
    'country':           dict(U=1.0),
    'folk / acoustic':   dict(U=0.5, M=0.5),
    'singer-songwriter': dict(M=0.8, U=0.2),
    'indie / alternative': dict(M=0.4, I=0.3, S=0.3),
    'rock':              dict(I=0.6, U=0.4),
    'metal':             dict(I=1.0),
    'punk / hardcore':   dict(I=1.0),
    'electronic':        dict(S=0.4, C=0.4, M=0.2),
    'dream pop / shoegaze': dict(M=0.6, S=0.4),
    'ambient / new age': dict(M=0.6, S=0.4),
    'post-rock / experimental': dict(S=0.6, I=0.4),
    'jazz':              dict(S=0.7, M=0.3),
    'blues':             dict(U=0.5, S=0.3, M=0.2),
    'classical':         dict(S=1.0),
    'soundtrack / score': dict(S=0.6, M=0.4),
    'world / traditional': dict(S=0.5, U=0.5),
    'holiday / novelty': dict(U=1.0),
}
DIMS = [('M', 'Mellow'), ('U', 'Unpretentious'), ('S', 'Sophisticated'), ('I', 'Intense'), ('C', 'Contemporary')]


def lin(x, lo, hi):
    """0 at lo, 100 at hi (hi may be below lo for 'less is more')."""
    if hi == lo:
        return 0
    return max(0, min(100, round((x - lo) / (hi - lo) * 100)))


def pct(x):
    return round(x * 100)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    W = lambda f: os.path.join(a.work, f)  # noqa: E731
    D = json.load(open(W('data.json'), encoding='utf-8'))
    facts = open(W('facts.md'), encoding='utf-8').read()
    m = re.search(r'## Left out of taste sections[^\n]*\n- ([^\n]*)', facts)
    functional = {re.sub(r' [\d,]+ streams$', '', x) for x in m.group(1).split('; ')} if m else set()
    artists = []  # (hours, listens, name) from the top-200 table
    for line in open(W('artists.tsv'), encoding='utf-8').read().splitlines()[1:]:
        p = line.split('\t')
        if len(p) >= 3 and p[2] not in functional:
            artists.append((float(p[0]), int(p[1]), p[2]))
    if not os.path.exists(W('genres.json')):
        sys.exit('genres.json is missing: tag the top artists first (see SKILL.md step 4).')
    gj = json.load(open(W('genres.json'), encoding='utf-8'))
    tags = gj.get('artists', gj)
    bad = sorted({g for g in tags.values() if g not in GENRES and g != 'unsure'})
    if bad:
        sys.exit('genres.json uses genres outside the list: ' + ', '.join(bad) + '\nUse one of: ' + ', '.join(GENRES) + ', or "unsure".')

    T = D['totals']
    func_h = D.get('functional', {}).get('hours', 0)
    taste_h = max(1, T['hours'] - func_h)
    top_h = sum(h for h, _, _ in artists) or 1
    tagged = [(h, tags[n], n) for h, _, n in artists if tags.get(n) in GENRES]
    tag_h = sum(h for h, _, _ in tagged) or 1
    gshare = {}
    gart = {}
    for h, g, n in tagged:
        gshare[g] = gshare.get(g, 0) + h / tag_h
        gart.setdefault(g, []).append(n)
    dim = {k: 0.0 for k, _ in DIMS}
    dim_art = {k: {} for k, _ in DIMS}
    for h, g, n in tagged:
        for k, w in GENRES[g].items():
            dim[k] += w * h / tag_h
            dim_art[k][n] = dim_art[k].get(n, 0) + w * h
    dscore = {k: lin(v, 0, 0.5) for k, v in dim.items()}
    dtop = {k: [n for n, _ in sorted(dim_art[k].items(), key=lambda x: -x[1])[:3]] for k in dim}

    # behavior signals
    years = D['years']
    yk = sorted(years)
    hsum = sum(years[y]['hours'] for y in yk) or 1
    wavg = lambda key: sum((years[y].get(key) or 0) * years[y]['hours'] for y in yk) / hsum  # noqa: E731
    skip = wavg('skip')
    shuffle = wavg('shuffle')
    starts = dict((k, v) for k, v in D.get('starts', []))
    streams = sum(starts.values()) or T['streams']
    picked = starts.get('Picked a song', 0) / streams if starts else 0
    heat = D['heat']
    hours_day = [sum(row[h] for row in heat) for h in range(24)]
    hd = sum(hours_day) or 1
    night = sum(hours_day[h] for h in (21, 22, 23, 0, 1, 2)) / hd
    morning = sum(hours_day[h] for h in range(5, 10)) / hd
    weekend = sum(sum(r) for r in heat[5:]) / hd
    peak_hour = max(range(24), key=lambda h: hours_day[h])
    top10 = sum(h for h, _, _ in artists[:10]) / taste_h
    loops = D.get('loops', [])
    loop = loops[0] if loops else None
    disc = [D['discovery'][y]['share'] for y in sorted(D['discovery'])[1:]]
    disc_avg = sum(disc) / len(disc) if disc else 0
    new_avg = sum(D['discovery'][y]['new'] for y in D['discovery']) / max(1, len(D['discovery']))
    fshare = D.get('functional', {}).get('share', 0)
    trips = [t for t in D.get('travel', {}).get('trips', []) if not t.get('maybe_vpn')]
    home = D.get('travel', {}).get('home')
    countries = sorted({c for t in trips for c in t['c'].split(' → ') if c != home})
    rituals = D.get('rituals', [])
    eras = D.get('eras', [])
    span_years = max(1, len(yk))
    eras_py = len(eras) / span_years
    forgotten = D.get('forgotten_artists', []) + D.get('forgotten', [])
    flings = D.get('flings', [])
    lifers = D.get('lifers', [])
    sess = D.get('session_median_min', 0)
    stops = [x['a'][0] if isinstance(x['a'], list) else x['a'] for x in D.get('seasons', []) if x.get('a')]
    variety = len(set(stops)) / len(stops) if stops else 0
    from datetime import datetime
    span_days = max(1, (datetime.fromisoformat(T['last'][:10]) - datetime.fromisoformat(T['first'][:10])).days + 1)
    steady = T['active_days'] / span_days
    biggest_fling = max((f['peak_share'] for f in flings), default=0)
    ext = D.get('meta', {}).get('export') == 'extended'

    def arts(*names):
        return [n for n in names if n][:3]

    # name, score, clue (numbers here go to you_facts.md), evidence artists
    TR = [
        ('free_thinker', 'Free Thinker', dscore['I'], f"{pct(dim['I'])}% of your tagged listening is intense (metal, punk, rock, heavy hip-hop)", dtop['I']),
        ('experimenter', 'Experimenter', dscore['S'], f"{pct(dim['S'])}% of your tagged listening is sophisticated (jazz, classical, experimental, ambient)", dtop['S']),
        ('romantic', 'Romantic', lin(dim['M'], 0.15, 0.45), f"{pct(dim['M'])}% of your tagged listening is mellow", dtop['M']),
        ('party_starter', 'Party Starter', lin(dim['C'], 0.2, 0.55), f"{pct(dim['C'])}% of your tagged listening is contemporary (pop, dance, hip-hop, latin)", dtop['C']),
        ('down_to_earth', 'Down to Earth', lin(dim['U'], 0.12, 0.4), f"{pct(dim['U'])}% of your tagged listening is unpretentious (country, folk, rock, singalongs)", dtop['U']),
        ('creature_of_habit', 'Creature of Habit', lin(top10, 0.3, 0.75), f"your top 10 artists get {pct(top10)}% of your music time", [n for _, _, n in artists[:3]]),
        ('comfort_seeker', 'Comfort Seeker', lin(loop['n'] if loop else 0, 8, 45), (f"you played “{loop['t']}” by {loop['a']} {loop['n']} times in a row" if loop else 'no song played 5+ times in a row'), arts(loop['a'] if loop else None)),
        ('explorer', 'Explorer', lin(disc_avg, 0.08, 0.35), f"new artists get {pct(disc_avg)}% of a typical year's hours ({round(new_avg)} new artists a year)", []),
        ('night_owl', 'Night Owl', lin(night, 0.18, 0.38), f"{pct(night)}% of your listening happens between 21:00 and 03:00", []),
        ('early_bird', 'Early Bird', lin(morning, 0.08, 0.3), f"{pct(morning)}% of your listening happens between 05:00 and 10:00", []),
        ('restless', 'Restless', lin(skip, 0.2, 0.5), f"you skip {pct(skip)}% of songs within 30 seconds", []),
        ('patient', 'Patient', lin(skip, 0.25, 0.08), f"you skip only {pct(skip)}% of songs within 30 seconds", []),
        ('decisive', 'Knows What They Want', lin(picked, 0.04, 0.3) if ext else 0, f"you pick {pct(picked)}% of songs by hand", []),
        ('go_with_the_flow', 'Goes With the Flow', lin(shuffle, 0.4, 0.95) if ext else 0, f"shuffle is on for {pct(shuffle)}% of your listening", []),
        ('deep_worker', 'Deep Worker', lin(fshare, 0.03, 0.2), f"{pct(fshare)}% of your listening is focus or sleep audio ({func_h} hours)", sorted(functional)[:3]),
        ('globetrotter', 'Globetrotter', lin(len(countries), 0, 6), f"you listened from {len(countries)} other countries" + (f" ({', '.join(countries)})" if countries else ''), []),
        ('seasonal_soul', 'Seasonal Soul', lin(len(rituals), 0, 5), f"{len(rituals)} artists come back in the same months every year", [r['name'] for r in rituals][:3]),
        ('all_in', 'Goes All In', lin(eras_py, 4, 14), f"{len(eras)} eras of one artist on repeat in {span_years} years", [e['a'] for e in sorted(eras, key=lambda e: -e['n'])][:3]),
        ('heart_on_sleeve', 'Heart on Sleeve', lin(len(forgotten) / span_years, 0.3, 2), f"{len(forgotten)} past favorites you stopped playing completely", [f.get('a') for f in forgotten][:3]),
        ('loyalist', 'Loyalist', lin(len(lifers), 3, 14), f"{len(lifers)} artists you've played steadily for 4+ years", lifers[:3]),
        ('weekend_person', 'Weekend Person', lin(weekend, 0.27, 0.4), f"{pct(weekend)}% of your listening happens on weekends", []),
        ('marathoner', 'Marathoner', lin(sess, 25, 90), f"a typical listening session lasts {sess} minutes", []),
        ('shape_shifter', 'Shape-Shifter', lin(variety, 0.25, 0.65), f"{len(set(stops))} different artists topped your {len(stops)} seasons", list(dict.fromkeys(stops))[:3]),
        ('everyday', 'Everyday Listener', lin(steady, 0.6, 0.95), f"music on {pct(steady)}% of days, {T['active_days']:,} in all", []),
    ]
    if biggest_fling:
        TR.append(('crush', 'Falls Hard', lin(biggest_fling, 0.2, 0.6), f"{flings[0]['artist']} took {pct(biggest_fling)}% of your listening in its best month", [flings[0]['artist']]))
    traits = [dict(key=k, name=n, score=s, clue=c, artists=[x for x in ar if x]) for k, n, s, c, ar in TR]
    traits.sort(key=lambda t: -t['score'])
    S = {t['key']: t['score'] for t in traits}
    avg = lambda *k: round(sum(S.get(x, 0) for x in k) / len(k))  # noqa: E731
    lvl = lambda v: 'Very high' if v >= 75 else 'High' if v >= 55 else 'Medium' if v >= 35 else 'Low'  # noqa: E731
    reads = [
        dict(key='open', name='Open to new ideas', score=avg('free_thinker', 'experimenter', 'explorer'), from_=['free_thinker', 'experimenter', 'explorer']),
        dict(key='habit', name='Creature of habit', score=avg('creature_of_habit', 'comfort_seeker', 'loyalist'), from_=['creature_of_habit', 'comfort_seeker', 'loyalist']),
        dict(key='party', name='Life of the party', score=avg('party_starter', 'weekend_person', 'down_to_earth'), from_=['party_starter', 'weekend_person', 'down_to_earth']),
        dict(key='plans', name='Plans ahead', score=avg('decisive', 'deep_worker', 'patient'), from_=['decisive', 'deep_worker', 'patient']),
        dict(key='deep', name='Feels things deeply', score=avg('romantic', 'heart_on_sleeve', 'all_in'), from_=['romantic', 'heart_on_sleeve', 'all_in']),
    ]
    for r in reads:
        r['level'] = lvl(r['score'])
        r['from'] = r.pop('from_')
    sp = lambda v: max(0, min(100, round(v)))  # noqa: E731
    spectrum = [
        dict(l='Cabin in the woods', r='City rooftop', pos=sp(50 + (dscore['C'] - dscore['M']) / 2), clue=f"contemporary {pct(dim['C'])}%, mellow {pct(dim['M'])}%"),
        dict(l='Old friends', r='New people', pos=sp(50 + (S['explorer'] - S['creature_of_habit']) / 2), clue=f"top 10 artists {pct(top10)}% of your time, new artists {pct(disc_avg)}%"),
        dict(l='Read the recipe', r='Wing it', pos=sp(50 + (S['go_with_the_flow'] - S['decisive']) / 2), clue=f"shuffle {pct(shuffle)}%, picked by hand {pct(picked)}%"),
        dict(l='Early bird', r='Night owl', pos=sp(50 + (S['night_owl'] - S['early_bird']) / 2), clue=f"busiest hour {peak_hour}:00"),
        dict(l='Patient', r='Next!', pos=sp(S['restless'] if S['restless'] else 50 - S['patient'] / 2), clue=f"skip rate {pct(skip)}%"),
        dict(l='Stay home', r='Go everywhere', pos=sp(15 + S['globetrotter'] * 0.85), clue=f"{len(countries)} other countries"),
    ]
    clock = [round(v, 1) for v in hours_day]
    years_series = {y: dict(skip=years[y].get('skip'), shuffle=years[y].get('shuffle'), night=years[y].get('night'),
                            new_share=D['discovery'].get(y, {}).get('share'), func=years[y].get('func_hours'), hours=years[y]['hours']) for y in yk}
    coverage = tag_h / top_h
    out = dict(genres=sorted(([g, round(v, 3), gart[g][:4]] for g, v in gshare.items()), key=lambda x: -x[1]),
               dims=[dict(k=k, name=nm, share=round(dim[k], 3), score=dscore[k], artists=dtop[k]) for k, nm in DIMS],
               traits=traits, reads=reads, spectrum=spectrum, clock=clock, peak_hour=peak_hour, years=years_series,
               loop=loop, top10=round(top10, 3), countries=countries, trips=trips, weekend=round(weekend, 3),
               skip=round(skip, 3), picked=round(picked, 3), shuffle=round(shuffle, 3), night=round(night, 3),
               coverage=round(coverage, 3), tagged=len(tagged), extended=ext,
               top_artists=[n for _, _, n in artists[:12]])
    json.dump(out, open(W('you_data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    F = ['# Facts for the "you" page (quote numbers from here or facts.md)',
         f'\n## Genres ({len(tagged)} artists tagged, {pct(coverage)}% of top-artist hours; focus/sleep audio excluded)']
    F += [f"- {g}: {pct(v)}% (" + ', '.join(gart[g][:4]) + ')' for g, v, _ in out['genres']]
    F.append('\n## Taste directions (share of tagged listening; score 0-100)')
    F += [f"- {nm}: {pct(dim[k])}%, score {dscore[k]} (" + ', '.join(dtop[k]) + ')' for k, nm in DIMS]
    F.append('\n## Habits')
    F += [f"- Skip rate (within 30 s): {pct(skip)}%",
          f"- Shuffle on: {pct(shuffle)}% of listening" if ext else '- Shuffle: not in this export',
          f"- Songs picked by hand: {pct(picked)}% of starts" if ext else '- Picked by hand: not in this export',
          f"- Between 21:00 and 03:00: {pct(night)}%; between 05:00 and 10:00: {pct(morning)}%; busiest hour {peak_hour}:00",
          f"- Weekends: {pct(weekend)}% of listening",
          f"- Top 10 artists: {pct(top10)}% of taste hours",
          f"- New artists: {round(new_avg)} a year on average, {pct(disc_avg)}% of a typical year's hours",
          f"- Typical session: {sess} minutes",
          f"- Days with music: {pct(steady)}% of days",
          f"- Different top artists across {len(stops)} seasons: {len(set(stops))}"]
    if loop:
        F.append(f"- Longest loop: “{loop['t']}” by {loop['a']}, {loop['n']} times in a row on {loop['date']}")
    F.append('\n## Traits (score 0-100; 60+ earned, 35-59 almost)')
    F += [f"- {t['name']}: {t['score']} ({t['clue']})" for t in traits]
    F.append('\n## Life reads (average of three traits)')
    F += [f"- {r['name']}: {r['score']}, {r['level']} (from " + ', '.join(r['from']) + ')' for r in reads]
    F.append('\n## This or that (0 = left, 100 = right)')
    F += [f"- {s['l']} vs {s['r']}: {s['pos']} ({s['clue']})" for s in spectrum]
    open(W('you_facts.md'), 'w', encoding='utf-8').write('\n'.join(F) + '\n')
    earned = [t['name'] for t in traits if t['score'] >= 60]
    print(f"{len(earned)} traits earned: {', '.join(earned) or 'none'}. Genres cover {pct(coverage)}% of top-artist hours."
          f" Wrote you_data.json and you_facts.md to {a.work}")
    if coverage < 0.6:
        print(f'WARNING: genres.json covers only {pct(coverage)}% of top-artist hours. Tag more artists (aim for 80%+) and run again.')


if __name__ == '__main__':
    main()
