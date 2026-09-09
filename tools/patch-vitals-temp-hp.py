from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'MISSING {label}')
    s=s.replace(old,new,1)

# CSS
rep(".hp b{color:#ff9c71}.turnline{", ".hp b{color:#ff9c71}.temp b{color:#9fe7ff}.vitalsbar{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:5px}.vitalctl{display:grid;grid-template-columns:auto 1fr auto;gap:4px;align-items:center;border:1px solid #343c47;background:#0d1116;border-radius:10px;padding:4px}.vitalctl span{font-size:9px;color:var(--muted);font-weight:800;text-align:center}.vitalctl button{min-width:34px;height:28px;border:1px solid #505b68;border-radius:8px;background:#171d24;color:#fff;font-weight:900}.vitalctl.tempctl{border-color:#355b6e}.vitalctl.tempctl button{border-color:#4b7b91;color:#b9ecff}.turnline{", 'vitals css')

# HUD row + controls
old="<div class=\"hudrow\"><div class=\"chip hp\"><small>PV</small><b id=\"hpTop\">84/84</b></div><div class=\"chip\"><small>CA</small><b>21</b></div><div class=\"chip\"><small>Tour</small><b id=\"turnTop\">1</b></div><div class=\"chip\"><small>Dégâts</small><b id=\"dmgTop\">0</b></div></div>"
new="<div class=\"hudrow\"><div class=\"chip hp\"><small>PV</small><b id=\"hpTop\">84/84</b></div><div class=\"chip temp\"><small>PV temp</small><b id=\"tempHpTop\">0</b></div><div class=\"chip\"><small>CA</small><b>21</b></div><div class=\"chip\"><small>Tour</small><b id=\"turnTop\">1</b></div></div><div class=\"vitalsbar\"><div class=\"vitalctl\"><button id=\"hpMinus\" type=\"button\">−</button><span>PV <b id=\"dmgTop\">0</b> dmg/tour</span><button id=\"hpPlus\" type=\"button\">+</button></div><div class=\"vitalctl tempctl\"><button id=\"tempMinus\" type=\"button\">−</button><span>PV temporaires</span><button id=\"tempPlus\" type=\"button\">+</button></div></div>"
rep(old,new,'hud vitals')

# State
rep("var S={hp:84,maxHp:84,turn:1,", "var S={hp:84,maxHp:84,tempHp:0,turn:1,", 'state tempHp')

# Load migration/default
rep("if(x.slots)for(var sl in x.slots)S.slots[sl]=x.slots[sl]}catch(e){}}", "if(x.slots)for(var sl in x.slots)S.slots[sl]=x.slots[sl];if(!Number.isFinite(S.tempHp))S.tempHp=0}catch(e){}}", 'load tempHp')

# Helpers before askHit
needle="function askHit(label,a){return new Promise(function(resolve){"
helpers="""function applyDamage(n,label){n=Math.max(0,Math.floor(Number(n)||0));if(!n)return{temp:0,hp:0};var beforeTemp=S.tempHp||0;var absorbed=Math.min(beforeTemp,n);S.tempHp=beforeTemp-absorbed;var remain=n-absorbed;var hpLost=Math.min(S.hp,remain);S.hp=Math.max(0,S.hp-remain);return{temp:absorbed,hp:hpLost}}
function healSelf(n){n=Math.max(0,Math.floor(Number(n)||0));var before=S.hp;S.hp=Math.min(S.maxHp,S.hp+n);return S.hp-before}
function setTempHp(n){n=Math.max(0,Math.floor(Number(n)||0));var old=S.tempHp||0;if(n>old){S.tempHp=n;return n-old}return 0}
function hpAdjust(mode){var label=mode==='damage'?'Dégâts subis':'PV récupérés';var raw=prompt(mode==='damage'?'Combien de dégâts Zéphyr subit-il ?':'Combien de PV Zéphyr récupère-t-il ?','5');if(raw===null)return;var n=Math.floor(Number(raw));if(!Number.isFinite(n)||n<=0){ribbon('Valeur invalide');return}if(mode==='damage'){var d=applyDamage(n);addLog('PV modifiés',n+' dégâts • '+d.temp+' absorbés par PV temporaires • '+d.hp+' retirés aux PV','resource')}else{var h=healSelf(n);addLog('PV modifiés','+'+h+' PV récupérés','resource')}}
function tempAdjust(mode){var raw=prompt(mode==='add'?'Combien de PV temporaires ajouter/remplacer ?':'Combien de PV temporaires retirer ?','5');if(raw===null)return;var n=Math.floor(Number(raw));if(!Number.isFinite(n)||n<=0){ribbon('Valeur invalide');return}if(mode==='add'){var old=S.tempHp||0;S.tempHp=n;addLog('PV temporaires','Valeur fixée à '+n+' (anciennement '+old+').','resource')}else{var lost=Math.min(S.tempHp||0,n);S.tempHp=Math.max(0,(S.tempHp||0)-n);addLog('PV temporaires','-'+lost+' PV temporaires.','resource')}}
"""
rep(needle,helpers+needle,'hp helpers')

# Silver arrow self damage should use temp hp
rep("else{S.hp=Math.max(0,S.hp-r.sum);addLog('Flèche sacrificielle'", "else{var selfDmg=applyDamage(r.sum);addLog('Flèche sacrificielle'", 'arrow damage')
rep("attackText(a,8)+' • Zéphyr subit '+r.sum+' • cible récupère '+r.sum+' PV'", "attackText(a,8)+' • Zéphyr subit '+r.sum+' ('+selfDmg.temp+' PV temp absorbés) • cible récupère '+r.sum+' PV'", 'arrow log')

# Special case Agathys in cast
old="function hellish(){var l=Number($('hellishLevel').value);if(!useEco('r','Réaction'))return;if(!spendSlot(l)){S.eco.r=false;render();return}var r=roll(l+1,10);S.dmg+=r.sum;spellFx('Représailles infernales',true);addLog('Représailles infernales N'+l,(l+1)+'d10 feu = '+r.sum+' • DEX DD16 moitié.','spell')}function cast(name,l,eco,conc){if(!spendSlot(l))return;if(eco&&!useEco(eco,eco==='a'?'Action':'Action bonus')){S.slots[l]++;return}if(conc){S.spellSmite=null;S.conc=name}spellFx(name,false);addLog(name,'Slot N'+l+' dépensé'+(conc?' • concentration':''),'spell')}"
new="function hellish(){var l=Number($('hellishLevel').value);if(!useEco('r','Réaction'))return;if(!spendSlot(l)){S.eco.r=false;render();return}var r=roll(l+1,10);S.dmg+=r.sum;spellFx('Représailles infernales',true);addLog('Représailles infernales N'+l,(l+1)+'d10 feu = '+r.sum+' • DEX DD16 moitié.','spell')}function cast(name,l,eco,conc){if(!spendSlot(l))return;if(eco&&!useEco(eco,eco==='a'?'Action':'Action bonus')){S.slots[l]++;return}if(conc){S.spellSmite=null;S.conc=name}spellFx(name,false);var extra='';if(name==='Armure d’Agathys'){var gain=setTempHp(5*l);extra=' • PV temp : '+S.tempHp+(gain?(' (+'+gain+')'):' (valeur actuelle conservée)')}addLog(name,'Slot N'+l+' dépensé'+(conc?' • concentration':'')+extra,'spell')}"
rep(old,new,'Agathys cast')

# Long rest clears temp HP
rep("function longRest(){S.hp=84;S.maxHp=84;S.slots=", "function longRest(){S.hp=84;S.maxHp=84;S.tempHp=0;S.slots=", 'long rest temp')

# Render temp
rep("function render(){if($('hpTop'))$('hpTop').textContent=S.hp+'/'+S.maxHp;if($('turnTop'))", "function render(){if($('hpTop'))$('hpTop').textContent=S.hp+'/'+S.maxHp;if($('tempHpTop'))$('tempHpTop').textContent=S.tempHp||0;if($('turnTop'))", 'render temp')

# Bind buttons
rep("$('rollModeBtn').addEventListener('click',function(){S.rollMode=S.rollMode==='auto'?'manual':'auto';render()});", "$('rollModeBtn').addEventListener('click',function(){S.rollMode=S.rollMode==='auto'?'manual':'auto';render()});$('hpMinus').addEventListener('click',function(){hpAdjust('damage')});$('hpPlus').addEventListener('click',function(){hpAdjust('heal')});$('tempMinus').addEventListener('click',function(){tempAdjust('remove')});$('tempPlus').addEventListener('click',function(){tempAdjust('add')});", 'bind vitals')

p.write_text(s,encoding='utf-8')
print('patched',len(s))
