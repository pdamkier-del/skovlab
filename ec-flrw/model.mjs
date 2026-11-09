/** Effective, isotropically averaged Weyssenhoff fluid. See MODEL.md. */
export const defaults = {
  geometry: "flrw",
  w: 0,
  spin: 1,
  a0: 1,
  branch: "bounce",
  X0: 1,
  Y0: 1,
  hr0: -0.3,
  ho0: -0.3,
  T: 12,
  tol: 1e-8,
};
export function setup(p) {
  const { geometry, w, spin, a0, X0, Y0, hr0, ho0 } = p;
  if (
    ![w, spin, a0, X0, Y0, hr0, ho0, p.T, p.tol].every(Number.isFinite) ||
    w < 0 ||
    w >= 1 ||
    spin < 0 ||
    a0 <= 0 ||
    X0 <= 0 ||
    Y0 <= 0 ||
    p.T <= 0 ||
    p.T > 100 ||
    p.tol <= 0 ||
    (p.maxStep !== undefined && (!Number.isFinite(p.maxStep) || p.maxStep <= 0))
  )
    throw Error(
      "Invalid parameters: require 0 ≤ w < 1, positive scales, interval and tolerance, and nonnegative spin.",
    );
  if (geometry === "flrw") {
    const rho0 = p.branch === "bounce" ? spin * a0 ** (-3 * (1 - w)) : 1;
    if (rho0 <= 0)
      throw Error("A flat FLRW bounce requires positive spin and density.");
    const h2 = rho0 * a0 ** (-3 * (1 + w)) - spin * a0 ** -6;
    if (h2 < -1e-12)
      throw Error(
        "Initial Friedmann constraint has H² < 0. Reduce spin or increase a(0).",
      );
    const H =
      p.branch === "bounce"
        ? 0
        : (p.branch === "contract" ? -1 : 1) * Math.sqrt(Math.max(0, h2));
    const derivative = ([a, v]) => [
      v,
      -0.5 * (1 + 3 * w) * rho0 * a ** (-2 - 3 * w) + 2 * spin * a ** -5,
    ];
    return { rho0, q: [a0, a0 * H], derivative };
  }
  const rhoInitial = ho0 ** 2 + 1 / Y0 ** 2 + 2 * hr0 * ho0 + spin;
  if (rhoInitial <= 0)
    throw Error(
      "The KS constraint requires a positive initial matter density.",
    );
  const V0 = X0 * Y0 ** 2;
  const rho0 = rhoInitial * V0 ** (1 + w),
    sCoeff = spin * V0 ** 2;
  const derivative = ([X, Y, vX, vY]) => {
    const V = X * Y ** 2,
      rho = rho0 * V ** (-1 - w),
      S = sCoeff / V ** 2,
      pressure = w * rho - S;
    const ddY = -(vY ** 2 + 1) / (2 * Y) - (pressure * Y) / 2;
    const ddX = -X * (ddY / Y + (vX * vY) / (X * Y) + pressure);
    return [vX, vY, ddX, ddY];
  };
  return { rho0, sCoeff, q: [X0, Y0, X0 * hr0, Y0 * ho0], derivative };
}
function rk4(q, h, f) {
  const k1 = f(q),
    k2 = f(q.map((x, i) => x + (h * k1[i]) / 2)),
    k3 = f(q.map((x, i) => x + (h * k2[i]) / 2)),
    k4 = f(q.map((x, i) => x + h * k3[i]));
  return q.map((x, i) => x + (h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])) / 6);
}
export function quantities(t, q, p, m) {
  const d = m.derivative(q);
  let a,
    H,
    dH,
    acc,
    shear = 0,
    rho,
    S,
    C,
    den,
    extra = {},
    K,
    R;
  if (p.geometry === "flrw") {
    const [scale, v] = q;
    a = scale;
    H = v / a;
    acc = d[1] / a;
    dH = acc - H ** 2;
    rho = m.rho0 * a ** (-3 * (1 + p.w));
    S = p.spin * a ** -6;
    C = H ** 2 - rho + S;
    den = H ** 2 + rho + S;
    K = 12 * (acc ** 2 + H ** 4);
    R = 6 * (dH + 2 * H ** 2);
    extra = { adot: v };
  } else {
    const [X, Y, vX, vY] = q,
      V = X * Y ** 2,
      hr = vX / X,
      ho = vY / Y,
      ar = d[2] / X,
      ao = d[3] / Y;
    a = Math.cbrt(V);
    H = (hr + 2 * ho) / 3;
    dH = (ar - hr ** 2 + 2 * (ao - ho ** 2)) / 3;
    acc = dH + H ** 2;
    shear = (hr - ho) ** 2 / 3;
    rho = m.rho0 * V ** (-1 - p.w);
    S = m.sCoeff / V ** 2;
    C = ho ** 2 + 1 / Y ** 2 + 2 * hr * ho - rho + S;
    den = ho ** 2 + 1 / Y ** 2 + Math.abs(2 * hr * ho) + rho + S;
    K =
      4 *
      (ar ** 2 +
        2 * ao ** 2 +
        2 * (hr * ho) ** 2 +
        (ho ** 2 + 1 / Y ** 2) ** 2);
    R = 2 * (ar + 2 * ao + 2 * hr * ho + ho ** 2 + 1 / Y ** 2);
    extra = { X, Y, hr, ho };
  }
  return {
    t,
    a,
    H,
    dH,
    acc,
    shear,
    rho,
    S,
    C,
    residual: Math.abs(C) / Math.max(1e-30, den),
    K,
    R,
    ...extra,
  };
}
export function simulate(parameters = {}) {
  const p = { ...defaults, ...parameters },
    m = setup(p),
    initial = quantities(0, m.q, p, m),
    warnings = [];
  const minScale = 1e-5,
    maxRate = 1e6,
    events = [];
  const eventKeys = p.geometry === "ks" ? ["hr", "ho", "H"] : ["H"];
  function addEvent(s, key) {
    const rate =
      key === "H"
        ? s.dH
        : key === "hr"
          ? m.derivative(s._q)[2] / s.X - s.hr ** 2
          : m.derivative(s._q)[3] / s.Y - s.ho ** 2;
    if (Math.abs(rate) < 1e-13) return;
    const kind =
      key === "hr"
        ? "Radial"
        : key === "ho"
          ? "Angular"
          : p.geometry === "ks"
            ? "Volume"
            : "FLRW";
    events.push({
      t: s.t,
      label: `${kind} ${rate > 0 ? "candidate bounce" : "recollapse"}`,
      finite:
        s.a > 0 &&
        Number.isFinite(s.K) &&
        (p.geometry === "flrw" || (s.X > 0 && s.Y > 0)),
      K: s.K,
      dH: s.dH,
      sample: Object.fromEntries(Object.entries(s).filter(([k]) => k !== "_q")),
    });
  }
  for (const key of eventKeys)
    if (initial[key] === 0) addEvent({ ...initial, _q: m.q }, key);
  function integrate(end) {
    let q = m.q.slice(),
      t = 0,
      h = Math.sign(end) * Math.min(0.01, p.T / 100),
      steps = 0;
    const out = [initial];
    let stop = "interval completed";
    outer: for (let k = 1; k <= 800; k++) {
      const target = (end * k) / 800;
      while (Math.abs(target - t) > 1e-13 * Math.max(1, p.T)) {
        if (++steps > 200000) {
          stop = "integration work limit";
          break outer;
        }
        h =
          Math.sign(end) *
          Math.min(Math.abs(h), Math.abs(target - t), p.maxStep ?? p.T / 800);
        const full = rk4(q, h, m.derivative),
          half = rk4(rk4(q, h / 2, m.derivative), h / 2, m.derivative);
        const error = Math.max(
          ...half.map(
            (v, i) =>
              Math.abs(v - full[i]) /
              (15 * p.tol * (1 + Math.max(Math.abs(q[i]), Math.abs(v)))),
          ),
        );
        if (!Number.isFinite(error) || error > 1) {
          h *= Number.isFinite(error)
            ? Math.max(0.1, 0.85 * error ** -0.2)
            : 0.2;
          if (Math.abs(h) < 1e-12) {
            stop = "integrator breakdown: minimum step";
            break outer;
          }
          continue;
        }
        const next = quantities(t + h, half, p, m);
        if (!Object.values(next).every(Number.isFinite)) {
          stop = "integrator breakdown: nonfinite state";
          break outer;
        }
        if (
          half[0] < minScale ||
          (p.geometry === "ks" && half[1] < minScale) ||
          Math.abs(next.H) > maxRate ||
          Math.abs(next.dH) > maxRate ** 2
        ) {
          stop = "integration stopping threshold (scale or rate)";
          break outer;
        }
        const previous = quantities(t, q, p, m);
        for (const key of eventKeys) {
          if (
            !(
              (previous[key] < 0 && next[key] >= 0) ||
              (previous[key] > 0 && next[key] <= 0)
            )
          )
            continue;
          let low = 0,
            high = 1,
            rootQ;
          for (let j = 0; j < 35; j++) {
            const f = (low + high) / 2;
            rootQ = rk4(
              rk4(q, (h * f) / 2, m.derivative),
              (h * f) / 2,
              m.derivative,
            );
            const v = quantities(t + h * f, rootQ, p, m)[key];
            if (v > 0 === previous[key] > 0) low = f;
            else high = f;
          }
          const f = (low + high) / 2;
          rootQ = rk4(
            rk4(q, (h * f) / 2, m.derivative),
            (h * f) / 2,
            m.derivative,
          );
          addEvent({ ...quantities(t + h * f, rootQ, p, m), _q: rootQ }, key);
        }
        q = half;
        t += h;
        h *= error === 0 ? 2 : Math.min(2, 0.9 * error ** -0.2);
      }
      out.push(quantities(t, q, p, m));
    }
    // Preserve the final accepted state even if a threshold fell between output times.
    if (t !== out.at(-1).t) out.push(quantities(t, q, p, m));
    if (stop !== "interval completed")
      warnings.push(
        `${end < 0 ? "Past" : "Future"} integration: ${stop} at τ=${t.toPrecision(6)}. This is not proof of a spacetime singularity.`,
      );
    return out;
  }
  const future = integrate(p.T),
    past =
      p.geometry === "flrw" && p.branch === "bounce" ? integrate(-p.T) : [];
  const data = [...past.slice(1).reverse(), ...future];
  // Keep turning points in the plotted time series even if an episode is shorter than the output spacing.
  for (const e of events)
    if (!data.some((s) => Math.abs(s.t - e.t) < 1e-12))
      data.push({ ...e.sample, eventSample: 1 });
  data.sort((a, b) => a.t - b.t);
  for (const e of events) delete e.sample;
  const aStart = data[0].a;
  let nAcc = 0;
  for (let i = 0; i < data.length; i++) {
    const s = data[i];
    s.N = Math.log(s.a / aStart);
    if (i) {
      const prev = data[i - 1],
        dt = s.t - prev.t; // Endpoint-gated trapezoid, converges with output refinement.
      nAcc +=
        (dt *
          (Math.max(0, prev.H) * (prev.acc > 0 ? 1 : 0) +
            Math.max(0, s.H) * (s.acc > 0 ? 1 : 0))) /
        2;
    }
    s.Nacc = nAcc;
  }
  const maxResidual = Math.max(...data.map((s) => s.residual));
  if (maxResidual > 1e-5)
    warnings.push(
      "Possible numerical divergence: relative constraint residual exceeds 10⁻⁵. Reduce tolerance and compare.",
    );
  const danger = data.filter(
    (s) =>
      Math.abs(s.H) > 100 ||
      Math.abs(s.dH) > 1e4 ||
      s.a < 0.01 ||
      s.shear > 1e4 ||
      (p.geometry === "ks" && Math.min(s.X, s.Y) < 0.01),
  );
  if (danger.length)
    warnings.push(
      `Candidate singular behaviour / rapid growth near τ=${danger[0].t.toPrecision(5)}. Threshold-based diagnostic; check step convergence and curvature.`,
    );
  return {
    p,
    data,
    events: events.sort((a, b) => a.t - b.t),
    warnings,
    maxResidual,
    rho0: m.rho0,
    initial,
  };
}
export function convergence(a, b) {
  // Compare independently integrated solutions at identical output times.
  const index = new Map(b.data.map((s) => [s.t.toPrecision(13), s]));
  let error = 0,
    count = 0;
  for (const s of a.data) {
    if (s.eventSample) continue;
    const r = index.get(s.t.toPrecision(13));
    if (!r) continue;
    count++;
    for (const k of ["a", "H", "dH", "K"])
      error = Math.max(error, Math.abs(s[k] - r[k]) / (1 + Math.abs(r[k])));
  }
  return {
    error,
    count,
    complete:
      Math.abs(a.data.at(-1).t - b.data.at(-1).t) < 1e-10 &&
      Math.abs(a.data[0].t - b.data[0].t) < 1e-10 &&
      count === a.data.filter((s) => !s.eventSample).length,
  };
}
