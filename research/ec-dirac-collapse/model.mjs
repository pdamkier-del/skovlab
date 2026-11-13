// Classical single-spinor, aligned LRS Bianchi I; NOT an inhomogeneous solver.
export const KAPPA = 1, GA = 3 / 16, LIMIT = 0.1;
export function initialData({m = .1, n0 = .01, L0 = 1, D0 = 0, spin = 1, branch = -1, H0} = {}) {
  if (![m,n0,L0,D0,spin,branch].every(Number.isFinite) || m < 0 || n0 < 0 || L0 <= 0 || ![-1,1].includes(spin) || ![-1,1].includes(branch)) throw Error('Kræver m ≥ 0, n₀ ≥ 0, L₀ > 0 og gyldig spin/udviklingsgren.');
  const E0 = m*n0 + GA*n0*n0;
  const H = branch * Math.sqrt((E0 + D0*D0/3)/3);
  if (H0 !== undefined && (!Number.isFinite(H0) || Math.abs(H0-H)>1e-10*Math.max(1,Math.abs(H)))) throw Error('H₀ er bundet af Hamilton-begrænsningen; vælg den afledte værdi.');
  const p = {m,n0,L0,D0,spin,branch,H0:H};
  const y = [0,H,D0,0,0,0];
  const d = diagnostics(y,p);
  if (!Object.values(d).every(Number.isFinite)) throw Error('Startdata giver ikke-endelige afledte størrelser.');
  if (d.validity >= LIMIT) throw Error('Startdata overskrider appens demonstrationsgrænse (0,1 i reducerede Planck-enheder). Reducér tæthed eller shear.');
  return {p,y};
}
export function rhs(y,p) {
  const n=p.n0*Math.exp(-y[0]), E=p.m*n+GA*n*n, P=GA*n*n, H=y[1], D=y[2];
  return [3*H, -3*H*H+(E-P)/2, -3*H*D, H-D/3, H+2*D/3, p.m+2*GA*n];
}
export function rk4(y,h,p) {
  const a=rhs(y,p), b=rhs(y.map((v,i)=>v+h*a[i]/2),p), c=rhs(y.map((v,i)=>v+h*b[i]/2),p), d=rhs(y.map((v,i)=>v+h*c[i]),p);
  return y.map((v,i)=>v+h*(a[i]+2*b[i]+2*c[i]+d[i])/6);
}
export function diagnostics(y,p) {
  const [logV,H,D,logA,logB,phase]=y, n=p.n0*Math.exp(-logV), E=p.m*n+GA*n*n, P=GA*n*n;
  const f=rhs(y,p), A=f[3], B=f[4], dA=f[1]-f[2]/3, dB=f[1]+2*f[2]/3;
  const shear=2*D*D/3, C=6*H*H-2*E-shear;
  const kretschmann=4*(2*(dA+A*A)**2+(dB+B*B)**2+A**4+2*A*A*B*B);
  const validity=Math.max(E,n,Math.sqrt(kretschmann));
  return {V:Math.exp(logV),aV:Math.exp(logV/3),a:Math.exp(logA),b:Math.exp(logB),H,dH:f[1],D,n,E,P,shear,phase,spinorReal:Math.sqrt(n)*Math.cos(phase),spinorImag:-Math.sqrt(n)*Math.sin(phase),number:n*Math.exp(logV)*p.L0**3,restContent:p.m*p.n0*p.L0**3,torsion:n/2,kretschmann,ricci:E-3*P,constraint:C,relativeConstraint:Math.abs(C)/Math.max(6*H*H,2*E+shear,1e-30),volumeResidual:Math.abs(logV-2*logA-logB),validity};
}
export function simulate(options={}, {resolution=1, maxSteps=30000}={}) {
  if (!Number.isFinite(resolution)||resolution<=0||!Number.isInteger(maxSteps)||maxSteps<1) throw Error('Ugyldig numerisk opløsning.');
  const {p,y:initial}=initialData(options); let y=initial,t=0;
  const duration=2/Math.max(Math.abs(p.H0),.01), rows=[{t,...diagnostics(y,p)}];
  let status='time-limit', steps=0;
  while(t<duration && steps<maxSteps) {
    const old=rows.at(-1), h=Math.min(Math.min(duration/600, .012/Math.max(Math.abs(y[1]),Math.abs(y[2]),p.m+2*GA*old.n,.001))/resolution,duration-t);
    const next=rk4(y,h,p), d=diagnostics(next,p);
    if (!Object.values(d).every(Number.isFinite)) {status='numerical-error';break;}
    if(d.validity>=LIMIT) {status='validity-limit';break;}
    if(d.relativeConstraint>1e-6 || d.volumeResidual>1e-7) {status='constraint-error';break;}
    t+=h;y=next;steps++;rows.push({t,...d});
  }
  if(steps>=maxSteps) status='step-limit';
  return {model:'LRS Bianchi I, classical aligned ECD',units:'c = ℏ = κ = 1',method:{name:'RK4',resolution,maxSteps,cutoff:LIMIT,spinorComponent:p.spin===1?2:3},p,rows,status,steps,bounce:false,bounceReason:'For denne gren er dH/dτ = −(E+P)/2 − D²/3 ≤ 0. Intet volumenbounce.',maximumConstraint:Math.max(...rows.map(r=>r.relativeConstraint)),maximumEnergy:Math.max(...rows.map(r=>r.E)),maximumTorsion:Math.max(...rows.map(r=>r.torsion))};
}
