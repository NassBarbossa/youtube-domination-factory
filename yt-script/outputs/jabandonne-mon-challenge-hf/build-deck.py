#!/usr/bin/env python3
"""Génère index.html (racine) + compositions/sXX.html (une sous-composition par slide).
Relancer après toute modif : python3 build-deck.py && npx hyperframes check"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent
SLIDE = 8  # secondes par slide sur la timeline racine

SHARED_CSS = r"""
#root { position: absolute; inset: 0; overflow: hidden; font-family: 'Inter', sans-serif; color: #FFFFFF; }
.veil { position: absolute; inset: 0; pointer-events: none; z-index: 1; background: radial-gradient(circle at 50% 45%, rgba(10,10,10,.30), rgba(10,10,10,.72)); }
.veil.light { background: radial-gradient(circle at 50% 45%, rgba(10,10,10,.10), rgba(10,10,10,.5)); }
.clip { position: absolute; inset: 0; z-index: 3; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 96px 120px; gap: 36px; }
.glow { position: absolute; width: 640px; height: 640px; border-radius: 50%; z-index: 2; pointer-events: none; }
.glow.o { background: radial-gradient(circle, rgba(255,107,53,.14), transparent 70%); }
.glow.c { background: radial-gradient(circle, rgba(0,229,255,.12), transparent 70%); }
.glow.u { background: radial-gradient(circle, rgba(22,199,132,.16), transparent 70%); }
.glow.d { background: radial-gradient(circle, rgba(234,57,67,.16), transparent 70%); }
.num { position: absolute; top: 36px; right: 44px; font-size: 16px; font-weight: 600; letter-spacing: .1em; color: rgba(255,255,255,.62); z-index: 4; }
.h1 { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 108px; line-height: 1.05; letter-spacing: -.02em; }
.h2 { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 68px; line-height: 1.12; letter-spacing: -.01em; }
.h3 { font-family: 'Syne', sans-serif; font-weight: 800; }
.p { font-size: 28px; line-height: 1.5; color: rgba(255,255,255,.78); }
.sub { font-size: 30px; line-height: 1.5; color: rgba(255,255,255,.78); max-width: 1200px; }
.src { font-size: 22px; color: rgba(255,255,255,.62); max-width: 1300px; line-height: 1.45; }
.kicker { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 20px; letter-spacing: .35em; text-transform: uppercase; color: #FF6B35; }
.divider { width: 88px; height: 4px; border-radius: 2px; }
.divider.o { background: #FF6B35; box-shadow: 0 0 20px rgba(255,107,53,.5); }
.divider.c { background: #00E5FF; box-shadow: 0 0 20px rgba(0,229,255,.4); }
.divider.u { background: #16C784; box-shadow: 0 0 20px rgba(22,199,132,.5); }
.t-up { color: #16C784; } .t-down { color: #EA3943; } .t-o { color: #FF6B35; }
.card { background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.14); border-radius: 22px; padding: 40px 44px; }
.ph { font-weight: 800; color: #FF6B35; background: rgba(255,107,53,.1); border: 2px dashed rgba(255,107,53,.7); border-radius: 8px; padding: .1em .5em; white-space: nowrap; }
.key { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 64px; line-height: 1.25; max-width: 1400px; }
.ghost { position: absolute; top: 50%; left: 50%; width: 1100px; height: 560px; line-height: 560px; white-space: nowrap; text-align: center; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 560px; z-index: 2; background: linear-gradient(135deg, #FF6B35, #00E5FF); -webkit-background-clip: text; background-clip: text; color: transparent; letter-spacing: -.03em; user-select: none; }
.stat { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 170px; line-height: .95; letter-spacing: -.04em; }
.cards3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px; width: 1440px; }
.cards3 .card { min-width: 0; }
"""

FONT_FACES = """@font-face { font-family: 'Syne'; src: url('assets/fonts/syne-800.woff2') format('woff2'); font-weight: 400 800; font-style: normal; font-display: block; }
@font-face { font-family: 'Inter'; src: url('assets/fonts/inter-400.woff2') format('woff2'); font-weight: 100 900; font-style: normal; font-display: block; }"""

HELPERS = r"""
const E = 'power3.out';
const $ = (id) => document.getElementById(id);
function up(tl, el, at, d = .6, y = 30) { tl.fromTo(el, { opacity: 0, y }, { opacity: 1, y: 0, duration: d, ease: E }, at); }
function pop(tl, el, at, d = .5) { tl.fromTo(el, { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: d, ease: 'back.out(2.2)' }, at); }
function draw(tl, el, at, d, ease = 'power2.inOut') { const L = el.getTotalLength(); tl.fromTo(el, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: d, ease }, at); }
function count(tl, el, target, at, d = 1.2) { const o = { v: 0 }; tl.to(o, { v: target, duration: d, ease: 'power3.out', onUpdate: () => { el.textContent = Math.round(o.v); } }, at); }
"""

# ---------------------------------------------------------------- scènes
# (id, label, raw, css propre, markup intérieur du clip, glows/extra hors clip, js timeline (t = 0), notes, fragments relatifs)
S = []

S.append(dict(id='s01', label='Titre', raw=True, notes="Dans cette vidéo, je vais vous partager les raisons de pourquoi j'arrête mon challenge.",
css=r"""
.pill { display: inline-flex; gap: 14px; align-items: center; font-weight: 800; letter-spacing: .25em; text-transform: uppercase; font-size: 18px; color: rgba(255,255,255,.78); }
.pill i { width: 14px; height: 14px; border-radius: 3px; display: inline-block; }
.pill i.u { background: #16C784; box-shadow: 0 0 12px #16C784; } .pill i.d { background: #EA3943; box-shadow: 0 0 12px #EA3943; }
.gl { position: relative; display: block; width: 1400px; height: 240px; }
.gl span, .gl strong { position: absolute; inset: 0; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 108px; line-height: 1.05; letter-spacing: -.02em; }
.gl span:nth-child(1) { color: #16C784; transform: translateX(var(--gu, 0px)); }
.gl span:nth-child(2) { color: #EA3943; transform: translateX(var(--gd, 0px)); }
.gl strong { color: #fff; }
""",
extra='<div class="glow d" style="top:-10%;left:-5%"></div><div class="glow u" style="bottom:-10%;right:-5%"></div>',
html=r"""<div class="pill" id="s01-pill"><i class="d"></i> Fin du challenge <i class="u"></i></div>
<h1 class="gl" id="s01-title" data-layout-allow-overlap><span>J'abandonne mon challenge</span><span>J'abandonne mon challenge</span><strong>J'abandonne mon challenge</strong></h1>
<p class="sub" id="s01-sub">Dans cette vidéo, je vais vous partager les raisons de pourquoi j'arrête mon challenge.</p>""",
js=r"""up(tl, $('s01-pill'), .2); up(tl, $('s01-title'), .4, .8, 40); up(tl, $('s01-sub'), 1.0);
[1.3, 3.4, 6.2].forEach(a => { tl.to($('s01-title'), { '--gu': '-9px', '--gd': '9px', duration: .06, repeat: 5, yoyo: true, ease: 'steps(1)' }, a); tl.set($('s01-title'), { '--gu': '0px', '--gd': '0px' }, a + .4); });"""))

S.append(dict(id='char-slam-explode', label='En toute transparence', notes="En toute transparence.",
block=dict(src='compositions/components/char-slam-explode.html', vars={"text": "TRANSPARENCE.", "accent": "blue", "spread": "wild"},
           style="--accent:#FF6B35; --fg:#FFFFFF; --font-display:'Syne', sans-serif;"), fragments=[2.6]))
S_UNUSED_s02 = (dict(id='s02', label='En toute transparence', raw=True, notes="En toute transparence.",
css=r"""
.rays { position: absolute; left: 50%; top: 50%; width: 4400px; height: 4400px; margin: -2200px 0 0 -2200px; z-index: 2; pointer-events: none;
  background: repeating-conic-gradient(from 0deg, rgba(22,199,132,.18) 0 6deg, transparent 6deg 18deg, rgba(234,57,67,.18) 18deg 24deg, transparent 24deg 36deg); border-radius: 50%;
  -webkit-mask: radial-gradient(circle, #000 0, #000 18%, transparent 55%); mask: radial-gradient(circle, #000 0, #000 18%, transparent 55%); }
.flash { position: absolute; inset: 0; background: #fff; z-index: 6; pointer-events: none; opacity: 0; }
.bang { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 150px; line-height: 1.02; }
.bang span { display: inline-block; }
.bang .w2 { background: linear-gradient(90deg, #FF6B35, #FFB020, #FF6B35); -webkit-background-clip: text; background-clip: text; color: transparent; }
.bangsub { font-weight: 600; font-size: 30px; color: rgba(255,255,255,.78); }
.wrap { display: flex; flex-direction: column; align-items: center; gap: 36px; }
""",
extra='<div class="rays" id="s02-rays"></div><div class="flash" id="s02-flash"></div>',
html=r"""<div class="wrap" id="s02-wrap"><p class="bang"><span class="w1" id="s02-w1">En toute</span> <span class="w2" id="s02-w2">transparence.</span></p><p class="bangsub" id="s02-sub">Les chiffres, les raisons, et ce que je fais maintenant.</p></div>""",
js=r"""tl.set($('s02-rays'), { scale: 0, opacity: 0 }, 0);
tl.fromTo($('s02-w1'), { opacity: 0, scale: 3, filter: 'blur(12px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: .45, ease: 'back.out(1.4)' }, .4);
tl.fromTo($('s02-w2'), { opacity: 0, scale: 3, filter: 'blur(12px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: .5, ease: 'back.out(1.4)' }, .95);
tl.fromTo($('s02-flash'), { opacity: .55 }, { opacity: 0, duration: .5, ease: 'power2.out' }, 1.0);
tl.to($('s02-rays'), { scale: 1, opacity: 1, duration: .7, ease: 'back.out(1.4)' }, 1.0);
tl.to($('s02-rays'), { rotation: 90, duration: 7, ease: 'none' }, 1.0);
tl.fromTo($('s02-wrap'), { x: 0, y: 0 }, { keyframes: [{ x: -10, y: 6, rotation: -1 }, { x: 9, y: -5, rotation: 1 }, { x: -6, y: 3, rotation: 0 }, { x: 0, y: 0, rotation: 0 }], duration: .45, ease: 'power1.inOut' }, 1.0);
up(tl, $('s02-sub'), 1.9);"""))

S.append(dict(id='s03', label='4 semaines', notes="Quatre semaines de challenge. Départ → aujourd'hui [À COMPLÉTER]. Du surplace. Pas une catastrophe, mais un signal.", fragments=[0.9, 4.0],
css=r"""
.flat { position: relative; width: 1200px; height: 230px; }
.flat svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.flat-line { stroke: #8A8A8A; stroke-width: 6; fill: none; stroke-linecap: round; filter: drop-shadow(0 0 8px rgba(138,138,138,.5)); }
.pin { position: absolute; width: 0; height: 0; }
.pin::before { content: ''; position: absolute; left: -9px; top: -9px; width: 18px; height: 18px; border-radius: 50%; background: #FF6B35; box-shadow: 0 0 20px #FF6B35; }
.pin b { position: absolute; left: 0; bottom: 22px; transform: translateX(-50%); white-space: nowrap; font-weight: 800; font-size: 24px; padding: 8px 20px; border-radius: 999px; background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.25); }
.pin small { position: absolute; left: 0; top: 22px; transform: translateX(-50%); white-space: nowrap; font-size: 20px; color: rgba(255,255,255,.42); }
.surplace { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 56px; color: #8A8A8A; }
""",
extra='<div class="glow o" style="top:-10%;left:30%"></div>',
html=r"""<div class="stat t-o" id="s03-stat"><span id="s03-n">0</span> semaines.</div>
<div class="flat"><svg viewBox="0 0 1200 230" preserveAspectRatio="none"><path id="s03-line" class="flat-line" d="M30,125 C180,115 270,140 390,124 S600,135 720,120 S960,130 1170,122"/></svg>
<span class="pin" id="s03-pa" style="left:30px;top:125px"><b>Départ : <span class="ph">[À COMPLÉTER]</span></b><small>[date]</small></span>
<span class="pin" id="s03-pb" style="left:1170px;top:122px"><b>Aujourd'hui : <span class="ph">[À COMPLÉTER]</span></b><small>[date]</small></span></div>
<p class="surplace" id="s03-sur">Du surplace.</p>
<p class="src" id="s03-src">Source : <span class="ph">[À COMPLÉTER : captures d'exchange ou transactions on-chain, datées]</span></p>""",
js=r"""up(tl, $('s03-stat'), .2, .6, 20); count(tl, $('s03-n'), 4, .3, 1.0);
tl.set([$('s03-pa'), $('s03-pb'), $('s03-sur'), $('s03-src'), $('s03-line')], { opacity: 0 }, 0);
tl.set($('s03-line'), { opacity: 1 }, 1.0); draw(tl, $('s03-line'), 1.0, 1.6);
pop(tl, $('s03-pa'), 1.1); pop(tl, $('s03-pb'), 2.5); up(tl, $('s03-sur'), 2.9); up(tl, $('s03-src'), 3.3, .5, 10);"""))

S.append(dict(id='s04', label='Le marché a changé', notes="Le marché a changé. Et quand le marché change, il faut s'adapter. Ça commence par regarder sa ligue en face.", fragments=[1.9, 4.0],
css=r"""
.chg { position: relative; width: 1200px; height: 230px; }
.chg svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.chg-smooth { stroke: #16C784; stroke-width: 6; fill: none; stroke-linecap: round; filter: drop-shadow(0 0 10px rgba(22,199,132,.7)); }
.chg-chop { stroke: #EA3943; stroke-width: 6; fill: none; stroke-linejoin: round; filter: drop-shadow(0 0 10px rgba(234,57,67,.7)); }
.chg-mark { position: absolute; left: 50%; top: 0; bottom: 0; width: 0; border-left: 2px dashed rgba(255,255,255,.35); }
.adapt { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 64px; }
""",
extra='<div class="glow d" style="bottom:-15%;right:-5%"></div>',
html=r"""<h2 class="h2" id="s04-h">Le marché a changé.</h2>
<div class="chg"><svg viewBox="0 0 1200 230" preserveAspectRatio="none"><path id="s04-smooth" class="chg-smooth" d="M30,195 C180,185 330,140 600,92"/><path id="s04-chop" class="chg-chop" d="M600,92 L645,138 L682,70 L727,172 L772,80 L817,190 L862,110 L915,200 L960,126 L1012,206 L1057,138 L1110,212 L1170,150"/></svg><span class="chg-mark" id="s04-mark"></span></div>
<p class="adapt" id="s04-adapt">Il faut s'adapter.</p>""",
js=r"""up(tl, $('s04-h'), .2);
tl.set([$('s04-smooth'), $('s04-chop'), $('s04-mark'), $('s04-adapt')], { opacity: 0 }, 0);
tl.set($('s04-smooth'), { opacity: 1 }, .6); draw(tl, $('s04-smooth'), .6, 1.1, 'power2.out');
tl.to($('s04-mark'), { opacity: 1, duration: .3 }, 1.7);
tl.set($('s04-chop'), { opacity: 1 }, 2.0); draw(tl, $('s04-chop'), 2.0, 1.3, 'power1.inOut');
up(tl, $('s04-adapt'), 3.4);"""))

def transition(id, n, color, title, sub, notes):
    return dict(id=id, label=f'Transition : {title}', notes=notes, css='',
        extra=f'<div class="ghost" id="{id}-ghost">{n}</div>',
        html=f'<div class="divider {color}" id="{id}-d"></div><h2 class="h2" id="{id}-h">{title}</h2><p class="sub" id="{id}-p">{sub}</p>',
        js=f"""tl.fromTo($('{id}-ghost'), {{ opacity: 0, scale: .9, xPercent: -50, yPercent: -50 }}, {{ opacity: .15, scale: 1, xPercent: -50, yPercent: -50, duration: 1.2, ease: E }}, 0);
tl.fromTo($('{id}-d'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: .5, ease: E }}, .3); up(tl, $('{id}-h'), .5); up(tl, $('{id}-p'), .8);""")

S.append(transition('s05', '01', 'o', 'Ma ligue', 'Qui gagne vraiment.', "Ma ligue, justement, parlons-en."))

S.append(dict(id='s06', label='80 / 20', notes="Pour simplifier : 80 % de perdants, 20 % de gagnants.", fragments=[2.2, 4.0],
css=r"""
.crowd { display: grid; grid-template-columns: repeat(20, 44px); gap: 14px; }
.crowd i { display: block; width: 44px; height: 44px; border-radius: 4px; background: #2A2A2A; }
.legend { display: flex; gap: 80px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 52px; }
""",
extra='',
html=r"""<p class="kicker" id="s06-k">Pour simplifier</p><div class="crowd" id="s06-crowd"></div>
<div class="legend"><span class="t-down" id="s06-l1">80 % de perdants</span><span class="t-up" id="s06-l2">20 % de gagnants</span></div>""",
js=r"""function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const g = $('s06-crowd'), rnd = mulberry32(42), idx = [...Array(100).keys()];
for (let i = idx.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [idx[i], idx[j]] = [idx[j], idx[i]]; }
const win = new Set(idx.slice(0, 20)), all = [], lose = [], wins = [];
for (let i = 0; i < 100; i++) { const d = document.createElement('i'); g.appendChild(d); all.push(d); (win.has(i) ? wins : lose).push(d); }
const order = idx.slice(); // ordre d'apparition seedé
up(tl, $('s06-k'), .2);
order.forEach((i, k) => tl.fromTo(all[i], { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: 'back.out(2)' }, .3 + k * .007));
tl.to(lose, { backgroundColor: '#EA3943', boxShadow: '0 0 10px rgba(234,57,67,.6)', duration: .3, stagger: .008 }, 1.2);
up(tl, $('s06-l1'), 1.6);
tl.to(wins, { backgroundColor: '#16C784', boxShadow: '0 0 10px rgba(22,199,132,.7)', duration: .3, stagger: .03 }, 2.4);
up(tl, $('s06-l2'), 3.0);"""))

S.append(dict(id='s07', label='Les vrais chiffres', notes="Dune / CoinGecko, Pump.fun, août 2026 : 4 wallets sur 10 ont perdu. La majorité des gagnants gagne moins de 500 $. 5 % passent 1 000 $.", fragments=[1.9, 4.0],
css=r"""
.bars { width: 1200px; display: flex; flex-direction: column; gap: 22px; }
.bar { display: grid; grid-template-columns: 330px 1fr 150px; align-items: center; gap: 24px; text-align: left; }
.bar .lab { font-weight: 600; font-size: 26px; color: rgba(255,255,255,.78); white-space: nowrap; }
.bar .trk { height: 40px; background: rgba(255,255,255,.07); border-radius: 8px; overflow: hidden; border: 1px solid rgba(255,255,255,.1); }
.bar .fil { display: block; height: 100%; border-radius: 8px; transform-origin: left center; }
.fil.d { background: #EA3943; box-shadow: 0 0 14px rgba(234,57,67,.5); }
.fil.u { background: #16C784; box-shadow: 0 0 14px rgba(22,199,132,.5); }
.fil.u2 { background: linear-gradient(90deg, #16C784, #00E5FF); }
.fil.o { background: #FF6B35; box-shadow: 0 0 14px rgba(255,107,53,.55); }
.bar .val { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 40px; text-align: right; white-space: nowrap; }
""",
extra='<div class="glow u" style="top:-10%;right:0"></div>',
html=r"""<div class="divider u" id="s07-d"></div><h2 class="h2" id="s07-h">Ce que disent les vrais chiffres</h2>
<p class="sub" id="s07-s">Pump.fun · août 2026 · résultat réalisé par wallet dans le mois</p>
<div class="bars">
<div class="bar"><span class="lab">Ont perdu de l'argent</span><div class="trk"><i class="fil d" id="s07-f1" style="width:40.2%"></i></div><span class="val t-down" id="s07-v1">40,2 %</span></div>
<div class="bar"><span class="lab">Ont gagné 1 à 500 $</span><div class="trk"><i class="fil u" id="s07-f2" style="width:51.5%"></i></div><span class="val t-up" id="s07-v2">51,5 %</span></div>
<div class="bar"><span class="lab">Ont gagné 500 à 1&nbsp;000&nbsp;$</span><div class="trk"><i class="fil u2" id="s07-f3" style="width:3.1%"></i></div><span class="val" id="s07-v3">3,1 %</span></div>
<div class="bar"><span class="lab">Ont gagné plus de 1&nbsp;000&nbsp;$</span><div class="trk"><i class="fil o" id="s07-f4" style="width:5.3%"></i></div><span class="val t-o" id="s07-v4">5,3 %</span></div>
</div>
<p class="src" id="s07-src">Source : Dune, dashboard CoinGecko « Pump.fun Trader Profitability », août 2026 (862 734 wallets), consulté le 16 oct. 2026. PnL réalisé · un wallet n'est pas une personne.</p>""",
js=r"""tl.fromTo($('s07-d'), { scaleX: 0 }, { scaleX: 1, duration: .5, ease: E }, .1); up(tl, $('s07-h'), .2); up(tl, $('s07-s'), .4);
[[1, .8], [2, 1.6], [3, 2.1], [4, 2.6]].forEach(([i, a]) => { tl.fromTo($('s07-f' + i), { scaleX: 0 }, { scaleX: 1, duration: 1.0, ease: 'power3.out' }, a); tl.fromTo($('s07-v' + i), { opacity: 0 }, { opacity: 1, duration: .4 }, a + .5); });
up(tl, $('s07-src'), 3.3, .5, 10);"""))

S.append(dict(id='s08', label='Ma ligue, étage par étage', notes="Ta pyramide à l'oral (top 20 / 10 / 1 / 0,1 %). À l'écran, les étages sourcés : >1 000 $ ≈ 5 %, >10 000 $ 0,41 %, >100 000 $ 0,05 %, >1 M$ 293 wallets.", fragments=[1.1, 1.9, 4.0],
css=r"""
.ladder { display: flex; flex-direction: column-reverse; gap: 12px; align-items: center; width: 1200px; }
.rung { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 20px; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.16); border-radius: 14px; padding: 12px 28px; text-align: left; }
.rung .t { font-weight: 600; font-size: 24px; color: rgba(255,255,255,.78); white-space: nowrap; }
.rung .n { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 36px; white-space: nowrap; }
.rung.lose { background: rgba(234,57,67,.85); border-color: #EA3943; } .rung.lose .t { color: rgba(255,255,255,.9); }
.rung.top { background: #FF6B35; border-color: #FF6B35; box-shadow: 0 0 30px rgba(255,107,53,.45); } .rung.top .t { color: rgba(10,10,10,.8); } .rung.top .n { color: #0A0A0A; }
""",
extra='<div class="glow o" style="top:10%;left:-5%"></div>',
html=r"""<h2 class="h2" id="s08-h">Ma ligue, étage par étage</h2>
<div class="ladder">
<div class="rung lose" id="s08-r1" style="width:100%"><span class="t">Ont perdu de l'argent dans le mois</span><span class="n">~40 %</span></div>
<div class="rung" id="s08-r2" style="width:90%"><span class="t">Ont gagné 1 à 500 $ dans le mois</span><span class="n">~51 %</span></div>
<div class="rung" id="s08-r3" style="width:80%"><span class="t">Plus de 1 000 $ dans le mois</span><span class="n">~5 %</span></div>
<div class="rung" id="s08-r4" style="width:70%"><span class="t">Plus de 10 000 $ réalisés (cumul)</span><span class="n">0,41 %</span></div>
<div class="rung" id="s08-r5" style="width:62%"><span class="t">Plus de 100 000 $ (cumul)</span><span class="n">0,05 %</span></div>
<div class="rung top" id="s08-r6" style="width:58%"><span class="t">Plus de 1 M$ (cumul) : 293 wallets</span><span class="n">0,002 %</span></div>
</div>
<p class="src" id="s08-src">Sources : Dune, dashboard CoinGecko, août 2026 (3 premiers étages) · Dune Adam Tehc, cumul au 11 janv. 2025, via Cointelegraph (3 derniers). Wallets, pas des personnes · PnL réalisé.</p>""",
js=r"""up(tl, $('s08-h'), .2);
[[1, .6], [2, .85], [3, 1.35], [4, 2.0], [5, 2.3], [6, 2.6]].forEach(([i, a]) => tl.fromTo($('s08-r' + i), { opacity: 0, y: 26, scale: .96 }, { opacity: 1, y: 0, scale: 1, duration: .55, ease: E }, a));
up(tl, $('s08-src'), 3.3, .5, 10);"""))

S.append(dict(id='s09', label='AMF 89 %', notes="Pas que les memecoins : AMF, 14 799 clients Forex/CFD, 89 % perdants sur 4 ans, −10 887 € en moyenne, plus actif = plus de pertes.", fragments=[1.8, 4.0],
css=r"""
.cards3 .card b { display: block; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 38px; line-height: 1.15; margin-bottom: 10px; color: #FF6B35; }
.cards3 .card p { font-size: 22px; line-height: 1.4; color: rgba(255,255,255,.78); }
.stat.down { color: #EA3943; text-shadow: 0 0 30px rgba(234,57,67,.45); }
""",
extra='<div class="glow d" style="top:-10%;left:20%"></div>',
html=r"""<p class="kicker" id="s09-k">Et ce n'est pas que les memecoins</p>
<div class="stat down" id="s09-stat"><span id="s09-n">0</span> %</div>
<h2 class="h2" id="s09-h">de perdants sur 4 ans</h2>
<div class="cards3">
<div class="card" id="s09-c1"><b>14 799</b><p>clients de courtiers Forex et CFD suivis par l'AMF, 2009-2012</p></div>
<div class="card" id="s09-c2"><b>−10 887 €</b><p>résultat moyen par client sur la période</p></div>
<div class="card" id="s09-c3"><b>Plus actif, plus de pertes</b><p>1 000 ordres et plus : −31 349 € en moyenne</p></div>
</div>
<p class="src" id="s09-src">Source : AMF, Lettre de l'Observatoire de l'épargne n° 10, octobre 2014.</p>""",
js=r"""up(tl, $('s09-k'), .2);
tl.fromTo($('s09-stat'), { opacity: 0, scale: .7 }, { opacity: 1, scale: 1, duration: .7, ease: 'back.out(1.6)' }, .5); count(tl, $('s09-n'), 89, .5, 1.2);
up(tl, $('s09-h'), 1.1); [1, 2, 3].forEach(i => up(tl, $('s09-c' + i), 1.9 + (i - 1) * .3)); up(tl, $('s09-src'), 3.2, .5, 10);"""))

S.append(dict(id='s10', label='Exemples', notes="Tes exemples [À COMPLÉTER].",
css=r"""
.cards3 .card { min-height: 220px; display: flex; flex-direction: column; justify-content: center; gap: 12px; }
.cards3 .card h3 { font-size: 30px; } .cards3 .card h3 .ph { font-size: 24px; }
.cards3 .card p { color: rgba(255,255,255,.78); }
""",
extra='<div class="glow c" style="bottom:-15%;right:-5%"></div>',
html=r"""<div class="divider c" id="s10-d"></div><h2 class="h2" id="s10-h">Des exemples</h2>
<div class="cards3">
<div class="card" id="s10-c1"><h3 class="h3"><span class="ph">[À COMPLÉTER]</span></h3><p class="p">Qui · résultat · source datée</p></div>
<div class="card" id="s10-c2"><h3 class="h3"><span class="ph">[À COMPLÉTER]</span></h3><p class="p">Qui · résultat · source datée</p></div>
<div class="card" id="s10-c3"><h3 class="h3"><span class="ph">[À COMPLÉTER]</span></h3><p class="p">Qui · résultat · source datée</p></div>
</div>""",
js=r"""tl.fromTo($('s10-d'), { scaleX: 0 }, { scaleX: 1, duration: .5, ease: E }, .1); up(tl, $('s10-h'), .2); [1, 2, 3].forEach(i => up(tl, $('s10-c' + i), .6 + (i - 1) * .2));"""))

S.append(dict(id='s11', label='Connaître ma ligue', notes="Et donc, c'est important de connaître ma ligue.",
css=r"""
.stampwrap { display: block; width: 420px; height: 100px; }
.stamp { display: inline-block; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 60px; letter-spacing: .12em; color: #EA3943; border: 6px solid #EA3943; border-radius: 12px; padding: 4px 24px; text-transform: uppercase; mix-blend-mode: screen; white-space: nowrap; }
.tier { font-weight: 600; font-size: 30px; color: rgba(255,255,255,.78); }
""",
extra='<div class="glow o" style="top:20%;right:10%"></div>',
html=r"""<p class="key" id="s11-key">C'est important de connaître ma ligue.</p>
<div class="stampwrap"><span class="stamp" id="s11-stamp">Ma ligue</span></div>
<p class="tier" id="s11-tier">Mon étage : <span class="ph">[À COMPLÉTER]</span></p>""",
js=r"""up(tl, $('s11-key'), .3, .7, 30);
tl.fromTo($('s11-stamp'), { opacity: 0, scale: 4, rotation: -6 }, { opacity: .95, scale: 1, rotation: -6, duration: .4, ease: 'back.out(1.4)' }, 1.4); up(tl, $('s11-tier'), 2.2);"""))

S.append(transition('s12', '02', 'c', "Pourquoi j'attends", 'Le moment compte plus que la méthode.', "Pourquoi j'attends."))

S.append(dict(id='s13', label='Le moment compte plus que la méthode', graph=True, notes="Même dashboard, part de gagnants par mois : juin 2025, 30 %. Juin 2026, 80 %. Mêmes gens, mêmes outils : seul le marché a changé. Le moment compte plus que la méthode.", fragments=[1.2, 4.0]))
S_UNUSED_s13 = (dict(id='s13', label='Le moment compte plus que la méthode', notes="Même dashboard, part de gagnants par mois : juin 2025, 30 %. Juin 2026, 80 %. Mêmes gens, mêmes outils : seul le marché a changé. Le moment compte plus que la méthode.", fragments=[1.6, 4.0],
css=r"""
.chart { position: relative; width: 1300px; height: 400px; }
.chart svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.chart .grid { stroke: rgba(255,255,255,.1); stroke-width: 1; }
.chart .gl2 { font-family: 'Inter', sans-serif; font-size: 18px; fill: rgba(255,255,255,.7); }
.chart .ln { stroke: #16C784; stroke-width: 6; fill: none; stroke-linecap: round; stroke-linejoin: round; filter: drop-shadow(0 0 10px rgba(22,199,132,.6)); }
.chart .ar { fill: url(#s13-area-grad); }
.pt { position: absolute; width: 0; height: 0; }
.pt::before { content: ''; position: absolute; left: -8px; top: -8px; width: 16px; height: 16px; border-radius: 50%; background: #fff; border: 3px solid #16C784; box-shadow: 0 0 14px rgba(22,199,132,.7); }
.pt.lo::before { border-color: #EA3943; box-shadow: 0 0 14px rgba(234,57,67,.7); }
.pt b { position: absolute; left: 0; bottom: 20px; transform: translateX(-50%); white-space: nowrap; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 34px; }
.pt small { position: absolute; left: 0; top: 18px; transform: translateX(-50%); white-space: nowrap; font-size: 20px; color: #FFB020; font-weight: 600; }
.pt.lo b { color: #EA3943; } .pt.hi b { color: #16C784; }
.pt.below b { bottom: auto; top: 20px; } .pt.below small { top: 62px; }
.pt.above small { top: auto; bottom: 62px; }
""",
extra='<div class="glow u" style="bottom:-10%;right:0"></div>',
html=r"""<h2 class="h2" id="s13-h">Le moment compte plus que la méthode</h2>
<p class="sub" id="s13-s">Part de wallets gagnants sur Pump.fun, par mois</p>
<div class="chart"><svg viewBox="0 0 1300 400" preserveAspectRatio="none">
<defs><linearGradient id="s13-area-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16C784" stop-opacity=".35"/><stop offset="1" stop-color="#16C784" stop-opacity="0"/></linearGradient></defs>
<line class="grid" x1="60" y1="40" x2="1250" y2="40"/><text class="gl2" x="0" y="46">80 %</text>
<line class="grid" x1="60" y1="160" x2="1250" y2="160"/><text class="gl2" x="0" y="166">50 %</text>
<line class="grid" x1="60" y1="280" x2="1250" y2="280"/><text class="gl2" x="0" y="286">20 %</text>
<line class="grid" x1="60" y1="360" x2="1250" y2="360"/>
<path class="ar" id="s13-area" d="M81,320 L894,147 L1056,122 L1138,138 L1219,200 L1219,360 L81,360 Z"/>
<path class="ln" id="s13-line" d="M81,320 L894,147 L1056,122 L1138,138 L1219,200"/></svg>
<span class="pt lo below" id="s13-p1" style="left:81px;top:320px"><b>30,1 %</b><small>juin 2025</small></span>
<span class="pt" id="s13-p2" style="left:894px;top:147px"><b>73,3 %</b><small>avril 2026</small></span>
<span class="pt hi above" id="s13-p3" style="left:1056px;top:122px"><b>79,5 %</b><small>juin 2026</small></span>
<span class="pt below" id="s13-p4" style="left:1138px;top:138px"><b>75,4 %</b><small>juil. 2026</small></span>
<span class="pt below" id="s13-p5" style="left:1219px;top:200px"><b>59,8 %</b><small>août 2026</small></span></div>
<p class="src" id="s13-src">Source : Dune, dashboard CoinGecko « Pump.fun Trader Profitability », PnL réalisé par mois, consulté le 16 oct. 2026. Mêmes outils, même plateforme : seul le marché a changé.</p>""",
js=r"""up(tl, $('s13-h'), .2); up(tl, $('s13-s'), .4);
tl.set([$('s13-area'), $('s13-line')], { opacity: 0 }, 0); tl.set($('s13-line'), { opacity: 1 }, .8); draw(tl, $('s13-line'), .8, 2.4, 'power1.inOut');
pop(tl, $('s13-p1'), .9); pop(tl, $('s13-p2'), 2.3); pop(tl, $('s13-p3'), 2.7); pop(tl, $('s13-p4'), 2.95); pop(tl, $('s13-p5'), 3.2);
tl.to($('s13-area'), { opacity: 1, duration: .8 }, 3.2); up(tl, $('s13-src'), 3.5, .5, 10);"""))

S.append(dict(id='s14', label='Pas le moment', notes="Dans ma ligue, pour le moment, c'est pas le moment de prendre beaucoup de risques.",
css=r"""
.gauge { position: relative; width: 640px; height: 340px; }
.gauge svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.glab { display: flex; justify-content: space-between; width: 640px; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; font-size: 20px; }
""",
extra='<div class="glow d" style="top:-10%;left:10%"></div>',
html=r"""<p class="key" id="s14-key">Pour le moment, c'est pas le moment de prendre beaucoup de risques.</p>
<div class="gauge"><svg viewBox="0 0 320 170">
<defs><linearGradient id="s14-gg" x1="0" x2="1"><stop offset="0" stop-color="#16C784"/><stop offset=".5" stop-color="#FF6B35"/><stop offset="1" stop-color="#EA3943"/></linearGradient></defs>
<path d="M20,150 A140,140 0 0 1 300,150" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="22" stroke-linecap="round"/>
<path d="M20,150 A140,140 0 0 1 300,150" fill="none" stroke="url(#s14-gg)" stroke-width="22" stroke-linecap="round" opacity=".85"/>
<g id="s14-needle"><line x1="160" y1="150" x2="160" y2="40" stroke="#fff" stroke-width="6" stroke-linecap="round"/><circle cx="160" cy="150" r="12" fill="#fff"/></g></svg></div>
<div class="glab" id="s14-lab"><span class="t-up">Risque faible</span><span class="t-down">Risque élevé</span></div>""",
js=r"""up(tl, $('s14-key'), .3, .7, 30);
tl.fromTo($('s14-needle'), { rotation: 80, svgOrigin: '160 150' }, { rotation: -78, svgOrigin: '160 150', duration: 1.8, ease: 'back.out(1.2)' }, 1.0); up(tl, $('s14-lab'), .6);"""))

S.append(dict(id='s15', label='Être patient', notes="Être patient. Attendre les meilleures conditions de marché, là où je serai performant.", fragments=[2.6, 4.0],
css=r"""
.wait { display: flex; align-items: flex-end; gap: 22px; height: 260px; }
.wait i { display: block; width: 38px; border-radius: 4px; background: #2A2A2A; position: relative; }
.wait i::before { content: ''; position: absolute; left: 50%; top: -16px; bottom: -12px; width: 3px; margin-left: -1.5px; background: inherit; opacity: .7; }
.waitsub { font-size: 32px; max-width: 1200px; color: rgba(255,255,255,.78); }
""",
extra='<div class="glow u" style="bottom:-10%;right:10%"></div>',
html=r"""<h2 class="h2" id="s15-h">Être patient.</h2>
<div class="wait" id="s15-wait"><i style="height:45%"></i><i style="height:60%"></i><i style="height:38%"></i><i style="height:52%"></i><i style="height:30%"></i><i style="height:48%"></i><i style="height:35%"></i><i style="height:55%"></i><i style="height:42%"></i><i style="height:62%"></i><i style="height:78%"></i><i style="height:95%"></i></div>
<p class="waitsub" id="s15-sub">Attendre les meilleures conditions de marché, là où je serai performant.</p>""",
js=r"""up(tl, $('s15-h'), .2); const bars = Array.from($('s15-wait').children);
tl.fromTo(bars, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .45, ease: E, stagger: .18 }, .4);
tl.to(bars.slice(9), { backgroundColor: '#16C784', boxShadow: '0 0 18px rgba(22,199,132,.75)', duration: .35, stagger: .2 }, 2.7); up(tl, $('s15-sub'), 3.4);"""))

S.append(dict(id='s16', label='Un appartement par semaine', notes="Vous qui investissez dans l'immobilier : on n'achète pas un appartement par semaine. Le bon bien, au bon prix. Entre deux, rien. La crypto, pareil.",
css=r"""
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; width: 1400px; }
.two .card { text-align: left; display: flex; flex-direction: column; gap: 10px; }
.two .k { font-family: 'Syne', sans-serif; font-weight: 700; letter-spacing: .25em; text-transform: uppercase; font-size: 18px; color: #00E5FF; }
.two h3 { font-size: 40px; line-height: 1.25; }
""",
extra='<div class="glow o" style="top:-10%;left:30%"></div>',
html=r"""<h2 class="h2" id="s16-h" style="max-width:1300px">On n'achète pas un appartement par semaine.</h2>
<div class="two">
<div class="card" id="s16-c1"><span class="k">Immobilier</span><h3 class="h3">Le bon bien, au bon prix.</h3><p class="p">Et entre deux, on ne fait rien.</p></div>
<div class="card" id="s16-c2"><span class="k">Crypto</span><h3 class="h3">La bonne opportunité, au bon moment.</h3><p class="p">Et entre deux, on ne fait rien.</p></div>
</div>""",
js=r"""up(tl, $('s16-h'), .2); up(tl, $('s16-c1'), .7); up(tl, $('s16-c2'), .95);"""))

S.append(dict(id='s17', label='CTA formation offerte', notes="Formation offerte, 3 vidéos, lien en description. Pas un conseil en investissement.",
css=r"""
.cta { border-radius: 28px; padding: 64px 80px; border: 2px solid rgba(255,107,53,.6); background: rgba(10,10,10,.45); max-width: 1300px; }
.cta p { font-size: 30px; color: rgba(255,255,255,.78); line-height: 1.5; }
.desc { display: inline-flex; align-items: center; gap: 12px; font-weight: 800; font-size: 24px; color: #0A0A0A; background: #FF6B35; border-radius: 999px; padding: 14px 30px; box-shadow: 0 0 24px rgba(255,107,53,.5); }
.desc span { display: inline-block; }
.disc { font-size: 20px; color: rgba(255,255,255,.42); letter-spacing: .04em; }
""",
extra='<div class="glow o" style="top:10%;left:20%"></div><div class="glow c" style="bottom:20%;right:20%"></div>',
html=r"""<div class="cta" id="s17-box"><h2 class="h2" style="margin-bottom:18px">La formation offerte</h2><p>3 vidéos pour comprendre comment on achète en dehors des échanges, avant que les coins soient connus de tous.</p></div>
<span class="desc" id="s17-desc">Lien dans la description <span id="s17-arrow">↓</span></span>
<p class="disc" id="s17-disc">Pas un conseil en investissement.</p>""",
js=r"""tl.fromTo($('s17-box'), { opacity: 0, scale: .94 }, { opacity: 1, scale: 1, duration: .7, ease: E }, .3);
tl.to($('s17-box'), { boxShadow: '0 0 48px rgba(255,107,53,.35)', duration: 1.2, yoyo: true, repeat: 5, ease: 'sine.inOut' }, .8);
up(tl, $('s17-desc'), .9); up(tl, $('s17-disc'), 1.2, .5, 10);
tl.to($('s17-arrow'), { y: 5, duration: .7, yoyo: true, repeat: 9, ease: 'sine.inOut' }, 1.0);"""))


GRAPH_TEMPLATE = """<!doctype html>
<html lang="fr"><head><meta charset="UTF-8" /><title>s13 — courbe (bloc mk-line-graph adapté)</title></head>
<body>
<template>
<style>
__FONTS__
#root { position: absolute; inset: 0; overflow: hidden; font-family: 'Inter', sans-serif; color: #fff;
  --mk-font: 'Inter', sans-serif; --mk-ink: #FFFFFF; --mk-ink-dim: rgba(255,255,255,.72); --mk-accent: #16C784; --mk-paper: #0A0A0A; --mk-blob-2: #00E5FF; --mk-axis: rgba(255,255,255,.25); }
.veil { position: absolute; inset: 0; pointer-events: none; z-index: 1; background: radial-gradient(circle at 50% 45%, rgba(10,10,10,.30), rgba(10,10,10,.72)); }
.num { position: absolute; top: 36px; right: 44px; font-size: 16px; font-weight: 600; letter-spacing: .1em; color: rgba(255,255,255,.62); z-index: 4; }
#s13-svg { position: absolute; inset: 0; z-index: 2; }
#s13-labels { position: absolute; inset: 0; z-index: 3; }
.mk-lg-line { fill: none; stroke-width: 6; stroke-linecap: round; stroke-linejoin: round; filter: drop-shadow(0 0 10px rgba(22,199,132,.6)); }
.mk-lg-dot { stroke-width: 4; fill: var(--mk-paper); }
.mk-lg-axis { stroke: var(--mk-axis); stroke-width: 2; }
.mk-lg-value { position: absolute; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 40px; letter-spacing: -0.01em; color: var(--mk-ink); font-variant-numeric: tabular-nums; transform: translate(-50%, 0); line-height: 44px; white-space: nowrap; }
.mk-lg-value.first { color: #EA3943; } .mk-lg-value.peak { color: #16C784; }
.mk-lg-xlabel { position: absolute; font-weight: 600; font-size: 24px; color: #FFB020; transform: translateX(-50%); white-space: nowrap; }
.mk-lg-legend { position: absolute; display: flex; gap: 40px; }
.mk-lg-legend-item { display: flex; align-items: center; gap: 12px; font-weight: 500; font-size: 26px; color: var(--mk-ink-dim); }
.mk-lg-legend-dot { width: 14px; height: 14px; border-radius: 50%; }
.s13-title { position: absolute; left: 0; right: 0; top: 110px; text-align: center; white-space: nowrap; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 58px; line-height: 1.12; letter-spacing: -.01em; z-index: 3; }
.s13-sub { position: absolute; left: 0; right: 0; top: 200px; text-align: center; font-size: 30px; color: rgba(255,255,255,.78); z-index: 3; }
.s13-src { position: absolute; left: 0; right: 0; bottom: 70px; text-align: center; font-size: 22px; color: rgba(255,255,255,.62); z-index: 3; padding: 0 200px; line-height: 1.45; }
.s13-area { fill: url(#s13-grad); opacity: 0; }
</style>
<div id="root" data-composition-id="s13" data-width="1920" data-height="1080">
  <div class="veil"></div>
  <span class="num">13 / 17</span>
  <h2 class="s13-title" id="s13-title">Le moment compte plus que la méthode</h2>
  <p class="s13-sub" id="s13-sub">Part de wallets gagnants sur Pump.fun, par mois</p>
  <svg id="s13-svg" viewBox="0 0 1920 1080"><defs><linearGradient id="s13-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16C784" stop-opacity=".35"/><stop offset="1" stop-color="#16C784" stop-opacity="0"/></linearGradient></defs></svg>
  <div id="s13-labels"></div>
  <p class="s13-src" id="s13-src">Source : Dune, dashboard CoinGecko « Pump.fun Trader Profitability », PnL réalisé par mois, consulté le 16 oct. 2026. Mêmes outils, même plateforme : seul le marché a changé.</p>
  <div id="s13-clip" class="clip" data-start="0" data-duration="8" data-track-index="1" style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none"></div>
</div>
<script>
(function () {
  /* mk-line-graph (registre HyperFrames), adapté : une série, valeurs en %, charte Nass */
  var CONFIG = {
    series: [{ name: "Wallets gagnants dans le mois", color: null, values: [30.1, 73.3, 79.5, 75.4, 59.8] }],
    xLabels: ["juin 2025", "avril 2026", "juin 2026", "juil. 2026", "août 2026"],
    showValues: true, area: { x: 300, y: 320, w: 1320, h: 440 }, animationIn: true, animationOut: false
  };
  var NS = "http://www.w3.org/2000/svg";
  var root = document.getElementById("root") || document.querySelector('[data-composition-id="s13"]');
  var svg = document.getElementById("s13-svg"), labels = document.getElementById("s13-labels"), A = CONFIG.area;
  var accent = "#16C784";
  var max = 100; var n = CONFIG.series[0].values.length;
  function px(i) { return A.x + (i / (n - 1)) * A.w; }
  function py(v) { return A.y + A.h - (v / max) * A.h; }
  function fr(v) { return String(v).replace('.', ',') + " %"; }
  var axis = document.createElementNS(NS, "line"); axis.setAttribute("class", "mk-lg-axis");
  axis.setAttribute("x1", A.x - 20); axis.setAttribute("y1", A.y + A.h); axis.setAttribute("x2", A.x + A.w + 20); axis.setAttribute("y2", A.y + A.h); axis.id = "s13-axis"; svg.appendChild(axis);
  var s = CONFIG.series[0], color = accent;
  var d = s.values.map(function (v, i) { return (i === 0 ? "M" : "L") + px(i) + " " + py(v); }).join(" ");
  var area = document.createElementNS(NS, "path"); area.setAttribute("class", "s13-area"); area.id = "s13-areapath";
  area.setAttribute("d", d + " L" + px(n - 1) + " " + (A.y + A.h) + " L" + px(0) + " " + (A.y + A.h) + " Z"); svg.appendChild(area);
  var path = document.createElementNS(NS, "path"); path.setAttribute("class", "mk-lg-line"); path.setAttribute("d", d); path.setAttribute("stroke", color); path.id = "s13-path"; svg.appendChild(path);
  var dots = [], vals = [];
  s.values.forEach(function (v, i) {
    var dot = document.createElementNS(NS, "circle"); dot.setAttribute("class", "mk-lg-dot"); dot.setAttribute("cx", px(i)); dot.setAttribute("cy", py(v)); dot.setAttribute("r", 10);
    dot.setAttribute("stroke", i === 0 ? "#EA3943" : color); dot.id = "s13-dot-" + i; svg.appendChild(dot); dots.push(dot);
    var val = document.createElement("div"); val.className = "mk-lg-value" + (i === 0 ? " first" : (i === 2 ? " peak" : "")); val.id = "s13-val-" + i; val.textContent = fr(v);
    val.style.left = px(i) + "px"; val.style.top = py(v) - 66 + "px"; labels.appendChild(val); vals.push(val);
  });
  CONFIG.xLabels.forEach(function (t, i) { var xl = document.createElement("div"); xl.className = "mk-lg-xlabel"; xl.id = "s13-xl-" + i; xl.textContent = t; xl.style.left = px(i) + "px"; xl.style.top = A.y + A.h + 24 + "px"; labels.appendChild(xl); });
  var legend = document.createElement("div"); legend.className = "mk-lg-legend"; legend.id = "s13-legend"; legend.style.left = A.x + "px"; legend.style.top = A.y + A.h + 80 + "px";
  var item = document.createElement("div"); item.className = "mk-lg-legend-item"; var ld = document.createElement("span"); ld.className = "mk-lg-legend-dot"; ld.style.background = color; item.appendChild(ld); item.appendChild(document.createTextNode(s.name)); legend.appendChild(item); labels.appendChild(legend);

  var tl = gsap.timeline({ paused: true }); var DRAW = 2.2;
  tl.fromTo("#s13-title", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .6, ease: "power3.out" }, .1);
  tl.fromTo("#s13-sub", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .6, ease: "power3.out" }, .3);
  tl.fromTo(axis, { opacity: 0 }, { opacity: 1, duration: .5, ease: "power2.out" }, .4);
  CONFIG.xLabels.forEach(function (t, i) { tl.fromTo("#s13-xl-" + i, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: .4, ease: "power2.out" }, .45 + i * .06); });
  var t0 = .7, len = path.getTotalLength();
  tl.fromTo(path, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: DRAW, ease: "power2.inOut" }, t0);
  s.values.forEach(function (v, i) {
    var td = t0 + (i / (n - 1)) * DRAW * 0.92;
    tl.fromTo(dots[i], { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: .35, ease: "back.out(1.2)" }, td);
    tl.fromTo(vals[i], { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: .35, ease: "power2.out" }, td + .06);
  });
  tl.to(area, { opacity: 1, duration: .8 }, t0 + DRAW);
  tl.fromTo(legend, { opacity: 0 }, { opacity: 1, duration: .5, ease: "power2.out" }, t0 + DRAW);
  tl.fromTo("#s13-src", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: .5 }, t0 + DRAW + .3);
  window.__timelines["s13"] = tl;
})();
</script>
</template>
</body></html>
"""

# ---------------------------------------------------------------- génération
assert len(S) == 17
manifest = {"slides": [], "slideSequences": []}
hosts = []
for k, sc in enumerate(S):
    start = k * SLIDE
    sid = sc['id']
    entry = {"sceneId": sid, "notes": sc['notes']}
    if sc.get('fragments'):
        entry["fragments"] = [round(start + f, 3) for f in sc['fragments']]
    manifest["slides"].append(entry)
    if sc.get('block'):
        b = sc['block']
        hosts.append(f'<div id="{sid}-host" data-composition-id="{sid}" data-composition-src="{b["src"]}" data-variable-values=\'{json.dumps(b["vars"], ensure_ascii=False)}\' style="{b["style"]}" data-start="{start}" data-duration="{SLIDE}" data-track-index="1" data-width="1920" data-height="1080" data-label="{sc["label"]}"></div>')
        continue
    hosts.append(f'<div id="{sid}-host" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start}" data-duration="{SLIDE}" data-track-index="1" data-width="1920" data-height="1080" data-label="{sc["label"]}"></div>')
    if sc.get('graph'):
        (ROOT / 'compositions' / f'{sid}.html').write_text(GRAPH_TEMPLATE.replace('__FONTS__', FONT_FACES), encoding='utf-8')
        continue
    sub = f"""<!doctype html>
<html lang="fr"><head><meta charset="UTF-8" /><title>{sid} — {sc['label']}</title></head>
<body>
<template>
<style>
{FONT_FACES}
{SHARED_CSS}
{sc['css']}
</style>
<div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
  <div class="veil{' light' if sc.get('raw') else ''}"></div>
  {sc['extra']}
  <span class="num">{k+1:02d} / 17</span>
  <section class="clip" id="{sid}-clip" data-start="0" data-duration="{SLIDE}" data-track-index="1">
{sc['html']}
  </section>
</div>
<script>
(function () {{
{HELPERS}
const tl = gsap.timeline({{ paused: true }});
{sc['js']}
window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
</body></html>
"""
    (ROOT / 'compositions' / f'{sid}.html').write_text(sub, encoding='utf-8')

total = len(S) * SLIDE
index = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>J'abandonne mon challenge — Nass Riviera</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{FONT_FACES}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0A0A0A; }}
body {{ font-family: 'Inter', sans-serif; color: #fff; -webkit-font-smoothing: antialiased; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: url('assets/bg-nass-v2.jpg') center / cover no-repeat, #0A0A0A; }}
#deck-candles {{ position: absolute; inset: 0; width: 1920px; height: 1080px; z-index: 0; pointer-events: none; }}
#root > [data-composition-src] {{ position: absolute; inset: 0; }}
/* bloc char-slam-explode : charte Nass forcée (le bloc pose ses variables en inline) */
[data-composition-id="char-slam-explode"], [data-composition-id="char-slam-explode"] * {{ --cse-accent: #FF6B35 !important; --accent: #FF6B35; --fg: #FFFFFF; --font-display: 'Syne', sans-serif; }}
[data-composition-id="char-slam-explode"] .cse-glyph, [data-composition-id="char-slam-explode"] [class*="cse-"] {{ font-family: 'Syne', sans-serif; font-weight: 800; }}
</style>
</head>
<body>
<script type="application/hyperframes-slideshow+json">
{json.dumps(manifest, ensure_ascii=False, indent=2)}
</script>

<div id="root" data-composition-id="deck" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
  <img id="deck-candles" alt="" src="" data-timeline-role="persistent-overlay" />
{chr(10).join('  ' + h for h in hosts)}
</div>

<script>
window.__timelines = window.__timelines || {{}};
/* fond bougies vert/rouge, dessiné une fois, seedé (déterministe) */
(function () {{
  function mulberry32(a) {{ return function () {{ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }}; }}
  const c = document.createElement('canvas'); c.width = 1920; c.height = 1080;
  const ctx = c.getContext('2d'), rnd = mulberry32(6995), W = 1920, H = 1080, w = 22, gap = 12; let p = H * .55;
  ctx.globalAlpha = .18;
  for (let x = -w; x < W + w; x += w + gap) {{
    const o = p, d = (rnd() - .5) * H * .12, cl = Math.min(Math.max(o + d, H * .25), H * .85);
    const hi = Math.max(o, cl) + rnd() * H * .05, lo = Math.min(o, cl) - rnd() * H * .05, col = cl >= o ? '#16C784' : '#EA3943';
    ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x + w / 2, lo); ctx.lineTo(x + w / 2, hi); ctx.stroke();
    ctx.fillRect(x, Math.min(o, cl), w, Math.max(4, Math.abs(cl - o)));
    p = cl;
  }}
  document.getElementById('deck-candles').src = c.toDataURL('image/png');
}})();
const tl = gsap.timeline({{ paused: true }});
window.__timelines["deck"] = tl;
</script>
</body>
</html>
"""
(ROOT / 'index.html').write_text(index, encoding='utf-8')
print('généré : index.html +', len(S), 'sous-compositions ; durée racine', total, 's')
