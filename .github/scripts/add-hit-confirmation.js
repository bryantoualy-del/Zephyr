const fs=require('fs');
const p='index.html';
let s=fs.readFileSync(p,'utf8');

const css=`
/* hit-confirm-v1 */
.hit-modal{position:fixed;inset:0;z-index:120;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(2,4,7,.72);backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px)}
.hit-modal.show{display:flex}.hit-box{width:min(92vw,420px);border:1px solid #8d6d38;border-radius:18px;background:radial-gradient(circle at 50% 0,rgba(255,218,138,.13),transparent 42%),linear-gradient(180deg,#191c22,#0d1014);box-shadow:0 24px 70px rgba(0,0,0,.68),0 0 32px rgba(229,184,95,.12);padding:18px;text-align:center}.hit-kicker{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#c9ad76;font-weight:900}.hit-title{font-size:20px;font-weight:900;margin-top:5px;color:#fff2ca}.hit-roll{font-size:13px;color:#c9d0d8;margin-top:5px}.hit-question{font-size:14px;margin-top:13px;color:#f2f0eb}.hit-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}.hit-actions button{min-height:54px;border-radius:13px;font-weight:900}.hit-yes{border:1px solid #9b783d;background:linear-gradient(180deg,#6f5427,#3f2f17);color:#fff1bd}.hit-no{border:1px solid #6e4850;background:linear-gradient(180deg,#51242b,#30161b);color:#ffc0c5}
`;
if(!s.includes('/* hit-confirm-v1 */')) s=s.replace('</style>',css+'\n</style>');

const modal=`<div id="hitModal" class="hit-modal" aria-hidden="true"><div class="hit-box" role="dialog" aria-modal="true" aria-labelledby="hitTitle"><div class="hit-kicker">Résolution d’attaque</div><div class="hit-title" id="hitTitle">L’attaque touche ?</div><div class="hit-roll" id="hitRoll"></div><div class="hit-question">Le MJ confirme-t-il la touche ?</div><div class="hit-actions"><button id="hitYes" class="hit-yes" type="button">✓ Touché</button><button id="hitNo" class="hit-no" type="button">✕ Raté</button></div></div></div>`;
if(!s.includes('id="hitModal"')) s=s.replace('<div id="fxLayer" class="fx-layer"></div>','<div id="fxLayer" class="fx-layer"></div>\n'+modal);

const marker="function makeAttackRoll(base,label)";
if(!s.includes('function askHit(')){
  const ask=`function askHit(label,a){return new Promise(function(resolve){var m=$('hitModal'),t=$('hitTitle'),r=$('hitRoll'),y=$('hitYes'),n=$('hitNo');if(!m||!y||!n){resolve(true);return}t.textContent=label;r.textContent='Jet d’attaque : '+a.total+(a.nat===20?' • 20 naturel':'');m.classList.add('show');m.setAttribute('aria-hidden','false');function done(v){m.classList.remove('show');m.setAttribute('aria-hidden','true');y.onclick=null;n.onclick=null;resolve(v)}y.onclick=function(){done(true)};n.onclick=function(){done(false)}})}\n`;
  s=s.replace(marker,ask+marker);
}

s=s.replace(/function attack\(\)\{.*?\}function guided\(\)/s,`async function attack(){if(S.attackCount>=2){ribbon('Les 2 attaques ont déjà été utilisées');return}if(S.attackCount===0&&S.eco.a){ribbon('Action déjà utilisée ce tour');return}var a=makeAttackRoll(11,'Poings de paladin');if(!a)return;if(S.attackCount===0)S.eco.a=true;S.attackCount++;commitAttack(a);var crit=a.nat===20;var hit=await askHit('Poings de paladin',a);if(!hit){S.lastHit=null;addLog('Poings • attaque '+S.attackCount+'/2','RATÉ • '+attackText(a,11),'attack');return}var d=roll(crit?2:1,8),total=d.sum+7;S.dmg+=total;S.lastHit={turn:S.turn,index:S.attackCount,crit:crit,divineUsed:false};impactFx();var extra=triggerSpellSmite(crit);addLog('Poings • attaque '+S.attackCount+'/2',(crit?'CRITIQUE • ':'')+attackText(a,11)+' • '+d.a.join('+')+' +7 = '+total+' contondants'+(extra?' • châtiment de sort +'+extra:''),crit?'crit':'attack')}function guided()`);

s=s.replace(/function silverArrow\(mode\)\{.*?\}function presence\(\)/s,`async function silverArrow(mode){if(S.arrows<=0){ribbon('Plus de charge');return}if(S.eco.a){ribbon('Action déjà utilisée');return}var slot=Number($('arrowSlot').value||0);if(slot>0&&S.slots[slot]<=0){ribbon('Plus de slot N'+slot);return}var a=makeAttackRoll(8,'Flèche de la Flamme d’Argent');if(!a)return;S.eco.a=true;if(slot>0)S.slots[slot]--;S.arrows--;commitAttack(a);var hit=await askHit(mode==='strike'?'Flèche d’Argent — infliger & se soigner':'Flèche d’Argent — soigner un allié',a);arrowFx(mode);if(!hit){addLog(mode==='strike'?'Flèche d’Argent':'Flèche sacrificielle','RATÉ • '+attackText(a,8)+' • charge'+(slot?(' + slot N'+slot):'')+' consommée','attack');return}var r=roll(2+slot,6);if(mode==='strike'){S.dmg+=r.sum;S.hp=Math.min(S.maxHp,S.hp+r.sum);addLog('Flèche d’Argent',attackText(a,8)+' • '+r.sum+' radiants • Zéphyr récupère '+r.sum+' PV','attack')}else{S.hp=Math.max(0,S.hp-r.sum);addLog('Flèche sacrificielle',attackText(a,8)+' • Zéphyr subit '+r.sum+' • cible récupère '+r.sum+' PV','attack')}}function presence()`);

if(!s.includes('async function attack()')) throw new Error('attack patch failed');
if(!s.includes('async function silverArrow(mode)')) throw new Error('arrow patch failed');
if(!s.includes('function askHit(')) throw new Error('askHit patch failed');
fs.writeFileSync(p,s);
