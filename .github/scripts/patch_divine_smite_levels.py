from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="function holySmiteFx(){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-holy';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1150)}"
new="function holySmiteFx(level){var layer=$('fxLayer');if(!layer)return;level=Math.max(1,Math.min(3,Number(level)||1));var b=document.createElement('div');b.className='fx-holy fx-holy-l'+level;layer.appendChild(b);for(var i=0;i<level*2;i++){var sp=document.createElement('i');sp.className='holy-spark holy-spark-'+(i%4);sp.style.setProperty('--a',(i*(360/(level*2)))+'deg');sp.style.setProperty('--d',(42+level*20+(i%2)*15)+'px');b.appendChild(sp)}if(level>=2){var ring=document.createElement('i');ring.className='holy-ring';b.appendChild(ring)}if(level===3){var flash=document.createElement('div');flash.className='holy-screen-flash';layer.appendChild(flash);setTimeout(function(){if(flash.parentNode)flash.parentNode.removeChild(flash)},520);document.body.classList.remove('holy-shake');void document.body.offsetWidth;document.body.classList.add('holy-shake');setTimeout(function(){document.body.classList.remove('holy-shake')},430)}setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1350)}"
if old not in s:
    raise SystemExit('holySmiteFx pattern not found')
s=s.replace(old,new,1)
old2="holySmiteFx();addLog('Châtiment divin N'+l"
new2="holySmiteFx(l);addLog('Châtiment divin N'+l"
if old2 not in s:
    raise SystemExit('divine smite call pattern not found')
s=s.replace(old2,new2,1)
css="""
/* divine-smite-levels-v1 */
.fx-holy.fx-holy-l1{transform:translate(-50%,-50%) scale(.78);filter:drop-shadow(0 0 12px #fff6c8) drop-shadow(0 0 28px #ffd55c)}
.fx-holy.fx-holy-l1:before{font-size:74px;text-shadow:0 0 10px #fff,0 0 22px #ffd34f,0 0 38px #ffb300}
.fx-holy.fx-holy-l1:after{width:10px;height:270px;top:-125px;opacity:.72}
.fx-holy.fx-holy-l2{transform:translate(-50%,-50%) scale(1.03);filter:drop-shadow(0 0 20px #fff9d9) drop-shadow(0 0 52px #ffd55c)}
.fx-holy.fx-holy-l2:before{font-size:106px;text-shadow:0 0 14px #fff,0 0 34px #ffd34f,0 0 68px #ffb300}
.fx-holy.fx-holy-l2:after{width:22px;height:410px;top:-195px;opacity:.92;box-shadow:-70px 30px 50px rgba(255,220,110,.68),70px 30px 50px rgba(255,220,110,.68)}
.fx-holy.fx-holy-l3{transform:translate(-50%,-50%) scale(1.34);filter:drop-shadow(0 0 28px #fff) drop-shadow(0 0 75px #ffd34f) drop-shadow(0 0 110px #ff9f1a)}
.fx-holy.fx-holy-l3:before{font-size:138px;text-shadow:0 0 18px #fff,0 0 46px #ffe06e,0 0 92px #ffb300,0 0 130px #ff8a00}
.fx-holy.fx-holy-l3:after{width:36px;height:520px;top:-245px;opacity:1;box-shadow:-95px 35px 68px rgba(255,232,150,.85),95px 35px 68px rgba(255,232,150,.85),0 0 90px rgba(255,255,255,.8)}
.holy-spark{position:absolute;left:50%;top:50%;width:7px;height:22px;border-radius:999px;background:linear-gradient(#fff,#ffd95c);box-shadow:0 0 10px #fff,0 0 22px #ffc928;transform-origin:50% 50%;animation:holySpark .82s ease-out forwards;transform:translate(-50%,-50%) rotate(var(--a)) translateY(calc(var(--d)*-1))}
.fx-holy-l2 .holy-spark{width:8px;height:28px}.fx-holy-l3 .holy-spark{width:10px;height:34px;box-shadow:0 0 14px #fff,0 0 30px #ffd13b}
.holy-ring{position:absolute;left:50%;top:50%;width:115px;height:115px;border:3px solid #ffe57d;border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 18px #fff8c5,0 0 42px #ffc928;animation:holyRingPulse .8s ease-out forwards}
.fx-holy-l3 .holy-ring{width:155px;height:155px;border-width:5px;box-shadow:0 0 25px #fff,0 0 62px #ffc928}
.holy-screen-flash{position:fixed;inset:0;background:radial-gradient(circle at 50% 43%,rgba(255,255,255,.98),rgba(255,230,120,.62) 24%,rgba(255,190,45,.16) 56%,transparent 78%);animation:holyScreenFlash .48s ease-out forwards}
body.holy-shake{animation:holyShake .4s cubic-bezier(.36,.07,.19,.97) both}
@keyframes holySpark{0%{opacity:0;filter:brightness(2)}24%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) rotate(var(--a)) translateY(calc((var(--d) + 85px)*-1)) scale(.3)}}
@keyframes holyRingPulse{0%{opacity:0;transform:translate(-50%,-50%) scale(.18)}25%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(2.3)}}
@keyframes holyScreenFlash{0%{opacity:0}15%{opacity:.95}100%{opacity:0}}
@keyframes holyShake{0%,100%{transform:translate3d(0,0,0)}16%{transform:translate3d(-6px,3px,0)}32%{transform:translate3d(7px,-4px,0)}48%{transform:translate3d(-5px,4px,0)}64%{transform:translate3d(5px,-3px,0)}80%{transform:translate3d(-3px,2px,0)}}
"""
marker='@media(max-width:390px)'
if marker not in s:
    raise SystemExit('CSS insertion marker not found')
s=s.replace(marker,css+'\n'+marker,1)
p.write_text(s,encoding='utf-8')
