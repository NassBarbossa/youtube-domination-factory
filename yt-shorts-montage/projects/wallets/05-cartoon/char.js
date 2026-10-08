// Personnage cartoon vectoriel du punk @punk6995 (et variantes : foule grise, garde).
// Repère local : pieds en (0,0), y négatif vers le haut. Membres = groupes animables (rotation autour de l'articulation).
window.CHAR = (() => {
  const K = '#0B0B0B';
  const PUNK = { skin: '#E2BA84', skinS: '#C99A62', hair: '#E8C089', hairS: '#9C7748', jacket: '#4F6C7B', jacketS: '#3B5463', collar: '#F3D6A8',
    belt: '#DBB17F', pants: '#2E3236', shoe: '#DBB17F', lens: '#EDE6D6', pupil: '#3B4048', gold: '#F2C230', vape: '#6D6A64', tip: '#2D5BFF' };
  const GREY = { skin: '#A5A29A', skinS: '#8A877F', hair: '#7E7B74', hairS: '#5F5C56', jacket: '#5A5955', jacketS: '#4A4945', collar: '#8A877F',
    belt: '#6D6A64', pants: '#3B3A37', shoe: '#6D6A64', lens: '#8A877F', pupil: '#2C2C2A', gold: '#8A877F', vape: '#6D6A64', tip: '#6D6A64' };

  function make(id, opt = {}) {
    const c = Object.assign({}, opt.grey ? GREY : PUNK, opt.colors || {});
    const S = 'stroke="' + K + '" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"';
    const leg = (n, sh) => `<g id="${id}-${n}"><rect x="-19" y="0" width="38" height="146" rx="19" fill="${sh ? '#222528' : c.pants}" ${S}/>
      <path d="M -22 132 Q -24 162 6 164 L 40 164 Q 52 162 48 148 Q 44 134 22 132 Z" fill="${c.shoe}" ${S}/></g>`;
    const arm = (n, sh) => `<g id="${id}-${n}"><rect x="-16" y="-6" width="32" height="132" rx="16" fill="${sh ? c.jacketS : c.jacket}" ${S}/>
      <circle cx="0" cy="134" r="19" fill="${c.skin}" ${S}/></g>`;
    const head = `<g id="${id}-head">
      <rect x="-24" y="-4" width="50" height="34" fill="${c.skinS}" ${S}/>
      <path d="M -74 -8 L -78 -168 Q -78 -196 -50 -196 L 64 -196 Q 88 -196 88 -172 L 88 -122 L 102 -100 Q 106 -86 92 -82 L 84 -81 L 84 -42 Q 84 -24 66 -22 L 32 -20 L 32 0 L -60 0 Q -74 0 -74 -8 Z" fill="${c.skin}" ${S}/>
      <path d="M 32 -20 L 32 0 L 10 0 L 10 -18 Z" fill="${c.skinS}"/>
      ${opt.helmet ? `<path d="M -90 -150 Q -90 -262 6 -262 Q 102 -262 102 -150 Z" fill="#9C7748" ${S}/><rect x="-96" y="-160" width="204" height="22" rx="8" fill="#DBB17F" ${S}/>` :
      `<path d="M -84 -164 L -88 -206 L -66 -240 L -50 -206 L -36 -250 L -18 -208 L 0 -256 L 18 -210 L 36 -250 L 48 -208 L 66 -244 L 74 -206 L 96 -226 L 94 -164 Z" fill="${c.hair}" ${S}/>
      <path d="M -50 -206 L -46 -176 M -18 -208 L -12 -178 M 18 -210 L 20 -176 M 48 -208 L 52 -178" stroke="${c.hairS}" stroke-width="7" stroke-linecap="round"/>
      <rect x="-84" y="-180" width="180" height="20" rx="6" fill="${K}"/>`}
      <g id="${id}-glasses"><rect x="-30" y="-158" width="50" height="38" rx="9" fill="${c.lens}" ${S}/><rect x="32" y="-158" width="50" height="38" rx="9" fill="${c.lens}" ${S}/>
        <path d="M 20 -142 L 32 -142" ${S}/><g id="${id}-pupils"><circle cx="2" cy="-139" r="7" fill="${c.pupil}"/><circle cx="62" cy="-139" r="7" fill="${c.pupil}"/></g></g>
      <ellipse cx="-72" cy="-108" rx="15" ry="24" fill="${c.skin}" ${S}/>
      <circle cx="-78" cy="-80" r="9" fill="${c.gold}" stroke="${K}" stroke-width="4"/>
      <rect x="46" y="-70" width="24" height="9" rx="4" fill="${K}"/>
      ${opt.grey ? '' : `<g id="${id}-vape"><rect x="62" y="-72" width="96" height="16" rx="6" fill="${c.vape}" ${S}/><rect x="142" y="-72" width="16" height="16" rx="4" fill="${c.tip}"/>
        <g id="${id}-smoke" opacity="0"><circle cx="178" cy="-82" r="10" fill="#F4EFE7" opacity=".7"/><circle cx="196" cy="-100" r="14" fill="#F4EFE7" opacity=".5"/><circle cx="212" cy="-124" r="18" fill="#F4EFE7" opacity=".3"/></g></g>`}
    </g>`;
    const torso = `<g id="${id}-torso">
      <path d="M -56 -300 Q -64 -300 -66 -288 L -74 -168 Q -74 -146 -54 -146 L 54 -146 Q 74 -146 74 -168 L 66 -288 Q 64 -300 56 -300 Z" fill="${c.jacket}" ${S}/>
      <path d="M -24 -300 L 0 -246 L 24 -300 Z" fill="${c.collar}" ${S}/>
      <rect x="-74" y="-176" width="148" height="24" rx="6" fill="${c.belt}" ${S}/>
      <rect x="-10" y="-174" width="20" height="20" rx="4" fill="${K}"/>
      ${opt.badge ? '' : ''}</g>`;
    return `<svg class="ch" id="${id}" width="10" height="10" viewBox="0 0 10 10" style="overflow:visible">
      <g id="${id}-root" transform="scale(${opt.scale || 0.78})"><g id="${id}-body">
        ${arm('armB', 1)}${leg('legB', 1)}${leg('legF')}${torso}${head}${arm('armF')}
      </g></g></svg>`;
  }

  // place les articulations (à appeler une fois le SVG dans le DOM)
  function rig(id) {
    const q = (n) => document.getElementById(id + '-' + n);
    gsap.set(q('legB'), { x: -16, y: -150, transformOrigin: '50% 0%' });
    gsap.set(q('legF'), { x: 18, y: -150, transformOrigin: '50% 0%' });
    gsap.set(q('armB'), { x: -46, y: -286, transformOrigin: '50% 4%' });
    gsap.set(q('armF'), { x: 44, y: -286, transformOrigin: '50% 4%' });
    gsap.set(q('head'), { x: 0, y: -312, transformOrigin: '30% 100%' });
    gsap.set(q('body'), { transformOrigin: '50% 100%' });
  }
  return { make, rig };
})();
