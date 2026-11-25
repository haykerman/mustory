"""Turn the YouTube analysis plus genres.json and topics.json into traits, taste directions and clues.

python3 you.py --work <dir>

Reads data.json, facts.md and artists.tsv (from analyze.py), genres.json (music artists -> genre) and
topics.json (their watch topics -> a part of life), both written by Claude.
Writes you_data.json (for the page) and you_facts.md (every number the page may quote).
Every trait is scored 0-100 from fixed thresholds, so the same history always gets the same traits.
"""
import argparse
import json
import os
import sys
from datetime import datetime

GENRES = {
    'pop': dict(C=1.0), 'k-pop / j-pop': dict(C=1.0), 'dance / edm': dict(C=1.0), 'hip-hop / rap': dict(C=0.8, I=0.2),
    'r&b / soul': dict(M=0.5, C=0.5), 'latin': dict(C=0.7, U=0.3), 'reggae': dict(U=0.5, C=0.5), 'country': dict(U=1.0),
    'folk / acoustic': dict(U=0.5, M=0.5), 'singer-songwriter': dict(M=0.8, U=0.2), 'indie / alternative': dict(M=0.4, I=0.3, S=0.3),
    'rock': dict(I=0.6, U=0.4), 'metal': dict(I=1.0), 'punk / hardcore': dict(I=1.0), 'electronic': dict(S=0.4, C=0.4, M=0.2),
    'dream pop / shoegaze': dict(M=0.6, S=0.4), 'ambient / new age': dict(M=0.6, S=0.4), 'post-rock / experimental': dict(S=0.6, I=0.4),
    'jazz': dict(S=0.7, M=0.3), 'blues': dict(U=0.5, S=0.3, M=0.2), 'classical': dict(S=1.0), 'soundtrack / score': dict(S=0.6, M=0.4),
    'world / traditional': dict(S=0.5, U=0.5), 'holiday / novelty': dict(U=1.0),
}
DIMS = [('M', 'Mellow'), ('U', 'Unpretentious'), ('S', 'Sophisticated'), ('I', 'Intense'), ('C', 'Contemporary')]
# The parts of life a watch topic can belong to (topics.json maps each topic to one of these keys).
LIFE = {
    'music': 'Music', 'learning': 'Learning & how-to', 'making': 'Making things', 'stories': 'Stories, film & TV',
    'news': 'News & ideas', 'comedy': 'Comedy', 'gaming': 'Gaming', 'lifestyle': 'Vlogs & lifestyle', 'tech': 'Tech',
    'self': 'Self & body', 'calm': 'Calm & sleep', 'other': 'Unsorted',
}


def lin(x, lo, hi):
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
    for f in ('genres.json', 'topics.json'):
        if not os.path.exists(W(f)):
            sys.exit(f'{f} is missing: write it first (see SKILL.md step 4).')
    tags = json.load(open(W('genres.json'), encoding='utf-8')).get('artists', {})
    bad = sorted({g for g in tags.values() if g not in GENRES and g != 'unsure'})
    if bad:
        sys.exit('genres.json uses genres outside the list: ' + ', '.join(bad) + '\nUse one of: ' + ', '.join(GENRES) + ', or "unsure".')
    tj = json.load(open(W('topics.json'), encoding='utf-8'))
    tmap = tj.get('topics', {})
    qmap = tj.get('quests', {})
    bad = sorted({v for v in list(tmap.values()) + list(qmap.values()) if v not in LIFE})
    if bad:
        sys.exit('topics.json uses parts of life outside the list: ' + ', '.join(bad) + '\nUse one of: ' + ', '.join(LIFE))

    artists = []
    for line in open(W('artists.tsv'), encoding='utf-8').read().splitlines()[1:]:
        p = line.split('\t')
        if len(p) >= 2 and p[0].isdigit():
            artists.append((int(p[0]), p[1]))
    top_n = sum(n for n, _ in artists) or 1
    tagged = [(n, tags[x], x) for n, x in artists if tags.get(x) in GENRES]
    tag_n = sum(n for n, _, _ in tagged) or 1
    gshare, gart = {}, {}
    dim = {k: 0.0 for k, _ in DIMS}
    dim_art = {k: {} for k, _ in DIMS}
    for n, g, x in tagged:
        gshare[g] = gshare.get(g, 0) + n / tag_n
        gart.setdefault(g, []).append(x)
        for k, w in GENRES[g].items():
            dim[k] += w * n / tag_n
            dim_art[k][x] = dim_art[k].get(x, 0) + w * n
    dscore = {k: lin(v, 0, 0.5) for k, v in dim.items()}
    dtop = {k: [x for x, _ in sorted(dim_art[k].items(), key=lambda t: -t[1])[:3]] for k in dim}

    # parts of life from watch topics
    topics = D.get('topics', [])
    if not topics:
        sys.exit('data.json has no topics: run analyze.py from this skill (it adds them).')
    tot = sum(n for _, n in topics) or 1
    life, life_top = {}, {}
    unmapped = []
    for c, n in topics:
        if c == 'Music':
            b = 'music'
        elif c == 'Other' or c.endswith('-language other'):
            b = 'other'
        else:
            b = tmap.get(c)
            if not b:
                unmapped.append(c)
                b = 'other'
        life[b] = life.get(b, 0) + n / tot
        life_top.setdefault(b, []).append(c)
    if unmapped:
        print('Topics not in topics.json (counted as Unsorted): ' + ', '.join(unmapped))
    # how-to hobbies count toward the part of life they belong to (scoring only)
    qplus = {}
    for q, v in D.get('quests', {}).items():
        b = qmap.get(q)
        if b:
            qplus[b] = qplus.get(b, 0) + v['n'] / tot
    L = lambda b: life.get(b, 0) + qplus.get(b, 0)  # noqa: E731

    T = D['totals']
    heat = D['heat']
    hours_day = [sum(row[h] for row in heat) for h in range(24)]
    hd = sum(hours_day) or 1
    night = sum(hours_day[h] for h in (21, 22, 23, 0, 1, 2)) / hd
    morning = sum(hours_day[h] for h in range(5, 10)) / hd
    weekend = sum(sum(r) for r in heat[5:]) / hd
    peak_hour = max(range(24), key=lambda h: hours_day[h])
    years = sorted(D.get('year_totals', {}))
    span_years = max(1, len(years))
    obs = D.get('obsessions', [])
    loop = dict(t=obs[0]['t'], n=obs[0]['n'], s=obs[0]['s'], e=obs[0]['e']) if obs else None
    once = T.get('once_share', 0)
    rewatch = T.get('share_to_10plus', 0)
    rabbit = D.get('rabbit', [{}])[0] if D.get('rabbit') else None
    searches_per_play = T.get('searches', 0) / max(1, T['plays'])
    quests = sorted(((k, v['n']) for k, v in D.get('quests', {}).items()), key=lambda x: -x[1])
    quest_videos = sum(n for _, n in quests)
    rituals = D.get('rituals', [])
    eras = D.get('eras', [])
    forgotten = D.get('forgotten', []) + D.get('forgotten_channels', [])
    flings = D.get('flings', [])
    steady = D.get('steady', [])
    stops = [x['a'][0] for x in D.get('seasons', []) if x.get('a')]
    variety = len(set(stops)) / len(stops) if stops else 0
    span_days = max(1, (datetime.fromisoformat(T['last'][:10]) - datetime.fromisoformat(T['first'][:10])).days + 1)
    everyday = T.get('active_days', 0) / span_days
    big_flings = [f for f in flings if f['n'] >= 30]
    biggest_fling = max(big_flings, key=lambda f: f['peak_share']) if big_flings else None
    comfort = D.get('comfort', [])

    def lt(b):
        return life_top.get(b, [])[:3]

    TR = [
        ('free_thinker', 'Free Thinker', dscore['I'], f"{pct(dim['I'])}% of your tagged music is intense (metal, punk, rock, heavy hip-hop)", dtop['I']),
        ('experimenter', 'Experimenter', dscore['S'], f"{pct(dim['S'])}% of your tagged music is sophisticated (jazz, classical, experimental, ambient)", dtop['S']),
        ('romantic', 'Romantic', lin(dim['M'], 0.15, 0.45), f"{pct(dim['M'])}% of your tagged music is mellow", dtop['M']),
        ('party_starter', 'Party Starter', lin(dim['C'], 0.2, 0.55), f"{pct(dim['C'])}% of your tagged music is contemporary (pop, dance, hip-hop, latin)", dtop['C']),
        ('down_to_earth', 'Down to Earth', lin(dim['U'], 0.12, 0.4), f"{pct(dim['U'])}% of your tagged music is unpretentious (country, folk, rock, singalongs)", dtop['U']),
        ('music_first', 'Music First', lin(L('music'), 0.35, 0.75), f"{pct(L('music'))}% of what you play is music", [x for _, x in artists[:3]]),
        ('lifelong_learner', 'Lifelong Learner', lin(L('learning'), 0.02, 0.08),
         f"{pct(L('learning'))}% of your plays are learning and how-to" + (f", counting {sum(n for q, n in quests if qmap.get(q) == 'learning'):,} videos on hobbies like {', '.join(q for q, _ in quests if qmap.get(q) == 'learning')[:60]}" if any(qmap.get(q) == 'learning' for q, _ in quests) else ''), [q for q, _ in quests if qmap.get(q) == 'learning'][:3] or lt('learning')),
        ('maker', 'Maker', lin(L('making'), 0.01, 0.07), f"{pct(L('making'))}% of your plays are about making things" + (f", counting {sum(n for q, n in quests if qmap.get(q) == 'making'):,} how-to videos" if any(qmap.get(q) == 'making' for q, _ in quests) else ''), [q for q, _ in quests if qmap.get(q) == 'making'][:3] or lt('making')),
        ('story_lover', 'Story Lover', lin(L('stories'), 0.05, 0.25), f"{pct(L('stories'))}% of your plays are stories, film and TV", lt('stories')),
        ('well_informed', 'Well Informed', lin(L('news'), 0.03, 0.15), f"{pct(L('news'))}% of your plays are news and ideas", lt('news')),
        ('class_clown', 'Class Clown', lin(L('comedy'), 0.03, 0.15), f"{pct(L('comedy'))}% of your plays are comedy", lt('comedy')),
        ('gamer', 'Gamer', lin(L('gaming'), 0.02, 0.12), f"{pct(L('gaming'))}% of your plays are gaming", lt('gaming')),
        ('gadget_head', 'Gadget Head', lin(L('tech'), 0.03, 0.15), f"{pct(L('tech'))}% of your plays are tech", lt('tech')),
        ('self_improver', 'Self-Improver', lin(L('self'), 0.02, 0.1), f"{pct(L('self'))}% of your plays are about mind and body", lt('self')),
        ('homebody', 'Homebody', lin(L('lifestyle'), 0.03, 0.15), f"{pct(L('lifestyle'))}% of your plays are vlogs and lifestyle", lt('lifestyle')),
        ('calm', 'Needs Quiet', lin(L('calm'), 0.01, 0.06), f"{pct(L('calm'))}% of your plays are calm and sleep sounds", lt('calm')),
        ('night_owl', 'Night Owl', lin(night, 0.18, 0.38), f"{pct(night)}% of your plays happen between 21:00 and 03:00", []),
        ('early_bird', 'Early Bird', lin(morning, 0.08, 0.3), f"{pct(morning)}% of your plays happen between 05:00 and 10:00", []),
        ('weekend_person', 'Weekend Person', lin(weekend, 0.27, 0.4), f"{pct(weekend)}% of your plays happen on weekends", []),
        ('comfort_seeker', 'Comfort Seeker', lin(loop['n'] if loop else 0, 12, 50), (f"you played “{loop['t']}” {loop['n']} times in a few weeks" if loop else 'no single obsession'), []),
        ('explorer', 'Explorer', lin(once, 0.7, 0.92), f"{pct(once)}% of the videos you open, you watch only once", []),
        ('creature_of_habit', 'Creature of Habit', lin(rewatch, 0.04, 0.2), f"videos you replayed 10+ times take {pct(rewatch)}% of your plays", []),
        ('rabbit_holer', 'Rabbit-Holer', lin(rabbit['n'] if rabbit else 0, 30, 120), (f"your deepest rabbit hole was {rabbit['n']} videos in one sitting" if rabbit else 'no long sessions'), []),
        ('asks_questions', 'Asks Questions', lin(searches_per_play, 0.15, 0.5), f"{T.get('searches', 0):,} searches, one for every {round(1 / searches_per_play) if searches_per_play else 0} plays", []),
        ('seasonal_soul', 'Seasonal Soul', lin(len(rituals), 1, 10), f"{len(rituals)} things come back in the same months every year", [r['name'].split(': ', 1)[-1] for r in rituals][:3]),
        ('all_in', 'Goes All In', lin(len(eras) / span_years, 1, 6), f"{len(eras)} eras of one artist on repeat in {span_years} years", [e['a'] for e in sorted(eras, key=lambda e: -e['n'])][:3]),
        ('heart_on_sleeve', 'Heart on Sleeve', lin(len(forgotten) / span_years, 1, 4), f"{len(forgotten)} past favorites and channels you stopped playing completely", [f.get('ch') for f in forgotten if f.get('ch')][:3]),
        ('loyalist', 'Loyalist', lin(len(steady), 2, 10), f"{len(steady)} artists you've played steadily for years", [x['artist'] for x in steady][:3]),
        ('shape_shifter', 'Shape-Shifter', lin(variety, 0.25, 0.65), f"{len(set(stops))} different artists topped your {len(stops)} seasons", list(dict.fromkeys(stops))[:3]),
        ('everyday', 'Everyday Viewer', lin(everyday, 0.6, 0.95), f"something played on {pct(everyday)}% of days, {T.get('active_days', 0):,} in all", []),
    ]
    if biggest_fling:
        TR.append(('crush', 'Falls Hard', lin(biggest_fling['peak_share'], 0.3, 0.8), f"{biggest_fling['artist']} got {pct(biggest_fling['peak_share'])}% of its plays in a single month", [biggest_fling['artist']]))
    if comfort:
        TR.append(('night_comfort', 'Midnight Regular', lin(len(comfort), 2, 12), f"{len(comfort)} videos you mostly play after midnight", []))
    traits = [dict(key=k, name=n, score=s, clue=c, artists=[x for x in ar if x]) for k, n, s, c, ar in TR]
    traits.sort(key=lambda t: -t['score'])
    S = {t['key']: t['score'] for t in traits}
    avg = lambda *k: round(sum(S.get(x, 0) for x in k) / len(k))  # noqa: E731
    lvl = lambda v: 'Very high' if v >= 75 else 'High' if v >= 55 else 'Medium' if v >= 35 else 'Low'  # noqa: E731
    reads = [
        dict(key='open', name='Open to new ideas', fr=['free_thinker', 'experimenter', 'explorer']),
        dict(key='habit', name='Creature of habit', fr=['creature_of_habit', 'comfort_seeker', 'loyalist']),
        dict(key='party', name='Life of the party', fr=['party_starter', 'class_clown', 'weekend_person']),
        dict(key='plans', name='Plans ahead', fr=['lifelong_learner', 'maker', 'asks_questions']),
        dict(key='deep', name='Feels things deeply', fr=['romantic', 'heart_on_sleeve', 'story_lover']),
    ]
    for r in reads:
        r['from'] = r.pop('fr')
        r['score'] = avg(*r['from'])
        r['level'] = lvl(r['score'])
    sp = lambda v: max(0, min(100, round(v)))  # noqa: E731
    spectrum = [
        dict(l='Cabin in the woods', r='City rooftop', pos=sp(50 + (dscore['C'] - dscore['M']) / 2), clue=f"contemporary {pct(dim['C'])}%, mellow {pct(dim['M'])}%"),
        dict(l='Old favorites', r='Something new', pos=sp(50 + (S['explorer'] - S['creature_of_habit']) / 2), clue=f"{pct(once)}% watched once, {pct(rewatch)}% on replays"),
        dict(l='A good laugh', r='A good argument', pos=sp(50 + (S['well_informed'] - S['class_clown']) / 2), clue=f"news {pct(L('news'))}%, comedy {pct(L('comedy'))}%"),
        dict(l='Early bird', r='Night owl', pos=sp(50 + (S['night_owl'] - S['early_bird']) / 2), clue=f"busiest hour {peak_hour}:00"),
        dict(l='One quick video', r='Down the rabbit hole', pos=sp(15 + S['rabbit_holer'] * 0.85), clue=(f"deepest session {rabbit['n']} videos" if rabbit else 'no long sessions')),
        dict(l='Watch it', r='Learn to do it', pos=sp(20 + S['lifelong_learner'] * 0.8), clue=f"{quest_videos:,} how-to videos"),
    ]
    nby = D.get('night_by_year', {})
    yt = D.get('year_totals', {})
    years_series = {y: dict(night=nby.get(y), plays=yt.get(y)) for y in years}
    life_list = sorted(([LIFE[b], round(v, 3), life_top[b][:4]] for b, v in life.items() if b not in ('music', 'other')), key=lambda x: -x[1])
    coverage = tag_n / top_n
    out = dict(genres=sorted(([g, round(v, 3), gart[g][:4]] for g, v in gshare.items()), key=lambda x: -x[1]),
               dims=[dict(k=k, name=nm, share=round(dim[k], 3), score=dscore[k], artists=dtop[k]) for k, nm in DIMS],
               life=life_list, quests=quests, rabbit=rabbit, traits=traits, reads=reads, spectrum=spectrum,
               clock=[round(v, 1) for v in hours_day], peak_hour=peak_hour, years=years_series, loop=loop,
               top10=round(rewatch, 3), weekend=round(weekend, 3), night=round(night, 3), coverage=round(coverage, 3), tagged=len(tagged),
               charts=['clock', 'night', 'morning', 'taste', 'dims', 'life', 'quests', 'rabbit', 'loop', 'night_years', 'plays_years', 'weekend'],
               clock_caption='Your real 24-hour clock: when YouTube is on',
               method=['This is for fun, not science. The guesses about life are playful readings of your YouTube history, loosely inspired by music-psychology research that links taste to personality (Rentfrow and Gosling\'s five taste directions). The numbers behind each clue are real.',
                       f'Music genres were tagged by hand for {len(tagged)} of your top artists, covering {pct(coverage)}% of their plays. Watch topics come from the channels you play most, each placed in a part of life by hand.',
                       'Each trait is scored 0–100 from fixed thresholds, so the same history always gets the same traits and two people\'s pages can be compared. 60 or more earns a badge.',
                       'Source: a Google Takeout export of YouTube watch and search history. Ads are left out; deleted videos still count as plays.'])
    json.dump(out, open(W('you_data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    F = ['# Facts for the "you" page (quote numbers from here or facts.md)',
         f'\n## Music genres ({len(tagged)} artists tagged, {pct(coverage)}% of top-artist plays)']
    F += [f"- {g}: {pct(v)}% (" + ', '.join(gart[g][:4]) + ')' for g, v, _ in out['genres']]
    F.append('\n## Taste directions (share of tagged music plays; score 0-100)')
    F += [f"- {nm}: {pct(dim[k])}%, score {dscore[k]} (" + ', '.join(dtop[k]) + ')' for k, nm in DIMS]
    F.append('\n## Parts of life (share of all playable videos)')
    F += [f"- {LIFE[b]}: {pct(v)}% (" + ', '.join(life_top[b][:4]) + ')' for b, v in sorted(life.items(), key=lambda x: -x[1])]
    F.append('\n## Habits')
    F += [f"- Between 21:00 and 03:00: {pct(night)}% of plays; between 05:00 and 10:00: {pct(morning)}%; busiest hour {peak_hour}:00",
          f"- Weekends: {pct(weekend)}% of plays",
          f"- Watched once: {pct(once)}% of videos; replayed 10+ times: {pct(rewatch)}% of plays",
          f"- Searches: {T.get('searches', 0):,} ({round(searches_per_play * 100)} per 100 plays)",
          f"- How-to hobbies: " + ', '.join(f'{q} {n}' for q, n in quests) + f" ({quest_videos:,} videos)",
          f"- Days with any play: {pct(everyday)}% of days",
          f"- Different top artists across {len(stops)} seasons: {len(set(stops))}"]
    if loop:
        F.append(f"- Biggest obsession: “{loop['t']}”, {loop['n']} plays between {loop['s']} and {loop['e']}")
    if rabbit:
        F.append(f"- Deepest rabbit hole: {rabbit['n']} videos on {rabbit['start'][:10]}")
    F.append('\n## Traits (score 0-100; 60+ earned, 35-59 almost)')
    F += [f"- {t['name']}: {t['score']} ({t['clue']})" for t in traits]
    F.append('\n## Life reads (average of three traits)')
    F += [f"- {r['name']}: {r['score']}, {r['level']} (from " + ', '.join(r['from']) + ')' for r in reads]
    F.append('\n## This or that (0 = left, 100 = right)')
    F += [f"- {s['l']} vs {s['r']}: {s['pos']} ({s['clue']})" for s in spectrum]
    open(W('you_facts.md'), 'w', encoding='utf-8').write('\n'.join(F) + '\n')
    earned = [t['name'] for t in traits if t['score'] >= 60]
    print(f"{len(earned)} traits earned: {', '.join(earned) or 'none'}. Genres cover {pct(coverage)}% of top-artist plays."
          f" Wrote you_data.json and you_facts.md to {a.work}")
    if coverage < 0.6:
        print(f'WARNING: genres.json covers only {pct(coverage)}% of top-artist plays. Tag more artists (aim for 80%+) and run again.')


if __name__ == '__main__':
    main()
