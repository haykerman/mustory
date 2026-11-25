"""Combine data.json + story.json into one self-contained compare.html (YouTube vs Spotify).

python3 render.py --work <dir> [--out <file.html>]

Checks the story before writing:
  - required keys present
  - every number of 10 or more in the story text appears in facts.md, or is listed
    in story.json "derived" with how it was computed. Song, artist and album names
    (from facts.md and artists.tsv) and clock times are skipped.
  It proves each number exists in facts.md, not that it belongs to the claim: still quote the right line.
Nothing is written until both pass (use --force to write a draft anyway).
"""
import argparse
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ['title', 'hero.h', 'hero.lede', 'split.h', 'split.lede', 'clock.h', 'lean.h', 'days.h', 'you.h', 'you.cards']
NUM = re.compile(r'(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?![\w])')


def get(o, path):
    for k in path.split('.'):
        o = o.get(k) if isinstance(o, dict) else None
    return o


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('chart_index', 'derived'):
                yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def known_titles(work):
    t = set(re.findall(r'“([^”]{8,})”', open(os.path.join(work, 'facts.md'), encoding='utf-8').read()))
    p = os.path.join(work, 'artists.tsv')
    if os.path.exists(p):  # artist names can hold numbers ("21 Savage", "blink-182")
        t.update(line.split('\t')[2] for line in open(p, encoding='utf-8').read().splitlines()[1:] if line.count('\t') >= 2)
    return sorted(t, key=len, reverse=True)


CLOCK = re.compile(r'\b\d{1,2}(:\d{2})?\s*(a\.m\.|p\.m\.|am|pm)|\b\d{1,2}:\d{2}\b', re.I)


def known_numbers(work):
    text = open(os.path.join(work, 'facts.md'), encoding='utf-8').read()
    known = set()
    for m in NUM.finditer(text):
        v = m.group(1).replace(',', '')
        known.add(v)
        if '.' in v:  # 0.461 also allows 46 (percent) and 0.5 → 50
            f = float(v)
            known.update({str(round(f * 100)), str(round(f)), str(round(f, 1))})
    return known


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--out')
    ap.add_argument('--force', action='store_true', help='write the page even if checks fail')
    a = ap.parse_args()
    data = json.load(open(os.path.join(a.work, 'data.json'), encoding='utf-8'))
    story = json.load(open(os.path.join(a.work, 'story.json'), encoding='utf-8'))
    missing = [k for k in REQUIRED if not get(story, k)]
    if missing:
        sys.exit('story.json is missing: ' + ', '.join(missing))
    known = known_numbers(a.work) | {str(k).replace(',', '') for k in story.get('derived', {})}
    titles = known_titles(a.work)
    unknown = []
    for s in strings(story):
        t = s
        for title in titles:
            if title in t:
                t = t.replace(title, ' ')
        t = CLOCK.sub(' ', t)
        for m in NUM.finditer(t):
            v = m.group(1).replace(',', '')
            if float(v) < 10 and '.' not in v:
                continue  # single digits: too common to check (write bigger numbers as digits)
            if v not in known:
                unknown.append((v, s[:90]))
    # Pairing check: a sentence that names an artist/song and a number should match a facts.md line holding both.
    # It catches a number that changed but still exists elsewhere in facts.md. Warnings only.
    facts_lines = open(os.path.join(a.work, 'facts.md'), encoding='utf-8').read().splitlines()
    names = [x for x in titles if 4 <= len(x) <= 60 and any(x in ln for ln in facts_lines)]
    unpaired = []
    for s in strings(story):
        for sent in re.split(r'(?<=[.!?])\s+', s):
            hits = [x for x in names if x in sent]
            if len(hits) != 1:
                continue
            nums = [m.group(1).replace(',', '') for m in NUM.finditer(CLOCK.sub(' ', sent.replace(hits[0], ' ')))]
            nums = [v for v in nums if float(v) >= 10 and v not in story.get('derived', {})]
            lines = [ln.replace(',', '') for ln in facts_lines if hits[0] in ln]
            bad = [v for v in nums if not any(re.search(rf'(?<![\d.]){re.escape(v)}(?![\d])', ln) for ln in lines)]
            if bad:
                unpaired.append((hits[0], bad, sent[:100]))
    if unpaired:
        print(f'PAIRING CHECK: {len(unpaired)} sentence(s) put a number next to a name with no facts.md line holding both. Check each:')
        for n_, b_, s_ in unpaired:
            print(f"  {n_} + {', '.join(b_)}  ←  {s_}")
    sys.path.insert(0, HERE)
    from page_template import TEMPLATE as tpl
    safe = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'), default=str).replace('</', '<\\/')  # noqa: E731
    out = (tpl.replace('__TITLE__', html.escape(story['title']))
              .replace('__DATA__', safe(data)).replace('__STORY__', safe(story)))
    path = a.out or os.path.join(a.work, 'compare.html')
    if unknown:
        print(f'FACT CHECK FAILED: {len(unknown)} number(s) in story.json are not in facts.md. For each, correct it from facts.md, '
              'or, if you computed it from facts.md numbers, add it to story.json "derived" as {"<number>": "<how>"}:')
        for v, s in unknown:
            print(f'  {v}  ←  {s}')
        if not a.force:
            sys.exit(2)
    open(path, 'w', encoding='utf-8').write(out)
    print(f'Wrote {path} ({len(out) // 1024} KB)')
    if not unknown:
        print('Fact check passed: every number in the story is in facts.md or listed as derived.')


if __name__ == '__main__':
    main()
