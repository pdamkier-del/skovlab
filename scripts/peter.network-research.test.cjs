const {test,before,after}=require("node:test");
const assert=require("node:assert/strict");
const {chromium}=require("playwright");
let browser,page;
before(async()=>{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||chromium.executablePath(),args:["--no-sandbox"]});
 page=await browser.newPage({viewport:{width:1000,height:800}});
 const errors=[];page.on("pageerror",e=>errors.push(e.message));
 await page.goto(process.env.SKOV_URL||"http://127.0.0.1:8000/");
 await page.waitForFunction(()=>!!window.__skovTest);
 assert.deepEqual(errors,[]);
});
after(async()=>{if(browser)await browser.close()});
test("scientific network metrics follow same-species live edges, not immune against attack",async()=>{
 const x=await page.evaluate(()=>{
  __skovTest.fixture({strategies:[.2,.8],sigmas:[0,0],cfg:{L:10,curvature:0,neighbors:4,periodic:false,alpha:.1,betHedging:true,energyEnabled:true},trees:{0:[0,1,5],1:[0,1,5],2:[1,1,5],10:[0,1,5]},pool:30});
  const m=__skovTest.activeNetworkMetrics();return{m,s:__skovTest.snapshot(),adj:__skovTest.external(1,0)};
 });
 assert.equal(x.m.liveTrees,4);
 assert.equal(x.m.liveComponents,2);
 assert.equal(x.m.largestShare,.75);
 assert.equal(x.m.activeEdges,2);
 assert.ok(x.adj.includes(2),"different species can be attacked");
 assert.ok(x.adj.includes(0),"same species can also be attacked in existing physics");
 assert.equal(x.s.config.alpha,.1);
});
test("live research section shows graph and faithful metric labels",async()=>{
 await page.evaluate(()=>{
  document.getElementById("size").value=10;
  document.getElementById("seed").value=19;
  __skovTest.restart();for(let i=0;i<31;i++)__skovTest.step();__skovTest.draw();
 });
 await page.locator("#networkResearch summary").click();
 assert.ok(await page.locator("#networkHistoryPlot").evaluate(el=>el.width>40&&el.height>40));
 const snap=await page.evaluate(()=>__skovTest.snapshot());
 const m=await page.evaluate(()=>__skovTest.activeNetworkMetrics());
 assert.ok(snap.history.length>3);
 assert.ok(snap.history.some(v=>Number.isFinite(v.netEdges)&&Number.isFinite(v.netLargest)));
 assert.equal(await page.locator("#netComponentsOut").innerText(),String(m.liveComponents));
 assert.equal(await page.locator("#netEdgesOut").innerText(),(m.edgeFraction*100).toFixed(1)+" %");
 assert.ok(Math.abs(snap.balanceError)<1e-6);
});
