(()=>{'use strict';
const mq=window.matchMedia('(min-width:768px) and (max-width:1366px) and (min-height:600px) and (orientation:landscape)');
const nav=document.querySelector('.nav');
const app=document.querySelector('.app');
const hud=document.querySelector('.hud');
if(!nav||!app||!hud)return;
const originalNext=app.nextSibling;
function measure(){
  const turnbar=document.querySelector('#cc-turnbar-standard');
  const th=Math.ceil(turnbar?.getBoundingClientRect().height||56);
  const nh=Math.ceil(nav.getBoundingClientRect().height||48);
  document.documentElement.style.setProperty('--zephyr-turnbar-h',th+'px');
  document.documentElement.style.setProperty('--zephyr-nav-h',nh+'px');
}
function scheduleMeasure(){
  scheduleMeasure();
  setTimeout(measure,180);
  setTimeout(measure,700);
}
function apply(){
  if(mq.matches){
    if(nav.parentElement!==app)hud.insertAdjacentElement('afterend',nav);
    requestAnimationFrame(measure);
  }else{
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