(()=>{
  'use strict';
  const landscape = window.matchMedia('(min-width:768px) and (max-width:1366px) and (min-height:600px) and (orientation:landscape)');
  const nav = document.querySelector('.nav');
  const app = document.querySelector('.app');
  const hud = app.querySelector('.hud');
  const smite = document.getElementById('divineSmiteCard');
  const smiteHome = document.createComment('Châtiment portrait');
  smite.before(smiteHome);
  const stack = document.createElement('div');
  stack.className = 'zephyr-tablet-navigation';
  // Keep the original insertion points so rotation restores the phone layout.
  const navHome = document.createComment('Navigation portrait');
  nav.before(navHome);

  function apply(){
    const turnbar = document.getElementById('cc-turnbar-standard');
    if(landscape.matches){
      app.querySelector('.content').before(stack);
      if(turnbar) stack.append(turnbar);
      stack.append(nav);
      document.querySelector('#combat > .arrow-card').after(smite);
    }else{
      if(turnbar && stack.contains(turnbar)) hud.after(turnbar);
      navHome.after(nav);
      smiteHome.after(smite);
      stack.remove();
    }
  }

  landscape.addEventListener('change',apply);
  // The shared turnbar registers its own DOMContentLoaded handler first.
  document.addEventListener('DOMContentLoaded',apply);
})();
