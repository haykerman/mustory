"""The "you" page template: HTML with __TITLE__, __DATA__ and __STORY__ placeholders that render.py fills.

Kept as a Python string so the plugin ships only text files the plugin directory accepts.
"""
TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Same world as the story pages: night navy, amber for data, lilac and aqua flood bands. Life first, music as the evidence. */
:root {
  color-scheme: dark;
  --ground: #0e1424; --ground-2: #172038; --ink: #f3efe6; --ink-2: #c3c8d8; --ink-3: #8a92ab; --rule: #283252;
  --amber: #ffb02e; --lilac: #c9b8ff; --aqua: #9fe3df; --dark: #0e1424; --dim: #3b4566;
  --m1: #5f86f5; --m2: #d14b6e; --m3: #b58a17; --m4: #239e74; --m5: #9a6fe0; --m6: #c2602f; /* validated on #0e1424 */
  --display: "Syne", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; }
a:focus-visible, button:focus-visible { outline: 3px solid var(--lilac); outline-offset: 2px; border-radius: 4px; }
.band { padding-block: clamp(56px, 9vw, 104px); }
.in { max-width: 1080px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 28px; }
.alt { background: var(--ground-2); }
.flood { color: var(--dark); } .amber { background: var(--amber); } .lilac { background: var(--lilac); } .aqua { background: var(--aqua); }
.hero { margin-top: calc(-1 * env(safe-area-inset-top, 0px)); padding-top: calc(env(safe-area-inset-top, 0px) + clamp(56px, 9vw, 104px)); }
.eyebrow { font: 12px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--ink-3); margin: 0; }
.flood .eyebrow { color: color-mix(in srgb, var(--dark) 70%, transparent); }
h1, h2, h3 { font-family: var(--display); margin: 0; letter-spacing: -0.02em; text-wrap: balance; }
h1 { font-size: clamp(40px, 6.6vw, 84px); line-height: .94; font-weight: 800; overflow-wrap: break-word; hyphens: auto; }
h2 { font-size: clamp(32px, 5.4vw, 64px); line-height: .98; font-weight: 800; }
h3 { font-size: 20px; font-weight: 700; letter-spacing: -0.01em; }
p { margin: 0; max-width: 65ch; }
.lede { font-size: clamp(17px, 2vw, 20px); color: var(--ink-2); }
.flood .lede { color: var(--dark); }
.muted { color: var(--ink-3); } .flood .muted { color: color-mix(in srgb, var(--dark) 65%, transparent); }
.mono { font-family: var(--mono); font-size: 12px; }
.two { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 40px; align-items: center; }
.stack { display: grid; gap: 20px; align-content: start; }
.made-of { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 8px; }
.made-of li { font: 12px var(--mono); letter-spacing: .06em; text-transform: uppercase; padding: 5px 10px; border-radius: 999px; background: color-mix(in srgb, var(--dark) 12%, transparent); }
.figure-card { background: var(--dark); color: var(--ink); border-radius: 22px; padding: 22px; display: grid; gap: 16px; }
.figure-card .fig { display: grid; place-items: center; }
.figure-card .fig svg { width: min(240px, 70%); height: auto; }
.portrait { margin: 0; display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 6px 14px; font-size: 14px; }
.portrait dt { font: 11px var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-3); padding-top: 3px; }
.portrait dd { margin: 0; }
.genres { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }
.genres li { display: grid; grid-template-columns: 11em minmax(0, 1fr) 3em; gap: 10px; align-items: center; font-size: 14px; }
.genres .bar { height: 10px; border-radius: 99px; background: var(--c); }
.genres .pc { font-family: var(--mono); font-size: 12px; text-align: right; color: var(--ink-2); }
.radar svg { width: 100%; max-width: 520px; height: auto; display: block; margin: 0 auto; }
.reads { list-style: none; padding: 0; margin: 0; display: grid; gap: 28px; }
.reads > li { display: grid; gap: 7px; }
.reads .top { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.reads .lvl { font: 12px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--amber); white-space: nowrap; }
.track { height: 10px; border-radius: 99px; background: var(--dim); position: relative; overflow: hidden; }
.track i { position: absolute; inset: 0 auto 0 0; border-radius: 99px; background: var(--amber); }
.reads p { font-size: 15px; color: var(--ink-2); }
.why { font: 12px var(--mono); color: var(--ink-3); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; list-style: none; padding: 0; margin: 0; }
.chips li { font: 11px var(--mono); padding: 3px 9px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 9%, transparent); color: var(--ink-2); }
.chips li::before { content: "♪ "; color: var(--amber); }
.guesses { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.guess { background: var(--dark); color: var(--ink); border-radius: 20px; padding: 24px; display: grid; gap: 14px; align-content: start; min-width: 0; }
.guess .q { font: 12px var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--lilac); }
.guess blockquote { margin: 0; font-family: var(--display); font-weight: 700; font-size: clamp(21px, 2.5vw, 27px); line-height: 1.12; }
.guess .because { border-top: 1px solid var(--rule); padding-top: 12px; display: grid; gap: 10px; font-size: 13px; color: var(--ink-2); }
.guess .because b { color: var(--amber); font-weight: 600; }
.guess svg { display: block; width: 100%; height: auto; }
.lbl { fill: var(--ink-3); font-family: var(--mono); font-size: 10px; }
.votes { display: flex; gap: 8px; }
.votes button { font: 12px var(--mono); background: transparent; color: var(--ink-2); border: 1px solid var(--rule); border-radius: 999px; padding: 6px 13px; cursor: pointer; }
.votes button[aria-pressed="true"] { background: var(--lilac); color: var(--dark); border-color: var(--lilac); }
.spectrum { list-style: none; padding: 0; margin: 0; display: grid; gap: 24px; }
.spectrum li { display: grid; grid-template-columns: 10em minmax(0, 1fr) 10em; gap: 6px 14px; align-items: center; }
.spectrum .r { text-align: right; }
.spectrum .bar { position: relative; height: 10px; border-radius: 99px; background: linear-gradient(90deg, var(--m1), var(--dim) 50%, var(--m2)); }
.spectrum .dot { position: absolute; top: 50%; width: 22px; height: 22px; border-radius: 50%; background: var(--amber); border: 3px solid var(--ground); transform: translate(-50%, -50%); }
.spectrum .cap { grid-column: 2; font: 12px var(--mono); color: var(--ink-3); }
.spectrum .end { font-family: var(--display); font-weight: 700; font-size: 15px; }
.day { list-style: none; padding: 0; margin: 0; display: grid; }
.day li { display: grid; grid-template-columns: 5.5em minmax(0, 1fr); gap: 14px; padding: 12px 0; border-top: 1px solid color-mix(in srgb, var(--dark) 25%, transparent); }
.day time { font-family: var(--mono); font-size: 13px; }
.day .song { display: block; font: 11px var(--mono); color: color-mix(in srgb, var(--dark) 65%, transparent); margin-top: 2px; }
.clock svg { width: 100%; max-width: 340px; height: auto; display: block; margin: 0 auto; }
.flags { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.flags section { border-radius: 18px; padding: 22px; display: grid; gap: 10px; align-content: start; }
.flags ul { margin: 0; padding-left: 1.1em; display: grid; gap: 10px; }
.flags small { display: block; font: 11px var(--mono); color: var(--ink-3); margin-top: 2px; }
.green { background: color-mix(in srgb, var(--m4) 22%, var(--ground)); } .red { background: color-mix(in srgb, var(--m2) 22%, var(--ground)); }
.badges { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 14px; }
.badge { background: var(--ground-2); border-radius: 16px; padding: 18px; display: grid; gap: 10px; align-content: start; border-top: 4px solid var(--c); }
.badge.almost { opacity: .66; border-top-style: dashed; }
.badge .row { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
.badge .track i { background: var(--c); }
.badge p { font-size: 13px; color: var(--ink-2); }
.share { width: min(340px, 100%); aspect-ratio: 9 / 16; margin: 0 auto; border-radius: 26px; background: var(--amber); color: var(--dark); padding: 26px; display: grid; grid-template-rows: auto 1fr auto auto auto; gap: 12px; text-align: center; box-shadow: 0 20px 60px rgb(0 0 0 / .4); box-sizing: border-box; }
.share .fig { display: grid; place-items: center; }
.share .fig svg { width: 72%; height: auto; }
.share h3 { font-size: 30px; line-height: .95; font-weight: 800; }
.share .line { font-family: var(--display); font-weight: 700; font-size: 17px; line-height: 1.2; }
footer { font-size: 13px; color: var(--ink-3); }
footer ul { margin: 0; padding-left: 1.2em; display: grid; gap: 6px; max-width: 75ch; }
@media (max-width: 820px) {
  .two, .flags, .guesses { grid-template-columns: minmax(0, 1fr); }
  .genres li { grid-template-columns: 8.5em minmax(0, 1fr) 3em; }
  .spectrum li { grid-template-columns: 1fr 1fr; }
  .spectrum .bar { grid-column: 1 / -1; grid-row: 2; }
  .spectrum .cap { grid-column: 1 / -1; }
}
@media (prefers-reduced-motion: no-preference) {
  .hero h1 { animation: rise .7s cubic-bezier(.2,.8,.2,1) both; }
  @keyframes rise { from { transform: translateY(18px); } to { transform: none; } }
}
</style>
</head>
<body>
<main>
<header class="band flood amber hero">
  <div class="in two">
    <div class="stack">
      <p class="eyebrow" data-s="eyebrow"></p>
      <h1 id="h-name"></h1>
      <p class="lede" data-s="character.lede"></p>
      <div class="stack" style="gap:8px">
        <p class="eyebrow">Made of</p>
        <ul class="made-of" id="l-madeof" aria-label="Traits this character is made of"></ul>
      </div>
    </div>
    <aside class="figure-card" aria-labelledby="h-portrait">
      <div class="fig" id="fig-hero"></div>
      <h3 id="h-portrait">If you were a person in a novel</h3>
      <dl class="portrait" id="l-portrait"></dl>
    </aside>
  </div>
</header>

<section class="band" aria-labelledby="h-taste">
  <div class="in two">
    <div class="stack">
      <p class="eyebrow">The bridge</p>
      <h2 id="h-taste" data-s="taste.h"></h2>
      <p class="lede" data-s="taste.lede"></p>
      <ul class="genres" id="l-genres" aria-label="Share of listening by genre"></ul>
    </div>
    <figure class="radar" style="margin:0;display:grid;gap:8px">
      <div id="c-radar"></div>
      <figcaption class="mono muted" style="text-align:center">Five taste directions, 0–100</figcaption>
    </figure>
  </div>
</section>

<section class="band alt" aria-labelledby="h-reads">
  <div class="in">
    <p class="eyebrow">What that says about you</p>
    <h2 id="h-reads" data-s="reads.h"></h2>
    <p class="lede" data-s="reads.lede"></p>
    <ul class="reads" id="l-reads"></ul>
  </div>
</section>

<section class="band flood lilac" aria-labelledby="h-guess">
  <div class="in">
    <p class="eyebrow">Guesses</p>
    <h2 id="h-guess" data-s="guesses.h"></h2>
    <p class="lede" data-s="guesses.lede"></p>
    <ul class="guesses" id="l-guesses"></ul>
  </div>
</section>

<section class="band" aria-labelledby="h-spec">
  <div class="in">
    <p class="eyebrow">This or that</p>
    <h2 id="h-spec" data-s="spectrum.h"></h2>
    <ul class="spectrum" id="l-spectrum"></ul>
  </div>
</section>

<section class="band flood aqua" aria-labelledby="h-day" data-need-s="day.items">
  <div class="in two">
    <div class="stack">
      <p class="eyebrow">A day in the life</p>
      <h2 id="h-day" data-s="day.h"></h2>
      <ol class="day" id="l-day"></ol>
    </div>
    <figure class="clock" style="margin:0;display:grid;gap:8px">
      <div id="c-clock"></div>
      <figcaption class="mono muted" style="text-align:center">Your real 24-hour clock: when the music plays</figcaption>
    </figure>
  </div>
</section>

<section class="band alt" aria-labelledby="h-flags" data-need-s="flags.green">
  <div class="in">
    <p class="eyebrow">As a friend</p>
    <h2 id="h-flags" data-s="flags.h"></h2>
    <div class="flags">
      <section class="green" aria-labelledby="h-green"><h3 id="h-green">Green flags</h3><ul id="l-green"></ul></section>
      <section class="red" aria-labelledby="h-red"><h3 id="h-red">Red flags</h3><ul id="l-red"></ul></section>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-traits">
  <div class="in">
    <p class="eyebrow">All your traits</p>
    <h2 id="h-traits"></h2>
    <p class="lede" id="p-traits"></p>
    <ul class="badges" id="l-badges"></ul>
  </div>
</section>

<section class="band alt" aria-labelledby="h-share">
  <div class="in" style="justify-items:center;text-align:center">
    <p class="eyebrow">Share card</p>
    <h2 id="h-share" data-s="share.h"></h2>
    <div class="share" role="img" id="share">
      <span class="mono">mustory · probably me</span>
      <div class="fig" id="fig-share"></div>
      <h3 id="share-name"></h3>
      <p id="share-traits" style="font-size:14px;margin:0 auto"></p>
      <p class="line" id="share-line" style="margin:0 auto"></p>
    </div>
  </div>
</section>
</main>

<footer class="band" aria-labelledby="h-method">
  <div class="in" style="gap:14px">
    <h2 id="h-method" style="font-size:24px">How this was made</h2>
    <ul id="l-method"></ul>
  </div>
</footer>

<script type="application/json" id="data">__DATA__</script>
<script type="application/json" id="story">__STORY__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const S = JSON.parse(document.getElementById('story').textContent);
const NS = 'http://www.w3.org/2000/svg';
const CAT = ['var(--m1)', 'var(--m2)', 'var(--m3)', 'var(--m4)', 'var(--m5)', 'var(--m6)'];
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const md = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const has = v => Array.isArray(v) ? v.length > 0 : v && typeof v === 'object' ? Object.keys(v).length > 0 : !!v;
const pc = v => Math.round(v * 100) + '%';
function svg(w, h, label, vb) { const s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', vb || `0 0 ${w} ${h}`); s.setAttribute('role', 'img'); s.setAttribute('aria-label', label); return s; }
function el(p, tag, attrs, text) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; p.appendChild(e); return e; }
function safe(fn) { try { fn(); } catch (e) { console.error(e); } }
const chips = list => (list || []).length ? `<ul class="chips" aria-label="Music behind this">${list.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : '';

document.querySelectorAll('[data-s]').forEach(n => { const v = get(S, n.dataset.s); n.innerHTML = md(v); if (!v) n.hidden = true; });
document.querySelectorAll('[data-need-s]').forEach(n => { if (!has(get(S, n.dataset.needS))) n.hidden = true; });
document.title = S.title || 'Who your music says you are';

const TR = Object.fromEntries(D.traits.map(t => [t.key, t]));
const earned = D.traits.filter(t => t.score >= 60);
const almost = D.traits.filter(t => t.score >= 35 && t.score < 60).slice(0, 3);
const ch = S.character || {};
const madeOf = (ch.made_of || earned.slice(0, 5).map(t => t.key)).map(k => TR[k]).filter(Boolean);

/* ---------- the figurine: drawn from traits, styled by character.look ---------- */
const SKIN = { a: '#f6d3b3', b: '#e8b48f', c: '#c98b62', d: '#a0673f', e: '#6e4428', f: '#4a2e1c', blue: '#8fb3ff', green: '#8fd6a8', lilac: '#c9b8ff' };
const HAIRC = { black: '#1d1a22', brown: '#5a3a24', blonde: '#e3c172', red: '#b4532a', gray: '#9aa0ad', pink: '#ff8fb8', blue: '#5f86f5', green: '#239e74' };
const OUTC = { navy: '#283252', amber: '#ffb02e', lilac: '#c9b8ff', aqua: '#9fe3df', blue: '#5f86f5', rose: '#d14b6e', ochre: '#b58a17', green: '#239e74', violet: '#9a6fe0', rust: '#c2602f', black: '#14151c' };
function pick(obj, key, fallback) { return obj[key] || obj[fallback]; }
function lookFor() {
  const L = Object.assign({}, ch.look || {});
  const has_ = k => (TR[k]?.score || 0) >= 60;
  L.skin = L.skin || 'c';
  L.hair = L.hair || (has_('free_thinker') ? 'spiky' : has_('romantic') ? 'long' : has_('party_starter') ? 'curly' : 'short');
  L.hair_color = L.hair_color || 'brown';
  L.outfit = L.outfit || (has_('free_thinker') ? 'jacket' : has_('deep_worker') ? 'hoodie' : has_('seasonal_soul') || has_('romantic') ? 'sweater' : 'tee');
  L.outfit_color = L.outfit_color || (has_('night_owl') ? 'violet' : has_('party_starter') ? 'rose' : 'blue');
  L.eyes = L.eyes || (has_('party_starter') ? 'sunglasses' : has_('night_owl') ? 'sleepy' : has_('experimenter') || has_('deep_worker') ? 'glasses' : 'dots');
  const auto = [['night_owl', 'moon'], ['early_bird', 'coffee'], ['globetrotter', 'plane'], ['deep_worker', 'laptop'], ['comfort_seeker', 'repeat'],
    ['explorer', 'compass'], ['seasonal_soul', 'sun'], ['romantic', 'heart'], ['heart_on_sleeve', 'heart'], ['restless', 'bolt'], ['loyalist', 'star'], ['party_starter', 'sparkle']];
  L.props = (L.props || [...new Set(auto.filter(([k]) => has_(k)).map(([, p]) => p))]).slice(0, 3);
  return L;
}
function figurine(target, label, bg) {
  const L = lookFor();
  const s = svg(200, 220, label, '0 0 200 220');
  const skin = pick(SKIN, L.skin, 'c'), hair = pick(HAIRC, L.hair_color, 'brown'), out = pick(OUTC, L.outfit_color, 'blue');
  el(s, 'circle', { cx: 100, cy: 112, r: 92, fill: bg });
  const g = el(s, 'g', {});
  // long hair sits behind the head
  if (L.hair === 'long') el(g, 'path', { d: 'M58 92 Q56 150 70 166 L130 166 Q144 150 142 92 Z', fill: hair });
  // body + outfit
  el(g, 'path', { d: 'M42 214 Q44 160 100 154 Q156 160 158 214 Z', fill: out });
  if (L.outfit === 'jacket') { el(g, 'path', { d: 'M100 156 L84 214 L78 214 L76 166 Z', fill: '#14151c' }); el(g, 'path', { d: 'M100 156 L116 214 L122 214 L124 166 Z', fill: '#14151c' }); el(g, 'path', { d: 'M88 158 L100 182 L112 158 Z', fill: '#f3efe6' }); }
  if (L.outfit === 'hoodie') { el(g, 'path', { d: 'M70 160 Q100 186 130 160', fill: 'none', stroke: 'rgba(0,0,0,.25)', 'stroke-width': 6, 'stroke-linecap': 'round' }); el(g, 'line', { x1: 92, y1: 172, x2: 92, y2: 192, stroke: '#f3efe6', 'stroke-width': 2 }); el(g, 'line', { x1: 108, y1: 172, x2: 108, y2: 192, stroke: '#f3efe6', 'stroke-width': 2 }); }
  if (L.outfit === 'sweater') { for (let y = 176; y < 212; y += 12) el(g, 'path', { d: `M50 ${y} Q100 ${y - 6} 150 ${y}`, fill: 'none', stroke: 'rgba(255,255,255,.18)', 'stroke-width': 4 }); el(g, 'path', { d: 'M78 158 Q100 170 122 158', fill: 'none', stroke: 'rgba(0,0,0,.25)', 'stroke-width': 6 }); }
  if (L.outfit === 'tee') el(g, 'path', { d: 'M84 156 Q100 168 116 156', fill: skin });
  // neck + head
  el(g, 'rect', { x: 90, y: 136, width: 20, height: 22, rx: 6, fill: skin });
  el(g, 'ellipse', { cx: 100, cy: 104, rx: 36, ry: 40, fill: skin });
  // hair on top
  const H = {
    short: 'M64 100 Q62 60 100 60 Q138 60 136 100 Q128 80 100 80 Q72 80 64 100 Z',
    long: 'M64 104 Q60 58 100 58 Q140 58 136 104 Q130 76 100 76 Q70 76 64 104 Z',
    curly: 'M62 98 Q56 76 70 70 Q70 56 86 58 Q94 48 108 56 Q124 50 130 64 Q146 70 138 98 Q128 80 100 80 Q72 80 62 98 Z',
    spiky: 'M64 98 L60 70 L76 78 L80 54 L92 74 L100 50 L108 74 L120 54 L124 78 L140 70 L136 98 Q126 80 100 80 Q74 80 64 98 Z',
    bun: 'M64 100 Q62 62 100 62 Q138 62 136 100 Q128 80 100 80 Q72 80 64 100 Z',
    buzz: 'M66 96 Q66 64 100 64 Q134 64 134 96 Q124 78 100 78 Q76 78 66 96 Z',
  };
  if (L.hair === 'bun') el(g, 'circle', { cx: 100, cy: 54, r: 14, fill: hair });
  if (L.hair === 'curly') [[66, 92, 11], [70, 76, 12], [82, 66, 12], [98, 62, 13], [114, 66, 12], [128, 76, 12], [134, 92, 11]].forEach(([cx, cy, r]) => el(g, 'circle', { cx, cy, r, fill: hair }));
  if (L.hair !== 'none') el(g, 'path', { d: H[L.hair] || H.short, fill: hair });
  // face
  if (L.eyes === 'sunglasses') { el(g, 'rect', { x: 74, y: 98, width: 22, height: 13, rx: 5, fill: '#14151c' }); el(g, 'rect', { x: 104, y: 98, width: 22, height: 13, rx: 5, fill: '#14151c' }); el(g, 'line', { x1: 96, y1: 103, x2: 104, y2: 103, stroke: '#14151c', 'stroke-width': 3 }); }
  else if (L.eyes === 'sleepy') { el(g, 'path', { d: 'M78 106 Q85 110 92 106', fill: 'none', stroke: '#14151c', 'stroke-width': 3, 'stroke-linecap': 'round' }); el(g, 'path', { d: 'M108 106 Q115 110 122 106', fill: 'none', stroke: '#14151c', 'stroke-width': 3, 'stroke-linecap': 'round' }); }
  else { el(g, 'circle', { cx: 86, cy: 105, r: 4, fill: '#14151c' }); el(g, 'circle', { cx: 114, cy: 105, r: 4, fill: '#14151c' }); if (L.eyes === 'glasses') { el(g, 'circle', { cx: 86, cy: 105, r: 10, fill: 'none', stroke: '#14151c', 'stroke-width': 2.5 }); el(g, 'circle', { cx: 114, cy: 105, r: 10, fill: 'none', stroke: '#14151c', 'stroke-width': 2.5 }); el(g, 'line', { x1: 96, y1: 105, x2: 104, y2: 105, stroke: '#14151c', 'stroke-width': 2.5 }); } }
  el(g, 'path', { d: 'M90 124 Q100 131 110 124', fill: 'none', stroke: '#14151c', 'stroke-width': 3, 'stroke-linecap': 'round' });
  el(g, 'circle', { cx: 78, cy: 118, r: 5, fill: '#d14b6e', opacity: .25 }); el(g, 'circle', { cx: 122, cy: 118, r: 5, fill: '#d14b6e', opacity: .25 });
  // headphones on everyone
  el(g, 'path', { d: 'M60 106 Q60 52 100 52 Q140 52 140 106', fill: 'none', stroke: '#14151c', 'stroke-width': 7, 'stroke-linecap': 'round' });
  el(g, 'rect', { x: 52, y: 96, width: 16, height: 28, rx: 7, fill: '#ffb02e', stroke: '#14151c', 'stroke-width': 3 });
  el(g, 'rect', { x: 132, y: 96, width: 16, height: 28, rx: 7, fill: '#ffb02e', stroke: '#14151c', 'stroke-width': 3 });
  // props float around
  const spots = [[34, 46], [166, 46], [166, 160]];
  L.props.forEach((p, i) => prop(s, p, ...spots[i]));
  $(target).appendChild(s);
}
function prop(s, p, x, y) {
  const g = el(s, 'g', { transform: `translate(${x} ${y})` });
  el(g, 'circle', { r: 19, fill: '#0e1424', stroke: '#f3efe6', 'stroke-width': 2 });
  const W = '#f3efe6', A = '#ffb02e';
  const P = {
    moon: () => { el(g, 'path', { d: 'M4 -10 A11 11 0 1 0 6 9 A8 8 0 1 1 4 -10 Z', fill: A }); el(g, 'circle', { cx: 8, cy: -6, r: 1.6, fill: W }); },
    coffee: () => { el(g, 'rect', { x: -9, y: -6, width: 14, height: 14, rx: 3, fill: W }); el(g, 'path', { d: 'M5 -3 Q11 -3 11 2 Q11 6 5 6', fill: 'none', stroke: W, 'stroke-width': 2.5 }); el(g, 'path', { d: 'M-5 -10 Q-3 -13 -5 -16 M0 -10 Q2 -13 0 -16', fill: 'none', stroke: A, 'stroke-width': 2, 'stroke-linecap': 'round' }); },
    plane: () => el(g, 'path', { d: 'M-12 2 L12 -8 L4 10 L1 3 Z M1 3 L12 -8', fill: A, stroke: '#0e1424', 'stroke-width': 1.5, 'stroke-linejoin': 'round' }),
    laptop: () => { el(g, 'rect', { x: -10, y: -9, width: 20, height: 13, rx: 2, fill: W }); el(g, 'rect', { x: -13, y: 5, width: 26, height: 4, rx: 2, fill: A }); },
    repeat: () => { el(g, 'path', { d: 'M-9 2 A9 9 0 0 1 7 -6', fill: 'none', stroke: A, 'stroke-width': 3, 'stroke-linecap': 'round' }); el(g, 'path', { d: 'M9 -2 A9 9 0 0 1 -7 6', fill: 'none', stroke: A, 'stroke-width': 3, 'stroke-linecap': 'round' }); el(g, 'path', { d: 'M3 -10 L8 -6 L3 -2', fill: 'none', stroke: A, 'stroke-width': 2.5 }); el(g, 'path', { d: 'M-3 10 L-8 6 L-3 2', fill: 'none', stroke: A, 'stroke-width': 2.5 }); },
    compass: () => { el(g, 'circle', { r: 11, fill: 'none', stroke: W, 'stroke-width': 2 }); el(g, 'path', { d: 'M0 -8 L3 0 L0 8 L-3 0 Z', fill: A }); },
    sun: () => { el(g, 'circle', { r: 6, fill: A }); for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; el(g, 'line', { x1: 9 * Math.cos(a), y1: 9 * Math.sin(a), x2: 13 * Math.cos(a), y2: 13 * Math.sin(a), stroke: A, 'stroke-width': 2.5, 'stroke-linecap': 'round' }); } },
    heart: () => el(g, 'path', { d: 'M0 10 C-14 0 -10 -12 0 -5 C10 -12 14 0 0 10 Z', fill: '#d14b6e' }),
    bolt: () => el(g, 'path', { d: 'M3 -13 L-7 2 L0 2 L-3 13 L8 -3 L1 -3 Z', fill: A }),
    star: () => el(g, 'path', { d: 'M0 -12 L3.5 -4 L12 -3.5 L5.5 2 L7.5 10.5 L0 6 L-7.5 10.5 L-5.5 2 L-12 -3.5 L-3.5 -4 Z', fill: A }),
    sparkle: () => el(g, 'path', { d: 'M0 -13 Q2 -2 13 0 Q2 2 0 13 Q-2 2 -13 0 Q-2 -2 0 -13 Z', fill: A }),
    note: () => { el(g, 'ellipse', { cx: -3, cy: 6, rx: 5, ry: 4, fill: A }); el(g, 'path', { d: 'M2 6 L2 -10 L10 -7', fill: 'none', stroke: A, 'stroke-width': 2.5 }); },
  };
  (P[p] || P.note)();
}

/* ---------- hero ---------- */
$('h-name').textContent = `You are ${ch.name || 'someone'}.`;
$('l-madeof').innerHTML = madeOf.map(t => `<li>${esc(t.name)}</li>`).join('');
$('l-portrait').innerHTML = (ch.portrait || []).map(p => `<dt>${esc(p.k)}</dt><dd>${md(p.v)}</dd>`).join('');
safe(() => figurine('fig-hero', `Illustration of ${ch.name || 'the character'}`, '#283252'));

/* ---------- taste ---------- */
safe(() => {
  const max = Math.max(...D.genres.map(g => g[1]), 0.01);
  $('l-genres').innerHTML = D.genres.slice(0, 8).map((g, i) => `<li><span>${esc(g[0])}</span><span class="bar" style="--c:${CAT[i % 6]};width:${Math.max(4, g[1] / max * 100)}%" title="${esc(g[2].join(', '))}"></span><span class="pc">${pc(g[1])}</span></li>`).join('');
  const dims = D.dims, s = svg(350, 244, 'Taste directions: ' + dims.map(d => `${d.name} ${d.score}`).join(', '), '-215 -122 430 244');
  const pt = (i, r) => { const a = i / 5 * 2 * Math.PI - Math.PI / 2; return [r * Math.cos(a), r * Math.sin(a)]; };
  [25, 50, 75, 100].forEach(r => el(s, 'polygon', { points: dims.map((_, i) => pt(i, r * .9).join(',')).join(' '), fill: 'none', stroke: 'var(--rule)' }));
  el(s, 'polygon', { points: dims.map((d, i) => pt(i, Math.max(d.score, 4) * .9).join(',')).join(' '), fill: 'rgba(255,176,46,.35)', stroke: 'var(--amber)', 'stroke-width': 2 });
  dims.forEach((d, i) => { const [x, y] = pt(i, 106); el(s, 'text', { x, y: y + 4, 'text-anchor': Math.abs(x) < 10 ? 'middle' : x > 0 ? 'start' : 'end', class: 'lbl', style: 'fill:var(--ink-2);font-size:11px' }, `${d.name} ${d.score}`); });
  $('c-radar').appendChild(s);
});

/* ---------- reads ---------- */
$('l-reads').innerHTML = D.reads.map(r => {
  const best = r.from.map(k => TR[k]).filter(Boolean).sort((a, b) => b.score - a.score)[0];
  const art = [...new Set(r.from.flatMap(k => TR[k]?.artists || []))].slice(0, 3);
  return `<li><div class="top"><h3>${esc(r.name)}</h3><span class="lvl">${esc(r.level)}</span></div>
    <div class="track" role="meter" aria-label="${esc(r.name)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${r.score}"><i style="width:${r.score}%"></i></div>
    <p>${md(S.reads?.items?.[r.key] || '')}</p><span class="why">Clue: ${esc(best?.clue || '')}</span>${chips(art)}</li>`;
}).join('');

/* ---------- guess charts ---------- */
const Y = D.years, YK = Object.keys(Y);
function miniYears(key, label, fmt = pc) {
  const vals = YK.map(y => Y[y][key] ?? 0), max = Math.max(...vals, 1e-9), bw = 240 / YK.length;
  const s = svg(240, 62, label);
  vals.forEach((v, i) => { const h = 38 * v / max; el(s, 'rect', { x: i * bw + 3, y: 44 - h, width: bw - 6, height: Math.max(h, 1), rx: 3, fill: 'var(--amber)' }); el(s, 'text', { x: i * bw + bw / 2, y: 58, 'text-anchor': 'middle', class: 'lbl' }, "'" + YK[i].slice(2)); el(s, 'text', { x: i * bw + bw / 2, y: 40 - h, 'text-anchor': 'middle', class: 'lbl' }, fmt(v)); });
  return s;
}
function split(parts, label) {
  const s = svg(240, 40, label); let x = 0; const tot = parts.reduce((a, p) => a + p[1], 0) || 1;
  parts.forEach(([n, v, c]) => { const w = 240 * v / tot; if (w < 1) return; el(s, 'rect', { x: x + 1, y: 0, width: Math.max(w - 2, 1), height: 20, rx: 4, fill: c }); if (w > 46) el(s, 'text', { x: x + 4, y: 34, class: 'lbl' }, `${n} ${pc(v / tot)}`); x += w; });
  return s;
}
const CH = {
  clock: () => { const s = svg(240, 56, 'Listening by hour of day'); const m = Math.max(...D.clock); D.clock.forEach((v, i) => { const h = 40 * v / m; el(s, 'rect', { x: i * 10, y: 42 - h, width: 8, height: Math.max(h, 1), rx: 1.5, fill: i === D.peak_hour ? 'var(--amber)' : 'var(--dim)' }); }); [0, 6, 12, 18].forEach(hh => el(s, 'text', { x: hh * 10, y: 54, class: 'lbl' }, hh + ':00')); return s; },
  night: () => { const s = svg(240, 56, 'Listening by hour, late night highlighted'); const m = Math.max(...D.clock); D.clock.forEach((v, i) => { const h = 40 * v / m; el(s, 'rect', { x: i * 10, y: 42 - h, width: 8, height: Math.max(h, 1), rx: 1.5, fill: (i >= 21 || i < 3) ? 'var(--amber)' : 'var(--dim)' }); }); [0, 6, 12, 18].forEach(hh => el(s, 'text', { x: hh * 10, y: 54, class: 'lbl' }, hh + ':00')); return s; },
  morning: () => { const s = svg(240, 56, 'Listening by hour, morning highlighted'); const m = Math.max(...D.clock); D.clock.forEach((v, i) => { const h = 40 * v / m; el(s, 'rect', { x: i * 10, y: 42 - h, width: 8, height: Math.max(h, 1), rx: 1.5, fill: (i >= 5 && i < 10) ? 'var(--amber)' : 'var(--dim)' }); }); [0, 6, 12, 18].forEach(hh => el(s, 'text', { x: hh * 10, y: 54, class: 'lbl' }, hh + ':00')); return s; },
  taste: () => split(D.genres.slice(0, 5).map((g, i) => [g[0], g[1], CAT[i]]), 'Top genres'),
  dims: () => split(D.dims.map((d, i) => [d.name, d.share, CAT[i]]), 'Taste directions'),
  skip_years: () => miniYears('skip', 'Skip rate by year'),
  shuffle_years: () => miniYears('shuffle', 'Shuffle by year'),
  night_years: () => miniYears('night', 'After-midnight share by year'),
  discovery_years: () => miniYears('new_share', 'Share of each year that went to new artists'),
  focus_years: () => miniYears('func', 'Focus audio hours by year', v => Math.round(v) + 'h'),
  hours_years: () => miniYears('hours', 'Hours by year', v => Math.round(v) + 'h'),
  loop: () => { const n = Math.min(D.loop?.n || 0, 40); const s = svg(240, 22, `${D.loop?.n || 0} plays in a row`); for (let i = 0; i < n; i++) el(s, 'rect', { x: i * 6, y: 0, width: 4.5, height: 22, rx: 1.5, fill: 'var(--amber)' }); return s; },
  top10: () => split([['top 10 artists', D.top10, 'var(--amber)'], ['everyone else', 1 - D.top10, 'var(--dim)']], 'Share of time on top 10 artists'),
  picked: () => split([['picked', D.picked, 'var(--amber)'], ['autoplay and skips', 1 - D.picked, 'var(--dim)']], 'Songs picked by hand'),
  shuffle: () => split([['shuffle', D.shuffle, 'var(--amber)'], ['in order', 1 - D.shuffle, 'var(--dim)']], 'Shuffle share'),
  weekend: () => split([['weekdays', 1 - D.weekend, 'var(--dim)'], ['weekends', D.weekend, 'var(--amber)']], 'Weekend share'),
  countries: () => { const s = svg(240, 30, 'Countries listened from'); (D.countries || []).slice(0, 8).forEach((c, i) => { el(s, 'circle', { cx: 12 + i * 30, cy: 10, r: 8, fill: 'var(--amber)' }); el(s, 'text', { x: 12 + i * 30, y: 28, 'text-anchor': 'middle', class: 'lbl' }, c.slice(0, 3).toUpperCase()); }); return s; },
};

/* ---------- guesses ---------- */
safe(() => {
  const ul = $('l-guesses');
  (S.guesses?.items || []).forEach((g, i) => {
    const li = document.createElement('li'); li.className = 'guess';
    li.innerHTML = `<span class="q">${md(g.q)}</span><blockquote>${md(g.a)}</blockquote><div class="because"><span>${md(g.because)}</span><div class="mc"></div>${chips(g.chips)}</div>
      <div class="votes" role="group" aria-label="Is this true?"><button type="button" aria-pressed="false">True</button><button type="button" aria-pressed="false">Not me</button></div>`;
    if (g.chart && CH[g.chart]) safe(() => li.querySelector('.mc').appendChild(CH[g.chart]()));
    ul.appendChild(li);
  });
  ul.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; b.parentElement.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b))); });
});

/* ---------- spectrum ---------- */
$('l-spectrum').innerHTML = D.spectrum.map(x => `<li><span class="end">${esc(x.l)}</span><div class="bar" role="meter" aria-label="${esc(x.l)} to ${esc(x.r)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${x.pos}"><span class="dot" style="left:${x.pos}%"></span></div><span class="end r">${esc(x.r)}</span><span class="cap">${esc(x.clue)}</span></li>`).join('');

/* ---------- day + clock ---------- */
$('l-day').innerHTML = (S.day?.items || []).map(d => `<li><time>${esc(d.time)}</time><span>${md(d.what)}${d.song ? `<span class="song">♪ ${esc(d.song)}</span>` : ''}</span></li>`).join('');
safe(() => {
  const s = svg(220, 220, `24-hour clock of listening, busiest at ${D.peak_hour}:00`, '-110 -110 220 220'), m = Math.max(...D.clock, 1e-9);
  el(s, 'circle', { r: 44, fill: 'none', stroke: 'rgba(14,20,36,.25)' });
  D.clock.forEach((v, i) => { const a = i / 24 * 2 * Math.PI - Math.PI / 2, a2 = a + 2 * Math.PI / 24 * .8, r0 = 46, r1 = 46 + 56 * v / m;
    const p = (r, t) => `${(r * Math.cos(t)).toFixed(1)} ${(r * Math.sin(t)).toFixed(1)}`;
    el(s, 'path', { d: `M${p(r0, a)} L${p(r1, a)} A${r1} ${r1} 0 0 1 ${p(r1, a2)} L${p(r0, a2)} A${r0} ${r0} 0 0 0 ${p(r0, a)}Z`, fill: v / m > .6 ? '#0e1424' : 'rgba(14,20,36,.38)' }); });
  [[0, '0'], [6, '6'], [12, '12'], [18, '18']].forEach(([i, t]) => { const a = i / 24 * 2 * Math.PI - Math.PI / 2; el(s, 'text', { x: (32 * Math.cos(a)).toFixed(1), y: (32 * Math.sin(a) + 4).toFixed(1), 'text-anchor': 'middle', 'font-family': 'var(--mono)', 'font-size': 10, fill: '#0e1424' }, t); });
  $('c-clock').appendChild(s);
});

/* ---------- flags ---------- */
const flag = f => `<li>${md(f.t)}${f.e ? `<small>♪ ${esc(f.e)}</small>` : ''}</li>`;
$('l-green').innerHTML = (S.flags?.green || []).map(flag).join('');
$('l-red').innerHTML = (S.flags?.red || []).map(flag).join('');

/* ---------- badges ---------- */
$('h-traits').textContent = `${earned.length} ${earned.length === 1 ? 'badge' : 'badges'}${almost.length ? `, ${almost.length} near ${almost.length === 1 ? 'miss' : 'misses'}` : ''}.`;
$('p-traits').textContent = `Out of ${D.traits.length} traits, each earned by a pattern in your history. The bar shows how strongly; 60 earns the badge.`;
$('l-badges').innerHTML = [...earned, ...almost].map((t, i) => `<li class="badge${t.score < 60 ? ' almost' : ''}" style="--c:${CAT[i % 6]}"><div class="row"><h3>${esc(t.name)}</h3><span class="mono">${t.score < 60 ? 'almost · ' : ''}${t.score}</span></div>
  <div class="track" role="meter" aria-label="${esc(t.name)} strength" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${t.score}"><i style="width:${t.score}%"></i></div><p>${esc(t.clue.charAt(0).toUpperCase() + t.clue.slice(1))}.</p>${chips(t.artists)}</li>`).join('');

/* ---------- share card ---------- */
$('share-name').textContent = ch.name || '';
$('share-traits').textContent = madeOf.slice(0, 3).map(t => t.name).join(' · ');
$('share-line').innerHTML = md(S.share?.line || '');
$('share').setAttribute('aria-label', `Share card: ${ch.name || ''}. ${S.share?.line || ''}`);
safe(() => figurine('fig-share', `Illustration of ${ch.name || 'the character'}`, '#0e1424'));

/* ---------- method ---------- */
$('l-method').innerHTML = [
  'This is for fun, not science. The guesses about life are playful readings of your listening, loosely inspired by music-psychology research that links taste to personality (Rentfrow and Gosling\'s five taste directions). The numbers behind each clue are real.',
  `Genres were tagged by hand for ${D.tagged} of your top artists, covering ${pc(D.coverage)} of their hours. Focus and sleep audio is left out of taste.`,
  'Each trait is scored 0–100 from fixed thresholds, so the same history always gets the same traits and two people\'s pages can be compared. 60 or more earns a badge.',
  `Source: a Spotify ${D.extended ? '"Extended streaming history"' : '"Account data" (last 12 months only)'} export. Private-session plays are never listed.`,
  ...(S.method_extra || []),
].map(t => `<li>${md(t)}</li>`).join('');
</script>
</body>
</html>
'''
