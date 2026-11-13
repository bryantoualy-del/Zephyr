import assert from 'node:assert/strict';
import {chromium,webkit} from 'playwright';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {resolve,extname} from 'node:path';
const root=process.cwd();
const server=createServer(async(req,res)=>{try{
 const u=new URL(req.url,'http://localhost'),file=resolve(root,'.'+u.pathname.replace(/\/$/,'/index.html'));
 if(!file.startsWith(root+'/'))throw Error('Outside repo');
 const data=await readFile(file);res.setHeader('Content-Type',({'.js':'text/javascript','.css':'text/css','.html':'text/html','.json':'application/json'})[extname(file)]||'application/octet-stream');res.end(data);
}catch{res.writeHead(404).end()}});
await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
const base='http://127.0.0.1:'+server.address().port;
const engine=process.env.E2E_BROWSER==='webkit'?webkit:chromium;
let browser;
try{
 browser=await engine.launch(engine===webkit?{}:{args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 for(const [width,height] of [[390,844],[768,1024],[1180,820]]){
  const page=await browser.newPage({viewport:{width,height}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.waitForFunction(()=>window.__CompanionBridge?.read);
  const initial=await page.evaluate(()=>{const s=window.__CompanionBridge.read();return{hp:s.hp,max:s.maxHp,lay:s.lay,slot3:s.slots[3],ac:window.__CompanionBridge.ac(s)}});
  assert.deepEqual(initial,{hp:92,max:92,lay:55,slot3:3,ac:20});
  await page.evaluate(()=>{const s=structuredClone(window.__CompanionBridge.read());s.hp=50;s.maxHp=84;s.lay=50;s.slots[3]=2;localStorage.setItem('zephyr-mobile-v20',JSON.stringify(s))});
  await page.reload();await page.waitForFunction(()=>window.__CompanionBridge?.read);
  const migrated=await page.evaluate(()=>{const s=window.__CompanionBridge.read();return{hp:s.hp,max:s.maxHp,lay:s.lay,slot3:s.slots[3],ac:window.__CompanionBridge.ac(s)}});
  assert.deepEqual(migrated,{hp:58,max:92,lay:55,slot3:3,ac:20});
  const ux=await page.evaluate(()=>{
    const $=id=>document.getElementById(id);
    const before={mode:$('titanAttackMode').textContent,damage:$('titanAttackDamage').textContent,stopHidden:$('titanStop').hidden};
    $('titanGrow').click();
    const enlarged={mode:$('titanAttackMode').textContent,damage:$('titanAttackDamage').textContent,skin:$('titanSkinState').textContent,growHidden:$('titanGrow').hidden,stopVisible:!$('titanStop').hidden};
    $('titanStoneSkin').click();const skinBroken=$('titanSkinState').textContent;
    $('titanStop').click();const stopped=$('titanAttackMode').textContent;
    return {before,enlarged,skinBroken,stopped,scrollWidth:document.documentElement.scrollWidth,viewportWidth:window.innerWidth};
  });
  assert.deepEqual(ux.before,{mode:'Taille normale',damage:'1d8+7',stopHidden:true});
  assert.equal(ux.enlarged.mode,'AGRANDI');
  assert.equal(ux.enlarged.damage,'2d8+7');
  assert.match(ux.enlarged.skin,/Active/);
  assert.equal(ux.enlarged.growHidden,true);
  assert.equal(ux.enlarged.stopVisible,true);
  assert.match(ux.skinBroken,/Rompue/);
  assert.equal(ux.stopped,'Taille normale');
  assert.ok(ux.scrollWidth<=ux.viewportWidth+2,'no horizontal overflow at '+width+'px: '+ux.scrollWidth+' > '+ux.viewportWidth);
  assert.deepEqual(errors,[],'no browser runtime errors');
  await page.close();
 }
 console.log('Level 11 browser smoke passed:',process.env.E2E_BROWSER||'chromium');
}finally{await browser?.close();await new Promise(ok=>server.close(ok))}
