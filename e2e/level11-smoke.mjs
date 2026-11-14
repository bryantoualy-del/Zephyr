import assert from 'node:assert/strict';
import {chromium,webkit} from 'playwright';
import {createServer} from 'node:http';
import {WebSocketServer} from 'ws';
import {mkdir,readFile} from 'node:fs/promises';
import {resolve,extname} from 'node:path';
const root=process.cwd();
const beforeRoot=process.env.E2E_BEFORE_ROOT&&resolve(process.env.E2E_BEFORE_ROOT);
const captureDir=process.env.E2E_CAPTURE_DIR&&resolve(process.env.E2E_CAPTURE_DIR);
if(captureDir)await mkdir(captureDir,{recursive:true});
const viewports=[[1180,820],[1024,768],[1366,1024],[820,1180],[390,844],[430,932]];
const landscape=width=>width>=1024;
const mime={'.js':'text/javascript','.css':'text/css','.html':'text/html','.json':'application/json','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml'};
const server=createServer(async(req,res)=>{try{
 const u=new URL(req.url,'http://localhost'), before=u.pathname.startsWith('/before/');
 const directory=before?beforeRoot:root;
 if(!directory)throw Error('No baseline checkout');
 const pathname=before?u.pathname.slice('/before'.length):u.pathname;
 const file=resolve(directory,'.'+pathname.replace(/\/$/,'/index.html'));
 if(!file.startsWith(directory+'/'))throw Error('Outside repo');
 const data=await readFile(file);res.setHeader('Content-Type',mime[extname(file)]||'application/octet-stream');res.end(data);
}catch{res.writeHead(404).end()}});
await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
const base='http://127.0.0.1:'+server.address().port;
const engine=process.env.E2E_BROWSER==='webkit'?webkit:chromium;
let browser;
try{
 for(const [width,height] of viewports){
  const executablePath=process.env.E2E_BROWSER_PATH;
  const localArgs=process.env.E2E_BROWSER_ARGS?.split(' ').filter(Boolean)||[];
  browser=await engine.launch({executablePath,args:engine===webkit?localArgs:['--disable-dev-shm-usage','--disable-gpu',...localArgs]});
  const page=await browser.newPage({viewport:{width,height},hasTouch:true});
  page.setDefaultTimeout(7000);
  const capture=async(label,fullPage=true)=>{
    if(!captureDir)return;
    await page.evaluate(()=>document.fonts.ready);
    await page.screenshot({path:resolve(captureDir,label+'-'+width+'.png'),fullPage});
  };
  if(beforeRoot&&captureDir&&[1180,390].includes(width)){
    await page.goto(base+'/before/');
    await capture('avant-normal');
    await page.locator('#titanGrow').tap();
    await page.locator('#ribbon').evaluate(el=>el.classList.remove('show'));
    await capture('avant-agrandi');
    await page.evaluate(()=>localStorage.clear());
  }
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.waitForFunction(()=>window.__CompanionBridge?.read);
  const initial=await page.evaluate(()=>{const s=window.__CompanionBridge.read();return{hp:s.hp,max:s.maxHp,lay:s.lay,slot3:s.slots[3],ac:window.__CompanionBridge.ac(s)}});
  assert.deepEqual(initial,{hp:92,max:92,lay:55,slot3:3,ac:20});
  await page.evaluate(()=>{const s=structuredClone(window.__CompanionBridge.read());s.hp=50;s.maxHp=84;s.lay=50;s.slots[3]=2;localStorage.setItem('zephyr-mobile-v20',JSON.stringify(s))});
  await page.reload();await page.waitForFunction(()=>window.__CompanionBridge?.read);
  const migrated=await page.evaluate(()=>{const s=window.__CompanionBridge.read();return{hp:s.hp,max:s.maxHp,lay:s.lay,slot3:s.slots[3],ac:window.__CompanionBridge.ac(s)}});
  assert.deepEqual(migrated,{hp:58,max:92,lay:55,slot3:3,ac:20});
  await checkLayout(page,width);
  await capture('apres-normal');
  const before=await page.evaluate(()=>CompanionAPI.getState());
  assert.equal(await page.locator('#titanAttackDamage').textContent(),'1d8+7');
  await page.evaluate(()=>{window.fxEvents=[];CompanionAPI.subscribe(e=>fxEvents.push(e.type))});
  await page.locator('#titanGrow').tap();
  await page.waitForSelector('.titan-fx-grow',{state:'attached'});
  const grew=await page.evaluate(()=>{
    const saved=JSON.parse(localStorage.getItem('zephyr-mobile-v20'));
    return {size:saved.titanEnlarged,ready:saved.titanReady,skin:saved.titanStoneSkin,bonus:saved.eco.b,logs:saved.log.length};
  });
  assert.deepEqual(grew,{size:true,ready:false,skin:true,bonus:true,logs:1});
  assert.equal(await page.locator('#titanAttackDamage').textContent(),'2d8+7');
  assert.equal(await page.evaluate(()=>CompanionAPI.getState().concentration),'Peau de pierre');
  assert.equal(await page.evaluate(()=>CompanionAPI.getState().concentrationInstance===null),false);
  if(width===1180&&captureDir){
    await page.waitForFunction(()=>Number(getComputedStyle(document.querySelector('.titan-fx-fissures')).opacity)>.45);
    await capture('apres-fx',false);
  }
  await page.waitForSelector('.titan-fx',{state:'detached'});
  assert.deepEqual(await page.evaluate(()=>fxEvents),['state:changed']);
  await page.locator('#ribbon').evaluate(el=>el.classList.remove('show'));
  await capture('apres-agrandi');
  await page.reload();
  assert.equal(await page.locator('#titanAttackMode').textContent(),'AGRANDI');
  assert.equal(await page.locator('.titan-fx').count(),0);
  await page.evaluate(()=>RPGConcentration.receive('concentration:break',{reason:'incapacitation'}));
  assert.match(await page.locator('#titanSkinState').textContent(),/Rompue/);
  assert.equal(await page.locator('#titanAttackDamage').textContent(),'2d8+7');
  await page.locator('#titanStop').tap();
  await page.waitForSelector('.titan-fx-release',{state:'attached'});
  assert.equal(await page.locator('#titanAttackDamage').textContent(),'1d8+7');
  assert.equal(await page.locator('#titanGrow').isDisabled(),true);
  await page.waitForSelector('.titan-fx',{state:'detached'});
  await page.locator('.cc-turn-rest').first().tap();
  await page.locator('.companion-rest-go').tap();
  assert.equal(await page.locator('#titanGrow').isEnabled(),true);
  assert.deepEqual(await page.evaluate(()=>CompanionAPI.getState().resources.slots),before.resources.slots);
  for(const tab of ['arsenal','binah','social','journal','combat']){
    await page.locator('[data-nav="'+tab+'"]').tap();
    await page.waitForSelector('#'+tab+'.active');
    await checkWidth(page,width,tab);
  }
  await page.locator('[data-rpg-group-tab]').tap();
  await page.waitForSelector('#rpgGroupView:not([hidden])');
  await checkWidth(page,width,'groupe');
  await page.locator('[data-nav="combat"]').tap();
  await page.locator('.rpg-connect-launch').first().tap();
  await page.waitForSelector('.rpg-connect-panel:not([hidden])');
  await page.evaluate(()=>RPGConnect.closePanel());
  if(width===1180||width===390)await checkSmite(page,width);
  if(width===1180){await checkExpiry(page);await checkRpgConnect(page);}
  assert.deepEqual(errors,[],'no browser runtime errors at '+width+'px');
  console.log('  Combat '+width+' × '+height+' passed');
  await browser.close();
 }
 console.log('Level 11 browser smoke passed:',process.env.E2E_BROWSER||'chromium');
}finally{await browser?.close();await new Promise(ok=>server.close(ok))}


async function checkWidth(page,width,tab){
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  assert.ok(overflow<=1,tab+' at '+width+'px overflows by '+overflow+'px');
}
async function checkLayout(page,width){
  await checkWidth(page,width,'combat');
  const rects=await page.evaluate(()=>{
    const elements=['#attackCard','#titanCard','#spellSmiteCard','.arrow-card','#divineSmiteCard','#cc-turnbar-standard','.nav','.hud'];
    return elements.map(selector=>{
      const r=document.querySelector(selector).getBoundingClientRect();
      return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width};
    });
  });
  const [attack,titan,spell,arrow,divine,turnbar,nav,hud]=rects;
  assert.ok(rects.every(r=>r.left>=-1&&r.right<=width+1),'elements stay inside viewport width');
  if(!landscape(width)){
    assert.ok(attack.bottom<=titan.top&&titan.bottom<=divine.top&&divine.bottom<=spell.top,'phone card order preserved');
    return;
  }
  assert.equal(attack.top,titan.top);
  assert.equal(spell.top,arrow.top);
  assert.ok(attack.right<titan.left&&attack.width>titan.width*1.85);
  assert.ok(spell.right<arrow.left&&spell.width>arrow.width*1.85);
  assert.equal(divine.left,attack.left);
  assert.equal(divine.right,titan.right);
  assert.ok(divine.top>=arrow.bottom&&spell.top>=titan.bottom);
  assert.ok(hud.bottom<=turnbar.top&&turnbar.bottom<=nav.top&&nav.bottom<attack.top);
  for(const button of await page.locator('#divineSmiteCard .smite').all()){
    const box=await button.boundingBox();
    assert.ok(box.width>=44&&box.height>=44);
  }
  await page.evaluate(()=>scrollTo(0,document.body.scrollHeight));
  const stack=await page.locator('.zephyr-tablet-navigation').boundingBox();
  const target=await page.locator('#divineSmiteCard').boundingBox();
  assert.ok(target.y>=stack.y+stack.height,'smite remains reachable when scrolling');
  await page.evaluate(()=>scrollTo(0,0));
}
async function attack(page,natural,hit){
  await page.locator('#attackBtn').tap();
  await page.locator('dialog input[name="answer"]').fill(String(natural));
  await page.locator('[data-dialog-accept]').tap();
  await page.locator(hit?'#hitYes':'#hitNo').tap();
}
async function checkSmite(page,width){
  const tablet=landscape(width);
  assert.equal(await page.locator('#titanWeaponSmite').count(),0,'improved smite is always enabled on gauntlets');
  assert.match(await page.locator('.titan-improved-smite').textContent(),/\+1d8 radiant/);
  await page.locator('#fiend').check();
  await page.locator('#guidedBtn').tap();
  await page.locator('#armSpellSmite').tap();
  await page.evaluate(()=>{CompanionAPI.setRollMode('manual');Math.random=()=>.5});
  await attack(page,20,true);
  const smite=page.locator(tablet?'#divineSmiteCard [data-level="2"]':'#zephyrDivineSmite [data-smite-level="2"]');
  await smite.waitFor({state:'visible'});
  assert.match(await smite.textContent(),/\+8d8/);
  const waiting=await page.evaluate(()=>window.__CompanionBridge.read().rpgZephyrAttack.roll);
  assert.equal(waiting.guided,10);
  assert.equal(waiting.total,43);
  if(tablet){
    assert.equal(await page.locator('#zephyrDivineSmite').evaluate(el=>el.open),false);
    const turn=await page.evaluate(()=>CompanionAPI.getState().turn.number);
    await page.locator('.cc-turn-next').tap();
    assert.equal(await page.evaluate(()=>CompanionAPI.getState().turn.number),turn);
    await page.setViewportSize({width:820,height:1180});
    await page.waitForSelector('#zephyrDivineSmite[open]');
    await page.setViewportSize({width:1180,height:820});
    await page.waitForSelector('#zephyrDivineSmite[open]',{state:'hidden'});
    await page.reload();
    await page.waitForSelector('#divineSmiteCard.is-awaiting');
    await page.evaluate(()=>{Math.random=()=>.5});
  }
  await smite.tap();
  await page.waitForFunction(()=>!window.__CompanionBridge.read().rpgZephyrAttack);
  const committed=await page.evaluate(()=>{
    const s=window.__CompanionBridge.read();
    return {slots:s.slots,count:s.attackCount,dmg:s.dmg,smiteLogs:s.log.filter(l=>l.title==='Châtiment divin N2').length,
      spellLogs:s.log.filter(l=>l.title==='Châtiment calcinant déclenché').length,attackLogs:s.log.filter(l=>l.title.startsWith('Titan • attaque')).length};
  });
  assert.deepEqual(committed,{slots:{1:3,2:2,3:3},count:1,dmg:75,smiteLogs:1,spellLogs:1,attackLogs:1});
  const close=page.getByRole('button',{name:'Fermer ce résultat'});
  if(await close.isVisible())await close.tap();
  assert.equal(await page.locator('#divineSmiteCard [data-level="2"]').isDisabled(),true);
  await attack(page,11,false);
  await page.waitForFunction(()=>!window.__CompanionBridge.read().rpgZephyrAttack);
  if(await close.isVisible())await close.tap();
  assert.equal(await page.evaluate(()=>window.__CompanionBridge.read().attackCount),2);
  await page.locator('#attackBtn').tap();
  assert.equal(await page.locator('dialog input[name="answer"]').count(),0);
}
async function checkExpiry(page){
  await page.clock.install();
  await page.evaluate(()=>CompanionAPI.nextTurn());
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.locator('#titanGrow').tap();
  assert.equal(await page.locator('.titan-fx i').count(),0);
  await page.evaluate(()=>CompanionAPI.setConcentration('Bouclier de la foi'));
  assert.match(await page.locator('#titanSkinState').textContent(),/Rompue/);
  await page.clock.fastForward(10*60*1000+10);
  assert.equal(await page.locator('#titanAttackDamage').textContent(),'1d8+7');
  assert.equal(await page.evaluate(()=>CompanionAPI.getState().concentration),'Bouclier de la foi');
  assert.equal(await page.evaluate(()=>window.__CompanionBridge.read().log.filter(l=>/durée de 10 minutes écoulée/.test(l.body)).length),1);
}


async function checkRpgConnect(page){
  await page.reload();
  const events=[];
  const mock=new WebSocketServer({server,path:'/zephyr-test'});
  mock.on('connection',socket=>socket.on('message',message=>{
    const packet=JSON.parse(message);
    events.push(packet);
    if(packet.type==='hello')socket.send(JSON.stringify({
      type:'welcome',protocolVersion:1,room:packet.room,
      capabilities:packet.clientCapabilities,payload:{sessionMode:'guided'}
    }));
    if(packet.type==='event')socket.send(JSON.stringify({type:'ack',id:packet.event.id}));
  }));
  try{
    await page.evaluate(()=>{
      document.querySelector('[name="endpoint"]').value='ws://'+location.host+'/zephyr-test';
      document.querySelector('[name="room"]').value='playwright';
      document.querySelector('[name="token"]').value='test-token';
      RPGConnect.connect();
    });
    await page.waitForFunction(()=>RPGConnect.getStatus().connected);
    await page.evaluate(()=>{
      RPGConnect.setTargets([{id:'titan-test-target',name:'Cible test',creatureType:'undead'}],'titan-test-target');
      scrollTo(0,document.body.scrollHeight);
    });
    const dock=await page.locator('#rpg-target-dock').boundingBox();
    const attack=await page.locator('#attackCard').boundingBox();
    assert.ok(dock.y+dock.height<=attack.y&&dock.width>attack.width);
    const stack=await page.locator('.zephyr-tablet-navigation').boundingBox();
    const banner=await page.locator('.rpg-session-banner').boundingBox();
    assert.ok(stack.y>=banner.y+banner.height,'connected RPG banner clears the sticky navigation');
    await page.locator('.cc-turn-rest').first().tap();
    await page.locator('.companion-rest-go').tap();
    await page.waitForFunction(()=>window.__CompanionBridge.read().titanReady);
    const start=events.length;
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.locator('#titanGrow').tap();
    await page.waitForSelector('.titan-fx-grow',{state:'attached'});
    await page.locator('#titanStop').tap();
    await page.waitForSelector('.titan-fx-release',{state:'attached'});
    assert.equal(await page.locator('.titan-fx').count(),1);
    await page.waitForSelector('.titan-fx',{state:'detached'});
    const outgoing=events.slice(start);
    const changes=outgoing.filter(packet=>packet.type==='state');
    assert.deepEqual(changes.map(packet=>packet.state.concentration),['Peau de pierre',null]);
    assert.deepEqual(changes.map(packet=>packet.state.statuses.includes('agrandi')),[true,false]);
    assert.deepEqual(outgoing.filter(packet=>packet.type==='event').map(packet=>packet.event.type),['state:changed','state:changed']);
    await page.evaluate(()=>RPGConnect.disconnect());
  }finally{
    for(const socket of mock.clients)socket.terminate();
    await new Promise(done=>mock.close(done));
  }
}
