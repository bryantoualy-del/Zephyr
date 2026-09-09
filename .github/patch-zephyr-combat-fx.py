from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css_old=""".journal-actions{display:flex;gap:6px}.journal-actions .btn{min-height:38px;padding:7px 10px;font-size:11px}\n"""
css_new=""".journal-actions{display:flex;gap:6px}.journal-actions .btn{min-height:38px;padding:7px 10px;font-size:11px}\n/* zephyr-combat-fx-v2 */\nbody.screen-shake{animation:screenShake .32s cubic-bezier(.36,.07,.19,.97) both}\n@keyframes screenShake{0%,100%{transform:translate3d(0,0,0)}15%{transform:translate3d(-5px,2px,0)}30%{transform:translate3d(6px,-3px,0)}45%{transform:translate3d(-4px,3px,0)}60%{transform:translate3d(4px,-2px,0)}75%{transform:translate3d(-2px,1px,0)}}\n.fx-impact{position:absolute;left:50%;top:46%;width:18px;height:18px;border-radius:50%;transform:translate(-50%,-50%);background:#fff;box-shadow:0 0 20px #fff,0 0 48px #f2c35c;animation:impactPop .42s ease-out forwards}\n.fx-impact:before,.fx-impact:after{content:\"\";position:absolute;left:50%;top:50%;width:150px;height:3px;background:linear-gradient(90deg,transparent,#fff,transparent);transform:translate(-50%,-50%) rotate(22deg);opacity:.9}.fx-impact:after{transform:translate(-50%,-50%) rotate(-22deg)}\n@keyframes impactPop{0%{opacity:0;transform:translate(-50%,-50%) scale(.2)}30%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(4.6)}}\n.fx-holy{position:absolute;left:50%;top:43%;width:34px;height:34px;transform:translate(-50%,-50%);animation:holyCore .95s ease-out forwards;filter:drop-shadow(0 0 18px #fff6c8) drop-shadow(0 0 42px #ffd55c)}\n.fx-holy:before{content:\"✦\";position:absolute;inset:-38px;display:grid;place-items:center;font-size:92px;color:#fff9d6;text-shadow:0 0 12px #fff,0 0 30px #ffd34f,0 0 60px #ffb300;animation:holySpin .95s ease-out forwards}\n.fx-holy:after{content:\"\";position:absolute;left:50%;top:-170px;width:18px;height:360px;transform:translateX(-50%);background:linear-gradient(180deg,transparent,rgba(255,255,255,.98) 32%,rgba(255,218,91,.95) 52%,transparent 78%);box-shadow:-55px 20px 40px rgba(255,220,110,.55),55px 20px 40px rgba(255,220,110,.55);animation:holyBeam .9s ease-out forwards}\n@keyframes holyCore{0%{opacity:0;transform:translate(-50%,-50%) scale(.25)}18%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(5.8)}}@keyframes holySpin{0%{opacity:0;transform:scale(.3) rotate(-25deg)}24%{opacity:1}100%{opacity:0;transform:scale(2.1) rotate(18deg)}}@keyframes holyBeam{0%{opacity:0;transform:translateX(-50%) scaleY(.2)}20%{opacity:1}100%{opacity:0;transform:translateX(-50%) scaleY(1.25)}}\n.fx-arrow{position:absolute;left:-28%;top:45%;width:130px;height:4px;border-radius:999px;animation:arrowFlight .8s cubic-bezier(.18,.76,.34,1) forwards;filter:drop-shadow(0 0 8px currentColor)}\n.fx-arrow:before{content:\"➤\";position:absolute;right:-20px;top:50%;transform:translateY(-52%);font-size:34px;color:currentColor;text-shadow:0 0 16px currentColor}.fx-arrow:after{content:\"\";position:absolute;right:78px;top:50%;width:170px;height:12px;transform:translateY(-50%);background:linear-gradient(90deg,transparent,currentColor);filter:blur(5px);opacity:.65}.fx-arrow-self{color:#7dff9f;background:linear-gradient(90deg,rgba(255,220,100,.15),#ffe27b 45%,#7dff9f)}.fx-arrow-ally{color:#7fd7ff;background:linear-gradient(90deg,rgba(255,255,255,.2),#edf7ff 42%,#7fd7ff)}\n@keyframes arrowFlight{0%{left:-30%;opacity:0;transform:translateY(16px) scale(.7)}12%{opacity:1}72%{opacity:1}100%{left:112%;opacity:0;transform:translateY(-12px) scale(1.12)}}\n"""
if css_old not in s:
    raise SystemExit('CSS anchor not found')
s=s.replace(css_old,css_new,1)

func_old="""function spellFx(name,strong){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-burst '+fxClass(name);if(strong)b.style.animationDuration='.72s';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1100)}\n"""
func_new="""function spellFx(name,strong){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-burst '+fxClass(name);if(strong)b.style.animationDuration='.72s';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1100)}\nfunction impactFx(){var layer=$('fxLayer');if(layer){var b=document.createElement('div');b.className='fx-impact';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},520)}document.body.classList.remove('screen-shake');void document.body.offsetWidth;document.body.classList.add('screen-shake');setTimeout(function(){document.body.classList.remove('screen-shake')},360)}\nfunction holySmiteFx(){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-holy';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1150)}\nfunction arrowFx(mode){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-arrow '+(mode==='strike'?'fx-arrow-self':'fx-arrow-ally');layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},950)}\n"""
if func_old not in s:
    raise SystemExit('FX function anchor not found')
s=s.replace(func_old,func_new,1)

attack_old="""S.dmg+=total;S.lastHit={turn:S.turn,index:S.attackCount,crit:crit,divineUsed:false};var extra=triggerSpellSmite(crit);addLog('Poings • attaque '"""
attack_new="""S.dmg+=total;S.lastHit={turn:S.turn,index:S.attackCount,crit:crit,divineUsed:false};impactFx();var extra=triggerSpellSmite(crit);addLog('Poings • attaque '"""
if attack_old not in s:
    raise SystemExit('Attack anchor not found')
s=s.replace(attack_old,attack_new,1)

smite_old="""S.dmg+=r.sum;S.lastHit.divineUsed=true;spellFx('Châtiment révélateur',true);addLog('Châtiment divin N'+l,"""
smite_new="""S.dmg+=r.sum;S.lastHit.divineUsed=true;holySmiteFx();addLog('Châtiment divin N'+l,"""
if smite_old not in s:
    raise SystemExit('Divine smite anchor not found')
s=s.replace(smite_old,smite_new,1)

arrow_old="""S.arrows--;commitAttack(a);var r=roll(2+slot,6);if(mode==='strike'){S.dmg+=r.sum;"""
arrow_new="""S.arrows--;commitAttack(a);var r=roll(2+slot,6);arrowFx(mode);if(mode==='strike'){S.dmg+=r.sum;"""
if arrow_old not in s:
    raise SystemExit('Arrow anchor not found')
s=s.replace(arrow_old,arrow_new,1)

p.write_text(s,encoding='utf-8')
print('patched')
