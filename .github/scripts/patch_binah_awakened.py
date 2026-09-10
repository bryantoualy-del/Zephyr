from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

new_binah='''<section class="screen" id="binah">
<div class="binah-hero"><div class="binah-sigil">◇</div><div><div class="binah-kicker">VESTIGE • REMPART PRISMATIQUE</div><div class="binah-name">BINAH</div><div class="binah-status">ÉTAT ÉVEILLÉ</div><div class="meta">Les capacités dormantes sont intégrées ici lorsqu'elles sont améliorées par l'éveil.</div></div></div>
<div class="section">Passifs</div>
<div class="card binah-card"><div class="binah-stage"><span>PASSIF</span><b>+2 CA magique</b></div><div class="binah-power"><b>◇ Résistance accordée</b><span>Après un repos long, choisir une résistance élémentaire.</span><div class="binah-inline"><select id="binahResist"><option value="feu">Feu</option><option value="froid">Froid</option><option value="foudre">Foudre</option><option value="tonnerre">Tonnerre</option><option value="acide">Acide</option><option value="poison">Poison</option><option value="radiant">Radiant</option><option value="nécrotique">Nécrotique</option></select><button class="btn silver" id="binahResistBtn" type="button">Choisir</button></div><div class="smite-state" id="binahResistState">Aucune résistance sélectionnée.</div></div></div>
<div class="section">Pouvoirs actifs</div>
<div class="card binah-card active"><div class="binah-power"><div class="binah-powerhead"><b>◈ Mue prismatique</b><span class="binah-badge reaction">Réaction</span></div><span>Usage illimité • immunité temporaire au type de dégâts choisi jusqu'à la fin du tour de l'attaquant.</span><div class="binah-inline"><select id="binahMueType"><option value="feu">Feu</option><option value="froid">Froid</option><option value="foudre">Foudre</option><option value="tonnerre">Tonnerre</option><option value="acide">Acide</option><option value="poison">Poison</option><option value="radiant">Radiant</option><option value="nécrotique">Nécrotique</option></select><button class="btn blue" id="binahMueBtn" type="button">Activer</button></div></div></div>
<div class="card binah-card awakened"><div class="binah-power"><div class="binah-powerhead"><b>✦ Déviation chromatique</b><span class="binah-badge reaction">Réaction</span></div><span>3/jour • l'attaquant fait un jet de CON DD 15 ; en cas d'échec, son attaque est à désavantage.</span><div class="binah-actionline"><div class="binah-count" id="binahChromaticCount">3/3</div><button class="btn gold" id="binahChromaticBtn" type="button">Dévier</button></div></div></div>
<div class="card binah-card awakened"><div class="binah-power"><div class="binah-powerhead"><b>▱ Mur prismatique mineur</b><span class="binah-badge action">Action</span></div><span>1/jour • mur 3 × 3 m • absorbe 40 dégâts par élément.</span><div class="binah-actionline"><div class="binah-count" id="binahWallCount">1/1</div><button class="btn blue" id="binahWallBtn" type="button">Déployer</button></div></div></div>
<div class="card binah-note"><div class="title">BINAH éveillée</div><div class="meta">La Mue prismatique éveillée remplace sa version dormante : usage illimité et immunité temporaire. Les réactions utilisent la Réaction du tour de Zéphyr.</div></div>
</section>'''

m=re.search(r'<section class="screen" id="binah">.*?</section>\n<section class="screen" id="powers">',s,re.S)
if not m: raise SystemExit('BINAH section not found')
s=s[:m.start()]+new_binah+'\n<section class="screen" id="powers">'+s[m.end():]

if 'binahChromatic:3' not in s:
    s=s.replace("anchor:1,arrows:3,mark:false", "anchor:1,arrows:3,binahChromatic:3,binahWall:1,binahResist:'',mark:false", 1)

css='''
/* binah-awakened-v2 */
.binah-status{display:inline-block;margin-top:2px;border:1px solid #b88de0;border-radius:999px;padding:4px 8px;font-size:9px;font-weight:1000;letter-spacing:.12em;color:#edd5ff;background:rgba(167,105,214,.12);box-shadow:0 0 16px rgba(188,123,239,.12)}.binah-powerhead{display:flex;align-items:center;justify-content:space-between;gap:8px}.binah-badge{flex:0 0 auto;border-radius:999px;padding:4px 8px;font-size:9px;font-weight:1000;letter-spacing:.08em;text-transform:uppercase}.binah-badge.reaction{border:1px solid #7d9bd6;color:#cfe0ff;background:rgba(86,119,182,.13)}.binah-badge.action{border:1px solid #b98d53;color:#ffe0a0;background:rgba(183,132,62,.12)}.binah-inline{display:grid;grid-template-columns:1fr auto;gap:7px;margin-top:9px;align-items:center}.binah-inline select{min-height:42px;border-radius:10px;border:1px solid #58748c;background:#0c1118;color:#eff8ff;padding:8px}.binah-inline .btn{min-height:42px;padding:7px 12px}.binah-actionline{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px}.binah-actionline .btn{min-height:44px;min-width:120px}.binah-count{min-width:58px;text-align:center;border:1px solid #6283a0;border-radius:999px;padding:7px 9px;font-weight:1000;color:#d8f2ff;background:#101722}.binah-card.active{box-shadow:0 0 22px rgba(98,190,255,.08)}
.fx-prism-shield{position:absolute;left:50%;top:44%;width:140px;height:170px;transform:translate(-50%,-50%);clip-path:polygon(50% 0,93% 17%,82% 73%,50% 100%,18% 73%,7% 17%);background:linear-gradient(135deg,rgba(255,80,80,.42),rgba(255,196,72,.4) 18%,rgba(111,255,169,.38) 36%,rgba(84,205,255,.45) 56%,rgba(116,104,255,.42) 73%,rgba(229,119,255,.4));border:2px solid rgba(236,249,255,.9);box-shadow:0 0 25px rgba(140,218,255,.75),0 0 70px rgba(194,122,255,.38);animation:prismShield .9s ease-out forwards}@keyframes prismShield{0%{opacity:0;transform:translate(-50%,-50%) scale(.55) rotate(-8deg)}25%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(1.35) rotate(8deg)}}
.fx-rainbow-arc{position:absolute;left:50%;top:43%;width:280px;height:140px;transform:translate(-50%,-50%);border-radius:280px 280px 0 0;background:conic-gradient(from 270deg at 50% 100%,#ff4b4b,#ffb84b,#fff36b,#66ff9b,#5ddcff,#7182ff,#d96bff,#ff5fb2,#ff4b4b);mask:radial-gradient(ellipse at 50% 100%,transparent 0 56%,#000 57% 69%,transparent 70%);-webkit-mask:radial-gradient(ellipse at 50% 100%,transparent 0 56%,#000 57% 69%,transparent 70%);filter:drop-shadow(0 0 16px rgba(180,220,255,.8));animation:rainbowArc .95s ease-out forwards}.fx-rainbow-flash{position:fixed;inset:0;background:linear-gradient(120deg,rgba(255,70,70,.20),rgba(255,215,80,.18),rgba(80,255,170,.16),rgba(90,180,255,.20),rgba(200,90,255,.18));mix-blend-mode:screen;animation:rainbowFlash .45s ease-out forwards}.fx-prism-wall{position:absolute;left:50%;top:46%;width:300px;height:170px;transform:translate(-50%,-50%);background:linear-gradient(110deg,rgba(255,91,91,.34),rgba(255,215,80,.34),rgba(83,255,171,.34),rgba(89,199,255,.40),rgba(187,109,255,.38));border:2px solid rgba(235,248,255,.9);box-shadow:0 0 30px rgba(107,202,255,.55),inset 0 0 40px rgba(255,255,255,.16);animation:prismWall .95s ease-out forwards}@keyframes rainbowArc{0%{opacity:0;transform:translate(-50%,-35%) scale(.4)}22%{opacity:1}100%{opacity:0;transform:translate(-50%,-55%) scale(1.25)}}@keyframes rainbowFlash{0%{opacity:0}18%{opacity:.8}100%{opacity:0}}@keyframes prismWall{0%{opacity:0;transform:translate(-50%,-50%) scaleX(.2)}24%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scaleX(1.15)}}
'''
if '/* binah-awakened-v2 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

marker='function addLog(title,body,type)'
funcs="""function binahElementFx(type){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-burst '+({feu:'fx-fire',froid:'fx-ice',foudre:'fx-thunder',tonnerre:'fx-thunder',acide:'fx-green',poison:'fx-green',radiant:'fx-radiant','nécrotique':'fx-shadow'}[type]||'fx-white');layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1100)}
function binahShieldFx(){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-prism-shield';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1100)}
function binahRainbowFx(){var layer=$('fxLayer');if(!layer)return;var a=document.createElement('div');a.className='fx-rainbow-arc';var f=document.createElement('div');f.className='fx-rainbow-flash';layer.appendChild(a);layer.appendChild(f);setTimeout(function(){if(a.parentNode)a.parentNode.removeChild(a);if(f.parentNode)f.parentNode.removeChild(f)},1100)}
function binahWallFx(){var layer=$('fxLayer');if(!layer)return;var b=document.createElement('div');b.className='fx-prism-wall';layer.appendChild(b);setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},1150)}
function chooseBinahResist(){var t=$('binahResist').value;S.binahResist=t;binahElementFx(t);addLog('BINAH • Résistance accordée','Résistance choisie : '+t+'.','power')}
function useBinahMue(){if(!useEco('r','Réaction'))return;var t=$('binahMueType').value;binahShieldFx();binahElementFx(t);addLog('BINAH • Mue prismatique','Réaction • immunité temporaire : '+t+' jusqu\'à la fin du tour de l\'attaquant.','power')}
function useBinahChromatic(){if((S.binahChromatic||0)<=0){ribbon('Déviation chromatique épuisée');return}if(!useEco('r','Réaction'))return;S.binahChromatic--;binahRainbowFx();addLog('BINAH • Déviation chromatique','Réaction • CON DD 15 • en cas d\'échec, attaque à désavantage.','power')}
function useBinahWall(){if((S.binahWall||0)<=0){ribbon('Mur prismatique déjà utilisé');return}if(!useEco('a','Action'))return;S.binahWall--;binahWallFx();addLog('BINAH • Mur prismatique mineur','Action • mur 3 × 3 m • absorbe 40 dégâts par élément.','power')}
"""
if 'function binahRainbowFx()' not in s:
    s=s.replace(marker,funcs+marker,1)

s=s.replace("S.anchor=1;S.arrows=3;S.mark=false", "S.anchor=1;S.arrows=3;S.binahChromatic=3;S.binahWall=1;S.mark=false", 1)
render_marker="if($('markText'))$('markText').textContent=S.mark?'PRÉSENTE — soins sur autrui réduisent vos PV max':'Absente';"
if "binahChromaticCount" not in s[s.find('function render()'):s.find('function bind()')]:
    s=s.replace(render_marker,render_marker+"if($('binahChromaticCount'))$('binahChromaticCount').textContent=(S.binahChromatic==null?3:S.binahChromatic)+'/3';if($('binahWallCount'))$('binahWallCount').textContent=(S.binahWall==null?1:S.binahWall)+'/1';if($('binahResistState'))$('binahResistState').textContent=S.binahResist?'Résistance actuelle : '+S.binahResist:'Aucune résistance sélectionnée.';",1)
bind_marker="$('anchorBtn').addEventListener('click',anchor);"
if "binahMueBtn').addEventListener" not in s:
    s=s.replace(bind_marker,bind_marker+"$('binahResistBtn').addEventListener('click',chooseBinahResist);$('binahMueBtn').addEventListener('click',useBinahMue);$('binahChromaticBtn').addEventListener('click',useBinahChromatic);$('binahWallBtn').addEventListener('click',useBinahWall);",1)

p.write_text(s)
