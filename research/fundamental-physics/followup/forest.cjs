const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const {loadModel} = require("../model.cjs");

const scenarios = [
  ["shared", "index.html", "original", {}],
  ["peter", "peter/index.html", "original", {}],
  ["peter", "peter/index.html", "bounded", {maxHeight: 8}],
  ["peter", "peter/index.html", "no_diffusion", {maxHeight: 8, alpha: 0}],
  ["peter", "peter/index.html", "no_combat", {maxHeight: 8, attackCost: 1000000}],
];
const directory = process.argv[2] || path.join(__dirname, "results");
const selection = process.argv[3];
fs.mkdirSync(directory, {recursive: true});
for (const [version, file, scenario, parameters] of scenarios) {
  if (selection && selection !== version + "_" + scenario) continue;
  const output = path.join(directory, version + "_" + scenario + ".csv");
  const model = loadModel(file);
  const rows = ["L,seed,t,reserve,structure,pool,variance,roughness,height,live,up,down,balance"];
  for (const L of [10, 20]) for (let seed=1; seed<=16; seed++) {
    model.init({L, seed, ...parameters, climateNoise:0, climateAmplitude:0,
      growthPriceAmplitude:0, spreadPriceAmplitude:0, maintenanceAmplitude:0,
      // Preserve default birth mutation in each full model.
      spontaneousMutation:0});
    const maxT = scenario==="original" ? 2400 : 1800;
    for(let t=0;t<=maxT;t++) {
      if(t%2===0){
        const s=model.stats(), {en,u}=model.state(), N=L*L;
        const mean=s.reserveTotal/N;
        let variance=0, roughness=0, up=0, down=0;
        for(let k=0;k<N;k++){
          variance+=(en[k]-mean)**2;
          roughness+=(en[k]-en[k%L===L-1?k-L+1:k+1])**2;
          if(k<N/2) up+=en[k]+u[k];
          else down+=en[k]+u[k];
        }
        assert.ok(Math.abs(s.balanceError)<1e-6);
        rows.push([L,seed,t,mean,s.potentialTotal/N,s.pool/N,variance/N,roughness/N,
          s.meanHeight,s.total/N,2*up/N,2*down/N,s.balanceError].join(","));
      }
      if(t<maxT) model.step();
    }
  }
  fs.writeFileSync(output, rows.join("\n")+"\n");
  console.log(output,rows.length-1);
}
