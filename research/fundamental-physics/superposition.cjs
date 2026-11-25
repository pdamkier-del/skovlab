const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {loadModel} = require('./model.cjs');

const out = path.resolve(process.argv[2] || path.join(__dirname,'results'));
fs.mkdirSync(out,{recursive:true});
const model = loadModel('peter/index.html');
const rows = ['L,neighbors,curvature,alpha,separation,t,superposition_error,mass_error'];
for (const L of [12,24,48]) for (const neighbors of [4,8]) {
  for (const curvature of [0,1,-1]) for (const alpha of [0,.1,.12]) {
    for (const separation of [2,L/2]) {
      const first = L*Math.floor(L/2);
      const second = first+separation;
      const fields = [[],[first],[second],[first,second]].map(positions => {
        model.init({L,neighbors,curvature,alpha,K:1,fill:1});
        const {en} = model.state();
        en.fill(1);
        for (const position of positions) en[position]+=1;
        const snapshots = new Map();
        for (let t=0; t<=64; t++){
          if ([0,1,4,16,64].includes(t)) snapshots.set(t,Float64Array.from(en));
          if (t<64) model.diffuseEnergy();
        }
        return snapshots;
      });
      for (const t of fields[0].keys()){
        const [e0,a,b,ab] = fields.map(f=>f.get(t));
        let error=0,sum=0;
        for (let i=0;i<ab.length;i++){
          error=Math.max(error,Math.abs(ab[i]-a[i]-b[i]+e0[i]));
          sum+=ab[i];
        }
        const massError=Math.abs(sum-(L**2+2));
        assert.ok(error<1e-12 && massError<1e-9);
        rows.push([L,neighbors,curvature,alpha,separation,t,error,massError].join(','));
      }
    }
  }
}
fs.writeFileSync(path.join(out,'superposition.csv'),rows.join('\n')+'\n');
