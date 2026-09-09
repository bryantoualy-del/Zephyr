from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'zephyr-fx-v1' in s:
    raise SystemExit('already patched')

s=s.replace('pointer-events:none}#ribbon.show','pointer-events:auto;cursor:pointer}#ribbon.show')
s=s.replace("window._rt=setTimeout(function(){r.classList.remove('show')},2200)","window._rt=setTimeout(function(){r.classList.remove('show')},7000)")

css='''\n/* zephyr-fx-v1 */\n.fx-layer{position:fixed;inset:0;z-index:95;pointer-events:none;overflow:hidden}.fx-burst{position:absolute;left:50%;top:44%;width:22px;height:22px;border-radius:50%;transform:translate(-50%,-50%);animation:fxBurst .9s ease-out forwards;box-shadow:0 0 22px currentColor,0 0 52px currentColor}.fx-burst:before,.fx-burst:after{content:"";position:absolute;inset:-42px;border:2px solid currentColor;border-radius:50%;animation:fxRing .9s ease-out forwards}.fx-burst:after{inset:-78px;opacity:.45;animation-delay:.08s}.fx-fire{color:#ff6b2c}.fx-thunder{color:#65c7ff}.fx-wrath{color:#c07cff}.fx-radiant{color:#ffe08a}.fx-blind{color:#fffbd7}.fx-ice{color:#8ddcff}.fx-green{color:#7ee0a5}.fx-shadow{color:#a889ff}.fx-white{color:#e9f3ff}@keyframes fxBurst{0%{opacity:0;transform:translate(-50%,-50%) scale(.15)}18%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(9)}}@keyframes fxRing{0%{opacity:.9;transform:scale(.1)}100%{opacity:0;transform:scale(2.8)}}\n.smite-spell-card.armed{animation:armedPulse 1.35s ease-in-out infinite alternate}.smite-spell-card.armed-searing{border-color:#ff6b2c;box-shadow:0 0 24px rgba(255,107,44,.25)}.smite-spell-card.armed-thunderous{border-color:#65c7ff;box-shadow:0 0 24px rgba(101,199,255,.24)}.smite-spell-card.armed-wrathful{border-color:#c07cff;box-shadow:0 0 24px rgba(192,124,255,.24)}.smite-spell-card.armed-branding{border-color:#ffe08a;box-shadow:0 0 24px rgba(255,224,138,.24)}.smite-spell-card.armed-blinding{border-color:#fffbd7;box-shadow:0 0 30px rgba(255,251,215,.30)}.smite-state.searing{color:#ffb18c;border-color:#ff6b2c}.smite-state.thunderous{color:#a9e4ff;border-color:#65c7ff}.smite-state.wrathful{color:#dab7ff;border-color:#c07cff}.smite-state.branding{color:#ffe7a8;border-color:#ffe08a}.smite-state.blinding{color:#fffde8;border-color:#fffbd7}@keyframes armedPulse{from{filter:brightness(.98)}to{filter:brightness(1.14)}}.journal-actions{display:flex;gap:6px}.journal-actions .btn{min-height:38px;padding:7px 10px;font-size:11px}\n'''
s=s.replace('@media(max-width:390px)',css+'@media(max-width:390px)')
s=s.replace('<body>\n<div id="ribbon"','<body>\n<div id="fxLayer" class="fx-layer"></div>\n<div id="ribbon"')
s=s.replace('<div class="card smite-spell-card"><div class="title">🔥 Châtiments de sort</div>','<div class="card smite-spell-card" id="spellSmiteCard"><div class="title">🔥 Châtiments de sort</div>')

old='<section class="screen" id="journal"><div class="journal-head"><div><div class="journal-title">Chronique de la Flamme</div><div class="journal-sub">Les coups, châtiments, pouvoirs et ressources de Zéphyr, tour après tour.</div></div><button class="btn silver" id="clearLog" type="button" style="min-height:38px">Effacer</button></div><div class="journal-feed" id="log"></div></section>'
new='<section class="screen" id="journal"><div class="journal-head"><div><div class="journal-title">Chronique de la Flamme</div><div class="journal-sub">Les coups, châtiments, pouvoirs et ressources de Zéphyr, tour après tour.</div></div><div class="journal-actions"><button class="btn gold" id="undoLog" type="button">↶ Annuler</button><button class="btn silver" id="clearLog" type="button">Effacer</button></div></div><div class="journal-feed" id="log"></div></section>'
if old not in s: raise SystemExit('journal block not found')
s=s.replace(old,new)

state="var S={hp:84,maxHp:84,turn:1,dmg:0,attackCount:0,rollMode:'auto',guidedReady:false,eco:{a:false,b:false,r:false,m:false},slots:{1:4,2:3,3:2},maxSlots:{1:4,2:3,3:2},lay:50,sense:5,channel:1,decree:1,anchor:1,arrows:3,mark:false,conc:'',spellSmite:null,lastHit:null,log:[]};"
if state not in s: raise SystemExit('state line not found')
s=s.replace(state,state+'\nvar undoStack=[];')

helpers='''function snapshotForUndo(){try{var raw=localStorage.getItem(key);if(raw){undoStack.push(raw);if(undoStack.length>30)undoStack.shift()}}catch(e){}}\nfunction undoLast(){if(!undoStack.length){ribbon('Rien à annuler');return}try{var x=JSON.parse(undoStack.pop());if(!x)return;Object.assign(S,x);S.eco=Object.assign({a:false,b:false,r:false,m:false},x.eco||{});S.slots=Object.assign({1:4,2:3,3:2},x.slots||{});render();ribbon('Dernière action annulée')}catch(e){ribbon('Impossible d’annuler')}}\nfunction fxClass(name){var n=String(name||'').toLowerCase();if(n.indexOf('calcin')>=0||n.indexOf('infern')>=0)return'fx-fire';if(n.indexOf('tonit')>=0)return'fx-thunder';if(n.indexOf('courrou')>=0||n.indexOf('peur')>=0||n.indexOf('maléd')>=0)return'fx-wrath';if(n.indexOf('aveugl')>=0)return'fx-blind';if(n.indexOf('révél')>=0||n.indexOf('bénéd')>=0||n.indexOf('foi')>=0||n.indexOf('reviv')>=0||n.indexOf('aide')>=0||n.indexOf('vitalité')>=0||n.indexOf('spirituelle')>=0)return'fx-radiant';if(n.indexOf('agathys')>=0)return'fx-ice';if(n.indexOf('chasseur')>=0)return'fx-green';if(n.indexOf('brumeuse')>=0)return'fx-shadow';return'fx-white'}\nfunction spellFx(name,strong){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-burst '+fxClass(name);if(strong)b.style.animationDuration='.72s';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1100)}\n'''
s=s.replace('function addLog(title,body,type){',helpers+'function addLog(title,body,type){snapshotForUndo();')

s=s.replace("addLog(def.name+' déclenché'","spellFx(def.name,true);addLog(def.name+' déclenché'")
s=s.replace("S.conc=def.name;addLog(def.name+' armé'","S.conc=def.name;spellFx(def.name,false);addLog(def.name+' armé'")
s=s.replace("S.lastHit.divineUsed=true;addLog('Châtiment divin N'+l","S.lastHit.divineUsed=true;spellFx('Châtiment révélateur',true);addLog('Châtiment divin N'+l")
s=s.replace("S.dmg+=r.sum;addLog('Représailles infernales N'+l","S.dmg+=r.sum;spellFx('Représailles infernales',true);addLog('Représailles infernales N'+l")
s=s.replace("if(conc){S.spellSmite=null;S.conc=name}addLog(name,","if(conc){S.spellSmite=null;S.conc=name}spellFx(name,false);addLog(name,")

old_render="else{st.textContent='Aucun châtiment de sort armé.';st.classList.remove('on')}}var lh=$('lastHitState');"
new_render="else{st.textContent='Aucun châtiment de sort armé.';st.classList.remove('on')}var card=$('spellSmiteCard');if(card){card.classList.remove('armed','armed-searing','armed-thunderous','armed-wrathful','armed-branding','armed-blinding');st.classList.remove('searing','thunderous','wrathful','branding','blinding');if(S.spellSmite){card.classList.add('armed','armed-'+S.spellSmite.key);st.classList.add(S.spellSmite.key)}}}var lh=$('lastHitState');"
if old_render not in s: raise SystemExit('render block not found')
s=s.replace(old_render,new_render)

old_bind="$('clearLog').addEventListener('click',function(){S.log=[];render()});$('ribbon').addEventListener('click',function(){$('ribbon').classList.remove('show')})"
new_bind="$('undoLog').addEventListener('click',undoLast);$('clearLog').addEventListener('click',function(){snapshotForUndo();S.log=[];render()});$('ribbon').addEventListener('click',function(){clearTimeout(window._rt);$('ribbon').classList.remove('show')})"
if old_bind not in s: raise SystemExit('bind block not found')
s=s.replace(old_bind,new_bind)

p.write_text(s,encoding='utf-8')
print('patched',len(s))
