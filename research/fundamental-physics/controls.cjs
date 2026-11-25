const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {loadModel} = require('./model.cjs');

const out = path.resolve(process.argv[2] || path.join(__dirname,'results'));
fs.mkdirSync(out,{recursive:true});
const model = loadModel('peter/index.html');
const fixed = {K:1,fill:1,climateNoise:0,climateAmplitude:0,growthPriceAmplitude:0,
  spreadPriceAmplitude:0,maintenanceAmplitude:0,maxHeight:1,birthMutation:0,
  spontaneousMutation:0,attackCost:100};
const rows = ['L,seed,d,control,delta,expected'];
for (const L of [12,24,36]) for (let seed=1;seed<=192;seed++){
  const N=L*L;
  const source=L+1;
  const d=L/2;
  const probe=source+d;
  for (const control of ['death','only_pool','fixed_point']){
    const values=[];
    const q=N/4;
    for (const modified of [false,true]){
      model.init({L,seed,...fixed,...(control==='fixed_point'?{energyInput:.1}:{})});
      model.setPool(control==='fixed_point'?2*N:q);
      if (modified && control==='death') model.killTree(source);
      // A Q-only positive control adds 12 units before each run's ledger starts.
      if (modified && control==='only_pool') model.setPool(q+12);
      model.resetLedger();
      const before = model.state().en[probe];
      const steps=control==='fixed_point'?20:1;
      for(let t=0;t<steps;t++) model.step();
      const s=model.stats();
      const delta=model.state().en[probe]-before;
      assert.ok(Math.abs(s.balanceError)<1e-8);
      if(control==='fixed_point') {
        assert.ok(Math.abs(delta)<1e-12 && s.total===N && Math.abs(s.pool-2*N)<1e-8);
      }
      values.push(delta);
    }
    const expected = control==='death' ? (q+12)/(N-1)-q/N :
      control==='only_pool' ? 12/N : 0;
    rows.push([L,seed,d,control,values[1]-values[0],expected].join(','));
  }
}
fs.writeFileSync(path.join(out,'controls.csv'),rows.join('\n')+'\n');
