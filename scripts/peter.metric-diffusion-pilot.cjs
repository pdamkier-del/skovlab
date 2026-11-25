// Standalone geometry-derived diffusion toy experiment. Does NOT modify forest rules.
// Surface embedding z(x,y) = A exp(-r^2/(2 sigma^2)), unit lattice coordinate steps.
// Horizontal edge length is approximately sqrt(1+(Delta z)^2); w=1/length^2.
// This is an edge-conductance proxy, not a fully consistent finite-volume Laplace-Beltrami scheme.
const L=31,A=7,sigma=6,rate=.18,sweeps=200,mid=(L-1)/2;
const z=Array.from({length:L*L},(_,i)=>{const x=Math.floor(i/L)-mid,y=i%L-mid;return A*Math.exp(-(x*x+y*y)/(2*sigma*sigma));});
const edges=[];
for(let i=0;i<L;i++)for(let j=0;j<L;j++){
 const a=i*L+j;
 for(const [di,dj] of [[1,0],[0,1]]){const ii=i+di,jj=j+dj;if(ii>=L||jj>=L)continue;
  const b=ii*L+jj,w=1/(1+(z[a]-z[b])**2);edges.push({a,b,w});}
}
const meanW=edges.reduce((s,e)=>s+e.w,0)/edges.length;
function run(start,mode){
 let E=new Float64Array(L*L);E[start]=1;const output=[];
 const sx=Math.floor(start/L),sy=start%L;
 for(let t=0;t<=sweeps;t++){
  if([0,20,50,100,200].includes(t)){
   let energy=0,msd=0,max=0,atStart=E[start];
   for(let i=0;i<E.length;i++){const dx=Math.floor(i/L)-sx,dy=i%L-sy;
    energy+=E[i];msd+=E[i]*(dx*dx+dy*dy);max=Math.max(max,E[i]);}
   output.push({t,energy,msd,atStart,max});
  }
  if(t===sweeps)break;
  const delta=new Float64Array(E.length);
  for(const e of edges){const w=mode==="flat"?1:mode==="uniform"?meanW:mode==="renormalized"?e.w/meanW:e.w;
   const f=rate*w*(E[e.a]-E[e.b]);delta[e.a]-=f;delta[e.b]+=f;}
  for(let i=0;i<E.length;i++)E[i]+=delta[i];
  if(E.some(v=>!Number.isFinite(v)||v < -1e-12))throw Error("Nonphysical energy in "+mode);
 }
 return output;
}
const results=[];
for(const [label,start] of [["center",15*L+15],["slope",15*L+21]])
 for(const mode of ["flat","uniform","metric","renormalized"]){
 const snapshots=run(start,mode);
 if(snapshots.some(v=>Math.abs(v.energy-1)>1e-9))throw Error("Conservation fail");
 results.push({label,mode,snapshots});
 }
const at=(label,mode,t)=>results.find(r=>r.label===label&&r.mode===mode).snapshots.find(s=>s.t===t);
const contrasts=[50,100,200].map(t=>({t,center:{
  flat:at("center","flat",t).msd,metric:at("center","metric",t).msd,
  uniform:at("center","uniform",t).msd,renormalized:at("center","renormalized",t).msd},
  slope:{flat:at("slope","flat",t).msd,metric:at("slope","metric",t).msd,
  uniform:at("slope","uniform",t).msd,renormalized:at("slope","renormalized",t).msd}}));
const output={protocol:{L,A,sigma,rate,sweeps,energy:1,
  explanation:"Surface gradient changes effective horizontal distance and conductances; a proxy not GR, not full Laplace-Beltrami"},
  edges:edges.length,weightMin:Math.min(...edges.map(e=>e.w)),weightMax:Math.max(...edges.map(e=>e.w)),
  weightMean:meanW,contrasts,results};
console.log("SKOV_METRIC_DIFFUSION_START");
console.log(JSON.stringify(output,null,2));
console.log("SKOV_METRIC_DIFFUSION_END");
