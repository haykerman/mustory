"""The page template: HTML with __TITLE__, __DATA__ and __STORY__ placeholders that render.py fills.

Kept as a Python string so the plugin ships only text files the plugin directory accepts.
"""
TEMPLATE = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Layout: a vertical run of full-bleed chapters on a night-navy ground, amber for data, lilac and aqua flood bands for the big reveals. Single dark world. */
:root {
  color-scheme: dark;
  --ground: #0e1424;      /* night navy: the default band */
  --ground-2: #172038;    /* raised surface inside dark bands */
  --ink: #f3efe6;         /* warm paper white */
  --ink-2: #c3c8d8;       /* secondary text on dark */
  --ink-3: #8a92ab;       /* muted text, axes */
  --rule: #283252;        /* grid lines on dark */
  --coral: #ffb02e;       /* flood band A (amber), hero */
  --butter: #c9b8ff;      /* flood band B (lilac) */
  --mint: #9fe3df;        /* flood band C (aqua) */
  --dark-ink: #0e1424;    /* text on flood bands */
  --hot: #ffb02e;         /* single-series accent on dark (amber) */
  --dim: #3b4566;         /* inactive bars */
  --yt: #d14b6e;          /* YouTube (validated pair with --sp on #0e1424) */
  --sp: #5f86f5;          /* Spotify */
  --m1: #5f86f5; --m2: #d14b6e; --m3: #b58a17; --m4: #239e74; --m5: #9a6fe0; --m6: #c2602f; /* validated on #0e1424 */
  --display: "Syne", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; }
a { color: inherit; text-decoration-thickness: 1px; text-underline-offset: 3px; text-decoration-color: color-mix(in srgb, currentColor 40%, transparent); }
a:hover { text-decoration-color: currentColor; }
a:focus-visible, button:focus-visible { outline: 3px solid var(--butter); outline-offset: 2px; border-radius: 4px; }
.band { padding-block: clamp(56px, 9vw, 112px); }
.band > .in { max-width: 1080px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 28px; }
.band.alt { background: var(--ground-2); }
.flood { color: var(--dark-ink); }
.flood.coral { background: var(--coral); } .flood.butter { background: var(--butter); } .flood.mint { background: var(--mint); }
.hero { margin-top: calc(-1 * env(safe-area-inset-top, 0px)); padding-top: calc(env(safe-area-inset-top, 0px) + clamp(56px, 9vw, 112px)); }
.eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-3); margin: 0; }
.flood .eyebrow { color: color-mix(in srgb, var(--dark-ink) 70%, transparent); }
h1, h2, h3 { font-family: var(--display); margin: 0; text-wrap: balance; letter-spacing: -0.02em; }
h1 { font-size: clamp(44px, 9vw, 112px); line-height: .92; font-weight: 800; }
h2 { font-size: clamp(34px, 5.6vw, 68px); line-height: .98; font-weight: 800; }
h3 { font-size: 20px; font-weight: 600; letter-spacing: -0.01em; }
.lede { font-size: clamp(17px, 2vw, 20px); max-width: 62ch; margin: 0; color: var(--ink-2); }
.flood .lede { color: var(--dark-ink); }
p { margin: 0; max-width: 65ch; }
.big { font-family: var(--display); font-weight: 800; font-variant-numeric: tabular-nums; }
.num { font-family: var(--mono); font-variant-numeric: tabular-nums; }
.muted { color: var(--ink-3); }
.flood .muted { color: color-mix(in srgb, var(--dark-ink) 65%, transparent); }
.stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; margin: 0; }
.stats div { display: grid; gap: 2px; border-top: 2px solid var(--dark-ink); padding-top: 10px; }
.stats dt { font-size: 13px; order: 2; }
.stats dd { margin: 0; font-family: var(--display); font-weight: 800; font-size: clamp(28px, 4.4vw, 48px); line-height: 1; font-variant-numeric: tabular-nums; }
.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px; align-items: start; }
.chart { width: 100%; overflow-x: auto; }
.chart svg { display: block; width: 100%; height: auto; }
.chart.wide svg { min-width: 720px; }
.axis text, .lbl { fill: var(--ink-3); font-family: var(--mono); font-size: 11px; }
.flood .axis text, .flood .lbl { fill: color-mix(in srgb, var(--dark-ink) 70%, transparent); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; list-style: none; padding: 0; margin: 0; font-size: 13px; color: var(--ink-2); }
.legend li { display: flex; align-items: center; gap: 8px; }
.sw { width: 12px; height: 12px; border-radius: 3px; display: inline-block; flex: none; }
.rank { list-style: none; padding: 0; margin: 0; display: grid; gap: 0; counter-reset: r; }
.rank li { display: grid; grid-template-columns: 2.2em minmax(0, 1fr) auto; gap: 12px; align-items: baseline; padding: 10px 0; border-bottom: 1px solid var(--rule); counter-increment: r; }
.flood .rank li { border-color: color-mix(in srgb, var(--dark-ink) 22%, transparent); }
.rank li::before { content: counter(r); font-family: var(--mono); font-size: 13px; color: var(--ink-3); }
.flood .rank li::before { color: color-mix(in srgb, var(--dark-ink) 60%, transparent); }
.rank .t { min-width: 0; overflow-wrap: anywhere; }
.rank .sub { display: block; font-size: 13px; color: var(--ink-3); }
.flood .rank .sub { color: color-mix(in srgb, var(--dark-ink) 65%, transparent); }
.callout { background: var(--ground); color: var(--ink); border-radius: 16px; padding: 22px 24px; display: grid; gap: 8px; }
.callout .big { font-size: 40px; line-height: 1; color: var(--hot); }
.cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.card { background: var(--ground-2); border-radius: 14px; padding: 18px 20px; display: grid; gap: 8px; align-content: start; min-width: 0; }
.band.alt .card { background: var(--ground); }
.flood .card { background: color-mix(in srgb, var(--dark-ink) 8%, transparent); }
.card .big { font-size: 34px; line-height: 1; }
.card p { font-size: 14px; }
.tag { display: inline-block; font-family: var(--mono); font-size: 11px; letter-spacing: .06em; text-transform: uppercase; padding: 3px 8px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 10%, transparent); color: var(--ink-2); }
.flood .tag { background: color-mix(in srgb, var(--dark-ink) 12%, transparent); color: var(--dark-ink); }
.seasons { display: grid; grid-template-columns: repeat(auto-fill, minmax(168px, 1fr)); gap: 10px; list-style: none; padding: 0; margin: 0; }
.seasons li { border-radius: 12px; padding: 12px 14px; display: grid; gap: 4px; min-width: 0; background: var(--ground-2); border-top: 4px solid var(--c); }
.seasons .l { font-family: var(--mono); font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-3); }
.seasons .a { font-family: var(--display); font-weight: 600; font-size: 17px; line-height: 1.15; }
.seasons .i { font-size: 12px; color: var(--ink-2); }
.years { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; }
.years section { display: grid; gap: 6px; align-content: start; min-width: 0; }
.years h3 { font-family: var(--display); font-size: 30px; font-weight: 800; }
.years ol { margin: 0; padding-left: 1.2em; font-size: 13px; display: grid; gap: 4px; }
.years li { overflow-wrap: anywhere; }
.dots { display: inline-flex; gap: 3px; align-items: center; }
.dots i { display: inline-block; border-radius: 50%; background: var(--dark-ink); }
.essay { display: grid; gap: 18px; }
.essay h3 { font-size: 24px; }
.timeline { list-style: none; padding: 0; margin: 0; display: grid; gap: 0; }
.timeline li { display: grid; grid-template-columns: 8.5em minmax(0, 1fr); gap: 16px; padding: 14px 0; border-top: 1px solid color-mix(in srgb, var(--dark-ink) 25%, transparent); }
.timeline .when { font-family: var(--mono); font-size: 13px; }
.timeline b { font-family: var(--display); font-size: 19px; display: block; }
.qa { font-family: var(--display); font-weight: 600; font-size: 22px; }
#tip { position: fixed; pointer-events: none; z-index: 20; background: var(--ink); color: var(--dark-ink); font-size: 12px; line-height: 1.35; padding: 7px 10px; border-radius: 8px; max-width: 260px; box-shadow: 0 6px 20px rgb(0 0 0 / .35); }
[data-tip] { cursor: default; }
.hit { fill: transparent; }
.hit:hover + .mark, .mark:hover { opacity: .8; }
footer { font-size: 13px; color: var(--ink-3); }
footer ul { margin: 0; padding-left: 1.2em; display: grid; gap: 6px; max-width: 75ch; }
details summary { cursor: pointer; font-size: 13px; color: var(--ink-3); }
details table { border-collapse: collapse; font-size: 12px; margin-top: 8px; font-family: var(--mono); }
details td, details th { padding: 3px 10px 3px 0; text-align: left; font-weight: 400; }
@media (max-width: 820px) {
  .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .two { grid-template-columns: minmax(0, 1fr); }
  .cards { grid-template-columns: minmax(0, 1fr); }
  .years { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .timeline li { grid-template-columns: minmax(0, 1fr); gap: 4px; }
}
@media (prefers-reduced-motion: no-preference) {
  .hero h1 { animation: rise .7s cubic-bezier(.2,.8,.2,1) both; }
  @keyframes rise { from { transform: translateY(18px); } to { transform: none; } }
}

.lean { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }
.lean li { display: grid; grid-template-columns: minmax(0, 11em) minmax(0, 1fr) 5.5em; gap: 12px; align-items: center; }
.lean .nm { overflow-wrap: anywhere; font-size: 14px; }
.lean .bar { display: flex; gap: 2px; height: 16px; border-radius: 4px; overflow: hidden; }
.lean .num { font-size: 12px; color: var(--ink-3); text-align: right; }
.split { display: flex; gap: 2px; min-height: 40px; border-radius: 8px; overflow: hidden; font-family: var(--mono); font-size: 12px; }
.split span { display: flex; align-items: center; padding: 0 10px; color: var(--ink); white-space: nowrap; overflow: hidden; }
.vs { display: grid; gap: 4px; font-size: 15px; } .vs b { font-family: var(--display); font-size: 26px; margin-left: 6px; }
.tbl { overflow-x: auto; } .tbl table { border-collapse: collapse; width: 100%; font-size: 14px; }
.tbl th, .tbl td { text-align: left; padding: 8px 10px 8px 0; border-bottom: 1px solid color-mix(in srgb, var(--dark-ink) 20%, transparent); }
.tbl .r { text-align: right; } .sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
@media (max-width: 820px) { .lean li { grid-template-columns: minmax(0, 7em) minmax(0, 1fr) 4.5em; } }
</style>

<main>
<header class="band flood coral hero" aria-labelledby="h-hero">
  <div class="in">
    <p class="eyebrow" id="eyebrow"></p>
    <h1 id="h-hero" data-s="hero.h" data-br></h1>
    <p class="lede" data-s="hero.lede"></p>
    <dl class="stats" id="stats"></dl>
  </div>
</header>

<section class="band" aria-labelledby="h-split">
  <div class="in">
    <p class="eyebrow">Who does the work</p>
    <h2 id="h-split" data-s="split.h"></h2>
    <p class="lede" data-s="split.lede"></p>
    <ul class="legend"><li><span class="sw" style="background:var(--yt)"></span>YouTube music plays</li><li><span class="sw" style="background:var(--sp)"></span>Spotify listens</li></ul>
    <div class="chart wide" id="c-split"></div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-clock">
  <div class="in">
    <p class="eyebrow">When</p>
    <h2 id="h-clock" data-s="clock.h"></h2>
    <p class="lede" data-s="clock.lede"></p>
    <ul class="legend"><li><span class="sw" style="background:var(--yt)"></span>YouTube</li><li><span class="sw" style="background:var(--sp)"></span>Spotify</li></ul>
    <div class="chart wide" id="c-clock"></div>
    <div class="cards" id="l-tiles"></div>
  </div>
</section>

<section class="band flood butter" aria-labelledby="h-disc" data-need="discovery.n">
  <div class="in">
    <p class="eyebrow">Discovery</p>
    <h2 id="h-disc" data-s="discovery.h"></h2>
    <p class="lede" data-s="discovery.lede"></p>
    <div id="c-disc"></div>
    <div class="two">
      <div style="display:grid;gap:8px"><h3>Slowest to make the move</h3><ol class="rank" id="l-slow"></ol></div>
      <div style="display:grid;gap:8px"><h3>The few that went the other way</h3><ol class="rank" id="l-spled"></ol></div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-lean">
  <div class="in">
    <p class="eyebrow">Which app owns which artist</p>
    <h2 id="h-lean" data-s="lean.h"></h2>
    <p class="lede" data-s="lean.lede"></p>
    <ul class="legend"><li><span class="sw" style="background:var(--yt)"></span>YouTube</li><li><span class="sw" style="background:var(--sp)"></span>Spotify</li></ul>
    <ol class="lean" id="l-lean"></ol>
  </div>
</section>

<section class="band alt" aria-labelledby="h-only" data-need="yt_only|sp_only">
  <div class="in">
    <p class="eyebrow">Exclusives</p>
    <h2 id="h-only" data-s="only.h"></h2>
    <p class="lede" data-s="only.lede"></p>
    <div class="two">
      <div style="display:grid;gap:8px"><h3>Only on YouTube</h3><ol class="rank" id="l-yt"></ol></div>
      <div style="display:grid;gap:8px"><h3>Only on Spotify</h3><ol class="rank" id="l-sp"></ol></div>
    </div>
  </div>
</section>

<section class="band flood mint" aria-labelledby="h-songs" data-need="songs">
  <div class="in">
    <p class="eyebrow">Common ground</p>
    <h2 id="h-songs" data-s="songs.h"></h2>
    <p class="lede" data-s="songs.lede"></p>
    <div class="tbl"><table id="t-songs"><caption class="sr">Songs played at least 20 times on both apps</caption><thead><tr><th scope="col">Song</th><th scope="col">Artist</th><th scope="col" class="r">YouTube</th><th scope="col" class="r">Spotify</th></tr></thead><tbody></tbody></table></div>
  </div>
</section>

<section class="band" aria-labelledby="h-days">
  <div class="in">
    <p class="eyebrow">Days</p>
    <h2 id="h-days" data-s="days.h"></h2>
    <p class="lede" data-s="days.lede"></p>
    <div id="c-days"></div>
  </div>
</section>

<section class="band flood coral" aria-labelledby="h-you">
  <div class="in">
    <p class="eyebrow">What it says</p>
    <h2 id="h-you" data-s="you.h"></h2>
    <div class="cards" id="l-you"></div>
  </div>
</section>

<footer class="band" aria-labelledby="h-method">
  <div class="in">
    <h2 id="h-method" style="font-size:24px">How this was made</h2>
    <ul id="l-method"></ul>
  </div>
</footer>
</main>
<div id="tip" hidden role="tooltip"></div>
<script id="data" type="application/json">__DATA__</script>
<script id="story" type="application/json">__STORY__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const NS = 'http://www.w3.org/2000/svg';
const $ = id => document.getElementById(id);
const fmt = n => Number(n).toLocaleString('en-US');
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
function svg(w, h, label) { const s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', `0 0 ${w} ${h}`); s.setAttribute('role', 'img'); s.setAttribute('aria-label', label); return s; }
function el(p, tag, attrs, text) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; p.appendChild(e); return e; }
function safe(fn) { try { fn(); } catch (e) { console.error(e); } }
const S = JSON.parse(document.getElementById('story').textContent);
const md = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
const get = (o, p) => p.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const has = v => Array.isArray(v) ? v.length > 0 : v && typeof v === 'object' ? Object.keys(v).length > 0 : !!v;
document.querySelectorAll('[data-s]').forEach(n => { const v = get(S, n.dataset.s); n.innerHTML = n.hasAttribute('data-br') ? md(v).replace(/\n/g, '<br>') : md(v); if (!v) n.hidden = true; });
document.querySelectorAll('[data-need]').forEach(n => { if (!n.dataset.need.split('|').some(p => has(get(D, p)))) n.hidden = true; });
document.title = S.title || 'YouTube vs Spotify';
const MY = s => { const [y, m] = s.split('-'); return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][+m - 1] + ' ' + y; };
$('eyebrow').textContent = `YouTube vs Spotify, ${MY(D.window[0])} – ${MY(D.window[1])}`;
const tip = $('tip');
document.addEventListener('pointermove', e => { const t = e.target.closest && e.target.closest('[data-tip]'); if (!t) { tip.hidden = true; return; }
  tip.innerHTML = t.getAttribute('data-tip'); tip.hidden = false; const r = tip.getBoundingClientRect(); let x = e.clientX + 14, y = e.clientY + 14;
  if (x + r.width > innerWidth - 8) x = e.clientX - r.width - 14; if (y + r.height > innerHeight - 8) y = e.clientY - r.height - 14; tip.style.left = x + 'px'; tip.style.top = y + 'px'; });

const dd = D.days;
$('stats').innerHTML = [[fmt(D.sp_total), 'Spotify listens'], [fmt(D.yt_total), 'YouTube music plays'], [fmt(dd.both), 'days with both'], [D.top50_overlap + ' of 50', 'top artists shared']]
  .map(([v, l]) => `<div><dt>${l}</dt><dd>${v}</dd></div>`).join('');

safe(() => { // 100% split per year
  const Y = D.years, W = 1000, rowH = 34, pl = 56, pr = 60, H = Y.length * rowH + 30;
  const s = svg(W, H, 'Share of music plays per app, by year'); const g = el(s, 'g', { class: 'axis' });
  [0, .25, .5, .75, 1].forEach(v => { const x = pl + (W - pl - pr) * v; el(g, 'line', { x1: x, x2: x, y1: 0, y2: H - 24, stroke: 'var(--rule)' }); el(g, 'text', { x, y: H - 6, 'text-anchor': 'middle' }, Math.round(v * 100) + '%'); });
  Y.forEach(([y, a, b], i) => { const tot = a + b, wy = (W - pl - pr) * a / tot, yy = i * rowH + 6;
    el(g, 'text', { x: pl - 10, y: yy + 16, 'text-anchor': 'end' }, y);
    el(s, 'rect', { x: pl, y: yy, width: Math.max(wy - 1, 0), height: rowH - 12, rx: 4, fill: 'var(--yt)', 'data-tip': `<b>${y}</b><br>YouTube ${fmt(a)} plays (${Math.round(100 * a / tot)}%)` });
    el(s, 'rect', { x: pl + wy + 1, y: yy, width: Math.max((W - pl - pr) - wy - 1, 0), height: rowH - 12, rx: 4, fill: 'var(--sp)', 'data-tip': `<b>${y}</b><br>Spotify ${fmt(b)} listens (${Math.round(100 * b / tot)}%)` });
    el(s, 'text', { x: W - pr + 8, y: yy + 16, fill: 'var(--ink-2)', 'font-size': 12, 'font-family': 'var(--mono)' }, Math.round(100 * b / tot) + '% S'); });
  $('c-split').appendChild(s);
});

safe(() => { // hour profile, two lines, one axis (share of each app's plays)
  const Hs = D.hours, W = 1000, H = 280, pl = 44, pr = 10, pt = 10, pb = 26, mx = Math.max(...Hs.flatMap(h => [h[1], h[2]])) * 1.1;
  const x = h => pl + (W - pl - pr) * h / 23, y = v => pt + (H - pt - pb) * (1 - v / mx);
  const s = svg(W, H, 'Share of plays by hour of day for each app'); const g = el(s, 'g', { class: 'axis' });
  for (let v = 0; v <= mx; v += .02) { el(g, 'line', { x1: pl, x2: W - pr, y1: y(v), y2: y(v), stroke: 'var(--rule)' }); el(g, 'text', { x: pl - 6, y: y(v) + 4, 'text-anchor': 'end' }, Math.round(v * 100) + '%'); }
  [0, 3, 6, 9, 12, 15, 18, 21, 23].forEach(h => el(g, 'text', { x: x(h), y: H - 6, 'text-anchor': 'middle' }, String(h).padStart(2, '0')));
  [[1, 'var(--yt)', 'YouTube'], [2, 'var(--sp)', 'Spotify']].forEach(([i, c, n]) => {
    el(s, 'polyline', { points: Hs.map(h => `${x(h[0])},${y(h[i])}`).join(' '), fill: 'none', stroke: c, 'stroke-width': 2.5, 'stroke-linejoin': 'round' });
    Hs.forEach(h => el(s, 'circle', { cx: x(h[0]), cy: y(h[i]), r: 4, fill: c, stroke: 'var(--ground-2)', 'stroke-width': 2 }));
    const last = Hs[23]; el(s, 'text', { x: x(23) - 4, y: y(last[i]) - 10, 'text-anchor': 'end', fill: 'var(--ink-2)', 'font-size': 12, 'font-family': 'var(--mono)' }, n); });
  Hs.forEach(h => el(s, 'rect', { x: x(h[0]) - (W - pl - pr) / 46, y: pt, width: (W - pl - pr) / 23, height: H - pt - pb, class: 'hit', 'data-tip': `<b>${String(h[0]).padStart(2, '0')}:00</b><br>YouTube ${(h[1] * 100).toFixed(1)}%<br>Spotify ${(h[2] * 100).toFixed(1)}%` }));
  $('c-clock').appendChild(s);
  const pct = v => Math.round(v * 100) + '%';
  $('l-tiles').innerHTML = [['Peak hour', String(D.peak[0]).padStart(2, '0') + ':00', String(D.peak[1]).padStart(2, '0') + ':00'], ['After midnight', pct(D.night[0]), pct(D.night[1])], ['On weekends', pct(D.weekend[0]), pct(D.weekend[1])]]
    .map(([l, a, b]) => `<div class="card"><span class="tag">${l}</span><p class="vs"><span style="color:var(--yt)">YouTube <b>${a}</b></span><span style="color:var(--sp)">Spotify <b>${b}</b></span></p></div>`).join('');
});

safe(() => { const d = D.discovery, t = d.yt_first + d.sp_first;
  $('c-disc').innerHTML = `<div class="split" role="img" aria-label="Found first on YouTube ${d.yt_first}, on Spotify ${d.sp_first}"><span style="flex:${d.yt_first};background:var(--yt)">YouTube first · ${d.yt_first}</span><span style="flex:${d.sp_first};background:var(--sp)">${d.sp_first}</span></div>`;
  $('l-slow').innerHTML = d.slow.map(([n, a, b, days]) => `<li><span class="t">${esc(n)}<span class="sub">YouTube ${a} → Spotify ${b}</span></span><span class="num">${fmt(days)} days</span></li>`).join('');
  $('l-spled').innerHTML = d.sp_led.map(([n, a, b, days]) => `<li><span class="t">${esc(n)}<span class="sub">Spotify ${a} → YouTube ${b}</span></span><span class="num">${days ? fmt(days) + ' days' : 'same day'}</span></li>`).join('');
});

$('l-lean').innerHTML = D.lean.map(([n, a, b]) => { const sa = a / D.yt_total, sb = b / D.sp_total, ys = sa / (sa + sb);
  return `<li data-tip="<b>${esc(n)}</b><br>YouTube ${fmt(a)} plays · Spotify ${fmt(b)} listens"><span class="nm">${esc(n)}</span><span class="bar"><span style="flex:${ys};background:var(--yt)"></span><span style="flex:${1 - ys};background:var(--sp)"></span></span><span class="num">${Math.round(ys * 100)}% YT</span></li>`; }).join('');
$('l-yt').innerHTML = D.yt_only.map(([n, a, b]) => `<li><span class="t">${esc(n)}<span class="sub">${fmt(b)} on Spotify</span></span><span class="num">${fmt(a)} plays</span></li>`).join('');
$('l-sp').innerHTML = D.sp_only.map(([n, a, b]) => `<li><span class="t">${esc(n)}<span class="sub">${fmt(a)} on YouTube</span></span><span class="num">${fmt(b)} listens</span></li>`).join('');
document.querySelector('#t-songs tbody').innerHTML = D.songs.map(([t, a, y, s]) => `<tr><td>${esc(t)}</td><td>${esc(a)}</td><td class="r num">${y}</td><td class="r num">${s}</td></tr>`).join('');
$('c-days').innerHTML = `<div class="split" role="img" aria-label="Days with YouTube only ${dd.yt}, both ${dd.both}, Spotify only ${dd.sp}"><span style="flex:${dd.yt};background:var(--yt)">YouTube only · ${fmt(dd.yt)}</span><span style="flex:${dd.both};background:var(--dim)">Both · ${fmt(dd.both)}</span><span style="flex:${dd.sp};background:var(--sp)">Spotify only · ${fmt(dd.sp)}</span></div>`;
$('l-you').innerHTML = (S.you?.cards || []).map(c => `<div class="card"><h3>${md(c.h)}</h3><p>${md(c.p)}</p></div>`).join('');
$('l-method').innerHTML = [
  `Window: ${D.window[0]} to ${D.window[1]}, the span both histories cover. Plays outside it are left out. All times are in ${esc(D.tz)} time.`,
  `YouTube side: plays of videos classified as music in a Google Takeout export (one play per video start). Spotify side: song streams of 30 seconds or more from a ${D.spotify_export === 'extended' ? 'lifetime "Extended streaming history"' : '12-month "Account data"'} export, with focus and sleep audio left out.`,
  'Artists are matched by name after removing case, punctuation and suffixes like "VEVO", plus hand-made aliases. A few may still be split by spelling.',
  '"Found first" means the first play inside the window, so artists known from YouTube before it count as found on YouTube.',
  ...(S.method_extra || []),
].map(t => `<li>${md(t)}</li>`).join('');
</script>
'''
