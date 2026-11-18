const {test,before,after}=require("node:test");
const assert=require("node:assert/strict");
const {chromium}=require("playwright");
let browser,page;
before(async()=>{browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||chromium.executablePath(),args:["--no-sandbox"]});page=await browser.newPage();const errors=[];page.on("pageerror",e=>errors.push(e.message));await page.goto(process.env.SKOV_URL||"http://127.0.0.1:8000/");await page.waitForFunction(()=>!!window.__skovTest);assert.deepEqual(errors,[]);});
after(async()=>browser?.close());
const run=(fn,args)=>page.evaluate(fn,args);
test("no immunity between identical or similar species, including own lineage",async()=>{
 const result=await run(()=>{
  __skovTest.fixture({strategies:[.45,.46],sigmas:[0,0],trees:{0:[0,2,10],1:[0,2,10],10:[1,2,10]},pool:100,cfg:{L:10,curvature:0,neighbors:4,periodic:false,alpha:0,energyEnabled:true,betHedging:true,hedgeWidth:0,spontaneousMutation:0,birthMutation:0,attackCost:1,growthCost:2,maintenancePerHeight:0}});
  return {targets:__skovTest.external(0,0),s:__skovTest.snapshot()};
 });
 assert.ok(result.targets.includes(1),"same-species neighbor should be attackable");
 assert.ok(result.targets.includes(10),"similar other species should be attackable");
 assert.equal(await page.locator("#deltaS").count(),0);
 assert.equal(await page.locator("#betHedging").count(),1);
});
test("hedged offspring are variable but remain inside inherited bounds",async()=>{
 const x=await run(()=>{
  __skovTest.fixture({strategies:[.5],sigmas:[.2],cfg:{L:10,curvature:0,betHedging:true,birthMutation:0},random:undefined});
  const draws=Array.from({length:300},()=>__skovTest.offspringTrait(0));
  const s=__skovTest.snapshot();
  return {draws,s};
 });
 assert.equal(x.s.sigmas[0],.2);
 assert.ok(x.draws.every(v=>v>=.3-1e-12&&v<=.7+1e-12));
 assert.ok(Math.max(...x.draws)-Math.min(...x.draws)>.25);
});
test("climate shocks vary across cycles, repeat with seed, and vanish at strength 0",async()=>{
 const x=await run(()=>{
  __skovTest.fixture({strategies:[.5],cfg:{L:10,curvature:0,seed:17,climatePeriod:40,climateNoise:.6,energyInput:1,energyEnabled:true}});
  const samples=[0,40,80,120,160].map(t=>__skovTest.climateShock(t));
  const within=__skovTest.climateShock(1)===__skovTest.climateShock(39);
  __skovTest.fixture({strategies:[.5],cfg:{L:10,curvature:0,seed:17,climatePeriod:40,climateNoise:.6}});
  const again=[0,40,80,120,160].map(t=>__skovTest.climateShock(t));
  __skovTest.fixture({strategies:[.5],cfg:{L:10,curvature:0,climateNoise:0}});
  return {samples,within,again,off:__skovTest.climateShock(999)};
 });
 assert.deepEqual(x.samples,x.again);assert.equal(x.within,true);assert.equal(x.off,1);
 assert.ok(new Set(x.samples.map(x=>x.toFixed(5))).size>=3);
});
test("same seed reproduces climate, phenotype distribution and forest trajectory",async()=>{
 const x=await run(()=>{
  const settings={size:12,species:6,fill:.6,seed:42,betHedging:"1",hedgeWidth:.25,climateNoise:.6,spontaneousMutation:0,birthMutation:.1};
  for(const [id,value] of Object.entries(settings))document.getElementById(id).value=String(value);
  function trajectory(){__skovTest.restart();for(let i=0;i<100;i++)__skovTest.step();const s=__skovTest.snapshot();return {sp:s.sp,phenotypes:s.phenotypes,sigmas:s.sigmas,entropy:s.entropy,energy:s.totalEnergy,history:s.history,events:s.events};}
  return [trajectory(),trajectory()];
 });
 assert.deepEqual(x[0],x[1]);
});
test("energy conservation under bet hedging with unpredictable climate and live competition",async()=>{
 for(const k of [0,1,-1]){
  const result=await run(curvature=>{
   const settings={size:12,species:6,fill:.65,seed:23,betHedging:"1",hedgeWidth:.35,climateNoise:.65,spontaneousMutation:0,birthMutation:1,neighbors:"4"};
   for(const [id,value] of Object.entries(settings))document.getElementById(id).value=String(value);
   document.getElementById("curvature").value=String(curvature);__skovTest.restart();
   const b=__skovTest.snapshot().totalEnergy;
   let maxError=0;
   for(let i=0;i<400;i++){__skovTest.step();const s=__skovTest.snapshot();maxError=Math.max(maxError,Math.abs(s.totalEnergy-b));}
   const s=__skovTest.snapshot();return {maxError,s};
  },k);
  assert.ok(result.maxError<1e-7,"energy drift: "+JSON.stringify({k,error:result.maxError}));
  assert.ok(result.s.phenotypes.every(v=>Number.isFinite(v)&&v>=0&&v<=1));
  assert.ok(result.s.sigmas.every(v=>Number.isFinite(v)&&v>=0&&v<=.5));
 }
});
test("hedged birth generates a distinct phenotype with same lineage and parent energy split",async()=>{
 const x=await run(()=>{
  __skovTest.fixture({strategies:[.5],sigmas:[.2],trees:{0:[0,4,12,10,.35]},pool:50,
    cfg:{L:10,curvature:0,neighbors:4,periodic:false,betHedging:true,birthMutation:0,energyEnabled:true,attackCost:0,growthCost:2,maintenancePerHeight:0}});
  const b=__skovTest.snapshot();
  __skovTest.spread(0,1,0);
  return {b,s:__skovTest.snapshot()};
 });
 assert.equal(x.s.sp[1],0);assert.equal(x.s.h[1],2);assert.equal(x.s.en[0],6);assert.equal(x.s.en[1],6);
 assert.ok(x.s.phenotypes[1]>=.3&&x.s.phenotypes[1]<=.7);
 assert.ok(x.s.sigmas[0]===.2);
 assert.ok(Math.abs(x.s.totalEnergy-x.b.totalEnergy)<1e-8);
});
test("strategy diversity and evolutionary charts available in research UI",async()=>{
 await page.evaluate(()=>{document.getElementById("seed").value="12";__skovTest.restart();for(let i=0;i<5;i++)__skovTest.step();__skovTest.draw();});
 assert.equal(await page.locator("#strategyDynamicsPlot").count(),1);
 assert.ok(await page.locator("#strategyDynamicsPlot").evaluate(e=>e.width>20&&e.height>20));
 await page.locator("#studyOutcome").selectOption("traitEntropy");
 assert.ok(await page.locator("#studyOutcomeLabel").innerText().then(v=>v.includes("Strategidiversitet")));
 await page.locator("#studyOutcome").selectOption("sigma");
 assert.ok(await page.locator("#studyOutcomeLabel").innerText().then(v=>v.includes("σ")));
});
