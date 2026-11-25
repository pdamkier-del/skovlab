const path=require("node:path");
const fs=require("node:fs");
const assert=require("node:assert/strict");
const {loadModel}=require("../model.cjs");
const model=loadModel("peter/index.html");
const out=process.argv[2]||path.join(__dirname,"results");
const policy=process.argv[3];
fs.mkdirSync(out,{recursive:true});
for(const floor of [0,1e-12,1e-8]){
  if(policy!==undefined && +policy!==floor)continue;
  const rows=["L,floor,seed,t,density,height,reserve,structure,nearzero,zero,max_height,balance"];
  for(const L of [10,20])for(let seed=1;seed<=8;seed++){
    model.init({L,seed,maxHeight:8,climateNoise:0,climateAmplitude:0,growthPriceAmplitude:0,
      spreadPriceAmplitude:0,maintenanceAmplitude:0,spontaneousMutation:0});
    for(let t=0;t<=1600;t++){
      const {sp,h}=model.state();
      if(floor>0)for(let i=0;i<h.length;i++)if(sp[i]>=0&&h[i]<floor)model.killTree(i);
      if(t%20===0){
        const s=model.stats(), n=h.length;
        let nearzero=0,zero=0;
        for(let i=0;i<n;i++)if(sp[i]>=0){
          nearzero+=h[i]<1e-8;
          zero+=h[i]===0;
        }
        assert.ok(Math.abs(s.balanceError)<1e-6);
        rows.push([L,floor,seed,t,s.density,s.meanHeight,s.reserveTotal/n,s.potentialTotal/n,
          nearzero/n,zero/n,s.highest,s.balanceError].join(","));
      }
      if(t<1600)model.step();
    }
  }
  fs.writeFileSync(path.join(out,"height_"+floor+".csv"),rows.join("\n")+"\n");
}
