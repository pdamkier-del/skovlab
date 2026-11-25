// Exact symmetric Jacobi eigenspectra for a SMALL frozen forest graph.
// Compares underlying geometry vs ACTUAL live same-lineage diffusion edges.
// No changes to the simulator. The beta/noise and alpha values are controls, not new physics.
const {chromium}=require("playwright");
const seeds=[11,23,37],geometries=[0,1,-1],N=10;
function eigLaplacian(n,edges){
 const M=new Float64Array(n*n);
 for(const [i,j] of edges){M[i*n+i]++;M[j*n+j]++;M[i*n+j]--;M[j*n+i]--;}
 let sweeps=0,lastMax=Infinity;
 for(;sweeps<35;sweeps++){
  let max=0;
  for(let p=0;p<n-1;p++)for(let q=p+1;q<n;q++){
   const pq=p*n+q,a=M[pq],abs=Math.abs(a);
   if(abs>max)max=abs;if(abs<1e-10)continue;
   const tau=(M[q*n+q]-M[p*n+p])/(2*a),t=(tau>=0?1:-1)/(Math.abs(tau)+Math.sqrt(1+tau*tau));
   const c=1/Math.sqrt(1+t*t),s=t*c;
   const app=M[p*n+p],aqq=M[q*n+q];
   M[p*n+p]=app-t*a;M[q*n+q]=aqq+t*a;M[pq]=0;M[q*n+p]=0;
   for(let k=0;k<n;k++)if(k!==p&&k!==q){
    const kp=M[k*n+p],kq=M[k*n+q],np=c*kp-s*kq,nq=s*kp+c*kq;
    M[k*n+p]=np;M[p*n+k]=np;M[k*n+q]=nq;M[q*n+k]=nq;
   }
  }
  lastMax=max;if(max<1e-9)break;
 }
 const eig=Array.from({length:n},(_,i)=>M[i*n+i]).sort((a,b)=>a-b);
 if(eig.some(x=>x<-1e-6))throw Error("Laplacian must be PSD");
 const positive=eig.filter(x=>x>1e-7),zeros=n-positive.length;
 return {nodes:n,edges:edges.length,nonzero:positive.length,zeroModes:zeros,
  lambdaMin:positive.length?positive[0]:null,
  zeta1:positive.reduce((a,x)=>a+1/x,0),zeta2:positive.reduce((a,x)=>a+1/x**2,0),
  traceCheck:eig.reduce((a,x)=>a+x,0)-2*edges.length,maxOffdiag:lastMax,sweeps};
}
function edgesFromSnapshot(snapshot,neighbours,all=false){
 const edges=[];
 for(let i=0;i<snapshot.sp.length;i++)for(const j of neighbours[i]){
  if(i>=j)continue;
  if(all||(snapshot.sp[i]>=0&&snapshot.sp[j]>=0&&snapshot.sp[i]===snapshot.sp[j]))edges.push([i,j]);
 }
 return edges;
}
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||chromium.executablePath(),args:["--no-sandbox"]});
 try {
 const page=await browser.newPage({viewport:{width:750,height:700}});
 await page.goto(process.env.SKOV_URL||"http://127.0.0.1:8000/");
 await page.waitForFunction(()=>!!window.__skovTest);
 const rows=[];
 for(const curvature of geometries)for(const seed of seeds){
  const samples=await page.evaluate(({curvature,seed,N})=>{
   const fields={size:N,species:8,fill:.55,seed,neighbors:4,alpha:.1,
    energyInput:1,climateAmplitude:.5,climateNoise:.6,climatePeriod:80,
    growthCost:2,growthPriceAmplitude:.5,growthPhase:180,attackCost:1,
    spreadPriceAmplitude:.5,spreadPhase:180,maintenancePerHeight:.1,
    maintenanceAmplitude:.5,maintenancePhase:180,startEnergy:10,offspringEnergy:2,
    birthMutation:.1,spontaneousMutation:0,mutationEpsilon:.05,
    betHedging:"1",hedgeWidth:.25,maxHeight:0};
   for(const [id,value] of Object.entries(fields))document.getElementById(id).value=String(value);
   document.getElementById("curvature").value=String(curvature);
   document.getElementById("periodic").checked=true;
   __skovTest.restart();const start=__skovTest.snapshot();
   const neigh=Array.from({length:start.sp.length},(_,i)=>__skovTest.neighbours(i));
   const samples=[{t:0,s:start}];
   for(let i=1;i<=300;i++){__skovTest.step();if(i===150||i===300)samples.push({t:i,s:__skovTest.snapshot()});}
   return{samples,neigh};
  },{curvature,seed,N});
  for(const sample of samples.samples){
   const base=edgesFromSnapshot(sample.s,samples.neigh,true);
   const live=edgesFromSnapshot(sample.s,samples.neigh,false);
   const geom=eigLaplacian(N*N,base),dynamic=eigLaplacian(N*N,live);
   const error=Math.abs(sample.s.totalEnergy-samples.samples[0].s.totalEnergy);
   if(error>1e-6)throw Error("Conservation fail "+error);
   rows.push({curvature,seed,t:sample.t,H:sample.s.entropy,living:sample.s.total,
    species:sample.s.alive,traitH:sample.s.traitEntropy,
    activeEdgeFraction:live.length/base.length,geometry:geom,dynamic,
    energyError:error});
  }
 }
 console.log("SKOV_SPECTRAL_PILOT_START");
 console.log(JSON.stringify({protocol:{seeds,geometries,N,times:[0,150,300],
  graph:"unweighted simple undirected neighbor graph",
  activeEdges:"both live and same species, matching original diffusion eligibility",
  normalization:"unscaled combinatorial Laplacian, actual discrete operator I-dL",
  eigen:"Jacobi diagonalization, zero eigenvalues excluded; zeros encode components"},
  rows},null,2));
 console.log("SKOV_SPECTRAL_PILOT_END");
 await page.close();
 }finally{await browser.close();}
})().catch(err=>{console.error(err);process.exitCode=1;});
