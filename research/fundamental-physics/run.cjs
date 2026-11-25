const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {loadModel} = require('./model.cjs');
const out = path.resolve(process.argv[2] || path.join(__dirname, 'results'));
fs.mkdirSync(out, {recursive: true});
const rows = {};
function save(table, row) {
  (rows[table] ??= []).push(row);
}

function observables(model, block) {
  const {en} = model.state();
  const L = Math.sqrt(en.length);
  const n = L / block;
  const means = new Float64Array(n*n);
  let total = 0;
  let entropy = 0;
  for (let y=0; y<L; y++) for (let x=0; x<L; x++) {
    means[Math.floor(y/block)*n+Math.floor(x/block)] += en[y*L+x];
    total += en[y*L+x];
  }
  let variance = 0;
  let roughness = 0;
  for (let y=0; y<n; y++) for (let x=0; x<n; x++) {
    const e = means[y*n+x];
    variance += (e-total/means.length)**2;
    roughness += (e-means[y*n+(x+1)%n])**2 + (e-means[((y+1)%n)*n+x])**2;
    const p = total ? e/total : 0;
    if (p) entropy -= p*Math.log(p);
  }
  return {mean:total/en.length, variance:variance/means.length/block**4,
    roughness:roughness/means.length/block**4, entropy};
}

for (const file of ['index.html', 'peter/index.html']) {
  const model = loadModel(file);
  for (const L of [12,24,36]) for (let seed=1; seed<=24; seed++) {
    for (const protocol of ['published','constant']) {
      const forcing = protocol === 'constant' ? {
        climateNoise:0, climateAmplitude:0, growthPriceAmplitude:0,
        spreadPriceAmplitude:0, maintenanceAmplitude:0
      } : {};
      model.init({L,seed,...forcing});
      for (let t=0; t<=320; t++) {
        if (t % 4 === 0) {
          const s = model.stats();
          assert.ok(Math.abs(s.balanceError) < 1e-7, JSON.stringify({file,L,seed,t,error:s.balanceError}));
          for (const block of [1,3,6]) save('arrow',{file,L,seed,protocol,t,block,
            ...observables(model,block),pool:s.pool/L**2,structure:s.potentialTotal/L**2,
            density:s.total/L**2, balance:s.balanceError});
        }
        if (t<320) model.step();
      }
    }
  }
}

const model = loadModel('peter/index.html');
for (const L of [12,24,36,72]) for (const curvature of [0,1,-1]) {
  for (let seed=1; seed<=8; seed++) {
    const random = model.random(seed);
    model.init({L,seed,curvature,K:1,fill:1});
    const {en,geometry} = model.state();
    const origin = Math.floor(L/2)*L+Math.floor(L/2);
    en.fill(0);
    en[origin]=1;
    const distance=new Int32Array(en.length).fill(-1);
    const queue=[origin];
    distance[origin]=0;
    for (const i of queue) for (const j of model.neighbours(i)) if (distance[j]<0) {
      distance[j]=distance[i]+1;
      queue.push(j);
    }
    assert.equal(queue.length,en.length);
    for (let t=0; t<=256; t++) {
      if ([0,1,2,4,8,16,32,64,128,256].includes(t)) {
        let total=0, msd=0, support=0;
        for (let i=0; i<en.length; i++) {
          total+=en[i];
          msd+=en[i]*distance[i]**2;
          if (en[i]>0) support=Math.max(support,distance[i]);
        }
        assert.ok(Math.abs(total-1)<1e-12 && support<=t && Math.min(...en)>=0);
        save('pulse',{L,curvature,seed,t,total,msd,support,return:en[origin],
          rate:Math.min(.1,.45/(geometry?.maximumDegree ?? 4))});
      }
      if (t<256) model.diffuseEnergy();
    }
    // Random signed perturbations of strictly positive reserve, fixed species mask.
    for (const mask of ['single','labels']) {
      model.init({L,seed,curvature,K:mask==='single'?1:10,fill:1});
      const {en,sp} = model.state();
      for (let i=0;i<en.length;i++) en[i]=1+random();
      function measure(){
        let sum=0, squared=0, roughness=0;
        for (let i=0;i<en.length;i++){
          sum+=en[i];
          squared+=(en[i]-1.5)**2;
          for (const j of model.neighbours(i)) if(j>i && sp[i]===sp[j]) roughness+=(en[i]-en[j])**2;
        }
        return {sum,squared,roughness};
      }
      const start=measure();
      for (let t=0;t<=64;t++){
        if([0,1,4,16,64].includes(t)){
          const m=measure();
          assert.ok(m.squared<=start.squared+1e-9 && Math.abs(m.sum-start.sum)<1e-8);
          save('mixing',{L,curvature,seed,mask,t,...m});
        }
        if(t<64)model.diffuseEnergy();
      }
    }
  }
}

for (const L of [12,24,36]) for (let seed=1;seed<=96;seed++) {
  for (const pool of [L**2/4, 2*L**2]) {
    for (const d of [2,4,L/2]) for (const mode of ['uptake','sweep','local']) {
      for (const removed of [false,true]) {
        const source=L+1, probe=source+d;
        model.init({L,seed,K:1,fill:1,climateNoise:0,climateAmplitude:0,
          growthPriceAmplitude:0,spreadPriceAmplitude:0,maintenanceAmplitude:0,
          maxHeight:1,birthMutation:0,spontaneousMutation:0});
        model.setPool(pool);
        if (removed) model.killTree(source);
        model.resetLedger();
        const initial = model.state().en[probe];
        ({uptake:model.energyTick,sweep:model.step,local:model.diffuseEnergy})[mode]();
        const s=model.stats();
        assert.ok(Math.abs(s.balanceError)<1e-8);
        save('response',{L,seed,pool,d,mode,removed,reserve:model.state().en[probe]-initial,
          remaining:s.pool,balance:s.balanceError});
      }
    }
  }
}

for (const [table,data] of Object.entries(rows)) {
  const header=Object.keys(data[0]);
  fs.writeFileSync(path.join(out,table+'.csv'),[header.join(','),...data.map(r=>header.map(k=>r[k]).join(','))].join('\n')+'\n');
  console.log(table,data.length);
}
