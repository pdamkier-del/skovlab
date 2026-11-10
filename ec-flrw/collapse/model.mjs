import { integrate } from "./solver.mjs";
import { matter } from "./matter.mjs";
import { diagnose, surface } from "./geometry.mjs";
export const defaults = {
  theory: "ec",
  k: 0,
  w: 0,
  rho: 3,
  spin2: 1.2,
  a0: 1,
  H0: -1,
  branch: "contract",
  constraint: "density",
  boundary: "comoving",
  rb: 1.02,
  R0: 1.02,
  T: 1.3,
  tol: 1e-9,
};
export function initialData(parameters = {}) {
  const p = { ...defaults, ...parameters };
  if (
    !["gr", "ec"].includes(p.theory) ||
    ![-1, 0, 1].includes(p.k) ||
    !["density", "velocity"].includes(p.constraint) ||
    !["comoving", "physical"].includes(p.boundary) ||
    !["contract", "expand"].includes(p.branch)
  )
    throw Error("Unknown theory, curvature or initial-data convention.");
  if (
    !["w", "rho", "spin2", "a0", "H0", "rb", "R0", "T", "tol"].every((k) =>
      Number.isFinite(p[k]),
    ) ||
    p.w < 0 ||
    p.w >= 1 ||
    p.a0 <= 0 ||
    p.spin2 < 0 ||
    p.rho < 0 ||
    p.T <= 0 ||
    p.T > 100 ||
    p.tol <= 0 ||
    p.tol > 1e-3
  )
    throw Error(
      "Require finite inputs, 0 ≤ w < 1, nonnegative matter/spin and positive aᵢ, time extent and tolerance.",
    );
  if (p.theory === "gr") p.spin2 = 0;
  if (p.constraint === "velocity")
    p.rho = 3 * (p.H0 ** 2 + p.k / p.a0 ** 2) + p.spin2 / 4;
  else {
    const h2 = (p.rho - p.spin2 / 4) / 3 - p.k / p.a0 ** 2;
    if (h2 < -1e-13 * Math.max(1, p.rho, p.spin2))
      throw Error(
        "Inadmissible initial data: the Friedmann constraint gives Hᵢ² < 0.",
      );
    p.H0 = (p.branch === "contract" ? -1 : 1) * Math.sqrt(Math.max(0, h2));
  }
  if (p.rho < 0 || (p.spin2 > 0 && p.rho === 0))
    throw Error(
      "The constraint requires a nonnegative ordinary density; nonzero spin requires ordinary matter.",
    );
  if (p.boundary === "physical") p.rb = p.R0 / p.a0;
  else p.R0 = p.a0 * p.rb;
  if (!(p.rb > 0 && 1 - p.k * p.rb ** 2 > 0))
    throw Error(
      "Boundary is outside the regular FLRW chart: require r_b > 0 and 1 − k r_b² > 0. For k = +1, use r_b < 1.",
    );
  if (
    p.maxStep !== undefined &&
    (!Number.isFinite(p.maxStep) || p.maxStep <= 0)
  )
    throw Error("Maximum step must be finite and positive.");
  return p;
}
export function simulate(parameters = {}) {
  const p = initialData(parameters),
    context = { ...p, matter: (a) => matter(a, p) },
    q0 = [p.a0, p.a0 * p.H0];
  const f = (q) => {
    const m = matter(q[0], p);
    return [q[1], (-q[0] * (m.rho + 3 * m.pressure - m.spin2)) / 6];
  };
  const evaluate = (t, q) => diagnose(t, q, context);
  const integration = integrate({
    q0,
    f,
    end: p.T,
    tol: p.tol,
    maxStep: p.maxStep ?? p.T / 640,
    samples: p.samples ?? 640,
    events: [
      { key: "turn", value: (q) => q[1] },
      { key: "outer", value: (q) => surface(q[0], q[1], p.k, p.rb).outgoing },
      { key: "inner", value: (q) => surface(q[0], q[1], p.k, p.rb).ingoing },
    ],
    guard: (q) => {
      if (q[0] < p.a0 * 1e-5)
        return {
          kind: "threshold",
          message:
            "Integration stopped at a/aᵢ < 10⁻⁵; this is a stopping threshold, not a proven singularity.",
        };
      const s = evaluate(0, q);
      if (
        !Object.values(s)
          .filter((v) => typeof v === "number")
          .every(Number.isFinite)
      )
        return {
          kind: "nonfinite",
          message: "Nonfinite diagnostic; numerical evolution unresolved.",
        };
      if (Math.abs(s.H) > 1e7 || Math.abs(s.dH) > 1e14 || s.K > 1e32)
        return {
          kind: "threshold",
          message:
            "Rate or curvature safety threshold reached; endpoint unresolved.",
        };
      return null;
    },
  });
  const events = integration.events.map((e) => {
    const state = evaluate(e.t, e.q);
    let kind, label;
    if (e.key === "turn") {
      kind =
        state.acc > 0 ? "bounce" : state.acc < 0 ? "recollapse" : "stationary";
      label =
        kind === "bounce"
          ? "Candidate bounce"
          : kind === "recollapse"
            ? "Recollapse"
            : "Stationary point";
    } else if (e.key === "outer") {
      kind = e.direction < 0 ? "trapped-enter" : "trapped-exit";
      label =
        e.direction < 0
          ? "Boundary becomes future trapped"
          : "Boundary leaves future trapping";
    } else {
      kind = e.direction > 0 ? "anti-enter" : "anti-exit";
      label =
        e.direction > 0
          ? "Boundary becomes anti-trapped"
          : "Boundary leaves anti-trapping";
    }
    return {
      ...e,
      state,
      kind,
      label,
      bounceMargin: state.spin2 - (state.rho + 3 * state.pressure),
      constraintAtEvent: state.residual,
    };
  });
  const initial = evaluate(0, q0);
  if (Math.abs(p.H0) < 1e-14 && Math.abs(initial.acc) > 1e-14)
    events.unshift({
      key: "turn",
      t: 0,
      q: q0,
      state: initial,
      kind: initial.acc > 0 ? "bounce" : "recollapse",
      label: initial.acc > 0 ? "Initial imposed bounce" : "Initial recollapse",
      bounceMargin: initial.spin2 - initial.rho - 3 * initial.pressure,
      constraintAtEvent: initial.residual,
    });
  const data = integration.data.map((s) => evaluate(s.t, s.q));
  for (const e of events)
    if (!data.some((s) => Math.abs(s.t - e.t) < 1e-12))
      data.push({ ...e.state, eventSample: 1 });
  data.sort((a, b) => a.t - b.t);
  events.sort((a, b) => a.t - b.t);
  const residual = Math.max(...data.map((s) => s.residual)),
    massResidual = Math.max(...data.map((s) => s.massResidual));
  let matterDrift = 0,
    spinDrift = 0;
  for (const s of data) {
    matterDrift = Math.max(
      matterDrift,
      Math.abs(s.rho * (s.a / p.a0) ** (3 * (1 + p.w)) - p.rho) / (1 + p.rho),
    );
    spinDrift = Math.max(
      spinDrift,
      Math.abs(s.spin2 * (s.a / p.a0) ** 6 - p.spin2) / (1 + p.spin2),
    );
  }
  const warnings = [];
  if (integration.status !== "completed") warnings.push(integration.detail);
  if (residual > 1e-6)
    warnings.push(
      "Relative Friedmann residual exceeds 10⁻⁶; numerical accuracy is insufficient.",
    );
  if (data.some((s) => s.K > 1e8 || Math.abs(s.H) > 100))
    warnings.push(
      "Rapid curvature/rate growth: candidate singular behaviour. Inspect convergence; no event horizon or completed singular endpoint is inferred.",
    );
  const bounced = events.some((e) => e.kind === "bounce" && e.t > 1e-10),
    recollapsed = events.some((e) => e.kind === "recollapse"),
    trapped =
      data.some((s) => s.classification === "future trapped") ||
      events.some((e) => e.kind === "trapped-enter"),
    antiTrapped =
      data.some((s) => s.classification === "anti-trapped") ||
      events.some((e) => e.kind === "anti-enter");
  const min = data.reduce((a, b) => (a.R < b.R ? a : b));
  return {
    p,
    data,
    events,
    initial,
    stats: integration.stats,
    status: integration.status,
    stopReason: integration.detail,
    warnings,
    diagnostics: {
      residual,
      massResidual,
      matterDrift,
      spinDrift,
      minRadius: min.R,
      minTime: min.t,
      bounced,
      recollapsed,
      trapped,
      antiTrapped,
    },
    assumptions: {
      equations:
        "FLRW + homogeneous isotropically averaged Weyssenhoff closure; Hashemi et al. 2015 Eq. 9, 16–19",
      signature: "(-+++)",
      units: "τ=t/L*, a=a_phys/L*, ρbar=κL*²ρ, spin2bar=κ²L*²S², μ=Gm/L*; c=1",
      boundary:
        "Comoving diagnostic sphere; exterior matching and event horizons not solved.",
      particleProduction: false,
    },
  };
}
export function compare(primary, match = "density", ecSpin2 = defaults.spin2) {
  const p = {
    ...primary.p,
    theory: primary.p.theory === "ec" ? "gr" : "ec",
    spin2: primary.p.theory === "ec" ? 0 : ecSpin2,
  };
  if (match === "velocity") {
    p.constraint = "velocity";
    p.H0 = primary.p.H0;
  } else {
    p.constraint = "density";
    p.rho = primary.p.rho;
    p.branch = primary.p.H0 > 0 ? "expand" : "contract";
  }
  return simulate(p);
}
export function convergence(coarse, fine) {
  const index = new Map(
    fine.data
      .filter((s) => !s.eventSample)
      .map((s) => [s.t.toPrecision(12), s]),
  );
  let count = 0,
    error = 0;
  for (const s of coarse.data) {
    if (s.eventSample) continue;
    const r = index.get(s.t.toPrecision(12));
    if (!r) continue;
    count++;
    for (const key of ["a", "H", "K", "thetaPlus", "thetaMinus"])
      error = Math.max(
        error,
        Math.abs(s[key] - r[key]) / (1 + Math.abs(r[key])),
      );
  }
  const complete =
    Math.abs(coarse.data.at(-1).t - fine.data.at(-1).t) < 1e-10 &&
    count === coarse.data.filter((s) => !s.eventSample).length;
  const turns = coarse.events.filter((e) => e.key === "turn"),
    other = fine.events.filter((e) => e.key === "turn");
  const eventError =
    turns.length === other.length
      ? Math.max(0, ...turns.map((e, i) => Math.abs(e.t - other[i].t)))
      : Infinity;
  return {
    count,
    error,
    eventError,
    complete,
    passed:
      complete &&
      count > 1 &&
      error < 1e-5 &&
      eventError < 1e-5 &&
      coarse.diagnostics.residual < 1e-6 &&
      fine.diagnostics.residual < 1e-6,
  };
}
