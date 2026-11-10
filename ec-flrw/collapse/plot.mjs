import { surface } from "./geometry.mjs";
export const fmt = (v) =>
  !Number.isFinite(v)
    ? "—"
    : v === 0
      ? "0"
      : Math.abs(v) < 0.001 || Math.abs(v) > 1e4
        ? v.toExponential(3)
        : Number(v.toPrecision(5)).toString();
export const colors = [
  "#087f83",
  "#c97744",
  "#6775bd",
  "#a65b87",
  "#7b923a",
  "#536b75",
];
export const specs = {
  scale: ["a / aᵢ", "dimensionless"],
  volume: ["V / Vᵢ", "dimensionless"],
  a: ["a", "L*"],
  R: ["R_b", "L*"],
  v: ["ȧ", "c"],
  Rdot: ["Ṙ_b", "c"],
  H: ["H", "L*⁻¹"],
  dH: ["Ḣ", "L*⁻²"],
  acc: ["ä/a", "L*⁻²"],
  thetaPlus: ["θ₊ at boundary", "L*⁻¹"],
  thetaMinus: ["θ₋ at boundary", "L*⁻¹"],
  compactness: ["2Gm_MS / R_b", "dimensionless"],
  mu: ["Geometric Gm_MS / L*", "dimensionless"],
  massMatter: ["Source Gm_MS / L*", "dimensionless"],
  rho: ["Ordinary density", "1/(κL*²)"],
  pressure: ["Ordinary pressure", "1/(κL*²)"],
  spinCorrection: ["Spin correction κS²/4", "1/(κL*²)"],
  rhoEff: ["Effective density", "1/(κL*²)"],
  pEff: ["Effective pressure", "1/(κL*²)"],
  spin2: ["S²", "1/(κ²L*²)"],
  residual: ["Relative Friedmann residual", "dimensionless"],
  K: ["Metric Kretschmann K", "L*⁻⁴"],
  Rscalar: ["Metric Ricci R", "L*⁻²"],
};
export const graphs = {
  collapse: [
    ["relative", "Collapse & relative volume", ["scale", "volume"]],
    ["radius", "Scale factor & matter boundary", ["a", "R"]],
    ["rates", "Expansion dynamics", ["H", "dH", "acc"]],
    ["velocity", "Scale-factor & boundary velocity", ["v", "Rdot"]],
    ["curvature", "Metric curvature", ["K", "Rscalar"]],
  ],
  horizons: [
    ["null", "Future-directed null expansions", ["thetaPlus", "thetaMinus"]],
    ["compactness", "Boundary compactness", ["compactness"]],
    ["mass", "Misner–Sharp effective mass", ["mu", "massMatter"]],
    ["regions", "Spherical trapping map", []],
  ],
  matter: [
    [
      "sources",
      "Ordinary matter & spin correction",
      ["rho", "spinCorrection", "rhoEff"],
    ],
    ["pressure", "Ordinary & effective pressure", ["pressure", "pEff"]],
    ["spin", "Conserved spin-squared scaling", ["spin2"]],
    ["constraints", "Friedmann constraint residual", ["residual"]],
  ],
  research: [
    ["relative", "Compare collapse trajectories", ["scale", "volume"]],
    ["rates", "Compare expansion dynamics", ["H", "dH", "acc"]],
    ["curvature", "Compare curvature", ["K", "Rscalar"]],
  ],
};
export const signedLog = (y) =>
  Math.sign(y) * Math.log10(1 + Math.abs(y) / 0.01);
function ticks(series) {
  const values = series
      .filter((t) => t.visible !== "legendonly")
      .flatMap((t) => t.y ?? [])
      .filter(Number.isFinite),
    lo = Math.min(0, ...values),
    hi = Math.max(0, ...values),
    gap = (hi - lo || 1) / 7;
  const rows = [{ v: 0, text: "0" }];
  for (const sign of [-1, 1]) {
    let prev = 0;
    for (let e = -12; e <= 32; e++)
      for (const m of [1, 2, 5]) {
        const raw = sign * m * 10 ** e,
          v = signedLog(raw);
        if (v < lo || v > hi || Math.abs(v - prev) < gap) continue;
        rows.push({
          v,
          text:
            Math.abs(raw) >= 1000 || Math.abs(raw) < 0.001
              ? raw.toExponential(0).replace("e+", "e")
              : Number(raw.toPrecision(3)).toString(),
        });
        prev = v;
      }
  }
  rows.sort((a, b) => a.v - b.v);
  return {
    tickmode: "array",
    tickvals: rows.map((r) => r.v),
    ticktext: rows.map((r) => r.text),
  };
}
export class SimulationPlot {
  constructor(element) {
    this.el = element;
    this.version = 0;
    this.queue = Promise.resolve();
    this.ready = false;
    this.time = 0;
  }
  render(run, other, options) {
    this.run = run;
    this.time = options.time;
    this.options = options;
    this.ready = false;
    const token = ++this.version,
      def =
        graphs[options.section].find((d) => d[0] === options.graph) ??
        graphs[options.section][0],
      region = def[0] === "regions",
      signed = options.scale === "signedlog",
      log = options.scale === "log",
      groups = [],
      traces = [];
    let omissions = 0;
    const layout = {
      paper_bgcolor: "#fff",
      plot_bgcolor: "#fff",
      font: { family: "system-ui,sans-serif", size: 11, color: "#557078" },
      margin: { l: 68, r: 30, t: 25, b: 80 },
      hovermode: region ? "closest" : "x unified",
      dragmode: "zoom",
      legend: { orientation: "h", x: 0, y: -0.2, font: { size: 10 } },
      uirevision: `${options.runId}-${def[0]}-${options.scale}-${!!other}`,
      xaxis: {
        title: { text: "Shared proper time τ = t / L*" },
        gridcolor: "#eaf0ee",
        zerolinecolor: "#9badaa",
        ticks: "outside",
      },
      shapes: [],
      annotations: [],
    };
    if (region) {
      const columns = run.data.filter((_, i) => i % 4 === 0),
        rs = Array.from({ length: 40 }, (_, i) => (i + 1) / 40);
      const z = rs.map((fr) =>
        columns.map((s) => {
          const c = surface(s.a, s.v, run.p.k, fr * run.p.rb).classification;
          return c === "future trapped" ? 1 : c === "anti-trapped" ? 2 : 0;
        }),
      );
      traces.push({
        type: "heatmap",
        x: columns.map((s) => s.t),
        y: rs,
        z,
        zmin: 0,
        zmax: 2,
        colorscale: [
          [0, "#f0f4f2"],
          [0.249, "#f0f4f2"],
          [0.25, "#d9905e"],
          [0.749, "#d9905e"],
          [0.75, "#879bcc"],
          [1, "#879bcc"],
        ],
        colorbar: {
          tickvals: [0, 1, 2],
          ticktext: ["Untrapped", "Future trapped", "Anti-trapped"],
          len: 0.65,
          thickness: 10,
          x: 1.02,
          tickfont: { size: 9 },
        },
        hovertemplate:
          "τ=%{x:.6g}<br>r/r_b=%{y:.4g}<br>class code=%{z} (0 untrapped, 1 future trapped, 2 anti-trapped)<extra></extra>",
        meta: { fullZ: z },
      });
      traces.push({
        type: "scatter",
        mode: "lines",
        name: "Marginal sphere r_AH / r_b",
        x: run.data.map((s) => s.t),
        y: run.data.map((s) =>
          s.rAH !== null && s.rAH / run.p.rb <= 1.05 ? s.rAH / run.p.rb : null,
        ),
        line: { color: "#86522f", dash: "dot", width: 2 },
        connectgaps: false,
        meta: {
          fullY: run.data.map((s) =>
            s.rAH !== null && s.rAH / run.p.rb <= 1.05
              ? s.rAH / run.p.rb
              : null,
          ),
        },
        hovertemplate:
          "Marginal sphere<br>τ=%{x:.6g}<br>r_AH/r_b=%{y:.6g}<extra></extra>",
      });
      layout.yaxis = {
        title: { text: "Comoving shell r / r_b" },
        range: [0, 1.05],
        gridcolor: "#eaf0ee",
      };
      layout.shapes.push({
        type: "line",
        xref: "paper",
        yref: "y",
        x0: 0,
        x1: 1,
        y0: 1,
        y1: 1,
        line: { color: "#5b7378", width: 1 },
      });
      layout.margin.r = 114;
    } else {
      for (const [r, isOther] of [
        [run, false],
        [other, true],
      ]) {
        if (!r) continue;
        def[2].forEach((key, i) => {
          const [name, unit] = specs[key],
            axis = groups.indexOf(unit);
          if (axis < 0) groups.push(unit);
          const n = groups.indexOf(unit) + 1,
            raw = r.data.map((s) => s[key]),
            fullY = raw.map((v) => {
              if (log && v <= 0) {
                omissions++;
                return null;
              }
              return signed ? signedLog(v) : v;
            });
          traces.push({
            type: "scatter",
            mode: "lines",
            name: `${name} · ${r.p.theory.toUpperCase()}${isOther ? " reference" : ""} [${unit}]`,
            x: r.data.map((s) => s.t),
            y: fullY,
            customdata: raw,
            yaxis: n === 1 ? "y" : "y" + n,
            line: {
              color: colors[i % colors.length],
              width: isOther ? 1.7 : 2.4,
              dash: isOther ? "dash" : "solid",
            },
            connectgaps: false,
            fill: key === "volume" && !isOther ? "tozeroy" : undefined,
            fillcolor: "rgba(8,127,131,.06)",
            meta: { fullY, key },
            hovertemplate: `${name} · ${r.p.theory.toUpperCase()}<br>τ=%{x:.8g}<br>%{customdata:.9g} ${unit}<extra></extra>`,
          });
        });
      }
      groups.forEach((unit, j) => {
        const series = traces.filter(
            (t) => t.yaxis === (j ? "y" + (j + 1) : "y"),
          ),
          names = series
            .filter((t) => !t.name.includes("reference"))
            .map((t) => t.name.split(" · ")[0]);
        layout[j ? "yaxis" + (j + 1) : "yaxis"] = {
          title: {
            text: `${names.join(", ")} [${unit}]${signed ? " · signed log" : ""}`,
            font: { size: 10 },
          },
          type: log ? "log" : "linear",
          rangemode: signed ? "tozero" : "normal",
          gridcolor: "#eaf0ee",
          zerolinecolor: "#9badaa",
          ticks: "outside",
          ...(signed ? ticks(series) : {}),
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
      if (groups.length > 1) layout.margin.r = 95;
      if (def[0] === "compactness" && !log)
        layout.shapes.push({
          type: "line",
          xref: "paper",
          yref: "y",
          x0: 0,
          x1: 1,
          y0: signed ? signedLog(1) : 1,
          y1: signed ? signedLog(1) : 1,
          line: { color: "#b77f4b", width: 1, dash: "dot" },
        });
    }
    const allTimes = run.data
      .map((s) => s.t)
      .concat(other && !region ? other.data.map((s) => s.t) : []);
    layout.xaxis.range = [0, Math.max(...allTimes)];
    for (const e of run.events) {
      layout.shapes.push({
        type: "line",
        xref: "x",
        yref: "paper",
        x0: e.t,
        x1: e.t,
        y0: 0,
        y1: 1,
        line: {
          color: e.key === "turn" ? "#b39250" : "#9fb5b8",
          dash: "dot",
          width: 1,
        },
      });
      layout.annotations.push({
        xref: "x",
        yref: "paper",
        x: e.t,
        y: 1,
        text: e.key === "turn" ? "◇" : "·",
        showarrow: false,
        hovertext: e.label,
        font: { size: 15, color: "#a57f4a" },
      });
    }
    this.cursorIndex = layout.shapes.length;
    layout.shapes.push({
      type: "line",
      xref: "x",
      yref: "paper",
      x0: options.time,
      x1: options.time,
      y0: 0,
      y1: 1,
      line: { color: "#294953", width: 1.5, dash: "dash" },
    });
    this.traces = traces;
    const note =
      (region
        ? "Interior spherical surfaces only; colors use BOTH future null expansions. The line is a marginal sphere, not an event horizon. Comparison overlays apply to time-series graphs, not this map. "
        : def[0] === "relative"
          ? "Both quantities are divided by their initial values at τ=0; 1 means the starting size or volume. "
          : "") +
      (signed && !region
        ? "Signed log spacing is sign(u) log₁₀(1+|u|/0.01), with u in labelled units. Ticks and hover retain original values. "
        : "") +
      (log && !region
        ? `${omissions} nonpositive samples are omitted; use linear or signed log for zero crossings. `
        : "") +
      "All evolution curves share τ. Hover reads numerical samples; click legend entries to change visibility.";
    this.queue = this.queue
      .catch(() => {})
      .then(async () => {
        if (token !== this.version) return;
        await Plotly.react(this.el, traces, layout, {
          responsive: true,
          scrollZoom: true,
          displaylogo: false,
          modeBarButtonsToRemove: ["select2d", "lasso2d"],
        });
        if (token !== this.version) return;
        this.ready = true;
        this.move(this.time, options.progressive);
      });
    return { title: def[1], note, keys: def[2], promise: this.queue };
  }
  move(time, progressive) {
    this.time = time;
    if (!this.ready) return;
    Plotly.relayout(this.el, {
      [`shapes[${this.cursorIndex}].x0`]: time,
      [`shapes[${this.cursorIndex}].x1`]: time,
    });
    const update = {};
    const region = this.traces[0]?.type === "heatmap";
    if (region) {
      Plotly.restyle(
        this.el,
        {
          z: [
            this.traces[0].meta.fullZ.map((row) =>
              row.map((v, i) =>
                !progressive || this.traces[0].x[i] <= time ? v : null,
              ),
            ),
          ],
        },
        [0],
      );
      Plotly.restyle(
        this.el,
        {
          y: [
            this.traces[1].meta.fullY.map((v, i) =>
              !progressive || this.traces[1].x[i] <= time ? v : null,
            ),
          ],
        },
        [1],
      );
    } else
      Plotly.restyle(this.el, {
        y: this.traces.map((tr) =>
          tr.meta.fullY.map((v, i) =>
            !progressive || tr.x[i] <= time ? v : null,
          ),
        ),
      });
  }
  reset() {
    if (!this.ready) return;
    const layout = this.el.layout;
    Plotly.relayout(this.el, {
      "xaxis.autorange": true,
      ...Object.fromEntries(
        Object.keys(layout)
          .filter((k) => /^yaxis\d*$/.test(k))
          .map((k) => [k + ".autorange", true]),
      ),
    });
  }
  clear() {
    this.version++;
    this.ready = false;
    Plotly.purge(this.el);
  }
}
