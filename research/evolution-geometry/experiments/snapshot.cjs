const fs=require("node:fs");
const path=require("node:path");
const assert=require("node:assert/strict");
const {loadModel}=require("../../fundamental-physics/model.cjs");
const out=process.argv[2]||path.join(__dirname,"../results");
const geometry=+process.argv[3];
fs.mkdirSync(out,{recursive:true});
const model=loadModel("index.html");
const data=[];
for(const L of [12,20,28])for(let seed=1;seed<=12;seed++){
  for(const treatment of ["mutation","no_mutation"]){
    model.init({L,seed,curvature:geometry,climateAmplitude:0,growthPriceAmplitude:0,
      spreadPriceAmplitude:0,maintenanceAmplitude:0,
      birthMutation:treatment==="mutation"?.015:0,
      spontaneousMutation:treatment==="mutation"?.025:0});
    const edges=[];
    for(let i=0;i<L*L;i++)for(const j of model.neighbours(i))if(j>i)edges.push([i,j]);
    for(let t=0;t<=260;t++){
      if([0,20,60,120,260].includes(t)){
        const s=model.stats(),{sp,en,strategies}=model.state();
        assert.ok(Math.abs(s.balanceError)<1e-6);
        data.push({geometry,L,seed,t,treatment,edges:t===0?edges:null,
          labels:Array.from(sp),strategies,density:s.density,reserve:s.reserveTotal/(L*L),balance:s.balanceError});
      }
      if(t<260)model.step();
    }
  }
}
fs.writeFileSync(path.join(out,"snapshots_"+geometry+".json"),JSON.stringify(data));
console.log(geometry,data.length);
