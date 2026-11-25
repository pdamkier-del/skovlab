// Longitudinal held-out spectral-network predictability study. Unmodified forest engine.
// Predict future species entropy from the frozen same-lineage diffusion network,
// comparing a baseline using current entropy, occupancy, richness, and mean strategy.
// No eigenvalue claim: graph topology is a cheap spectral proxy (component count = nullity).
const {chromium}=require("playwright");
const seeds=[11,23,37,47,59,71,83,97,103,127,149,167,191,211,227,241,263,281,307,331];
const sizes=[10,20],climates=[0,.6],times=[100,200,300],lag=100;
function metrics(sp,adj) {
 const N=sp.length,seen=new Uint8Array(N);
 let edges=0,allEdges=0,components=0,largest=0,live=0;
 for(let i=0;i<N;i++) {
  if(sp[i]>=0)live++;
  for(const j of adj[i])if(i<j){
   allEdges++;
   if(sp[i]>=0 && sp[i]===sp[j])edges++;
  }
 }
 for(let i=0;i<N;i++)if(sp[i]>=0&&!seen[i]){
  components++;let count=0;const stack=[i];seen[i]=1;
  for(let k=0;k<stack.length;k++){
   const v=stack[k];count++;
   for(const j of adj[v])if(sp[j]===sp[v]&&!seen[j]){seen[j]=1;stack.push(j);}
  }
  largest=Math.max(largest,count);
 }
 return{activeEdgeFraction:allEdges?edges/allEdges:0,components,
  largestComponentShare:live?largest/live:0,componentPerTree:live?components/live:0};
}
function gauss(A,b){
 const n=b.length;A=A.map((row,i)=>[...row,b[i]]);
 for(let j=0;j<n;j++){
  let p=j;for(let i=j+1;i<n;i++)if(Math.abs(A[i][j])>Math.abs(A[p][j]))p=i;
  [A[j],A[p]]=[A[p],A[j]];
  if(Math.abs(A[j][j])<1e-14)return null;
  let v=A[j][j];for(let k=j;k<=n;k++)A[j][k]/=v;
  for(let i=0;i<n;i++)if(i!==j){v=A[i][j];for(let k=j;k<=n;k++)A[i][k]-=v*A[j][k];}
 }
 return A.map(row=>row[n]);
}
function fitRidge(rows,features,lambda=5){
 const mu=features.map(k=>rows.reduce((s,r)=>s+r[k],0)/rows.length);
 const sd=features.map((k,j)=>Math.sqrt(rows.reduce((s,r)=>s+(r[k]-mu[j])**2,0)/rows.length)||1);
 const XX=Array.from({length:features.length+1},()=>Array(features.length+1).fill(0));
 const XY=Array(features.length+1).fill(0);
 for(const r of rows){
  const x=[1,...features.map((k,j)=>(r[k]-mu[j])/sd[j])];
  for(let i=0;i<x.length;i++){XY[i]+=x[i]*r.target;
   for(let j=0;j<x.length;j++)XX[i][j]+=x[i]*x[j];}
 }
 for(let j=1;j<XX.length;j++)XX[j][j]+=lambda;
 const beta=gauss(XX,XY);
 return r=>beta[0]+features.reduce((s,k,j)=>s+beta[j+1]*(r[k]-mu[j])/sd[j],0);
}
function assess(rows,predict){
 const ae=rows.map(r=>Math.abs(predict(r)-r.target));
 const se=rows.map(r=>(predict(r)-r.target)**2);
 return {n:rows.length,mae:ae.reduce((a,b)=>a+b,0)/ae.length,
  rmse:Math.sqrt(se.reduce((a,b)=>a+b,0)/se.length)};
}
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||chromium.executablePath(),args:["--no-sandbox"]});
 try {
 const page=await browser.newPage({viewport:{width:800,height:720}});
 await page.goto(process.env.SKOV_URL||"http://127.0.0.1:8000/");
 await page.waitForFunction(()=>!!window.__skovTest);
 const rows=[];
 for(const size of sizes)for(const climateNoise of climates)for(const seed of seeds){
  const record=await page.evaluate(({size,climateNoise,seed,times,lag})=>{
   const fields={size,species:8,fill:.55,seed,neighbors:4,alpha:.1,
    energyInput:1,climateAmplitude:.5,climatePeriod:80,energyPhase:0,climateNoise,
    growthCost:2,growthPriceAmplitude:.5,growthPhase:180,attackCost:1,
    spreadPriceAmplitude:.5,spreadPhase:180,maintenancePerHeight:.1,
    maintenanceAmplitude:.5,maintenancePhase:180,startEnergy:10,offspringEnergy:2,
    birthMutation:.1,spontaneousMutation:0,mutationEpsilon:.05,
    betHedging:"1",hedgeWidth:.25,maxHeight:0};
   for(const [id,v] of Object.entries(fields))document.getElementById(id).value=String(v);
   document.getElementById("curvature").value="0";document.getElementById("periodic").checked=true;
   __skovTest.restart();const start=__skovTest.snapshot();
   if(start.config.L!==size)throw Error("L mismatch");
   const adj=Array.from({length:start.sp.length},(_,i)=>__skovTest.neighbours(i));
   const records={};let err=0;
   for(let t=1;t<=Math.max(...times)+lag;t++){
    __skovTest.step();if(!times.includes(t)&&!times.includes(t-lag))continue;
    const s=__skovTest.snapshot();err=Math.max(err,Math.abs(s.totalEnergy-start.totalEnergy));
    records[t]={H:s.entropy,species:s.alive,rho:s.density,meanStrategy:s.meanStrategy,
       sp:s.sp,edgeNeighbours:adj};
   }
   if(err>1e-6)throw Error("Energy drift "+err);
   return records;
  },{size,climateNoise,seed,times,lag});
  for(const t of times){const now=record[t],then=record[t+lag],g=metrics(now.sp,now.edgeNeighbours);
   rows.push({size,climateNoise,seed,t,H:now.H,species:now.species,rho:now.rho,
    meanStrategy:now.meanStrategy,...g,target:then.H,targetSpecies:then.species,
    deltaH:then.H-now.H});}
 }
 const training=rows.filter(r=>seeds.indexOf(r.seed)<12),held=rows.filter(r=>seeds.indexOf(r.seed)>=12);
 const base=["H","species","rho","meanStrategy","size","climateNoise","t"],
   topology=["activeEdgeFraction","componentPerTree","largestComponentShare"];
 const modelA=fitRidge(training,base),modelB=fitRidge(training,[...base,...topology]);
 const modelC=fitRidge(training,["H","species","rho","meanStrategy","size","climateNoise","t",...topology.slice(0,2)]);
 const output={
  protocol:{seeds,sizes,climates,times,lag,trainingSeeds:seeds.slice(0,12),heldoutSeeds:seeds.slice(12),
    measure:"Shannon genetic species H at t+100",
    baseline:base,extended:[...base,...topology],
    caveat:"Topological metrics are derived from CURRENT species labels; check incremental predictive value over richness/H"},
  results:{persistence:assess(held,r=>r.H),baseline:assess(held,modelA),
   extended:assess(held,modelB),extendedWithoutLargest:assess(held,modelC)},
  bySize:sizes.map(size=>({size,persistence:assess(held.filter(r=>r.size===size),r=>r.H),
   baseline:assess(held.filter(r=>r.size===size),modelA),
   extended:assess(held.filter(r=>r.size===size),modelB)})),
  byClimate:climates.map(climateNoise=>({climateNoise,baseline:assess(held.filter(r=>r.climateNoise===climateNoise),modelA),
   extended:assess(held.filter(r=>r.climateNoise===climateNoise),modelB)})),
  snapshots:rows.length,
  averages:{activeEdges:rows.reduce((a,x)=>a+x.activeEdgeFraction,0)/rows.length,
   liveComponents:rows.reduce((a,x)=>a+x.components,0)/rows.length,
   largestShare:rows.reduce((a,x)=>a+x.largestComponentShare,0)/rows.length},
  heldout:held.map(r=>({size:r.size,climateNoise:r.climateNoise,seed:r.seed,t:r.t,H:r.H,
     target:r.target,basePrediction:modelA(r),spectralPrediction:modelB(r),
     components:r.components,activeEdgeFraction:r.activeEdgeFraction,
     largestComponentShare:r.largestComponentShare}))
 };
 console.log("SKOV_PREDICT_START");console.log(JSON.stringify(output,null,2));console.log("SKOV_PREDICT_END");
 await page.close();
 }finally{await browser.close();}
})().catch(err=>{console.error(err);process.exitCode=1;});
