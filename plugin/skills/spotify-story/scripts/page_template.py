"""The page template: HTML with __TITLE__, __DATA__ and __STORY__ placeholders that render.py fills.

Kept as a Python string so the plugin ships only text files the plugin directory accepts.
"""
TEMPLATE = r'''<title>__TITLE__</title>
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
  --m1: #5f86f5; --m2: #d14b6e; --m3: #b58a17; --m4: #239e74; --m5: #9a6fe0; --m6: #c2602f; /* validated on #0e1424 */
  --display: "Syne", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
body { background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; }
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
</style>
<main>
<header class="band flood coral hero" aria-labelledby="h-hero">
  <div class="in">
    <p class="eyebrow" data-s="hero.eyebrow"></p>
    <h1 id="h-hero" data-s="hero.h" data-br></h1>
    <p class="lede" data-s="hero.lede"></p>
    <dl class="stats" id="stats"></dl>
  </div>
</header>

<section class="band" aria-labelledby="h-shape">
  <div class="in">
    <p class="eyebrow">The shape of it</p>
    <h2 id="h-shape" data-s="shape.h"></h2>
    <p class="lede" data-s="shape.lede"></p>
    <div class="chart wide" id="c-monthly"></div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-artists">
  <div class="in">
    <p class="eyebrow">Most played artists</p>
    <h2 id="h-artists" data-s="artists.h"></h2>
    <p class="lede" data-s="artists.lede"></p>
    <div class="two">
      <div style="display:grid;gap:10px"><h3>By hours</h3><ol class="rank" id="l-artists-h"></ol></div>
      <div style="display:grid;gap:18px">
        <div class="callout" data-need-s="artists.callout">
          <p class="eyebrow" data-s="artists.callout.eyebrow"></p>
          <span class="big" data-s="artists.callout.name"></span>
          <p data-s="artists.callout.body"></p>
        </div>
        <div style="display:grid;gap:10px"><h3>Top albums by hours</h3><ol class="rank" id="l-albums"></ol></div>
      </div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-tracks">
  <div class="in">
    <p class="eyebrow">Most played songs</p>
    <h2 id="h-tracks" data-s="tracks.h"></h2>
    <p class="lede" data-s="tracks.lede"></p>
    <ol class="rank" id="l-tracks"></ol>
  </div>
</section>

<section class="band flood mint" aria-labelledby="h-loops" data-need="loops">
  <div class="in">
    <p class="eyebrow">On repeat, literally</p>
    <h2 id="h-loops" data-s="loops.h"></h2>
    <p class="lede" data-s="loops.lede"></p>
    <div class="cards" id="l-loops"></div>
  </div>
</section>

<section class="band" aria-labelledby="h-eras" data-need="eras">
  <div class="in">
    <p class="eyebrow">Eras</p>
    <h2 id="h-eras" data-s="eras.h"></h2>
    <p class="lede" data-s="eras.lede"></p>
    <div class="chart wide" id="c-eras"></div>
    <h3>Songs you couldn't stop playing</h3>
    <ol class="rank" id="l-obs"></ol>
  </div>
</section>

<section class="band flood butter" aria-labelledby="h-ded" data-need="dedications">
  <div class="in">
    <p class="eyebrow">Dedications</p>
    <h2 id="h-ded" data-s="dedications.h"></h2>
    <p class="lede" data-s="dedications.lede"></p>
    <ol class="rank" id="l-ded"></ol>
  </div>
</section>

<section class="band" aria-labelledby="h-forgot" data-need="forgotten">
  <div class="in two">
    <div style="display:grid;gap:22px">
      <p class="eyebrow">Forgotten favorites</p>
      <h2 id="h-forgot" data-s="forgotten.h"></h2>
      <p class="lede" data-s="forgotten.lede"></p>
      <div class="card" data-need="forgotten_artists"><h3>Artists you left behind</h3><ol class="rank" id="l-fart"></ol></div>
    </div>
    <ol class="rank" id="l-forgot"></ol>
  </div>
</section>

<section class="band alt" aria-labelledby="h-skip">
  <div class="in">
    <p class="eyebrow">The skip button</p>
    <h2 id="h-skip" data-s="skips.h"></h2>
    <p class="lede" data-s="skips.lede"></p>
    <div class="two">
      <div style="display:grid;gap:10px"><h3>Quick-skip rate by year</h3><div class="chart" id="c-skip"></div></div>
      <div style="display:grid;gap:18px">
        <div style="display:grid;gap:8px" data-need="skipped"><h3>Skipped almost every time, yet it kept coming back</h3><ol class="rank" id="l-skipped"></ol></div>
        <div style="display:grid;gap:8px" data-need="untouchable"><h3>Untouchables: never skipped</h3><ol class="rank" id="l-untouch"></ol></div>
      </div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-auto" data-need="starts">
  <div class="in">
    <p class="eyebrow">Autopilot</p>
    <h2 id="h-auto" data-s="autopilot.h"></h2>
    <p class="lede" data-s="autopilot.lede"></p>
    <div class="two">
      <div style="display:grid;gap:12px"><h3>How each song started</h3><div id="c-starts"></div><h3>Shuffle, by year</h3><div class="chart" id="c-shuffle"></div></div>
      <div style="display:grid;gap:8px"><h3>The songs you went looking for</h3><ol class="rank" id="l-picked"></ol></div>
    </div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-focus" data-need="functional">
  <div class="in">
    <p class="eyebrow">Music as a tool</p>
    <h2 id="h-focus" data-s="focus.h"></h2>
    <p class="lede" data-s="focus.lede"></p>
    <div class="two">
      <div style="display:grid;gap:10px"><h3>Focus and sleep audio, hours by time of day</h3><div class="chart" id="c-focus"></div></div>
      <ol class="rank" id="l-focus"></ol>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-seasons" data-need="seasons">
  <div class="in">
    <p class="eyebrow">Seasons</p>
    <h2 id="h-seasons" data-s="seasons.h"></h2>
    <p class="lede" data-s="seasons.lede"></p>
    <ul class="seasons" id="l-seasons"></ul>
  </div>
</section>

<section class="band alt" aria-labelledby="h-sound">
  <div class="in">
    <p class="eyebrow">Soundtrack of each year</p>
    <h2 id="h-sound" data-s="soundtrack.h"></h2>
    <div class="years" id="l-years"></div>
  </div>
</section>

<section class="band" aria-labelledby="h-mood" data-need="mood">
  <div class="in">
    <p class="eyebrow">Mood weather</p>
    <h2 id="h-mood" data-s="mood.h"></h2>
    <p class="lede" data-s="mood.lede"></p>
    <ul class="legend" id="lg-mood"></ul>
    <div class="chart wide" id="c-mood"></div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-night">
  <div class="in">
    <p class="eyebrow">When you listen</p>
    <h2 id="h-night" data-s="night.h"></h2>
    <p class="lede" data-s="night.lede"></p>
    <div class="two">
      <div class="chart" id="c-heat"></div>
      <div style="display:grid;gap:10px"><h3>Share of hours between 00:00 and 05:00</h3><div class="chart" id="c-nightyear"></div></div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-dev" data-need="devices.order">
  <div class="in">
    <p class="eyebrow">The machines</p>
    <h2 id="h-dev" data-s="devices.h"></h2>
    <p class="lede" data-s="devices.lede"></p>
    <ul class="legend" id="lg-dev"></ul>
    <div class="chart wide" id="c-dev"></div>
  </div>
</section>

<section class="band flood butter" aria-labelledby="h-travel" data-need="travel.trips">
  <div class="in">
    <p class="eyebrow">Passport stamps</p>
    <h2 id="h-travel" data-s="travel.h"></h2>
    <p class="lede" data-s="travel.lede"></p>
    <ol class="timeline" id="l-travel"></ol>
  </div>
</section>

<section class="band" aria-labelledby="h-disc">
  <div class="in two">
    <div style="display:grid;gap:22px">
      <p class="eyebrow">Discovery</p>
      <h2 id="h-disc" data-s="discovery.h"></h2>
      <p class="lede" data-s="discovery.lede"></p>
    </div>
    <div style="display:grid;gap:10px"><h3>New artists each year</h3><div class="chart" id="c-disc"></div></div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-drift" data-need="drift.years.2">
  <div class="in two">
    <div style="display:grid;gap:22px">
      <p class="eyebrow">Taste drift</p>
      <h2 id="h-drift" data-s="drift.h"></h2>
      <p class="lede" data-s="drift.lede"></p>
    </div>
    <div class="chart" id="c-drift"></div>
  </div>
</section>

<section class="band" aria-labelledby="h-fl" data-need="flings|steady">
  <div class="in">
    <p class="eyebrow">Artist deep dives</p>
    <h2 id="h-fl" data-s="flings.h"></h2>
    <div class="two">
      <div style="display:grid;gap:12px" data-need="flings"><h3>Flings: found in the last three years, ranked by their best 30 days</h3><ol class="rank" id="l-flings"></ol></div>
      <div style="display:grid;gap:12px" data-need="steady"><h3 id="steady-h"></h3><ol class="rank" id="l-steady"></ol></div>
    </div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-gate" data-need="gateways">
  <div class="in">
    <p class="eyebrow">Gateway songs</p>
    <h2 id="h-gate" data-s="gateways.h"></h2>
    <p class="lede" data-s="gateways.lede"></p>
    <div class="cards" id="l-gate"></div>
  </div>
</section>

<section class="band flood mint" aria-labelledby="h-mara" data-need="marathons">
  <div class="in">
    <p class="eyebrow">Marathons</p>
    <h2 id="h-mara" data-s="marathons.h"></h2>
    <p class="lede" data-s="marathons.lede"></p>
    <div class="cards" id="l-mara"></div>
  </div>
</section>

<section class="band" aria-labelledby="h-ritual" data-need="rituals">
  <div class="in">
    <p class="eyebrow">Yearly rituals</p>
    <h2 id="h-ritual" data-s="rituals.h"></h2>
    <div class="two">
      <div style="display:grid;gap:14px"><p class="lede" data-s="rituals.lede"></p><div class="chart" id="c-ritual"></div></div>
      <div class="cards" style="grid-template-columns:minmax(0,1fr)" id="l-ritual"></div>
    </div>
  </div>
</section>

<section class="band alt" aria-labelledby="h-otd" data-need="otd">
  <div class="in">
    <p class="eyebrow">On this day</p>
    <h2 id="h-otd" data-s="otd.h"></h2>
    <ol class="timeline" id="l-otd" style="--dark-ink: var(--ink)"></ol>
  </div>
</section>

<section class="band flood butter" aria-labelledby="h-odd" data-need-s="odd.items">
  <div class="in">
    <p class="eyebrow">Wait, you played that?</p>
    <h2 id="h-odd" data-s="odd.h"></h2>
    <p class="lede" data-s="odd.lede"></p>
    <div class="cards" id="l-odd"></div>
  </div>
</section>

<section class="band flood coral" aria-labelledby="h-you">
  <div class="in">
    <p class="eyebrow">Who this history says you are</p>
    <h2 id="h-you" data-s="you.h"></h2>
    <div class="two essay">
      <div class="essay" id="l-essay"></div>
      <div style="display:grid;gap:12px"><h3>How you changed</h3><ol class="timeline" id="l-change"></ol></div>
    </div>
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

<script src="https://cdnjs.cloudflare.com/ajax/libs/luxon/3.4.4/luxon.min.js"></script>
<script id="data" type="application/json">__DATA__</script>
<script id="story" type="application/json">__STORY__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const S = JSON.parse(document.getElementById('story').textContent);
const { DateTime } = luxon;
const ZONE = D.meta.tz;
const TODAY = DateTime.fromISO(D.meta.today, { zone: ZONE });
const NS = 'http://www.w3.org/2000/svg';
const CAT = ['var(--m1)', 'var(--m2)', 'var(--m3)', 'var(--m4)', 'var(--m5)', 'var(--m6)'];
const $ = id => document.getElementById(id);
const fmt = n => Number(n).toLocaleString('en-US');
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const md = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const has = v => Array.isArray(v) ? v.length > 0 : v && typeof v === 'object' ? Object.keys(v).length > 0 : !!v;
const ago = iso => { const d = TODAY.diff(DateTime.fromISO(iso, { zone: ZONE }), ['years', 'months']); return d.years >= 1 ? `${Math.floor(d.years)} yr ${Math.floor(d.months)} mo ago` : `${Math.floor(d.months)} months ago`; };
const monthName = iso => DateTime.fromISO(iso).toFormat('LLL yyyy');
const day = iso => DateTime.fromISO(iso).toFormat('d LLL yyyy');
const h = v => v >= 10 ? `${fmt(Math.round(v))} h` : `${v} h`;
function svg(w, ht, label) { const s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', `0 0 ${w} ${ht}`); s.setAttribute('role', 'img'); s.setAttribute('aria-label', label); return s; }
function el(parent, tag, attrs, text) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; parent.appendChild(e); return e; }
function safe(fn) { try { fn(); } catch (e) { console.error(e); } }
function yearBars(target, entries, { label, fmtV = v => `${Math.round(v * 100)}%`, max } = {}) {
  const W = 420, H = 220, pl = 6, pb = 22, bw = (W - pl * 2) / entries.length, top = max ?? Math.max(...entries.map(([, v]) => v), 1e-9);
  const s = svg(W, H, label); const g = el(s, 'g', { class: 'axis' });
  entries.forEach(([y, v], i) => {
    const hh = (H - pb - 22) * v / top, x = pl + i * bw;
    el(s, 'rect', { x: x + 3, y: H - pb - hh, width: bw - 6, height: Math.max(hh, 0), rx: 4, fill: 'var(--hot)', 'data-tip': `<b>${y}</b><br>${fmtV(v)}` });
    el(g, 'text', { x: x + bw / 2, y: H - 6, 'text-anchor': 'middle' }, "'" + String(y).slice(2));
    el(s, 'text', { x: x + bw / 2, y: H - pb - hh - 6, 'text-anchor': 'middle', fill: 'var(--ink-2)', 'font-size': 11, 'font-family': 'var(--mono)' }, fmtV(v));
  });
  $(target).appendChild(s);
}

document.querySelectorAll('[data-s]').forEach(n => { const v = get(S, n.dataset.s); n.innerHTML = n.hasAttribute('data-br') ? md(v).replace(/\n/g, '<br>') : md(v); if (!v) n.hidden = true; });
document.querySelectorAll('[data-need]').forEach(n => { const ok = n.dataset.need.split('|').some(p => { const parts = p.split('.'); if (/^\d+$/.test(parts.at(-1))) { const arr = get(D, parts.slice(0, -1).join('.')); return Array.isArray(arr) && arr.length > +parts.at(-1); } return has(get(D, p)); }); if (!ok) n.hidden = true; });
document.querySelectorAll('[data-need-s]').forEach(n => { if (!has(get(S, n.dataset.needS))) n.hidden = true; });
document.title = S.title || 'Spotify Story';

const tip = $('tip');
document.addEventListener('pointermove', e => {
  const t = e.target.closest && e.target.closest('[data-tip]');
  if (!t) { tip.hidden = true; return; }
  tip.innerHTML = t.getAttribute('data-tip'); tip.hidden = false;
  const r = tip.getBoundingClientRect(); let x = e.clientX + 14, y = e.clientY + 14;
  if (x + r.width > innerWidth - 8) x = e.clientX - r.width - 14;
  if (y + r.height > innerHeight - 8) y = e.clientY - r.height - 14;
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
});

const T = D.totals, YR = D.years, YK = Object.keys(YR);
$('stats').innerHTML = [[fmt(T.hours), 'hours of music'], [fmt(T.tracks), 'different songs'], [fmt(T.artists), 'artists'], [fmt(T.active_days), 'days with music']]
  .map(([v, l]) => `<div><dt>${l}</dt><dd>${v}</dd></div>`).join('');

safe(() => {
  const M = D.monthly, W = 1000, H = 300, pl = 44, pr = 8, pt = 22, pb = 26;
  const top = Math.max(...M.map(m => m[1])), step = top > 100 ? 25 : top > 40 ? 10 : 5, max = Math.ceil(top / step) * step, bw = (W - pl - pr) / M.length;
  const s = svg(W, H, 'Hours of music per month'); const y = v => pt + (H - pt - pb) * (1 - v / max); const g = el(s, 'g', { class: 'axis' });
  for (let v = 0; v <= max; v += step) { el(g, 'line', { x1: pl, x2: W - pr, y1: y(v), y2: y(v), stroke: 'var(--rule)' }); el(g, 'text', { x: pl - 6, y: y(v) + 4, 'text-anchor': 'end' }, v + ' h'); }
  M.forEach(([k, hv, sk], i) => {
    const x = pl + i * bw;
    if (k.endsWith('-01') || i === 0) el(g, 'text', { x: x + 1, y: H - 8 }, k.slice(0, 4));
    el(s, 'rect', { x: x + .5, y: y(hv), width: Math.max(bw - 2, 1), height: H - pb - y(hv), fill: 'var(--hot)', rx: 1.5 });
    el(s, 'rect', { x, y: pt, width: bw, height: H - pt - pb, class: 'hit', 'data-tip': `<b>${monthName(k + '-01')}</b><br>${hv} hours · ${Math.round(sk * 100)}% quick skips` });
  });
  const pk = M.reduce((a, b) => b[1] > a[1] ? b : a); const i = M.indexOf(pk);
  el(s, 'text', { x: Math.min(Math.max(pl + i * bw, pl + 60), W - 80), y: Math.max(y(pk[1]) - 8, 14), 'text-anchor': 'middle', fill: 'var(--ink)', 'font-size': 12, 'font-family': 'var(--mono)' }, `${monthName(pk[0] + '-01')}: ${pk[1]} h`);
  $('c-monthly').appendChild(s);
});

$('l-artists-h').innerHTML = D.top_artists.map(([a, hv, n]) => `<li><span class="t">${esc(a)}<span class="sub">${fmt(n)} listens</span></span><span class="num">${fmt(hv)} h</span></li>`).join('');
$('l-albums').innerHTML = (D.top_albums || []).map(x => `<li><span class="t">${esc(x.t)}<span class="sub">${esc(x.a)}</span></span><span class="num">${h(x.h)}</span></li>`).join('');
$('l-tracks').innerHTML = D.top_tracks.map(x => `<li><span class="t">${esc(x.t)}<span class="sub">${esc(x.a)} · ${fmt(x.n)} listens</span></span><span class="num">${h(x.h)}</span></li>`).join('');
$('l-loops').innerHTML = D.loops.map(x => `<div class="card"><span class="tag">${day(x.date)}</span><span class="big">${x.n}×</span><p class="qa">${esc(x.t)}</p><p>${esc(x.a)}, back to back for ${x.hours} hours.</p></div>`).join('');

safe(() => {
  const E = D.eras; if (!E.length) return;
  const names = [...new Set(E.map(e => e.a))].slice(0, 24); const Es = E.filter(e => names.includes(e.a));
  const W = 1000, row = 24, pl = 160, pr = 10, pt = 6, pb = 24, H = pt + pb + names.length * row;
  const t0 = DateTime.fromISO(D.monthly[0][0] + '-01').toMillis(), t1 = DateTime.fromISO(D.monthly.at(-1)[0] + '-01').plus({ months: 1 }).toMillis();
  const x = iso => pl + (W - pl - pr) * (DateTime.fromISO(iso).toMillis() - t0) / (t1 - t0);
  const s = svg(W, H, 'Timeline of listening eras by artist'); const g = el(s, 'g', { class: 'axis' });
  for (let yr = +D.monthly[0][0].slice(0, 4) + 1; yr <= +D.monthly.at(-1)[0].slice(0, 4); yr++) { const xx = x(`${yr}-01-01`); el(g, 'line', { x1: xx, x2: xx, y1: pt, y2: H - pb, stroke: 'var(--rule)' }); el(g, 'text', { x: xx + 3, y: H - 8 }, yr); }
  names.forEach((nm, i) => el(s, 'text', { x: pl - 10, y: pt + i * row + row / 2 + 4, 'text-anchor': 'end', fill: 'var(--ink-2)', 'font-size': 12, 'font-family': 'var(--body)' }, nm.length > 22 ? nm.slice(0, 21) + '…' : nm));
  const maxN = Math.max(...Es.map(e => e.n));
  Es.forEach(e => { const i = names.indexOf(e.a), x1 = x(e.s), x2 = Math.max(x(e.e), x1 + 6);
    el(s, 'rect', { x: x1, y: pt + i * row + 5, width: x2 - x1, height: row - 10, rx: 4, fill: 'var(--hot)', 'fill-opacity': .45 + .55 * e.n / maxN, 'data-tip': `<b>${esc(e.a)}</b>, ${monthName(e.s)} to ${monthName(e.e)}<br>${e.n} listens · mostly “${esc(e.song)}”` }); });
  $('c-eras').appendChild(s);
});
$('l-obs').innerHTML = D.obsessions.map(o => `<li><span class="t">${esc(o.t)}<span class="sub">${esc(o.a)} · ${monthName(o.s)} to ${monthName(o.e)}</span></span><span class="num">${o.n}×</span></li>`).join('');
$('l-ded').innerHTML = D.dedications.map(d => { const ys = Object.entries(d.y), mx = Math.max(...ys.map(([, n]) => n));
  const dots = ys.map(([y, n]) => { const r = n ? 5 + 9 * Math.sqrt(n / mx) : 3; return `<i style="width:${r}px;height:${r}px;opacity:${n ? 1 : .25}" title="${y}: ${n}"></i>`; }).join('');
  return `<li><span class="t">${esc(d.t)} <span class="muted">· ${esc(d.a)}</span><span class="sub"><span class="dots" role="img" aria-label="Listens per year: ${ys.map(([y, n]) => y + ' ' + n).join(', ')}">${dots}</span></span></span><span class="num">${d.n}×</span></li>`; }).join('');
$('l-forgot').innerHTML = D.forgotten.map(f => `<li><span class="t">${esc(f.t)}<span class="sub">${esc(f.a)} · peak ${f.py} · last played ${ago(f.last)}</span></span><span class="num">${f.n}×</span></li>`).join('');
$('l-fart').innerHTML = (D.forgotten_artists || []).map(x => `<li><span class="t">${esc(x.a)}<span class="sub">last played ${ago(x.last)}</span></span><span class="num">${fmt(x.n)}</span></li>`).join('');

safe(() => yearBars('c-skip', YK.map(y => [y, YR[y].skip]), { label: 'Quick-skip rate by year', max: 1 }));
$('l-skipped').innerHTML = D.skipped.map(x => `<li><span class="t">${esc(x.t)}<span class="sub">${esc(x.a)}</span></span><span class="num">${x.s} of ${x.n}</span></li>`).join('');
$('l-untouch').innerHTML = D.untouchable.map(x => `<li><span class="t">${esc(x.t)}<span class="sub">${esc(x.a)}</span></span><span class="num">${x.n}×</span></li>`).join('');

safe(() => {
  if (!D.starts) return;
  const tot = D.starts.reduce((a, [, n]) => a + n, 0);
  $('c-starts').innerHTML = `<div style="display:flex;height:28px;border-radius:6px;overflow:hidden;gap:2px" role="img" aria-label="${D.starts.map(([k, n]) => `${k} ${Math.round(100 * n / tot)}%`).join(', ')}">` +
    D.starts.map(([k, n], i) => `<span data-tip="<b>${esc(k)}</b><br>${fmt(n)} streams · ${(100 * n / tot).toFixed(1)}%" style="flex:${n};background:${CAT[i % 6]}"></span>`).join('') + '</div>' +
    `<ul class="legend" style="margin-top:10px">${D.starts.map(([k, n], i) => `<li><span class="sw" style="background:${CAT[i % 6]}"></span>${esc(k)} ${(100 * n / tot).toFixed(1)}%</li>`).join('')}</ul>`;
  yearBars('c-shuffle', YK.map(y => [y, YR[y].shuffle]), { label: 'Share of streams on shuffle by year', max: 1 });
});
$('l-picked').innerHTML = (D.picked || []).map(x => `<li><span class="t">${esc(x.t)}<span class="sub">${esc(x.a)}</span></span><span class="num">${x.n}×</span></li>`).join('');

safe(() => {
  const Fn = D.functional; if (!Fn) return;
  const W = 420, H = 200, pb = 22, bw = W / 24, mx = Math.max(...Fn.hours_of_day, 1e-9);
  const s = svg(W, H, 'Focus and sleep audio by hour of day'); const g = el(s, 'g', { class: 'axis' });
  Fn.hours_of_day.forEach((v, i) => { const hh = (H - pb - 10) * v / mx;
    el(s, 'rect', { x: i * bw + 1.5, y: H - pb - hh, width: bw - 3, height: hh, rx: 2, fill: 'var(--hot)', 'data-tip': `<b>${String(i).padStart(2, '0')}:00</b><br>${v} h` });
    if (i % 6 === 0) el(g, 'text', { x: i * bw + bw / 2, y: H - 6, 'text-anchor': 'middle' }, String(i).padStart(2, '0')); });
  $('c-focus').appendChild(s);
  $('l-focus').innerHTML = Fn.tracks.map(x => `<li><span class="t">${esc(x.t)}<span class="sub">${esc(x.a)}</span></span><span class="num">${h(x.h)}</span></li>`).join('');
});

$('l-seasons').innerHTML = D.seasons.map(s => { const c = `color-mix(in srgb, var(--hot) ${Math.round(20 + 80 * Math.min(1, s.skip / .7))}%, var(--ground-2))`;
  return `<li style="--c:${c}" data-tip="<b>${esc(s.l)}</b><br>${s.h} hours · ${Math.round(s.skip * 100)}% quick skips"><span class="l">${esc(s.l)} · ${s.h} h</span><span class="a">${esc(s.a[0] || '—')}</span><span class="i">${s.new[0] ? 'New find: ' + esc(s.new[0]) : ''}</span></li>`; }).join('');
$('l-years').innerHTML = Object.entries(D.soundtrack).filter(([, s]) => s.length).map(([y, s]) => `<section><h3>${y}</h3><ol>${s.map(t => `<li>${esc(t.t)} <span class="muted">· ${esc(t.a)} · <span class="num">${t.n}</span></span></li>`).join('')}</ol></section>`).join('');

safe(() => {
  if (!D.mood) return;
  const order = D.mood.order; $('lg-mood').innerHTML = order.map((m, i) => `<li><span class="sw" style="background:${CAT[i]}"></span>${esc(m)}</li>`).join('');
  const Q = D.mood.q.filter(([, v]) => Object.values(v).reduce((a, b) => a + b, 0) >= 2);
  const W = 1000, H = 260, pl = 36, pr = 6, pt = 6, pb = 24, bw = (W - pl - pr) / Q.length;
  const s = svg(W, H, 'Share of each mood per quarter'); const g = el(s, 'g', { class: 'axis' });
  [0, .5, 1].forEach(v => el(g, 'text', { x: pl - 6, y: pt + (H - pt - pb) * (1 - v) + 4, 'text-anchor': 'end' }, Math.round(v * 100) + '%'));
  Q.forEach(([k, v], i) => { const tot = Object.values(v).reduce((a, b) => a + b, 0); let acc = 0; const x = pl + i * bw;
    if (k.endsWith('Q1') || i === 0) el(g, 'text', { x: x + 1, y: H - 8 }, k.slice(0, 4));
    order.forEach((m, j) => { const sh = (v[m] || 0) / tot, hh = (H - pt - pb) * sh, yt = pt + (H - pt - pb) * (1 - acc - sh);
      if (hh > 0) el(s, 'rect', { x: x + 1, y: yt + 1, width: Math.max(bw - 2, 1), height: Math.max(hh - 2, 0), fill: CAT[j], rx: 1.5 }); acc += sh; });
    el(s, 'rect', { x, y: pt, width: bw, height: H - pt - pb, class: 'hit', 'data-tip': `<b>${k}</b><br>` + order.map(m => `${esc(m)}: ${Math.round(100 * (v[m] || 0) / tot)}%`).join('<br>') }); });
  $('c-mood').appendChild(s);
});

safe(() => {
  const Hm = D.heat, days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], cw = 18, ch = 22, pl = 34, pt = 4, pb = 22, W = pl + 24 * cw + 4, H = pt + 7 * ch + pb, mx = Math.max(...Hm.flat());
  const s = svg(W, H, 'Hours of music by weekday and hour'); const g = el(s, 'g', { class: 'axis' });
  days.forEach((d, i) => el(g, 'text', { x: pl - 6, y: pt + i * ch + ch / 2 + 4, 'text-anchor': 'end' }, d));
  [0, 6, 12, 18, 23].forEach(hh => el(g, 'text', { x: pl + hh * cw + cw / 2, y: H - 6, 'text-anchor': 'middle' }, String(hh).padStart(2, '0')));
  Hm.forEach((row, i) => row.forEach((n, hh) => el(s, 'rect', { x: pl + hh * cw + 1, y: pt + i * ch + 1, width: cw - 2, height: ch - 2, rx: 3, fill: `color-mix(in srgb, var(--hot) ${Math.round(8 + 92 * n / mx)}%, var(--ground))`, 'data-tip': `<b>${days[i]} ${String(hh).padStart(2, '0')}:00</b><br>${n} hours` })));
  $('c-heat').appendChild(s);
  yearBars('c-nightyear', Object.entries(D.night_by_year), { label: 'Share of hours after midnight by year' });
});

safe(() => {
  const Dv = D.devices; if (!Dv.order.length) return;
  $('lg-dev').innerHTML = Dv.order.map((p, i) => `<li><span class="sw" style="background:${CAT[i]}"></span>${esc(p)}</li>`).join('');
  const ys = Object.keys(Dv.years), W = 1000, H = 260, pl = 50, pt = 6, pb = 24, bw = (W - pl) / ys.length, mx = Math.max(...ys.map(y => Object.values(Dv.years[y]).reduce((a, b) => a + b, 0)));
  const s = svg(W, H, 'Hours of music per device type per year'); const g = el(s, 'g', { class: 'axis' });
  ys.forEach((y, i) => { let acc = 0; const x = pl + i * bw;
    el(g, 'text', { x: x + bw / 2, y: H - 6, 'text-anchor': 'middle' }, y);
    Dv.order.forEach((p, j) => { const v = Dv.years[y][p] || 0, hh = (H - pt - pb) * v / mx, yt = H - pb - acc - hh;
      if (hh > 0) el(s, 'rect', { x: x + 8, y: yt + 1, width: bw - 16, height: Math.max(hh - 2, 0), rx: 3, fill: CAT[j], 'data-tip': `<b>${y} · ${esc(p)}</b><br>${fmt(v)} hours` }); acc += hh; }); });
  $('c-dev').appendChild(s);
});

$('l-travel').innerHTML = (D.travel?.trips || []).filter(t => !t.maybe_vpn).map(t => `<li><span class="when">${day(t.s)}${t.days > 1 ? '<br>to ' + day(t.e) : ''}<br><span class="muted">${fmt(t.n)} streams</span></span><span><b>${esc(t.c)}</b>First song: ${esc(t.first)}<br>Most played: ${esc(t.top)}</span></li>`).join('');

safe(() => yearBars('c-disc', YK.filter((y, i) => i > 0).map(y => [y, YR[y].new_artists]), { label: 'New artists per year', fmtV: v => fmt(v) }));

safe(() => {
  const ys = D.drift.years, m = D.drift.m; if (ys.length < 3) return;
  const c = Math.min(40, Math.floor(440 / ys.length)), pl = 36, pt = 4, pb = 24, W = pl + ys.length * c + 4, H = pt + ys.length * c + pb, mx = Math.max(.05, ...m.flatMap((r, i) => r.filter((_, j) => i !== j)));
  const s = svg(W, H, 'Overlap of top-40 artists between every pair of years'); const g = el(s, 'g', { class: 'axis' });
  ys.forEach((y, i) => { el(g, 'text', { x: pl - 6, y: pt + i * c + c / 2 + 4, 'text-anchor': 'end' }, "'" + String(y).slice(2)); el(g, 'text', { x: pl + i * c + c / 2, y: H - 6, 'text-anchor': 'middle' }, "'" + String(y).slice(2)); });
  m.forEach((row, i) => row.forEach((v, j) => el(s, 'rect', i === j ? { x: pl + j * c + 1, y: pt + i * c + 1, width: c - 2, height: c - 2, rx: 4, fill: 'var(--ground-2)' } :
    { x: pl + j * c + 1, y: pt + i * c + 1, width: c - 2, height: c - 2, rx: 4, fill: `color-mix(in srgb, var(--hot) ${Math.round(6 + 94 * v / mx)}%, var(--ground))`, 'data-tip': `<b>${ys[i]} vs ${ys[j]}</b><br>${Math.round(v * 100)}% overlap in top-40 artists` })));
  $('c-drift').appendChild(s);
});
$('l-flings').innerHTML = D.flings.map(f => `<li><span class="t">${esc(f.artist)}<span class="sub">${f.peak30} listens in their best 30 days · first heard ${monthName(f.first)}</span></span><span class="num">${fmt(f.n)}</span></li>`).join('');
$('steady-h').textContent = `Lifers: played in ${D.steady_years}+ different years, spread most evenly`;
$('l-steady').innerHTML = D.steady.map(f => `<li><span class="t">${esc(f.artist)}<span class="sub">${f.years} years · busiest month held ${Math.round(f.peak_share * 100)}%</span></span><span class="num">${fmt(f.n)}</span></li>`).join('');
$('l-gate').innerHTML = D.gateways.map(g => `<div class="card"><span class="tag">${esc(g.artist)} · ${day(g.date)}</span><p class="qa">${esc(g.title)}</p><p>${g.next30} listens of ${esc(g.artist)} in the next 30 days. ${fmt(g.total)} in total.</p></div>`).join('');
$('l-mara').innerHTML = D.marathons.map((r, i) => `<div class="card"><span class="tag">${DateTime.fromISO(r.start).toFormat('ccc d LLL yyyy, HH:mm')}</span><span class="big">${h(r.h)}</span>${S.marathons?.notes?.[i] ? `<p>${md(S.marathons.notes[i])}</p>` : ''}<p class="muted">Mostly ${esc(r.top)}, ${fmt(r.n)} streams.<br>From “${esc(r.first)}”<br>to “${esc(r.last)}”</p></div>`).join('');

safe(() => {
  const R = D.rituals[S.rituals?.chart_index ?? 0]; if (!R) return;
  const mn = 'JFMAMJJASOND', W = 420, H = 200, pb = 22, bw = W / 12, mx = Math.max(...R.months);
  const s = svg(W, H, `${R.name}: listens by calendar month, all years combined`);
  R.months.forEach((n, i) => { const hh = (H - pb - 18) * n / mx;
    el(s, 'rect', { x: i * bw + 3, y: H - pb - hh, width: bw - 6, height: hh, rx: 4, fill: R.window.includes(i + 1) ? 'var(--hot)' : 'var(--dim)', 'data-tip': `<b>${DateTime.fromObject({ month: i + 1 }).toFormat('LLLL')}</b><br>${n} listens` });
    el(s, 'text', { x: i * bw + bw / 2, y: H - 6, 'text-anchor': 'middle', class: 'lbl' }, mn[i]); });
  $('c-ritual').appendChild(s);
});
$('l-ritual').innerHTML = (S.rituals?.cards || []).map(c => `<div class="card"><span class="tag">${esc(c.tag)}</span><p class="qa">${md(c.title)}</p><p>${md(c.body)}</p></div>`).join('');
$('l-otd').innerHTML = Object.entries(D.otd).reverse().map(([y, o]) => `<li><span class="when">${TODAY.set({ year: +y }).toFormat('d LLL yyyy')}<br><span class="muted">${o.n} listens</span></span><span>${o.s.map(esc).join('<br>')}</span></li>`).join('');
$('l-odd').innerHTML = (S.odd?.items || []).map(o => `<div class="card"><span class="tag">${esc(o.date)}</span><p class="qa">${esc(o.title)}</p><p>${md(o.note)}</p></div>`).join('')
  + (S.odd?.feature ? `<div class="card" style="grid-column:1/-1"><span class="tag">${esc(S.odd.feature.tag)}</span><p class="qa">${md(S.odd.feature.title)}</p><p>${md(S.odd.feature.body)}</p></div>` : '');
$('l-essay').innerHTML = (S.you?.essay || []).map(e => `<div><h3>${md(e.h)}</h3><p>${md(e.p)}</p></div>`).join('');
$('l-change').innerHTML = (S.you?.change || []).map(c => `<li><span class="when">${esc(c.when)}</span><span><b>${md(c.title)}</b>${md(c.body)}</span></li>`).join('');
$('l-method').innerHTML = [
  `Source: a Spotify ${D.meta.export === 'extended' ? '"Extended streaming history"' : '"Account data" (last 12 months only)'} export, read on ${TODAY.toFormat('d LLLL yyyy')}. All times are in ${esc(ZONE)} time, including streams played abroad.`,
  'A listen is a song stream of 30 seconds or more, Spotify\'s own threshold. A quick skip is a stream ended with the next button before 30 seconds.',
  `Hours remove overlaps: when two streams overlap (two devices at once, or one left running), the earlier one is cut where the next begins. That removes ${fmt(T.raw_hours - T.hours)} of ${fmt(T.raw_hours)} raw hours. A loop left playing overnight still counts.`,
  'Focus and sleep audio is detected from track names (focus, sleep, meditation, noise, Hz…) plus artists marked by hand. Moods are hand-tagged per artist. Countries come from Spotify\'s connection data, so a VPN can look like a trip.',
  `${fmt(T.incognito)} streams were in private sessions. They count in the totals and are never listed.`,
  ...(S.method_extra || []),
].map(t => `<li>${md(t)}</li>`).join('');
</script>
'''
