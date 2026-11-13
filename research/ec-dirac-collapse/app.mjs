import {simulate,GA} from './model.mjs';
const $=id=>document.getElementById(id); let solution;
const fmt=x=>Number(x).toExponential(3).replace('e+','e');
function plot(id,key){
 const canvas=$(id),rect=canvas.getBoundingClientRect(),dpr=devicePixelRatio||1;canvas.width=rect.width*dpr;canvas.height=rect.height*dpr;const c=canvas.getContext('2d');c.scale(dpr,dpr);
 const w=rect.width,h=rect.height,pad=58,right=12,top=22,bottom=28,rows=solution.rows;
 let lo=Math.min(...rows.map(r=>r[key])),hi=Math.max(...rows.map(r=>r[key]));if(hi-lo<1e-12){lo-=.01;hi+=.01;}const margin=(hi-lo)*.08;lo-=margin;hi+=margin;
 const X=t=>pad+(w-pad-right)*t/Math.max(rows.at(-1).t,1e-10),Y=v=>top+(h-top-bottom)*(hi-v)/(hi-lo);
 c.font='10px system-ui';c.textAlign='right';for(let i=0;i<3;i++){const v=lo+(hi-lo)*i/2,y=Y(v);c.strokeStyle='#e3e7dd';c.beginPath();c.moveTo(pad,y);c.lineTo(w-right,y);c.stroke();c.fillStyle='#647269';c.fillText(fmt(v),pad-7,y+3);}
 c.textAlign='left';c.fillText('0',pad,h-8);c.textAlign='right';c.fillText(rows.at(-1).t.toFixed(2)+' τ',w-right,h-8);
 c.strokeStyle='#166553';c.lineWidth=2;c.beginPath();rows.forEach((r,i)=>i?c.lineTo(X(r.t),Y(r[key])):c.moveTo(X(r.t),Y(r[key])));c.stroke();
}
function draw(){if(!solution)return;plot('size','aV');plot('rate','H');plot('accel','dH');}
function run(event){event?.preventDefault();$('error').textContent='';$('export').disabled=true;solution=undefined;
 try{const m=+$('particle').value,L0=+$('length').value,M=+$('mass').value,n0=M/(m*L0**3),r=+$('anisotropy').value,E=m*n0+GA*n0*n0;
 solution=simulate({m,n0,L0,D0:r*Math.sqrt(E),spin:+$('spin').value});$('h0').textContent=fmt(solution.p.H0);$('anisotropy-value').textContent=r.toFixed(2);
 const last=solution.rows.at(-1);$('interval').textContent='0 → '+last.t.toFixed(2)+' τ';
 $('outcome').textContent=['numerical-error','constraint-error'].includes(solution.status)?'Numerisk beregning afbrudt; ingen numerisk bouncekonklusion.':'Intet volumenbounce i den beregnede udvikling.';
 const metrics=[['Maks. energitæthed',fmt(solution.maximumEnergy)],['Maks. |T̂₀₁₂| = n/2',fmt(solution.maximumTorsion)],['Maks. relativ constraintfejl',fmt(solution.maximumConstraint)],['Slutstørrelse aᵥ',last.aV.toFixed(3)]];
 $('metrics').replaceChildren(...metrics.map(([label,value])=>{const d=document.createElement('div');d.textContent=label;const s=document.createElement('strong');s.textContent=value;d.append(s);return d;}));
 const reasons={'validity-limit':'Stoppet før demonstrationsgrænsen: max(E, n, √Kretschmann) = 0,1. Dette er en valgt forsigtighedsgrænse, ikke en bevist fysisk overgang.','time-limit':'Det valgte tidsinterval er beregnet.','step-limit':'Tringrænsen er nået; udviklingen er uafklaret.','constraint-error':'Numerisk constraintfejl: løsningen skal undersøges ved højere opløsning.','numerical-error':'Numerisk fejl: ingen fortsættelse eller bounce kan konkluderes.'};
 $('stop').textContent=reasons[solution.status]+' '+solution.bounceReason;$('export').disabled=false;draw();
 }catch(e){$('error').textContent=e.message;$('h0').textContent='Ugyldige startdata';$('outcome').textContent='Ingen gyldig beregning.';$('metrics').replaceChildren();$('stop').textContent='Ret startdata og beregn igen.';$('interval').textContent='';for(const id of ['size','rate','accel']){const c=$(id);c.getContext('2d').clearRect(0,0,c.width,c.height);}}
}
$('controls').addEventListener('submit',run);$('anisotropy').addEventListener('input',()=>{$('anisotropy-value').textContent=(+$('anisotropy').value).toFixed(2)});window.addEventListener('resize',draw);
$('export').addEventListener('click',()=>{if(!solution)return;const url=URL.createObjectURL(new Blob([JSON.stringify(solution,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='ecd-lrs-solution.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});run();
