import { defaults, simulate, compare, convergence } from "./model.mjs";
import { SimulationPlot, graphs, specs, colors, fmt } from "./plot.mjs";
const $ = (id) => document.getElementById(id),
  plot = new SimulationPlot($("plot")),
  ids = [
    "theory",
    "k",
    "w",
    "rho",
    "spin2",
    "a0",
    "H0",
    "branch",
    "constraint",
    "boundary",
    "rb",
    "R0",
    "T",
    "tol",
  ],
  strings = ["theory", "branch", "constraint", "boundary"];
let run,
  other,
  savedRun = null,
  section = "collapse",
  index = 0,
  playing = false,
  playTime = 0,
  lastFrame = 0,
  frame,
  runId = 0,
  selectedKeys = [],
  worker = null,
  sweepResult = null;
const presets = {
  default: { ...defaults },
  small: { ...defaults, rb: 0.3 },
  gr: { ...defaults, theory: "gr" },
  radiation: { ...defaults, w: 1 / 3, spin2: 0.6 },
  reference: {
    ...defaults,
    k: 1,
    a0: 1 / Math.sqrt(2.14),
    rho: 6.66,
    spin2: 0.96,
    rb: 0.5,
    constraint: "velocity",
    H0: 0,
    T: 2,
  },
};
function read() {
  const p = {};
  for (const id of ids)
    p[id] = strings.includes(id) ? $(id).value : +$(id).value;
  p.Lkm = +$("Lkm").value;
  return p;
}
function load(p) {
  for (const id of ids) $(id).value = p[id] ?? defaults[id];
  $("Lkm").value = p.Lkm || "";
}
function pause() {
  playing = false;
  $("play").textContent = "Play";
  cancelAnimationFrame(frame);
}
function message(text, cls = "warning") {
  const el = document.createElement("div");
  el.className = cls;
  el.textContent = text;
  $("warnings").append(el);
}
function updateFields() {
  const density = $("constraint").value === "density";
  $("rho").disabled = !density;
  $("H0").disabled = density;
  $("branchField").hidden = !density;
  $("spin2").disabled = $("theory").value === "gr";
  $("rbField").hidden = $("boundary").value !== "comoving";
  $("R0Field").hidden = $("boundary").value !== "physical";
}
function record() {
  try {
    localStorage.setItem(
      "ec-collapse-lab-v1",
      JSON.stringify({ parameters: read(), mode: $("mode").value }),
    );
  } catch {}
}
function draw() {
  if (!run) return;
  const r = plot.render(run, other, {
    section,
    graph: $("graph").value,
    scale: $("scale").value,
    time: run.data[index].t,
    progressive: $("progressive").checked,
    runId,
  });
  selectedKeys = r.keys;
  $("plotTitle").textContent = r.title;
  $("plotNote").textContent = r.note;
  updateCursor();
  return r.promise;
}
function recalculate() {
  pause();
  runId++;
  updateFields();
  $("warnings").replaceChildren();
  $("validation").textContent =
    "Step convergence has not been checked for these parameters.";
  try {
    const input = read();
    if (!Number.isFinite(input.Lkm) || input.Lkm < 0)
      throw Error(
        "The optional reference length must be positive, or left unspecified.",
      );
    run = simulate(input);
    index = 0;
    other = null;
    $("H0").value = run.p.H0;
    $("rho").value = run.p.rho;
    if (run.p.boundary === "comoving") $("R0").value = run.p.R0;
    else $("rb").value = run.p.rb;
    record();
    const p = run.p,
      d = run.diagnostics,
      b = run.events.find((e) => e.kind === "bounce" && e.t > 1e-10),
      rec = run.events.find((e) => e.kind === "recollapse" && e.t > 1e-10);
    $("outcome").textContent = b
      ? `Bounce at τ ${fmt(b.t)}`
      : run.status !== "completed"
        ? "Endpoint unresolved"
        : rec
          ? "Recollapse detected"
          : p.H0 === 0
            ? run.initial.acc > 0
              ? "Starts at imposed bounce"
              : run.initial.acc < 0
                ? "Starts at recollapse"
                : "Static initial state"
            : "No bounce in this interval";
    $("minimumSummary").textContent =
      `Min R_b=${fmt(d.minRadius)} L* at τ=${fmt(d.minTime)}`;
    $("trappingSummary").textContent = d.trapped
      ? "Detected in this interval"
      : "None detected in this interval";
    $("constraintSummary").textContent = d.residual.toExponential(2);
    $("equationLabel").textContent =
      `FLRW k=${p.k} · ${p.theory === "ec" ? "EC / HASHEMI AVERAGED SPIN FLUID" : "GENERAL RELATIVITY / PERFECT FLUID"}`;
    $("initialConstraint").textContent =
      `Hᵢ² + k/aᵢ² = (ρ̄ᵢ − S̄ᵢ²/4)/3. Derived ${p.constraint === "density" ? `HᵢL* = ${fmt(p.H0)}` : `ρ̄ᵢ = ${fmt(p.rho)}`}. Initial relative residual ${run.initial.residual.toExponential(1)}.`;
    $("boundaryNote").textContent =
      `Rᵢ/L* = aᵢ r_b = ${fmt(p.R0)}; Ṙ_b = r_b ȧ. Initial compactness Cᵢ=${fmt(run.initial.compactness)}. The finite region is an interior diagnostic; exterior matching is not supplied.`;
    $("health").textContent =
      `${run.status === "completed" ? "Interval completed" : run.stopReason} ${run.stats.accepted} accepted steps, ${run.stats.rejected} rejected. Mass-identity scaled error ${d.massResidual.toExponential(2)}.`;
    $("conservation").textContent =
      `Ordinary/spin invariant drifts: ${d.matterDrift.toExponential(1)} / ${d.spinDrift.toExponential(1)}. These scalings are enforced by the closure; the Friedmann residual is the independent evolution check.`;
    run.warnings.forEach((w) => message(w));
    $("comparisonNote").hidden = true;
    if ($("showSaved").checked && savedRun) {
      other = savedRun;
      $("comparisonNote").hidden = false;
      $("comparisonNote").textContent =
        `Saved reference: ${other.p.theory.toUpperCase()}, ρ̄ᵢ=${fmt(other.p.rho)}, S̄ᵢ²=${fmt(other.p.spin2)}, Hᵢ=${fmt(other.p.H0)}, aᵢ=${fmt(other.p.a0)}, k=${other.p.k}, r_b=${fmt(other.p.rb)}. Both begin at normalized τ=0. Reference L*=${other.p.Lkm ? fmt(other.p.Lkm) + " km" : "unspecified"}; current L*=${p.Lkm ? fmt(p.Lkm) + " km" : "unspecified"}. Physical times are comparable only with a common reference scale. These are user-selected initial data.`;
    } else if ($("compare").checked) {
      try {
        other = compare(run, $("match").value, +$("spin2").value);
        $("comparisonNote").hidden = false;
        const density = $("match").value === "density";
        $("comparisonNote").textContent =
          `Solid: ${p.theory.toUpperCase()}; dashed: ${other.p.theory.toUpperCase()}. Same aᵢ, k, r_b, w and declared L*. Initial spin²: ${fmt(p.spin2)} vs ${fmt(other.p.spin2)}. ${density ? `Same ordinary density; Hᵢ differs (${fmt(p.H0)} vs ${fmt(other.p.H0)}).` : `Same Hᵢ; ordinary density differs (${fmt(p.rho)} vs ${fmt(other.p.rho)}).`} Both start at τ=0. ${other.status !== "completed" ? `Reference stops early: ${other.stopReason}` : ""}`;
        other.warnings.forEach((w) => message("Comparison: " + w));
      } catch (e) {
        message("Comparison unavailable: " + e.message);
      }
    }
    $("events").replaceChildren();
    $("eventDetail").textContent = "";
    $("eventCount").textContent = `/ ${run.events.length}`;
    if (!run.events.length)
      $("events").textContent =
        "No turning or marginal-trapping events detected in this interval.";
    run.events.forEach((e) => {
      const b = document.createElement("button");
      b.className = "quiet";
      b.textContent = `${e.label} · τ ${fmt(e.t)}`;
      b.onclick = () => {
        pause();
        selectTime(e.t);
        $("eventDetail").textContent =
          e.key === "turn"
            ? `a=${fmt(e.state.a)} L*, R_b=${fmt(e.state.R)} L*, Ḣ=${fmt(e.state.dH)} L*⁻², curvature K=${fmt(e.state.K)} L*⁻⁴. Bounce inequality margin κL*²[4ρ_s−(ρ+3p)]=${fmt(e.bounceMargin)}. Constraint ${e.constraintAtEvent.toExponential(2)}.`
            : `θ₊=${fmt(e.state.thetaPlus)}, θ₋=${fmt(e.state.thetaMinus)} in L*⁻¹; compactness=${fmt(e.state.compactness)}. This is a marginal boundary surface, not an event horizon.`;
      };
      $("events").append(b);
    });
    $("play").disabled = false;
    $("validate").disabled = false;
    draw();
  } catch (e) {
    run = null;
    other = null;
    plot.clear();
    $("outcome").textContent = "Inadmissible / invalid data";
    $("minimumSummary").textContent = "";
    $("constraintSummary").textContent = "—";
    $("trappingSummary").textContent = "Not evaluated";
    $("liveState").textContent = "";
    $("values").replaceChildren();
    $("surfaceState").textContent = "";
    $("referenceState").hidden = true;
    $("physicalScale").textContent = "";
    $("events").replaceChildren();
    $("health").textContent = "No solution computed.";
    $("initialConstraint").textContent = e.message;
    message(e.message, "warning error");
    $("play").disabled = true;
    $("validate").disabled = true;
  }
}
function setSection(name) {
  pause();
  section = name;
  document
    .querySelectorAll("[data-section]")
    .forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.section === name)),
    );
  $("graph").replaceChildren(
    ...graphs[name].map(([value, title]) => {
      const o = document.createElement("option");
      o.value = value;
      o.textContent = title;
      return o;
    }),
  );
  $("researchPanel").hidden = name !== "research";
  $("scale").disabled = false;
  if (name === "matter") $("scale").value = "signedlog";
  else if (name === "collapse") $("scale").value = "linear";
  draw();
}
function updateCursor() {
  if (!run) return;
  const s = run.data[index];
  $("time").value = (index / (run.data.length - 1)) * 1000;
  $("clock").textContent = `τ = ${fmt(s.t)}`;
  const state =
    s.H < -1e-10 ? "Contracting" : s.H > 1e-10 ? "Expanding" : "Stationary";
  $("liveState").textContent =
    `${state} · ${(100 * s.volume).toPrecision(4)}% of initial volume · R_b/Rᵢ=${fmt(s.R / run.p.R0)}`;
  const keys = selectedKeys.length
    ? selectedKeys
    : ["R", "compactness", "thetaPlus", "thetaMinus"];
  $("values").innerHTML = keys
    .slice(0, 4)
    .map(
      (k, i) =>
        `<div class="value" style="--c:${colors[i]}"><span>${specs[k][0]} · ${specs[k][1]}</span><strong>${fmt(s[k])}</strong></div>`,
    )
    .join("");
  $("surfaceState").textContent =
    `Boundary: ${s.classification}. θ₊=${fmt(s.thetaPlus)}, θ₋=${fmt(s.thetaMinus)} L*⁻¹. ${s.classification === "anti-trapped" ? "Both light-front areas increase; this is not future trapping." : ""}`;
  const scale = Math.max(1, ...run.data.map((p) => p.R / run.p.R0)),
    radius = (65 * (s.R / run.p.R0)) / scale,
    initial = 65 / scale;
  $("initialSphere").setAttribute("r", initial);
  $("matterSphere").setAttribute("r", Math.max(0.15, radius));
  $("equator").setAttribute("rx", Math.max(0.15, radius));
  $("equator").setAttribute("ry", Math.max(0.05, radius / 4));
  $("matterSphere").setAttribute(
    "stroke",
    s.classification === "future trapped" ? "#b76e3a" : "#087f83",
  );
  const ahRadius =
    s.rAH !== null ? (65 * ((s.a * s.rAH) / run.p.R0)) / scale : Infinity;
  $("horizonSphere").setAttribute(
    "r",
    Number.isFinite(ahRadius) ? ahRadius : 1,
  );
  $("horizonSphere").setAttribute(
    "visibility",
    ahRadius <= 75 && s.rAH <= run.p.rb ? "visible" : "hidden",
  );
  $("horizonSphere").removeAttribute("hidden");
  const L = run.p.Lkm || 0;
  $("physicalScale").textContent =
    L > 0
      ? `Chosen L*=${fmt(L)} km: t=${fmt((s.t * L) / 299792.458)} s, R_b=${fmt(s.R * L)} km, effective m_MS=${fmt((s.mu * L) / 1.47662504)} M☉. Scale conversion, not an astrophysical calibration.`
      : "";
  $("referenceState").hidden = !other;
  if (other) {
    if (s.t > other.data.at(-1).t + 1e-12) {
      $("referenceState").textContent =
        `${other.p.theory.toUpperCase()} reference: no computed state at this time; stopped at τ=${fmt(other.data.at(-1).t)}. No extrapolation.`;
    } else {
      const ref = other.data.reduce((a, b) =>
        Math.abs(a.t - s.t) < Math.abs(b.t - s.t) ? a : b,
      );
      $("referenceState").textContent =
        `${other.p.theory.toUpperCase()} reference sample at τ=${fmt(ref.t)}: ${keys
          .slice(0, 4)
          .map((k) => `${specs[k][0]}=${fmt(ref[k])} ${specs[k][1]}`)
          .join("; ")}.`;
    }
  }
  plot.move(s.t, $("progressive").checked);
}
function selectTime(t) {
  if (!run) return;
  let best = 0;
  for (let i = 1; i < run.data.length; i++)
    if (Math.abs(run.data[i].t - t) < Math.abs(run.data[best].t - t)) best = i;
  index = best;
  updateCursor();
}
function animate(now) {
  if (!playing || !run) return;
  playTime +=
    (((now - lastFrame) / 1000) * +$("speed").value * run.data.at(-1).t) / 20;
  lastFrame = now;
  selectTime(Math.min(playTime, run.data.at(-1).t));
  if (playTime >= run.data.at(-1).t) pause();
  else frame = requestAnimationFrame(animate);
}
$("play").onclick = () => {
  if (playing) return pause();
  if (!run || !plot.ready) return;
  if (index === run.data.length - 1) index = 0;
  playTime = run.data[index].t;
  lastFrame = performance.now();
  playing = true;
  $("play").textContent = "Pause";
  frame = requestAnimationFrame(animate);
};
$("start").onclick = () => {
  pause();
  index = 0;
  updateCursor();
};
$("time").oninput = () => {
  pause();
  if (!run) return;
  index = Math.round((+$("time").value / 1000) * (run.data.length - 1));
  updateCursor();
};
$("progressive").onchange = updateCursor;
$("resetView").onclick = () => plot.reset();
for (const id of [...ids, "Lkm"])
  $(id).addEventListener("input", () => {
    $("preset").value = "custom";
    recalculate();
  });
$("graph").onchange = () => {
  pause();
  $("scale").disabled = $("graph").value === "regions";
  draw();
};
$("scale").onchange = () => {
  pause();
  draw();
};
$("compare").onchange = () => {
  $("showSaved").checked = false;
  recalculate();
};
$("match").onchange = recalculate;
$("showSaved").onchange = () => {
  $("compare").checked = false;
  recalculate();
};
$("preset").onchange = () => {
  const p = presets[$("preset").value];
  if (p) {
    load(p);
    recalculate();
  }
};
$("reset").onclick = () => {
  load(defaults);
  $("preset").value = "default";
  $("compare").checked = false;
  $("showSaved").checked = false;
  recalculate();
};
$("mode").onchange = () => {
  document.body.classList.toggle("research", $("mode").value === "research");
  record();
};
for (const b of document.querySelectorAll("[data-section]"))
  b.onclick = () => setSection(b.dataset.section);
$("validate").onclick = () => {
  if (!run) return;
  pause();
  const finer = simulate({
      ...run.p,
      tol: run.p.tol / 16,
      maxStep: run.p.T / 1280,
    }),
    c = convergence(run, finer);
  $("validation").textContent =
    `${c.passed ? "PASS" : "NOT ESTABLISHED"} · tolerance ÷16; max step ÷2. Max scaled difference (a,H,K,θ±): ${c.error.toExponential(2)}, turning-time difference ${fmt(c.eventError)}. ${c.count} shared regular samples. ${c.complete ? "Same interval endpoint." : "Stopping endpoints differ."}`;
};
function download(text, name, type) {
  const url = URL.createObjectURL(new Blob([text], { type })),
    a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
$("exportJSON").onclick = () => {
  if (run)
    download(
      JSON.stringify(
        {
          version: 1,
          created: new Date().toISOString(),
          run,
          comparison: other,
        },
        null,
        2,
      ),
      "ec-collapse-run.json",
      "application/json",
    );
};
$("exportCSV").onclick = () => {
  if (!run) return;
  const cols = Object.keys(run.data[0]).filter(
      (k) =>
        typeof run.data[0][k] === "number" ||
        typeof run.data[0][k] === "string" ||
        run.data[0][k] === null,
    ),
    metadata =
      "# " +
      JSON.stringify({
        parameters: run.p,
        assumptions: run.assumptions,
        status: run.status,
      }) +
      "\n";
  download(
    metadata +
      cols.join(",") +
      "\n" +
      run.data.map((s) => cols.map((k) => s[k] ?? "").join(",")).join("\n"),
    "ec-collapse-" + run.p.theory + ".csv",
    "text/csv",
  );
};
$("saveRun").onclick = () => {
  if (!run) return;
  savedRun = run;
  $("showSaved").disabled = false;
  $("savedRunNote").textContent =
    `Saved ${run.p.theory.toUpperCase()} run: ρ̄ᵢ=${fmt(run.p.rho)}, S̄ᵢ²=${fmt(run.p.spin2)}, Hᵢ=${fmt(run.p.H0)}, aᵢ=${fmt(run.p.a0)}, k=${run.p.k}, r_b=${fmt(run.p.rb)}, T=${run.p.T}. Change parameters and overlay this reference.`;
};
function cancelSweep() {
  if (worker) {
    worker.terminate();
    worker = null;
  }
  $("runSweep").disabled = false;
  $("cancelSweep").hidden = true;
}
$("cancelSweep").onclick = () => {
  cancelSweep();
  $("sweepStatus").textContent = "Screen cancelled.";
};
$("runSweep").onclick = () => {
  if (!run) return;
  cancelSweep();
  $("runSweep").disabled = true;
  $("cancelSweep").hidden = false;
  $("sweepStatus").textContent =
    "Integrating admissible initial conditions in a background worker…";
  worker = new Worker(new URL("./sweep-worker.mjs", import.meta.url), {
    type: "module",
  });
  worker.onmessage = ({ data }) => {
    cancelSweep();
    if (data.error) {
      $("sweepStatus").textContent = data.error;
      return;
    }
    sweepResult = data.result;
    $("exportSweep").disabled = false;
    $("sweepStatus").textContent =
      `${sweepResult.rows.length} cases completed. Click a point to load its constrained configuration. Outcome tags apply only to the simulated interval; validate a selected run.`;
    const labels = [
      "No bounce in interval",
      "Bounce, no future trapping",
      "Bounce + future trapping",
      "Recollapse / turning",
      "Unresolved / threshold",
      "Inadmissible",
    ];
    Plotly.react(
      "sweepPlot",
      [
        {
          type: "scatter",
          mode: "markers",
          x: sweepResult.rows.map((r) => r.rb),
          y: sweepResult.rows.map((r) => r.spin2),
          text: sweepResult.rows.map((r) => r.label),
          customdata: sweepResult.rows.map((_, i) => i),
          marker: {
            symbol: "square",
            size: 22,
            color: sweepResult.rows.map((r) => r.code),
            cmin: 0,
            cmax: 5,
            colorscale: [
              [0, "#8aa9a0"],
              [0.199, "#8aa9a0"],
              [0.2, "#188c80"],
              [0.399, "#188c80"],
              [0.4, "#cc8046"],
              [0.599, "#cc8046"],
              [0.6, "#8b73af"],
              [0.799, "#8b73af"],
              [0.8, "#b8b4a3"],
              [0.999, "#b8b4a3"],
              [1, "#d8dcdd"],
            ],
            colorbar: {
              tickvals: [0, 1, 2, 3, 4, 5],
              ticktext: labels,
              thickness: 10,
              tickfont: { size: 9 },
            },
          },
          hovertemplate: "r_b=%{x}<br>S̄ᵢ²=%{y}<br>%{text}<extra></extra>",
        },
      ],
      {
        paper_bgcolor: "#fff",
        plot_bgcolor: "#fff",
        margin: { l: 60, r: 190, t: 15, b: 55 },
        xaxis: { title: "Comoving boundary r_b" },
        yaxis: { title: "Initial spin² κ²L*²Sᵢ²" },
        font: { family: "system-ui", size: 11 },
      },
      { responsive: true, displaylogo: false },
    );
    $("sweepPlot").removeAllListeners?.("plotly_click");
    $("sweepPlot").on("plotly_click", (event) => {
      const cell = sweepResult.rows[event.points[0].customdata];
      load(cell.parameters);
      $("preset").value = "custom";
      recalculate();
    });
  };
  worker.onerror = (e) => {
    cancelSweep();
    $("sweepStatus").textContent = "Screen failed: " + e.message;
  };
  worker.postMessage({
    parameters: run.p,
    options: {
      n: +$("sweepN").value,
      spinMax: +$("sweepSpin").value,
      radiusMax: +$("sweepRadius").value,
    },
  });
};
$("exportSweep").onclick = () => {
  if (sweepResult)
    download(
      JSON.stringify(sweepResult, null, 2),
      "ec-collapse-screen.json",
      "application/json",
    );
};
let initial = defaults;
try {
  const stored = JSON.parse(localStorage.getItem("ec-collapse-lab-v1"));
  if (stored?.parameters) {
    initial = { ...defaults, ...stored.parameters };
    $("mode").value = stored.mode === "research" ? "research" : "basic";
  }
} catch {}
load(initial);
document.body.classList.toggle("research", $("mode").value === "research");
setSection("collapse");
recalculate();
