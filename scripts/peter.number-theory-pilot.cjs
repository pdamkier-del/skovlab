// Numerical pilot of reserve-energy rank spectra in the UNMODIFIED Skovlaboratoriet engine.
// Descriptive rank regressions only, NOT Clauset-style power-law tests.
// Same-seed paired conditions, three lattice sizes and two controls.
// To run: node scripts/peter.number-theory-pilot.cjs (serve index.html on port 8000).
const {chromium}=require("playwright");
const seeds=[11,23,37,47],sizes=[10,20,30],climates=[0,.6],diffusions=[0,.1];
function regress(x,y,power){const n=x.length,k=power+1;
 let A=Array.from({length:k},()=>new Array(k+1).fill(0));
 for(let i=0;i<n;i++){let p=Array.from({length:k},(_,j)=>x[i]**j);for(let j=0;j<k;j++){A[j][k]+=p[j]*y[i];for(let q=0;q<k;q++)A[j][q]+=p[j]*p[q];}}
 for(let j=0;j<k;j++){let v=j;for(let i=j+1;i<k;i++)if(Math.abs(A[i][j])>Math.abs(A[v][j]))v=i;[A[v],A[j]]=[A[j],A[v]];if(Math.abs(A[j][j])<1e-14)return null;let z=A[j][j];for(let q=j;q<=k;q++)A[j][q]/=z;for(let i=0;i<k;i++)if(i!==j){z=A[i][j];for(let q=j;q<=k;q++)A[i][q]-=z*A[j][q];}}
 const beta=A.map(row=>row[k]),prediction=x.map(xx=>beta.reduce((z,b,j)=>z+b*xx**j,0));
 const sse=y.reduce((z,v,i)=>z+(v-prediction[i])**2,0),mean=y.reduce((a,b)=>a+b,0)/n,tss=y.reduce((z,v)=>z+(v-mean)**2,0);
 return{beta,rmse:Math.sqrt(sse/n),r2:tss>0?1-sse/tss:1,sse};
}
function fitRank(energies){const arr=energies.filter(v=>v>1e-9).sort((a,b)=>b-a),n=arr.length;if(n<20)return{n};
 const x=arr.map((_,i)=>Math.log(i+1)),y=arr.map(Math.log),fraction=arr.map((_,i)=>(i+1)/n);
 const pow=regress(x,y,1),quadratic=regress(x,y,2),exp=regress(fraction,y,1);
 const first=Math.max(2,Math.floor(.1*n)),last=Math.max(first+2,Math.floor(.8*n));
 const tail=regress(x.slice(first,last),y.slice(first,last),1);
 return{n,alpha:-pow.beta[1],r2:pow.r2,rmsePower:pow.rmse,rmseCurved:quadratic.rmse,
  curvature:quadratic.beta[2],rmseExp:exp.rmse,midAlpha:tail?-tail.beta[1]:null,
  energyTop:arr[0],energyMedian:arr[Math.floor(n/2)],energyMin:arr[n-1],
  top10Share:arr.slice(0,Math.ceil(n*.1)).reduce((a,b)=>a+b,0)/arr.reduce((a,b)=>a+b,0)};
}
function spectralTorus(N){let eigen=[];for(let k=0;k<N;k++)for(let j=0;j<N;j++){const v=4-2*Math.cos(2*Math.PI*k/N)-2*Math.cos(2*Math.PI*j/N);if(v>1e-10)eigen.push(v);}
 return{N,nonzero:eigen.length,lambda2:Math.min(...eigen),zeta1:eigen.reduce((s,v)=>s+1/v,0),zeta2:eigen.reduce((s,v)=>s+1/v**2,0),lambdaMax:Math.max(...eigen)};}
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||chromium.executablePath(),args:["--no-sandbox"]});
 try {
 const page=await browser.newPage({viewport:{width:800,height:720}});
 await page.goto(process.env.SKOV_URL||"http://127.0.0.1:8000/");
 await page.waitForFunction(()=>!!window.__skovTest);
 const rows=[];
 for(const size of sizes)for(const climateNoise of climates)for(const alpha of diffusions)for(const seed of seeds){
  const r=await page.evaluate(({size,climateNoise,alpha,seed})=>{
   const config={size,species:8,fill:.55,seed,neighbors:4,alpha,energyInput:1,
     climateAmplitude:.5,climatePeriod:80,energyPhase:0,climateNoise,
     growthCost:2,growthPriceAmplitude:.5,growthPhase:180,attackCost:1,
     spreadPriceAmplitude:.5,spreadPhase:180,maintenancePerHeight:.1,
     maintenanceAmplitude:.5,maintenancePhase:180,startEnergy:10,offspringEnergy:2,
     birthMutation:.1,spontaneousMutation:0,mutationEpsilon:.05,
     betHedging:"1",hedgeWidth:.25,maxHeight:0};
   for(const [id,value] of Object.entries(config)){const el=document.getElementById(id);if(!el)throw Error("Missing "+id);el.value=String(value);}
   document.getElementById("curvature").value="0";document.getElementById("periodic").checked=true;
   __skovTest.restart();const start=__skovTest.snapshot();if(start.config.L!==size)throw Error("Grid mismatch");
   const snaps=[];let maxError=0;
   for(let t=1;t<=500;t++){
    __skovTest.step();if(t!==300&&t!==400&&t!==500)continue;
    const s=__skovTest.snapshot();maxError=Math.max(maxError,Math.abs(s.totalEnergy-start.totalEnergy));
    const reserves=[],totals=[];for(let i=0;i<s.sp.length;i++)if(s.sp[i]>=0){reserves.push(s.en[i]);totals.push(s.en[i]+s.u[i]);}
    // Avoid returning field-level arrays from GitHub Actions.
    snaps.push({t,living:s.total,aliveSpecies:s.alive,H:s.entropy,traitH:s.traitEntropy,
      meanStrategy:s.meanStrategy,density:s.density,poolFrac:s.pool/s.totalEnergy,
      reserve:reserves,total:totals});
   }
   if(maxError>1e-6)throw Error("Energy conservation failed "+maxError);
   return{size,seed,climateNoise,alpha,actualL:start.config.L,actualAlpha:start.config.alpha,
     maxError,snaps};
  },{size,climateNoise,alpha,seed});
  for(const z of r.snaps){rows.push({size,seed,climateNoise,alpha,t:z.t,living:z.living,
    species:z.aliveSpecies,entropy:z.H,traitEntropy:z.traitH,meanStrategy:z.meanStrategy,density:z.density,
    poolFrac:z.poolFrac,maxError:r.maxError,reserve:fitRank(z.reserve),total:fitRank(z.total)});}
 }
 const summary=[];
 for(const size of sizes)for(const climateNoise of climates)for(const alpha of diffusions){
   const subset=rows.filter(x=>x.size===size&&x.climateNoise===climateNoise&&x.alpha===alpha);
   const mean=key=>{const values=subset.map(x=>key(x)).filter(x=>Number.isFinite(x));return values.length?values.reduce((a,b)=>a+b,0)/values.length:null;};
   summary.push({size,climateNoise,alpha,measurements:subset.length,seeds:seeds.length,
     living:mean(x=>x.living),density:mean(x=>x.density),species:mean(x=>x.species),
     H:mean(x=>x.entropy),traitH:mean(x=>x.traitEntropy),meanStrategy:mean(x=>x.meanStrategy),
     alphaReserve:mean(x=>x.reserve.alpha),alphaTotal:mean(x=>x.total.alpha),
     fitR2Reserve:mean(x=>x.reserve.r2),fitRmsePower:mean(x=>x.reserve.rmsePower),
     fitRmseCurved:mean(x=>x.reserve.rmseCurved),fitRmseExponential:mean(x=>x.reserve.rmseExp),
     curvature:mean(x=>x.reserve.curvature),top10Share:mean(x=>x.reserve.top10Share),
     energyErrorMax:Math.max(...subset.map(x=>x.maxError))});
 }
 const spectral=sizes.map(spectralTorus);
 console.log("SKOV_ZETA_PILOT_START");
 console.log(JSON.stringify({protocol:{seeds,sizes,climates,diffusions,
  sweeps:500,snapshotSweeps:[300,400,500],engine:"original unmodified peter-dev/index.html",
  rankFit:"OLS log E vs log rank, evaluated on SAME data; descriptive not model confirmation",
  curvedFit:"quadratic log(rank), not a direct lognormal likelihood",
  spectralReference:"exact eigenvalues for FLAT degree-4 periodic lattice only; NOT dynamic diffusion graph"},
  summary,spectral,rows},null,2));
 console.log("SKOV_ZETA_PILOT_END");
 await page.close();
 }finally{await browser.close();}
})().catch(err=>{console.error(err);process.exitCode=1;});
