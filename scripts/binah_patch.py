from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
old_nav='<button class="navbtn" data-nav="auras" type="button"><span class="ico">◉</span><span>Auras</span></button>'
new_nav='<button class="navbtn" data-nav="binah" type="button"><span class="ico">◇</span><span>BINAH</span></button>'
if old_nav not in s:
    raise SystemExit('Auras nav button not found')
s=s.replace(old_nav,new_nav,1)
binah='''<section class="screen" id="binah">
<div class="binah-hero"><div class="binah-sigil">◇</div><div><div class="binah-kicker">VESTIGE • REMPART PRISMATIQUE</div><div class="binah-name">BINAH</div><div class="meta">Bouclier vivant de lumière fracturée • ses pouvoirs évoluent avec son éveil.</div></div></div>
<div class="section">État dormant</div>
<div class="card binah-card dormant"><div class="binah-stage"><span>DORMANT</span><b>+1 CA magique</b></div><div class="binah-power"><b>◈ Mue prismatique</b><span>Réaction • 3/jour • résistance au type de dégâts choisi jusqu’à la fin du tour de l’attaquant.</span></div><div class="binah-power"><b>◇ Résistance accordée</b><span>Après un repos long, choisir une résistance élémentaire.</span></div><div class="binah-power"><b>✧ Parade prismatique</b><span>Réaction • 1/jour • sur un impact élémentaire, lancer 1d6 : sur 5–6, les dégâts sont annulés.</span></div></div>
<div class="section">État éveillé</div>
<div class="card binah-card awakened"><div class="binah-stage"><span>ÉVEILLÉ</span><b>+2 CA magique</b></div><div class="binah-power"><b>◈ Mue prismatique</b><span>Usage illimité • immunité temporaire au type de dégâts choisi jusqu’à la fin du tour de l’attaquant.</span></div><div class="binah-power"><b>▱ Mur prismatique mineur</b><span>Action • 1/jour • mur de 3 × 3 m • absorbe 40 dégâts par élément.</span></div><div class="binah-power"><b>✦ Déviation chromatique</b><span>Réaction • 3/jour • l’attaquant fait un jet de CON DD 15 ; en cas d’échec, son attaque est à désavantage.</span></div></div>
<div class="card binah-note"><div class="title">Utilisation</div><div class="meta">BINAH reste un vestige séparé du bouclier +3 de Zéphyr. Les deux états sont affichés ici comme référence ; n’active que les pouvoirs correspondant à son niveau d’éveil actuel.</div></div>
</section>'''
m=re.search(r'<section class="screen" id="auras">.*?</section>\n<section class="screen" id="powers">',s,re.S)
if not m:
    raise SystemExit('Auras section not found')
s=s[:m.start()]+binah+'\n<section class="screen" id="powers">'+s[m.end():]
marker='<section class="screen" id="powers"><div class="section">Ressources</div>'
insert='''<section class="screen" id="powers"><div class="section">Auras</div><div class="card gold"><div class="title">Aura de protection</div><div class="meta">Zéphyr et alliés à 3 m : +4 aux jets de sauvegarde.</div></div><div class="card red"><div class="title">Aura de conquête</div><div class="meta">Cible terrorisée par Zéphyr à 3 m : vitesse 0 et 5 dégâts psychiques au début de son tour.</div></div><div class="card silver"><div class="title">Aura de bravoure</div><div class="meta">Zéphyr et alliés à 3 m ne peuvent pas être terrorisés.</div></div><div class="card green"><div class="title">Défenses passives</div><div class="meta">Résistance feu • Immunité maladies.</div></div><div class="section">Ressources</div>'''
if marker not in s:
    raise SystemExit('Powers marker not found')
s=s.replace(marker,insert,1)
css='''
/* binah-tab-v1 */
.binah-hero{position:relative;overflow:hidden;display:grid;grid-template-columns:74px 1fr;gap:12px;align-items:center;border:1px solid #7fa7c8;border-radius:18px;padding:16px;margin-bottom:12px;background:radial-gradient(circle at 15% 20%,rgba(137,215,255,.24),transparent 34%),radial-gradient(circle at 85% 0,rgba(216,162,255,.16),transparent 36%),linear-gradient(145deg,#18202c,#0d1118 64%);box-shadow:0 0 32px rgba(116,190,235,.13),inset 0 0 0 1px rgba(255,255,255,.03)}
.binah-hero:after{content:"";position:absolute;inset:-55%;background:conic-gradient(from 10deg,transparent,rgba(126,219,255,.12),transparent,rgba(255,207,122,.10),transparent,rgba(199,137,255,.12),transparent);animation:binahPrism 11s linear infinite;pointer-events:none}.binah-sigil{position:relative;z-index:1;width:68px;height:68px;border-radius:18px;display:grid;place-items:center;font-size:44px;color:#eaf8ff;border:1px solid #8ed9ff;background:linear-gradient(145deg,rgba(126,216,255,.18),rgba(186,124,255,.12));box-shadow:0 0 20px rgba(126,216,255,.24),inset 0 0 24px rgba(255,255,255,.06)}.binah-kicker{position:relative;z-index:1;font-size:9px;letter-spacing:.14em;font-weight:900;color:#a8dfff}.binah-name{position:relative;z-index:1;font-size:29px;line-height:1;font-weight:1000;letter-spacing:.16em;margin:4px 0 7px;background:linear-gradient(90deg,#f4fbff,#8ddcff,#e7b2ff,#ffd98a);-webkit-background-clip:text;background-clip:text;color:transparent}.binah-hero .meta{position:relative;z-index:1}
.binah-card{border-color:#52728b;background:radial-gradient(circle at 90% 0,rgba(115,202,255,.10),transparent 34%),linear-gradient(180deg,#151c25,#0d1117)}.binah-card.awakened{border-color:#9e79bd;background:radial-gradient(circle at 82% 0,rgba(208,143,255,.16),transparent 35%),radial-gradient(circle at 10% 100%,rgba(255,215,122,.09),transparent 38%),linear-gradient(180deg,#1a1722,#0d1016);box-shadow:0 0 24px rgba(181,122,225,.08)}.binah-stage{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}.binah-stage span{font-size:10px;letter-spacing:.13em;font-weight:1000;color:#aee4ff}.binah-card.awakened .binah-stage span{color:#e4baff}.binah-stage b{font-size:12px;color:#fff1b8;border:1px solid rgba(255,220,132,.35);border-radius:999px;padding:5px 9px;background:rgba(255,216,122,.07)}.binah-power{display:grid;gap:3px;padding:10px 0;border-top:1px solid rgba(121,152,177,.18)}.binah-power:first-of-type{border-top:0}.binah-power b{font-size:12px;color:#eaf7ff}.binah-power span{font-size:11px;line-height:1.4;color:#aeb9c5}.binah-note{border-color:#594f68;background:linear-gradient(180deg,#17141d,#0e1015)}@keyframes binahPrism{to{transform:rotate(360deg)}}
'''
if '/* binah-tab-v1 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s)
