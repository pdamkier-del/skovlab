import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,rhs,rk4,diagnostics,simulate,GA,LIMIT} from '../model.mjs';
const close=(a,b,tol=1e-9)=>assert.ok(Math.abs(a-b)<tol,`${a} != ${b}`);
function integrate(p,y,T,N){for(let i=0;i<N;i++)y=rk4(y,T/N,p);return y;}
test('constraint-solved initial data and invalid combinations',()=>{
 const {p,y}=initialData({D0:.01});close(diagnostics(y,p).constraint,0);
 for(const x of [{n0:-1},{L0:0},{m:NaN},{spin:0},{H0:0},{n0:1},{D0:2},{L0:1e308}])assert.throws(()=>initialData(x));
 assert.throws(()=>simulate({}, {resolution:0}));
});
test('RK4 converges against exact coupled volume and expansion',()=>{
 const {p,y}=initialData({n0:.01,m:.1,D0:.02});const T=8;
 const V=1+3*p.H0*T+.75*p.m*p.n0*T*T, H=(3*p.H0+1.5*p.m*p.n0*T)/(3*V);
 const errors=[10,20,40].map(N=>{const z=integrate(p,y,T,N);return Math.abs(Math.exp(z[0])-V)+Math.abs(z[1]-H);});
 assert.ok(errors[0]/errors[1]>12);assert.ok(errors[1]/errors[2]>12);
});
test('spinor current, shear integral and metric volume preserved',()=>{
 const {p,y}=initialData({D0:.015});const z=integrate(p,y,8,200),d=diagnostics(z,p);
 close(d.number,p.n0*p.L0**3);close(d.D*d.V,p.D0);close(d.a*d.a*d.b,d.V);assert.ok(d.relativeConstraint<1e-10);
 close(d.spinorReal*d.spinorReal+d.spinorImag*d.spinorImag,d.n);
});
test('full ADM evolution agrees with focusing equation on constraint',()=>{
 const {p,y}=initialData({D0:.012});const d=diagnostics(y,p);
 close(rhs(y,p)[1],-(d.E+d.P)/2-d.D*d.D/3);
 close(6*d.H*d.H,2*d.E+d.shear);
});
test('vacuum Kasner and Minkowski limits',()=>{
 const {p,y}=initialData({n0:0,D0:.02});const T=4,z=integrate(p,y,T,200),d=diagnostics(z,p);
 close(d.V,1+3*p.H0*T);close(d.E,0);close(d.torsion,0);close(d.ricci,0);assert.ok(d.kretschmann>0);
 const flat=initialData({n0:0,D0:0});assert.ok(rhs(flat.y,flat.p).slice(0,5).every(v=>v===0));
});
test('massless field and isotropic limits remain regular before cutoff',()=>{
 const {p,y}=initialData({m:0,D0:0});const T=2,z=integrate(p,y,T,100),d=diagnostics(z,p);
 close(d.E,d.P);close(d.a,d.b);close(d.V,1+3*p.H0*T);assert.ok(d.dH<0);
});
test('number-free limit is vacuum, not spinless massive dust',()=>{
 const {p,y}=initialData({n0:0});const d=diagnostics(y,p);close(d.E,0);close(d.P,0);
 // A single nonzero coherent spinor cannot independently switch off its axial current.
 close(GA,3/16);
});
test('production run stops before validity boundary without invented bounce',()=>{
 const r=simulate({D0:.01});assert.equal(r.status,'validity-limit');assert.equal(r.bounce,false);assert.ok(r.rows.length>100);
 assert.ok(r.rows.every(d=>d.validity<LIMIT&&d.H<0&&d.dH<0));assert.ok(r.maximumConstraint<1e-6);
 const flipped=simulate({D0:.01,spin:-1});assert.deepEqual(r.rows,flipped.rows);
 const refined=simulate({D0:.01},{resolution:2});assert.equal(refined.status,'validity-limit');
 close(refined.rows.at(-1).t,r.rows.at(-1).t,.1);
});
test('time interval completes under refinement; step exhaustion is explicit',()=>{
 assert.equal(simulate({}, {maxSteps:1}).status,'step-limit');
 const r=simulate({n0:0,D0:0},{resolution:2});assert.equal(r.status,'time-limit');close(r.rows.at(-1).t,200);
});
