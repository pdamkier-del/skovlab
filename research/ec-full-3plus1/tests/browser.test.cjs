const {chromium}=require('playwright'),{spawn}=require('node:child_process'),assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{const server=spawn('python',['research/ec-full-3plus1/server.py','--port','8771'],{stdio:'ignore'});let browser;
 try{for(let i=0;i<60;i++){try{if((await fetch('http://127.0.0.1:8771/api/status')).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
 browser=await chromium.launch({headless:true,...(fs.existsSync('/usr/bin/chromium')?{executablePath:'/usr/bin/chromium'}:{})});const page=await browser.newPage({viewport:{width:1280,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('http://127.0.0.1:8771/');await page.waitForFunction(()=>!document.querySelector('#run').disabled);
 assert.match(await page.locator('#availability').textContent(),/tilsluttet/);assert.equal(await page.locator('canvas').count(),4);
 await page.locator('#n').selectOption('7');await page.locator('#spin_twist').fill('1.1');await page.locator('#run').click();await page.waitForFunction(()=>document.querySelector('#availability').textContent.includes('afsluttet'),{timeout:90000});
 assert.equal(await page.locator('#error').textContent(),'');assert.match(await page.locator('#conservation').textContent(),/343/);
 const bad=await page.request.post('http://127.0.0.1:8771/api/run',{data:{amplitude:1}});assert.equal(bad.status(),400);
 const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#export').click()]);await download.saveAs('/tmp/full-ecd-export.json');const json=JSON.parse(fs.readFileSync('/tmp/full-ecd-export.json','utf8'));assert.equal(json.parameters.n,7);assert.equal(json.parameters.spin_twist,1.1);assert.equal(json.bounce,'not-assessed');assert.ok(json.rows.length>1);
 await page.screenshot({path:'/tmp/full-ecd-desktop.png',fullPage:true});await page.setViewportSize({width:390,height:844});await page.locator('#time-slider').fill('0');assert.equal(await page.locator('#time').textContent(),'0.000');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:'/tmp/full-ecd-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);console.log('PASS desktop/mobile, actual backend solve, changed spin profile, rejected data, slice and export.');
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
