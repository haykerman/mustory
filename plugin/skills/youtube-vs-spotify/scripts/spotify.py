"""Read a Spotify personal-data export (zip or folder).

Supports both packages:
  - Extended streaming history (Streaming_History_Audio_*.json, Streaming_History_Video_*.json):
    lifetime, one record per stream with ts (stream END, UTC), ms_played, reason_start/end,
    shuffle, skipped, offline, incognito_mode, platform, conn_country.
  - Account data (StreamingHistory_music_*.json / StreamingHistory_podcast_*.json):
    last 12 months only, with endTime, artistName, trackName, msPlayed.
IP addresses are read past and never kept. Stdlib only.
"""
import atexit
import glob
import json
import os
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def system_tz():
    p = os.path.realpath('/etc/localtime')
    return p.split('zoneinfo/', 1)[1] if 'zoneinfo/' in p else 'UTC'


def find_export(path):
    if path.endswith('.zip'):
        out = tempfile.mkdtemp(prefix='mustory-sp-')
        atexit.register(shutil.rmtree, out, True)  # never leave copies of private history behind
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if re.search(r'(Streaming_History_(Audio|Video)_.*|StreamingHistory_?(music|podcast)?_?\d*)\.json$', n)]
            if not names:
                raise SystemExit('No streaming history in the zip. Request "Extended streaming history" at spotify.com/account/privacy.')
            for n in names:
                z.extract(n, out)
        path = out
    return path


PLATFORMS = [('echo', 'Smart speaker'), ('amazon', 'Smart speaker'), ('sonos', 'Smart speaker'), ('google_home', 'Smart speaker'),
             ('cast', 'Chromecast / TV'), ('tv', 'Chromecast / TV'), ('playstation', 'Console'), ('xbox', 'Console'),
             ('car', 'Car'), ('tablet', 'Tablet'), ('ipad', 'Tablet'), ('android', 'Android phone'), ('ios', 'iPhone'),
             ('iphone', 'iPhone'), ('watch', 'Watch'), ('linux', 'Linux computer'), ('windows', 'Windows computer'),
             ('osx', 'Mac'), ('macos', 'Mac'), ('mac', 'Mac'), ('web', 'Web player')]


def platform(p):
    p = (p or '').lower()
    for k, v in PLATFORMS:
        if k in p:
            return v
    return 'Other'


def _rec(start, end, ms, track, artist, album, uri, kind, x, tz):
    return dict(start=start.astimezone(tz), end=end.astimezone(tz), ms=ms, track=track, artist=artist, album=album, uri=uri, kind=kind,
                rs=x.get('reason_start'), re=x.get('reason_end'), shuffle=x.get('shuffle'), skipped=x.get('skipped'),
                offline=bool(x.get('offline')), incognito=bool(x.get('incognito_mode')), platform=platform(x.get('platform')),
                country=x.get('conn_country'))


def load(path, tz_name):
    tz = ZoneInfo(tz_name)
    root = find_export(path)
    ext = sorted(glob.glob(os.path.join(root, '**', 'Streaming_History_*.json'), recursive=True))
    acc = sorted(glob.glob(os.path.join(root, '**', 'StreamingHistory*.json'), recursive=True))
    rows, kind_of_export = [], None
    if ext:
        kind_of_export = 'extended'
        for f in ext:
            video = '_Video_' in os.path.basename(f)
            for x in json.load(open(f, encoding='utf-8')):
                end = datetime.fromisoformat(x['ts'].replace('Z', '+00:00'))
                ms = int(x.get('ms_played') or 0)
                if x.get('spotify_track_uri'):
                    kind, uri = ('video' if video else 'track'), x['spotify_track_uri']
                    track, artist, album = x.get('master_metadata_track_name'), x.get('master_metadata_album_artist_name'), x.get('master_metadata_album_album_name')
                elif x.get('spotify_episode_uri'):
                    kind, uri, track, artist, album = 'episode', x['spotify_episode_uri'], x.get('episode_name'), x.get('episode_show_name'), None
                elif x.get('audiobook_uri'):
                    kind, uri, track, artist, album = 'audiobook', x.get('audiobook_chapter_uri') or x['audiobook_uri'], x.get('audiobook_chapter_title'), x.get('audiobook_title'), None
                else:
                    continue
                if not track or not artist:
                    continue
                rows.append(_rec(end - timedelta(milliseconds=ms), end, ms, track, artist, album, uri, kind, x, tz))
    elif acc:
        kind_of_export = 'account'
        for f in acc:
            pod = 'podcast' in os.path.basename(f).lower()
            for x in json.load(open(f, encoding='utf-8')):
                end = datetime.strptime(x['endTime'], '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                ms = int(x.get('msPlayed') or 0)
                track = x.get('trackName') or x.get('episodeName')
                artist = x.get('artistName') or x.get('podcastName')
                if not track or not artist:
                    continue
                rows.append(_rec(end - timedelta(milliseconds=ms), end, ms, track, artist, None, f'{artist}␟{track}',
                                 'episode' if pod else 'track', {}, tz))
    else:
        raise SystemExit(f'No Spotify streaming history files under {path}.')
    rows.sort(key=lambda r: r['start'])
    # Listening time without double counting (two devices at once): each stream counts only the part
    # of its interval not already covered by earlier streams, so the total equals the union of intervals.
    covered = None
    for r in rows:
        s, e = r['start'], r['end']
        if covered is None or s >= covered:
            r['eff'] = r['ms']
        else:
            r['eff'] = max(0, int((e - covered).total_seconds() * 1000))
        covered = e if covered is None else max(covered, e)
    return rows, kind_of_export
