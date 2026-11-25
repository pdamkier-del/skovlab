const fs=require("node:fs");
const path=require("node:path");
const assert=require("node:assert/strict");
const {loadModel}=require("../../fundamental-physics/model.cjs");

const out=process.argv[2]||path.join(__dirname,"../results");
fs.mkdirSync(out,{recursive:true});
const family=process.argv[3];
function make(L,seed){
  const n=L*L, edgeI=[],edgeJ=[],adj=Array.from({length:n},()=>[]);
  function join(i,j){edgeI.push(i);edgeJ.push(j);adj[i].push(j);adj[j].push(i);}
  if(family==="cliques"){
    for(let first=0;first<n;first+=5){
      for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)join(first+i,first+j);
      join(first+1,(first+5)%n);
    }
  }else if(family==="torus"){
    for(let i=0;i<n;i++){
      const right=i%L===L-1?i-L+1:i+1;
      join(i,right);
      join(i,(i+L)%n);
    }
  }else if(family==="regular"){
    const random=model.random(41041+seed);
    for(let i=0;i<n;i++)join(i,(i+1)%n);
    const order=Array.from({length:n},(_,i)=>i);
    let valid=false;
    do{
      for(let i=n-1;i>0;i--){
        const j=Math.floor(random()*(i+1));
        [order[i],order[j]]=[order[j],order[i]];
      }
      valid=order.every((v,i)=>!adj[v].includes(order[(i+1)%n]));
    }while(!valid);
    for(let i=0;i<n;i++)join(order[i],order[(i+1)%n]);
  }else throw Error("Choose cliques, torus, or regular.");
  assert.ok(adj.every(list=>list.length===4));
  return {adj,edgeI,edgeJ,maximumDegree:4};
}

const model=loadModel("index.html",undefined,make);
const result=[];
for(const L of [10,20])for(let seed=1;seed<=12;seed++){
  for(const treatment of ["mutation","no_mutation"]){
    model.init({L,seed,curvature:0,climateAmplitude:0,growthPriceAmplitude:0,
      spreadPriceAmplitude:0,maintenanceAmplitude:0,
      birthMutation:treatment==="mutation"?.015:0,
      spontaneousMutation:treatment==="mutation"?.025:0});
    for(let t=0;t<=260;t++){
      if([0,60,260].includes(t)){
        const s=model.stats(),{sp,geometry,strategies}=model.state();
        assert.ok(Math.abs(s.balanceError)<1e-6);
        result.push({geometry:family,L,seed,t,treatment,
          edges:t===0?geometry.edgeI.map((i,j)=>[i,geometry.edgeJ[j]]):null,
          labels:Array.from(sp),strategies:[...strategies],density:s.density,
          reserve:s.reserveTotal/(L*L),balance:s.balanceError});
      }
      if(t<260)model.step();
    }
  }
}
fs.writeFileSync(path.join(out,"snapshots_"+family+".json"),JSON.stringify(result));
console.log(family,result.length);
