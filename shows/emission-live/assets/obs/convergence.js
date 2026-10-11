// Convergence — scripts communs des écrans OBS
// 1. Wordmark : <span data-wm="anim"></span> ou <span data-wm=""></span>
const CONV_V = `<svg viewBox="0 0 60 64"><line class="vo" x1="5" y1="5" x2="30" y2="58"/><line class="vv" x1="55" y1="5" x2="30" y2="58"/><circle class="vr" cx="30" cy="58" r="5"/><circle class="vp" cx="30" cy="58" r="5.5"/></svg>`;
document.querySelectorAll('[data-wm]').forEach(el => {
  el.innerHTML = `<span class="wm ${el.dataset.wm === 'anim' ? 'anim' : ''}">CON${CONV_V}ERGENCE</span>`;
});

const params = new URLSearchParams(location.search);

// 2. Bandeau de cours
// Valeurs réelles : lancer « Lancer les cours en direct.bat », qui écrit obs/cours.js toutes les minutes.
// Sans ce script, on affiche ces valeurs de secours (exemples).
const COURS_SECOURS = [
  ["OR", "—", "+0,0 %"], ["S&P 500", "—", "+0,0 %"], ["BTC", "—", "+0,0 %"], ["SOL", "—", "+0,0 %"],
];
const isDown = v => /^[−-]/.test(String(v).trim());
const tkHTML = list => list.map(([n, p, v]) =>
  `<span class="tk"><b>${n}</b><span class="tp">${p}</span> <span class="tv ${isDown(v) ? 'dn' : 'up'}">${isDown(v) ? '▼' : '▲'} ${v}</span></span>`).join('');

function renderCours(data) {
  const list = data && data.ticker && data.ticker.length ? data.ticker : COURS_SECOURS;
  document.querySelectorAll('.ticker-track').forEach(track => {
    const spans = track.querySelectorAll('.tk');
    if (spans.length === list.length * 2) {
      // même structure : on met juste à jour les chiffres, sans faire sauter le défilement
      spans.forEach((sp, i) => {
        const [, p, v] = list[i % list.length];
        sp.querySelector('.tp').textContent = p;
        const tv = sp.querySelector('.tv');
        tv.className = 'tv ' + (isDown(v) ? 'dn' : 'up');
        tv.textContent = (isDown(v) ? '▼ ' : '▲ ') + v;
      });
    } else {
      track.innerHTML = tkHTML(list) + tkHTML(list);
    }
  });
  // Panneau « Cette semaine » (écran live)
  const panel = document.getElementById('semaine');
  if (panel && data && data.semaine && data.semaine.length) {
    panel.innerHTML = data.semaine.map(([n, v]) =>
      `<div class="row"><span>${n}</span><span class="${isDown(v) ? 'dn' : 'up'}">${v}</span></div>`).join('');
  }
  const maj = document.getElementById('maj');
  if (maj && data && data.maj) maj.textContent = 'MAJ ' + data.maj;
}

function chargerCours() {
  const s = document.createElement('script');
  s.src = 'cours.js?t=' + Date.now();          // relu à chaque fois, sans cache
  s.onload = () => { renderCours(window.COURS_LIVE); s.remove(); };
  s.onerror = () => { if (!window.COURS_LIVE) renderCours(null); s.remove(); };
  document.head.appendChild(s);
}
renderCours(null);
chargerCours();
setInterval(chargerCours, 60 * 1000);

// 3. Textes paramétrables : ?ep=03&cohost=…&nass=…  (voir chaque fichier)
document.querySelectorAll('[data-param]').forEach(el => {
  const v = params.get(el.dataset.param);
  if (v) el.textContent = v;
});
