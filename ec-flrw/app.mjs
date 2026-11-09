import { defaults, simulate, convergence } from "./model.mjs";
const $ = (id) => document.getElementById(id),
  fmt = (v) =>
    !Number.isFinite(v)
      ? "—"
      : v === 0
        ? "0"
        : Math.abs(v) < 0.001 || Math.abs(v) >= 1e4
          ? v.toExponential(4)
          : Number(v.toPrecision(6)).toString();
const palette = [
  "#087f83",
  "#cc7044",
  "#596ac5",
  "#af5892",
  "#82912d",
  "#545d68",
];
const specs = {
  H: ["H", "t*⁻¹"],
  dH: ["Ḣ", "t*⁻²"],
  a: ["a", "dimensionless"],
  adot: ["ȧ", "t*⁻¹"],
  X: ["X", "dimensionless"],
  Y: ["Y", "dimensionless"],
  acc: ["ä/a", "t*⁻²"],
  N: ["N", "e-folds"],
  Nacc: ["N accelerated", "e-folds"],
  hr: ["Hᵣ", "t*⁻¹"],
  ho: ["HΩ", "t*⁻¹"],
  shear: ["σ²", "t*⁻²"],
  K: ["Kretschmann K", "t*⁻⁴"],
  R: ["Ricci R", "t*⁻²"],
  residual: ["Relative constraint", "dimensionless"],
};
const titles = {
  expansion: "Expansion dynamics",
  geometry: "Geometry",
  acceleration: "Acceleration",
  efolds: "E-folds",
  anisotropy: "Directional expansion",
  curvature: "Curvature & constraint",
};
const inputs = [
  "w",
  "spin",
  "branch",
  "a0",
  "X0",
  "Y0",
  "hr0",
  "ho0",
  "T",
  "tol",
];
let active = location.hash === "#ks" ? "ks" : "flrw",
  saved = {
    flrw: { ...defaults },
    ks: { ...defaults, geometry: "ks", spin: 0.5, T: 5 },
  },
  result,
  comparison,
  index = 0,
  traces = [],
  playing = false,
  lastFrame = 0,
  frame,
  playTime = 0,
  plotVersion = 0,
  revision = 0,
  ready = false,
  renderQueue = Promise.resolve();
try {
  const stored = JSON.parse(localStorage.getItem("ec-geometry-v3"));
  if (stored)
    for (const g of ["flrw", "ks"])
      saved[g] = { ...saved[g], ...stored[g], geometry: g };
} catch {}
function read() {
  const p = { geometry: active };
  for (const id of inputs) p[id] = id === "branch" ? $(id).value : +$(id).value;
  return p;
}
function load() {
  for (const id of inputs) $(id).value = saved[active][id];
  $("geometry").value = active;
  $("flrwFields").hidden = active !== "flrw";
  $("ksFields").hidden = active !== "ks";
  $("spinLabel").textContent = active === "ks" ? "S(0) t*²" : "B · t*⁻²";
  $("graph").querySelector("[value=anisotropy]").disabled = active !== "ks";
  if (active === "flrw" && $("graph").value === "anisotropy")
    $("graph").value = "expansion";
}
function pause() {
  playing = false;
  $("play").textContent = "Play";
  cancelAnimationFrame(frame);
}
function persist() {
  try {
    localStorage.setItem("ec-geometry-v3", JSON.stringify(saved));
    history.replaceState(null, "", "#" + active);
  } catch {}
}
function recalculate() {
  pause();
  ready = false;
  plotVersion++;
  const p = read();
  saved[active] = p;
  persist();
  $("convergence").textContent =
    "Step convergence: not yet checked for these parameters.";
  try {
    result = simulate(p);
    index = 0;
    comparison = null;
    if ($("compare").checked) {
      try {
        comparison = simulate(saved[active === "ks" ? "flrw" : "ks"]);
      } catch (e) {
        throw Error("Comparison parameters: " + e.message);
      }
    }
    $("modelLabel").textContent =
      active === "ks"
        ? "KANTOWSKI–SACHS · VOLUME AVERAGES"
        : "SPATIALLY FLAT FLRW";
    $("initialNote").textContent =
      active === "ks"
        ? `ρ(0) = ${fmt(result.initial.rho)} from the KS constraint. Interval [0,T].`
        : p.branch === "bounce"
          ? `H(0) = 0 imposed; A = ${fmt(result.rho0)}. Interval [−T,T].`
          : `H(0) = ${fmt(result.initial.H)} from the constraint. Interval [0,T].`;
    $("health").textContent =
      `Max relative constraint residual: ${result.maxResidual.toExponential(3)} · ${result.data.length} samples.`;
    $("health").style.color = result.maxResidual > 1e-5 ? "#b56b24" : "#087864";
    const warnings = [
      ...result.warnings,
      ...(comparison ? comparison.warnings.map((w) => "Comparison: " + w) : []),
    ];
    $("warnings").replaceChildren(
      ...warnings.map((w) => {
        const el = document.createElement("div");
        el.className = "warning";
        el.textContent = w;
        return el;
      }),
    );
    $("eventDetail").textContent = "";
    $("eventCount").textContent = `/ ${result.events.length}`;
    $("events").replaceChildren();
    if (!result.events.length)
      $("events").textContent = "No turning points detected in this interval.";
    result.events.forEach((e) => {
      const b = document.createElement("button");
      b.className = "quiet";
      b.textContent = `${e.label} · τ ${fmt(e.t)}`;
      b.title = `Positive finite scales: ${e.finite ? "yes" : "no"}; K at refined root = ${fmt(e.K)} t*⁻⁴; mean Ḣ = ${fmt(e.dH)} t*⁻². Not proof of regularity.`;
      b.onclick = () => {
        pause();
        selectTime(e.t);
        $("eventDetail").textContent =
          `${e.label} at τ=${fmt(e.t)}. Positive finite scale factors: ${e.finite ? "yes" : "no"}; K=${fmt(e.K)} t*⁻⁴. Cursor selects the refined event sample. Finite values at this event do not establish global regularity.`;
      };
      $("events").append(b);
    });
    revision++;
    draw();
    $("play").disabled = false;
  } catch (e) {
    result = null;
    comparison = null;
    Plotly.purge("plot");
    $("values").replaceChildren();
    $("events").replaceChildren();
    $("health").textContent = "No valid solution.";
    $("warnings").innerHTML = "";
    const el = document.createElement("div");
    el.className = "warning error";
    el.textContent = e.message;
    $("warnings").append(el);
    $("play").disabled = true;
  }
}
function keys(g = active) {
  switch ($("graph").value) {
    case "geometry":
      return g === "ks" ? ["X", "Y", "a"] : ["a", "adot"];
    case "acceleration":
      return ["H", "dH", "acc"];
    case "efolds":
      return ["N", "Nacc"];
    case "anisotropy":
      return g === "ks" ? ["hr", "ho", "H", "shear"] : ["H"];
    case "curvature":
      return ["K", "R", "residual"];
    default:
      return ["H", "dH"];
  }
}
function label(key, g) {
  return key === "a" && g === "ks"
    ? "aᵥ / L*"
    : key === "X" && g === "ks"
      ? "X / L*"
      : key === "Y" && g === "ks"
        ? "Y / L*"
        : key === "H" && g === "ks"
          ? "Hᵥ"
          : key === "dH" && g === "ks"
            ? "Ḣᵥ"
            : key === "acc" && g === "ks"
              ? "äᵥ/aᵥ"
              : specs[key][0];
}
function draw() {
  if (!result) return;
  ready = false;
  const token = ++plotVersion,
    graph = $("graph").value,
    mode = $("axes").value,
    log = $("scale").value === "log";
  traces = [];
  const groups = [];
  let hiddenLog = 0;
  for (const [run, isCompare] of [
    [result, false],
    [comparison, true],
  ]) {
    if (!run) continue;
    const g = run.p.geometry;
    keys(g).forEach((key, i) => {
      const [_, unit] = specs[key],
        name = label(key, g) + (isCompare ? ` · ${g.toUpperCase()}` : "");
      const norm = Math.max(...run.data.map((s) => Math.abs(s[key]))) || 1,
        group =
          mode === "normalized"
            ? "normalized"
            : mode === "shared"
              ? "shared"
              : unit;
      if (!groups.includes(group)) groups.push(group);
      const axis = groups.indexOf(group) + 1;
      const ys = run.data.map((s) => {
        const y = s[key] / (mode === "normalized" ? norm : 1);
        if (log && y <= 0) {
          hiddenLog++;
          return null;
        }
        return y;
      });
      traces.push({
        type: "scatter",
        mode: "lines",
        name: `${name} [${mode === "normalized" ? "normalized" : unit}]`,
        x: run.data.map((s) => s.t),
        y: ys,
        customdata: run.data.map((s) => s[key]),
        yaxis: axis === 1 ? "y" : "y" + axis,
        line: {
          color: palette[i % palette.length],
          width: isCompare ? 1.7 : 2.3,
          dash: isCompare ? "dash" : "solid",
        },
        connectgaps: false,
        meta: { key, isCompare, ys, unit, norm, g },
        hovertemplate: `${name}<br>τ = %{x:.8g}<br>value = %{customdata:.9g} ${unit}<extra></extra>`,
      });
    });
  }
  const extent = result.data
      .map((s) => s.t)
      .concat(comparison ? comparison.data.map((s) => s.t) : []),
    lo = Math.min(...extent),
    hi = Math.max(...extent);
  const layout = {
    paper_bgcolor: "#fff",
    plot_bgcolor: "#fff",
    font: { family: "system-ui, sans-serif", size: 11, color: "#52636a" },
    margin: { l: 67, r: groups.length > 1 ? 95 : 24, t: 26, b: 78 },
    hovermode: "x unified",
    dragmode: "zoom",
    showlegend: true,
    legend: { orientation: "h", y: -0.19, x: 0, font: { size: 10 } },
    uirevision: `${active}-${graph}-${mode}-${$("scale").value}-${revision}`,
    xaxis: {
      title: { text: "Time τ = t / t*" },
      range: [lo, hi],
      gridcolor: "#edf0f0",
      zerolinecolor: "#b9c8ca",
      ticks: "outside",
    },
    shapes: [],
    annotations: [],
  };
  groups.forEach((group, j) => {
    const associated = traces
      .filter((t) => t.yaxis === (j ? "y" + (j + 1) : "y"))
      .map((t) => t.name.split(" [")[0]);
    const title =
      mode === "normalized"
        ? "Each curve / max |value| (dimensionless)"
        : mode === "shared"
          ? "Values · units specified in legend"
          : `${associated.join(", ")} [${group}]`;
    layout[j ? "yaxis" + (j + 1) : "yaxis"] = {
      title: { text: title, font: { size: 10 } },
      type: log ? "log" : "linear",
      gridcolor: "#edf0f0",
      zerolinecolor: "#b9c8ca",
      ticks: "outside",
      ...(j
        ? {
            overlaying: "y",
            side: "right",
            anchor: j > 1 ? "free" : "x",
            position: j > 1 ? 1 : undefined,
            autoshift: true,
          }
        : {}),
    };
  });
  for (const e of result.events) {
    layout.shapes.push({
      type: "line",
      xref: "x",
      yref: "paper",
      x0: e.t,
      x1: e.t,
      y0: 0,
      y1: 1,
      line: { color: "#b59058", width: 1, dash: "dot" },
    });
    layout.annotations.push({
      x: e.t,
      y: 1,
      xref: "x",
      yref: "paper",
      text: "◇",
      showarrow: false,
      font: { color: "#b59058", size: 16 },
      hovertext: e.label,
    });
  }
  layout.shapes.push(cursorShape());
  $("title").textContent = titles[graph];
  $("title").title =
    "Kinematic identity: ä/a = Ḣ + H². For KS this applies to aᵥ = (XY²)⅓, using the KS evolution equations.";
  $("plotNote").textContent =
    (mode === "normalized"
      ? "Normalization is separate for each curve over its full computed interval. Hover shows original values. "
      : "") +
    (log
      ? `Log scale omits ${hiddenLog} nonpositive values; zero crossings require linear scale. `
      : "") +
    (comparison
      ? "Dashed curves: other geometry, own initial data and density normalization. "
      : "") +
    "One shared time coordinate. Hover reads numerical samples. Double-click the plot to reset zoom.";
  renderQueue = renderQueue.then(async () => {
    if (token !== plotVersion) return;
    await Plotly.react("plot", traces, layout, {
      responsive: true,
      scrollZoom: true,
      displaylogo: false,
      modeBarButtonsToRemove: ["select2d", "lasso2d"],
      toImageButtonOptions: {
        filename: "einstein-cartan",
        format: "png",
        scale: 2,
      },
    });
    if (token !== plotVersion) return;
    ready = true;
    updateCursor();
  });
}
function cursorShape() {
  const t = result.data[index].t;
  return {
    type: "line",
    xref: "x",
    yref: "paper",
    x0: t,
    x1: t,
    y0: 0,
    y1: 1,
    line: { color: "#253e48", width: 1.5, dash: "dash" },
  };
}
function updateCursor() {
  if (!result) return;
  const s = result.data[index];
  $("time").value = (index / (result.data.length - 1)) * 1000;
  $("clock").textContent = `τ ${fmt(s.t)}`;
  $("values").innerHTML =
    keys()
      .map(
        (k, i) =>
          `<div class="value" style="--c:${palette[i % palette.length]}"><span>${label(k, active)} · ${specs[k][1]}</span><strong>${fmt(s[k])}</strong></div>`,
      )
      .join("") +
    `<div class="value" style="--c:#87979b"><span>Relative constraint</span><strong>${s.residual.toExponential(2)}</strong></div>`;
  if (!ready) return;
  const shapeIndex = result.events.length;
  Plotly.relayout("plot", {
    [`shapes[${shapeIndex}].x0`]: s.t,
    [`shapes[${shapeIndex}].x1`]: s.t,
  });
  if ($("progressive").checked)
    Plotly.restyle("plot", {
      y: traces.map((tr) =>
        tr.meta.ys.map((v, i) => (tr.x[i] <= s.t ? v : null)),
      ),
    });
}
function selectTime(t) {
  if (!result) return;
  let best = 0;
  for (let i = 1; i < result.data.length; i++)
    if (Math.abs(result.data[i].t - t) < Math.abs(result.data[best].t - t))
      best = i;
  index = best;
  updateCursor();
}
function tick(now) {
  if (!playing || !result) return;
  const dt = (now - lastFrame) / 1000;
  lastFrame = now;
  const data = result.data,
    t = playTime + (dt * +$("speed").value * (data.at(-1).t - data[0].t)) / 20;
  playTime = t;
  selectTime(t);
  if (index >= data.length - 1) pause();
  else frame = requestAnimationFrame(tick);
}
$("play").onclick = () => {
  if (playing) {
    pause();
    return;
  }
  if (!ready || !result) return;
  if (index === result.data.length - 1) index = 0;
  playTime = result.data[index].t;
  playing = true;
  $("play").textContent = "Pause";
  lastFrame = performance.now();
  frame = requestAnimationFrame(tick);
};
$("rewind").onclick = () => {
  pause();
  index = 0;
  updateCursor();
};
$("time").oninput = () => {
  pause();
  if (!result) return;
  index = Math.round((+$("time").value / 1000) * (result.data.length - 1));
  updateCursor();
};
$("progressive").onchange = () => {
  if (!ready) return;
  if (!$("progressive").checked)
    Plotly.restyle("plot", { y: traces.map((t) => t.meta.ys) });
  updateCursor();
};
$("geometry").onchange = () => {
  pause();
  active = $("geometry").value;
  load();
  recalculate();
};
for (const id of inputs)
  $(id).addEventListener("input", () => {
    recalculate();
  });
for (const id of ["graph", "axes", "scale"])
  $(id).onchange = () => {
    pause();
    draw();
  };
$("compare").onchange = recalculate;
$("view").onclick = () => {
  if (!ready) return;
  Plotly.relayout("plot", {
    "xaxis.autorange": true,
    ...Object.fromEntries(
      Object.keys($("plot").layout)
        .filter((k) => /^yaxis\d*$/.test(k))
        .map((k) => [k + ".autorange", true]),
    ),
  });
};
$("reset").onclick = () => {
  saved[active] =
    active === "flrw"
      ? { ...defaults }
      : { ...defaults, geometry: "ks", spin: 0.5, T: 5 };
  load();
  recalculate();
};
$("validate").onclick = () => {
  if (!result) return;
  const finer = simulate({
      ...result.p,
      tol: result.p.tol / 16,
      maxStep: result.p.T / 1600,
    }),
    c = convergence(result, finer);
  $("convergence").textContent =
    `Tolerance ÷16, maximum step ÷2: max scaled difference in a, H, Ḣ, K = ${c.error.toExponential(3)}; ${c.count} common samples. ${c.complete ? "Same endpoint." : "Endpoints differ; convergence not established."}`;
};
$("export").onclick = () => {
  if (!result) return;
  const columns = Object.keys(result.data[0]),
    metadata = `# Geometry=${active}; parameters=${JSON.stringify(result.p)}; time=t/t*; units and equations: MODEL.md\n`;
  const blob = new Blob(
      [
        metadata +
          columns.join(",") +
          "\n" +
          result.data.map((s) => columns.map((k) => s[k]).join(",")).join("\n"),
      ],
      { type: "text/csv" },
    ),
    url = URL.createObjectURL(blob),
    a = document.createElement("a");
  a.href = url;
  a.download = `ec-${active}.csv`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
load();
recalculate();
