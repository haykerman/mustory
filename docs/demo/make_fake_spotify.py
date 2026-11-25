"""Make a fake Spotify "Extended streaming history" export for the demo page.

python3 make_fake_spotify.py <out.zip>

Every artist, track and listener here is made up. The data has stories baked in so the
demo shows each chapter: eras, loops, a rising-then-falling skip rate, a focus-music habit,
a phone-to-laptop device switch, two trips, a summer ritual, Christmas songs, a playlist
left running overnight, and a few one-off oddities.
"""
import json
import random
import sys
import zipfile
from datetime import datetime, timedelta, timezone

rnd = random.Random(42)
ARTISTS = {
    'Paper Lanterns': ['Slow Satellites', 'Harbor Lights', 'Ink & Rain', 'Glass House', 'Northbound', 'Paper Sky'],
    'Nova Vale': ['Electric Orchard', 'Midnight Clinic', 'Velvet Static', 'Neon Hymn', 'Cold Signal'],
    'The Quiet Months': ['February', 'Snowblind', 'Low Tide', 'Kitchen Light', 'Half Asleep'],
    'Juno Park': ['Tangerine', 'Cartwheel', 'Sundress', 'Bicycle Bell', 'Lemon Sky', 'Disco Ghost'],
    'Iron Meridian': ['Cinder', 'Wolfram', 'Black Glass', 'Anvil Song', 'Furnace'],
    'Lumen Drive': ['Night Route 9', 'Chrome Horizon', 'Tunnel Lights', 'Overpass', 'Afterglow 1987'],
    'Marisol Reyes': ['Mar Abierto', 'Luz de Julio', 'Calle Nueve', 'Verano Lento'],
    'Okapi': ['Small Hours', 'Field Notes', 'Sleepwalk Hymn', 'Pale Fire'],
    'Ghost Choir': ['Hollow Bells', 'Saint Elmo', 'Ashfall', 'Lanterns Out'],
    'Sunny Days Club': ['Pool Party', 'Ice Cream Truck', 'Flip Flops'],
    'Cleo Marsh': ['Wildflower Radio', 'Burn Slow', 'Heartbeat Avenue', 'Cherry Static'],
    'Deep Focus Lab': ['Deep Focus 40Hz', 'Study Flow (Concentration)', 'Brain Waves for Coding', 'Calm Focus Rain'],
    'The Holly Lane Singers': ['Snow on Holly Lane', 'Christmas by the Window', 'Jingle Street'],
}
ADJ = ['Velvet', 'Static', 'Hollow', 'Golden', 'Paper', 'Quiet', 'Neon', 'Silver', 'Wild', 'Little', 'Lunar', 'Copper', 'Glass', 'Faded', 'Electric', 'Gentle', 'Crimson', 'Distant', 'Tiny', 'Restless']
NOUN = ['Ferns', 'Orchard', 'Harbor', 'Comets', 'Arcade', 'Foxes', 'Lagoon', 'Satellites', 'Parade', 'Willows', 'Machines', 'Tides', 'Choir', 'Postcards', 'Engines', 'Gardens', 'Echoes', 'Rivers', 'Kites', 'Monsoon']
_pool = rnd.sample([f'{a} {n}' for a in ADJ for n in NOUN], 400)
FILLER_BY_YEAR = {y: _pool[i * 80:(i + 1) * 80] for i, y in enumerate(range(2021, 2026))}  # new artists keep arriving
ODD = [('Cow Bells of Switzerland', 'Morning Pasture (Field Recording)'), ('Kazoo Quartet', 'Bohemian Kazoo'),
       ('Dr. Sound Bath', 'Gong Bath for Houseplants'), ('Polka Mechanics', 'Engine Polka No. 3'),
       ('The Whale Choir', 'Humpback Lullaby (Unedited)'), ('Yodel Academy', 'Beginner Yodel Lesson 1')]


def stream(t, artist, track, ms, platform, country='US', reason_start='trackdone', reason_end='trackdone', shuffle=True, skipped=False, offline=False):
    return {'ts': (t + timedelta(milliseconds=ms)).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'platform': platform,
            'ms_played': ms, 'conn_country': country, 'ip_addr': '0.0.0.0', 'master_metadata_track_name': track,
            'master_metadata_album_artist_name': artist, 'master_metadata_album_album_name': f'{artist} (Album)',
            'spotify_track_uri': f'spotify:track:{abs(hash((artist, track))) % 10**12:012d}', 'episode_name': None,
            'episode_show_name': None, 'spotify_episode_uri': None, 'audiobook_title': None, 'audiobook_uri': None,
            'audiobook_chapter_uri': None, 'audiobook_chapter_title': None, 'reason_start': reason_start, 'reason_end': reason_end,
            'shuffle': shuffle, 'skipped': skipped, 'offline': offline, 'offline_timestamp': None, 'incognito_mode': False}


def weights(day):
    y, m = day.year, day.month
    ym = (y, m)
    def season(start, end, hi, lo=0.15):
        return hi if start <= ym <= end else lo
    return {
        'Paper Lanterns': season((2021, 3), (2021, 12), 16, 0.8),  # the first love, still a lifer
        'Nova Vale': 22 if (2022, 2) <= ym <= (2022, 5) else (0.15 if ym < (2022, 6) else 0),  # the Nova Vale spring, then gone
        'Lumen Drive': season((2022, 9), (2023, 7), 14),            # synthwave year
        'Iron Meridian': season((2023, 9), (2024, 2), 12),          # heavy winter
        'Juno Park': season((2024, 3), (2025, 12), 14),             # pop takes over
        'The Quiet Months': 1.2, 'Okapi': 0.8, 'Ghost Choir': 0.8,  # steady background
        'Marisol Reyes': 12 if m in (7, 8) else 0.1,                # every summer
        'Sunny Days Club': 0.5,
        'Cleo Marsh': 18 if (2025, 2) <= ym <= (2025, 4) else (1 if ym > (2025, 4) else 0),  # a 2025 fling
        'The Holly Lane Singers': 8 if m == 12 else 0,
    }


def main(out):
    rows = []
    day = datetime(2021, 3, 1, tzinfo=timezone.utc)
    end = datetime(2025, 11, 20, tzinfo=timezone.utc)
    while day < end:
        y = day.year
        platform = 'android' if y <= 2022 else ('osx' if rnd.random() < 0.7 else 'ios')
        country = 'PT' if datetime(2023, 6, 10, tzinfo=timezone.utc) <= day < datetime(2023, 6, 20, tzinfo=timezone.utc) else \
                  'JP' if datetime(2024, 10, 3, tzinfo=timezone.utc) <= day < datetime(2024, 10, 12, tzinfo=timezone.utc) else 'US'
        skip_p = {2021: 0.15, 2022: 0.3, 2023: 0.55, 2024: 0.4, 2025: 0.25}[y]
        night = y <= 2022
        sessions = rnd.choice([1, 2, 2, 3])
        for _ in range(sessions):
            hour = rnd.choice([0, 1, 23, 22, 21] if night and rnd.random() < 0.5 else [8, 9, 13, 16, 17, 18, 19, 20])
            t = day + timedelta(hours=hour - 2, minutes=rnd.randint(0, 59))  # stored as UTC; demo runs in UTC-2
            # focus sessions on weekday afternoons in 2022-2023
            if y in (2022, 2023) and day.weekday() < 5 and hour in (13, 16, 17) and rnd.random() < 0.6:
                for _ in range(rnd.randint(3, 8)):
                    tr = rnd.choice(ARTISTS['Deep Focus Lab'])
                    ms = rnd.randint(600_000, 1_800_000)
                    rows.append(stream(t, 'Deep Focus Lab', tr, ms, platform, country))
                    t += timedelta(milliseconds=ms)
                continue
            w = weights(day)
            names = list(w)
            for _ in range(rnd.randint(6, 30)):
                if rnd.random() < 0.12:
                    pool = FILLER_BY_YEAR[y] * 3 + [x for yy in range(2021, y) for x in FILLER_BY_YEAR[yy]]
                    a = rnd.choice(pool)
                    tr = rnd.choice(['Blue Hour', 'Static Love', 'Window Seat', 'Last Train', 'Summer Teeth', 'Paper Planes', 'Slow Dance', 'Heatwave'])
                else:
                    a = rnd.choices(names, [w[n] for n in names])[0]
                    tr = rnd.choice(ARTISTS[a])
                if rnd.random() < skip_p:
                    ms = rnd.randint(400, 9000)
                    rows.append(stream(t, a, tr, ms, platform, country, 'fwdbtn', 'fwdbtn', skipped=True))
                else:
                    ms = rnd.randint(150_000, 260_000)
                    rows.append(stream(t, a, tr, ms, platform, country, rnd.choice(['trackdone'] * 9 + ['clickrow']), 'trackdone', shuffle=y > 2021))
                t += timedelta(milliseconds=ms + rnd.randint(0, 3000))
        day += timedelta(days=1 if rnd.random() < 0.85 else 2)
    # loops: one song on repeat
    t = datetime(2022, 3, 18, 21, 5, tzinfo=timezone.utc)
    for _ in range(37):
        rows.append(stream(t, 'Nova Vale', 'Midnight Clinic', 214_000, 'android', reason_start='trackdone', shuffle=False))
        t += timedelta(milliseconds=214_500)
    t = datetime(2024, 5, 2, 10, 0, tzinfo=timezone.utc)
    for _ in range(22):
        rows.append(stream(t, 'Juno Park', 'Tangerine', 188_000, 'osx', reason_start='trackdone', shuffle=False))
        t += timedelta(milliseconds=188_400)
    # a playlist left running overnight
    t = datetime(2023, 11, 3, 22, 0, tzinfo=timezone.utc)
    while t < datetime(2023, 11, 4, 15, 30, tzinfo=timezone.utc):
        for tr in ARTISTS['Lumen Drive'][:3]:
            rows.append(stream(t, 'Lumen Drive', tr, 241_000, 'osx', shuffle=False))
            t += timedelta(milliseconds=241_200)
    # oddities, played once
    for i, (a, tr) in enumerate(ODD):
        rows.append(stream(datetime(2021 + i % 5, 2 + i, 9 + i, 15, 0, tzinfo=timezone.utc), a, tr, 95_000, 'android' if i < 3 else 'osx'))
    rows.sort(key=lambda r: r['ts'])
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for y in range(2021, 2026):
            part = [r for r in rows if r['ts'].startswith(str(y))]
            z.writestr(f'Spotify Extended Streaming History/Streaming_History_Audio_{y}.json', json.dumps(part))
    print(f'{len(rows):,} fake streams -> {out}')


if __name__ == '__main__':
    main(sys.argv[1])
