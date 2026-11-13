(()=>{
  'use strict';
  const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
  const layer=document.getElementById('fxLayer');
  let current;
  let cleanupTimer;
  let shake;

  function clear(){
    clearTimeout(cleanupTimer);
    current?.remove();
    shake?.cancel();
    current=null;
    shake=null;
  }

  function play(grow){
    clear();
    const card=document.getElementById('titanCard');
    if(!card.getClientRects().length)return;
    const bounds=card.getBoundingClientRect();
    const fx=document.createElement('div');
    fx.className='titan-fx '+(grow?'titan-fx-grow':'titan-fx-release');
    fx.style.left=Math.max(0,Math.min(innerWidth,bounds.left+bounds.width/2))+'px';
    fx.style.top=Math.max(0,Math.min(innerHeight,bounds.top+Math.min(85,bounds.height/2)))+'px';
    for(const kind of ['flash','halo','dust','fissures']){
      const effect=document.createElement('span');
      effect.className='titan-fx-'+kind;
      fx.append(effect);
    }
    if(!reducedMotion.matches){
      const count=grow?12:5;
      for(let i=0;i<count;i++){
        const fragment=document.createElement('i');
        const angle=i*2.4;
        const distance=48+i*8;
        fragment.style.setProperty('--x',Math.round(Math.cos(angle)*distance)+'px');
        fragment.style.setProperty('--y',Math.round(Math.sin(angle)*distance*.7)+'px');
        fragment.style.setProperty('--spin',(i*37-85)+'deg');
        fragment.style.setProperty('--delay',(i%4)*30+'ms');
        fx.append(fragment);
      }
      if(grow){
        shake=card.animate([
          {translate:'0 0'},{translate:'1px -1px'},{translate:'-2px 1px'},
          {translate:'1px 0'},{translate:'0 0'}
        ],{duration:180,easing:'ease-out'});
      }
    }
    layer.append(fx);
    current=fx;
    cleanupTimer=setTimeout(clear,reducedMotion.matches?180:grow?1200:620);
  }

  reducedMotion.addEventListener('change',clear);
  window.ZephyrTitanFx={play};
})();
