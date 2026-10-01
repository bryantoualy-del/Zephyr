(()=>{'use strict';
const mq=window.matchMedia('(min-width:700px) and (max-width:1100px)');
const nav=document.querySelector('.nav');
const app=document.querySelector('.app');
const hud=document.querySelector('.hud');
if(!nav||!app||!hud)return;
const originalNext=app.nextSibling;
function measure(){
  const hh=Math.ceil(hud.getBoundingClientRect().height);
  const nh=Math.ceil(nav.getBoundingClientRect().height);
  document.documentElement.style.setProperty('--zephyr-hud-h',hh+'px');
  document.documentElement.style.setProperty('--zephyr-nav-h',nh+'px');
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
    document.documentElement.style.removeProperty('--zephyr-hud-h');
    document.documentElement.style.removeProperty('--zephyr-nav-h');
  }
}
mq.addEventListener?.('change',apply);
window.addEventListener('resize',()=>{if(mq.matches)requestAnimationFrame(measure)},{passive:true});
apply();
})();