const {chromium}=require('playwright');
const {spawn}=require('node:child_process');
const assert=require('node:assert/strict');
(async()=>{
 const server=spawn('python3',['-m','http.server','8769','--bind','127.0.0.1'],{stdio:'ignore'});
 let browser;
 try{
  for(let i=0;i<50;i++){try{if((await fetch('http://127.0.0.1:8769/')).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
  browser=await chromium.launch({headless:true,...(require('fs').existsSync('/usr/bin/chromium')?{executablePath:'/usr/bin/chromium'}:{})});const page=await browser.newPage({viewport:{width:1280,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8769/research/ec-dirac-collapse/');
  await page.waitForFunction(()=>document.querySelector('#h0').textContent.includes('e'));
  assert.match(await page.locator('#stop').textContent(),/demonstrationsgrænsen/);
  assert.match(await page.locator('#outcome').textContent(),/Intet volumenbounce/);
  assert.equal(await page.locator('canvas').count(),3);
  await page.screenshot({path:'/tmp/ec-dirac-desktop.png',fullPage:true});
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#export').click()]);assert.equal(download.suggestedFilename(),'ecd-lrs-solution.json');
  await download.saveAs('/tmp/ec-dirac-export.json');const exported=JSON.parse(require('fs').readFileSync('/tmp/ec-dirac-export.json','utf8'));assert.ok(exported.rows.length>100);assert.equal(exported.bounce,false);
  await page.locator('#mass').fill('1');await page.locator('button[type=submit]').click();assert.match(await page.locator('#error').textContent(),/overskrider/);assert.equal(await page.locator('#export').isDisabled(),true);
  await page.locator('#mass').fill('0.001');await page.locator('button[type=submit]').click();assert.equal(await page.locator('#error').textContent(),'');
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/ec-dirac-mobile.png',fullPage:true});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);console.log('PASS desktop/mobile, plots, export, invalid input and recovery; no page errors');
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
