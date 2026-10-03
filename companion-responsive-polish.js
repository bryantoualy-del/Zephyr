(()=>{'use strict';
const mq=window.matchMedia('(min-width:768px) and (max-width:1366px) and (min-height:600px) and (orientation:landscape)');
const nav=document.querySelector('.nav');
const app=document.querySelector('.app');
const hud=document.querySelector('.hud');
const combat=document.querySelector('#combat');
const combatHeading=combat?.querySelector('.section');
const attackCard=document.querySelector('#attackCard');
const spellSmiteCard=document.querySelector('#spellSmiteCard');
const arrowCard=document.querySelector('#combat .arrow-card');
const divineSmiteCard=attackCard?.nextElementSibling;
if(!nav||!app||!hud)return;
const originalNext=app.nextSibling;

function buildCombatColumns(){
  if(!combat||!combatHeading||!attackCard||!spellSmiteCard||!arrowCard||!divineSmiteCard)return;
  if(document.getElementById('zephyr-combat-main-col'))return;
  const main=document.createElement('div');
  const side=document.createElement('div');
  main.id='zephyr-combat-main-col';
  side.id='zephyr-combat-side-col';
  main.className='zephyr-combat-column zephyr-combat-main-col';
  side.className='zephyr-combat-column zephyr-combat-side-col';
  combatHeading.after(main);
  main.after(side);
  main.append(attackCard,spellSmiteCard);
  side.append(divineSmiteCard,arrowCard);
}
function restoreCombatColumns(){
  const main=document.getElementById('zephyr-combat-main-col');
  const side=document.getElementById('zephyr-combat-side-col');
  if(!main||!side||!combatHeading)return;
  combatHeading.after(attackCard);
  attackCard.after(divineSmiteCard);
  divineSmiteCard.after(spellSmiteCard);
  spellSmiteCard.after(arrowCard);
  main.remove();
  side.remove();
}
function measure(){
  const turnbar=document.querySelector('#cc-turnbar-standard');
  const th=Math.ceil(turnbar?.getBoundingClientRect().height||56);
  const nh=Math.ceil(nav.getBoundingClientRect().height||48);
  document.documentElement.style.setProperty('--zephyr-turnbar-h',th+'px');
  document.documentElement.style.setProperty('--zephyr-nav-h',nh+'px');
}
function scheduleMeasure(){
  requestAnimationFrame(measure);
  setTimeout(measure,180);
  setTimeout(measure,700);
}
function apply(){
  if(mq.matches){
    if(nav.parentElement!==app)hud.insertAdjacentElement('afterend',nav);
    buildCombatColumns();
    scheduleMeasure();
  }else{
    restoreCombatColumns();
    if(nav.parentElement===app){
      if(originalNext&&originalNext.parentNode===app.parentNode)app.parentNode.insertBefore(nav,originalNext);
      else app.insertAdjacentElement('afterend',nav);
    }
    document.documentElement.style.removeProperty('--zephyr-turnbar-h');
    document.documentElement.style.removeProperty('--zephyr-nav-h');
  }
}
mq.addEventListener?.('change',apply);
window.addEventListener('resize',()=>{if(mq.matches)scheduleMeasure()},{passive:true});
new MutationObserver(()=>{if(mq.matches)scheduleMeasure()}).observe(app,{childList:true});
apply();
})();