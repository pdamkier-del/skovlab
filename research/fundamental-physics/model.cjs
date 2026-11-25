const path = require('node:path');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');

const root = path.resolve(__dirname, '../..');
const base = 'cb5877888f5dc8fea06b8224f891a04a4be3302d';
function loadModel(file, onStage) {
  const html = execFileSync('git', ['show', base + ':' + file], {cwd: root, encoding:'utf8'});
  let script = html.split('<script>')[1].split('\n$("run").addEventListener')[0];
  if (onStage) {
    const phases = "energyTick();diffuseEnergy();maintenanceTick();";
    const final = "spontaneousMutation();record();";
    if (!script.includes(phases) || !script.includes(final)) throw Error("Unknown sweep layout");
    script = script.replace(phases, [
      'traceStage("before",sweep,stats());',
      'energyTick();traceStage("uptake",sweep,stats());',
      'diffuseEnergy();traceStage("diffusion",sweep,stats());',
      'maintenanceTick();traceStage("maintenance",sweep,stats());'
    ].join(""));
    script = script.replace(final, 'traceStage("competition",sweep,stats());'+
      'spontaneousMutation();traceStage("mutation",sweep,stats());record();');
  }
  const elements = new Map();
  const blank = () => ({addEventListener(){}, getContext(){return {createImageData(){}};},
    classList:{toggle(){}}, style:{}});
  for (const match of html.matchAll(/<(input|select|textarea)\b([^>]*\sid="([^"]+)"[^>]*)>(?:([^<]*)<\/textarea>)?/g)) {
    const [, kind, attrs, id, content] = match;
    const value = attrs.match(/\bvalue="([^"]*)"/)?.[1];
    const first = kind === 'select' ? html.slice(match.index).split('</select>')[0] : '';
    elements.set(id, {...blank(), checked:/\bchecked\b/.test(attrs),
      value:value ?? content ?? first.match(/value="([^"]+)"[^>]*\bselected\b/)?.[1] ?? first.match(/value="([^"]+)"/)?.[1]});
  }
  const sandbox = {traceStage:onStage, window:{addEventListener(){}}, document:{
    getElementById(id){if(!elements.has(id)) elements.set(id, blank()); return elements.get(id);},
    createElement:blank
  }};
  const code = script + `
    draw=()=>{};
    statusFormula=()=>{};
    return ({
      init(options) {
        const readInputs=inputs;
        inputs=()=>{readInputs();Object.assign(cfg,options);};
        try {init();} finally {inputs=readInputs;}
      },
      step, diffuseEnergy, energyTick, neighbours, stats, killTree,
      state:()=>({sp,h,en,u,pool,sweep,geometry,alpha:cfg.alpha}),
      setPool:value=>{pool=value;},
      resetLedger:()=>{energyLedger.initial=stats().totalEnergy;},
      random:mulberry32
    });
  })();`;
  const model = vm.runInNewContext(code, sandbox, {filename:file});
  return model;
}

module.exports = {loadModel};
