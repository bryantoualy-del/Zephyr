/* RPG Connect icon registry v1.
   Asset-first: if a future pack provides a URL, register it with RPGConnectIcons.set().
   Until then, compact vector fallbacks keep the targeting UI functional. */
(()=>{'use strict';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const creatureTypes=['aberration','beast','celestial','construct','dragon','elemental','fey','fiend','giant','humanoid','monstrosity','ooze','plant','undead'];
const labels={aberration:'Aberration',beast:'Bête',celestial:'Céleste',construct:'Artificiel',dragon:'Dragon',elemental:'Élémentaire',fey:'Fée',fiend:'Fiélon',giant:'Géant',humanoid:'Humanoïde',monstrosity:'Monstruosité',ooze:'Vase',plant:'Plante',undead:'Mort-vivant',unknown:'Inconnu'};
const marks={aberration:'AB',beast:'BE',celestial:'CE',construct:'CO',dragon:'DR',elemental:'EL',fey:'FE',fiend:'FI',giant:'GI',humanoid:'HU',monstrosity:'MO',ooze:'OO',plant:'PL',undead:'MV',unknown:'?'};
const urls=new Map();
function svgData(mark){
  const safe=esc(mark).slice(0,3);
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="#111b28" stroke="#c7d5df" stroke-width="3"/><path d="M32 7l5 8 9 2-4 8 5 7-8 5-1 10H26l-1-10-8-5 5-7-4-8 9-2z" fill="none" stroke="#7f9caf" stroke-width="2" opacity=".65"/><text x="32" y="38" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16" font-weight="800" fill="#f3f7fa">${safe}</text></svg>`;
  return 'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);
}
const api={
  creatureTypes:[...creatureTypes],
  label:type=>labels[String(type||'').toLowerCase()]||labels.unknown,
  creature:type=>{const key=String(type||'unknown').toLowerCase();return urls.get('creature:'+key)||svgData(marks[key]||marks.unknown)},
  ui:key=>urls.get('ui:'+String(key||''))||null,
  classIcon:key=>urls.get('class:'+String(key||''))||null,
  set:(kind,key,url)=>{if(!url)return false;urls.set(String(kind)+':'+String(key).toLowerCase(),String(url));return true}
};
window.RPGConnectIcons=Object.freeze(api);
})();