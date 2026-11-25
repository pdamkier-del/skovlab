const path=require("node:path");
const fs=require("node:fs");
const assert=require("node:assert/strict");
const {loadModel}=require("../model.cjs");
const model=loadModel("index.html");
const out=process.argv[2]||path.join(__dirname,"results");
const only=process.argv[3];
fs.mkdirSync(out,{recursive:true});
for(const L of [10,20]){
  if(only!==undefined&&L!==+only)continue;
  const rows=["L,seed,t,reserve,structure,pool,height,live,balance"];
  for(let seed=101;seed<=112;seed++){
    model.init({L,seed,climateNoise:0,climateAmplitude:0,growthPriceAmplitude:0,
      spreadPriceAmplitude:0,maintenanceAmplitude:0,spontaneousMutation:0});
    for(let t=0;t<=3600;t++){
      if(t>=2400){
        const s=model.stats(), n=L*L;
        assert.ok(Math.abs(s.balanceError)<1e-6);
        rows.push([L,seed,t,s.reserveTotal/n,s.potentialTotal/n,s.pool/n,s.meanHeight,s.density,s.balanceError].join(","));
      }
      if(t<3600)model.step();
    }
  }
  fs.writeFileSync(path.join(out,"shared_validation_"+L+".csv"),rows.join("\n")+"\n");
}
