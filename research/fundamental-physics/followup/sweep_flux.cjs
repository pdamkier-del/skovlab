const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {loadModel}=require("../model.cjs");
const out=process.argv[2]||path.join(__dirname,"results");
fs.mkdirSync(out,{recursive:true});
const rows=["seed,t,stage,dQ,dE,dU,dTrees"];
let previous,seed;
const model=loadModel("index.html",(stage,t,state)=>{
  if(t<1201)return;
  const current=[state.pool,state.reserveTotal,state.potentialTotal,state.total];
  if(stage!=="before"){
    const delta=current.map((value,i)=>value-previous[i]);
    assert.ok(Math.abs(delta[0]+delta[1]+delta[2])<1e-8);
    rows.push([seed,t,stage,...delta.map((v,i)=>v/(i<3?100:1))].join(","));
  }
  previous=current;
});
for(seed=1;seed<=8;seed++){
  model.init({L:10,seed,climateAmplitude:0,growthPriceAmplitude:0,spreadPriceAmplitude:0,
    maintenanceAmplitude:0,spontaneousMutation:0});
  for(let t=1;t<=1600;t++)model.step();
}
fs.writeFileSync(path.join(out,"sweep_flux.csv"),rows.join("\n")+"\n");
