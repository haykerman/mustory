"""Optional: save the history as SQLite for follow-up questions.

python3 build_db.py --export <takeout.zip|folder> --work <dir> [--tz Europe/Berlin]

Creates <work>/history.db with tables watches, searches, view videos, and
full-text index titles_fts (title, channel). Uses labels.json if present.
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from takeout import load, system_tz  # noqa: E402
from classify import artist, category  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--export', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--tz', default=system_tz())
    a = ap.parse_args()
    rows, srch, _ = load(a.export, a.tz)
    lp = os.path.join(a.work, 'labels.json')
    labels = {k.strip().lower(): v for k, v in (json.load(open(lp, encoding='utf-8')).get('channels', {}) if os.path.exists(lp) else {}).items()}
    db = os.path.join(a.work, 'history.db')
    if os.path.exists(db):
        os.remove(db)
    con = sqlite3.connect(db)
    con.executescript("""
    CREATE TABLE watches (id INTEGER PRIMARY KEY, ts_utc TEXT, ts_local TEXT, local_date TEXT, year INT, month INT, hour INT, weekday INT,
      video_id TEXT, title TEXT, channel TEXT, channel_url TEXT, topic TEXT, artist TEXT, removed INT, youtube_music INT);
    CREATE TABLE searches (id INTEGER PRIMARY KEY, ts_utc TEXT, ts_local TEXT, local_date TEXT, query TEXT);
    CREATE INDEX w_video ON watches(video_id); CREATE INDEX w_ts ON watches(ts_local); CREATE INDEX w_artist ON watches(artist);
    CREATE INDEX w_channel ON watches(channel);
    CREATE VIEW videos AS SELECT video_id, MAX(title) title, MAX(channel) channel, MAX(topic) topic, MAX(artist) artist,
      COUNT(*) plays, MIN(ts_local) first_played, MAX(ts_local) last_played, COUNT(DISTINCT year) years_played FROM watches GROUP BY video_id;
    CREATE VIRTUAL TABLE titles_fts USING fts5(title, channel, content='watches', content_rowid='id');
    """)
    for r in rows:
        t = r['ts']
        topic = 'Removed video' if r['removed'] else category(r['title'], r['ch'], labels)
        con.execute('INSERT INTO watches VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
            t.astimezone(timezone.utc).isoformat(), t.isoformat(), t.strftime('%Y-%m-%d'), t.year, t.month, t.hour, t.weekday(),
            r['v'], None if r['removed'] else r['title'], r['ch'], r['chu'], topic,
            artist(r['title'], r['ch']) if topic == 'Music' else None, int(r['removed']), int(r['music'])))
    for s in srch:
        con.execute('INSERT INTO searches VALUES (NULL,?,?,?,?)', (s['ts'].astimezone(timezone.utc).isoformat(), s['ts'].isoformat(), s['ts'].strftime('%Y-%m-%d'), s['q']))
    con.execute("INSERT INTO titles_fts(titles_fts) VALUES('rebuild')")
    con.commit()
    print(f'{len(rows):,} watches, {len(srch):,} searches -> {db}')


if __name__ == '__main__':
    main()
