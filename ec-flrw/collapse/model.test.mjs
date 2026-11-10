import test from "node:test";
import assert from "node:assert/strict";
import { integrate } from "./solver.mjs";
import {
  simulate,
  initialData,
  defaults,
  compare,
  convergence,
} from "./model.mjs";
import { surface } from "./geometry.mjs";
const near = (a, b, tol = 1e-7) =>
  assert.ok(Math.abs(a - b) < tol, `${a} differs from ${b}`);
test("Dormand–Prince exponential and oscillator; actual step refinement", () => {
  const a = integrate({
      q0: [1],
      f: (q) => q,
      end: 2,
      tol: 1e-8,
      maxStep: 0.4,
      samples: 5,
    }),
    b = integrate({
      q0: [1],
      f: (q) => q,
      end: 2,
      tol: 1e-11,
      maxStep: 0.02,
      samples: 5,
    });
  near(a.data.at(-1).q[0], Math.exp(2), 1e-6);
  near(b.data.at(-1).q[0], Math.exp(2), 1e-10);
  assert.ok(b.stats.accepted > a.stats.accepted);
  const r = integrate({
    q0: [1, 0],
    f: (q) => [q[1], -q[0]],
    end: 2 * Math.PI,
    tol: 1e-10,
    maxStep: 0.02,
  });
  near(r.data.at(-1).q[0], 1, 1e-9);
  near(r.data.at(-1).q[1], 0, 1e-9);
});
test("solver root refinement, guards and failure reporting", () => {
  const r = integrate({
    q0: [1],
    f: () => [-1],
    end: 2,
    events: [{ key: "zero", value: (q) => q[0] }],
  });
  near(r.events[0].t, 1, 1e-10);
  const fail = integrate({ q0: [1], f: () => [NaN], end: 1 });
  assert.equal(fail.status, "step-failure");
  const stop = integrate({
    q0: [1],
    f: () => [-1],
    end: 2,
    guard: (q) => (q[0] < 0.2 ? { kind: "threshold", message: "test" } : null),
  });
  assert.equal(stop.status, "threshold");
  assert.ok(stop.data.at(-1).q[0] >= 0.2);
});
test("constrained density/velocity and boundary modes; reject impossible data", () => {
  const p = initialData();
  near(p.H0, -Math.sqrt(0.9));
  const v = initialData({ ...p, constraint: "velocity" });
  near(v.rho, 3);
  const r = initialData({ a0: 2, boundary: "physical", R0: 3 });
  near(r.rb, 1.5);
  near(r.R0, 3);
  assert.throws(() => initialData({ k: 1, rho: 1 }), /Hᵢ²/);
  assert.throws(() => initialData({ k: 1, rho: 9, rb: 1 }), /chart/);
  assert.throws(
    () => initialData({ k: -1, constraint: "velocity", H0: 0, spin2: 0 }),
    /nonnegative/,
  );
  assert.throws(() => initialData({ spin2: 100 }), /Hᵢ²/);
  assert.throws(() => initialData({ a0: 0 }), /Require/);
});
test("GR flat dust analytic collapse and conserved geometric mass", () => {
  const r = simulate({ theory: "gr", T: 0.6 });
  for (const s of r.data) {
    near(s.a, (1 - 1.5 * s.t) ** (2 / 3), 2e-8);
    near(s.mu, r.initial.mu, 1e-8);
    near(s.K, (s.rho ** 2 * 5) / 3, 1e-5);
  }
  assert.ok(r.diagnostics.residual < 1e-7);
  assert.equal(
    r.events.some((e) => e.kind === "bounce"),
    false,
  );
});
test("flat EC dust: exact two-sided bounce solution and published Eq. 32–33 limit", () => {
  const r = simulate(),
    A = (r.p.rho * r.p.a0 ** 3) / 3,
    D = (r.p.spin2 * r.p.a0 ** 6) / 12,
    tB = (2 * Math.sqrt(A * r.p.a0 ** 3 - D)) / (3 * A),
    aB = Math.cbrt(D / A),
    e = r.events.find((e) => e.kind === "bounce");
  near(e.t, tB, 1e-8);
  near(e.state.a, aB, 1e-8);
  assert.ok(e.bounceMargin > 0);
  near(e.state.rhoEff, (3 * r.p.k) / e.state.a ** 2, 1e-6);
  for (const s of r.data)
    near(s.a ** 3, D / A + (9 * A * (s.t - tB) ** 2) / 4, 1e-7);
  assert.ok(r.diagnostics.residual < 1e-7);
  assert.equal(r.status, "completed");
});
test("closed GR cycloid and empty open Milne limit", () => {
  const r = simulate({ theory: "gr", k: 1, rho: 3, rb: 0.5, T: 1 });
  for (const s of r.data) {
    let lo = 0,
      hi = Math.PI;
    for (let n = 0; n < 55; n++) {
      let mid = (lo + hi) / 2;
      if ((mid + Math.sin(mid)) / 2 < s.t) lo = mid;
      else hi = mid;
    }
    near(s.a, (1 + Math.cos((lo + hi) / 2)) / 2, 1e-8);
  }
  const m = simulate({ theory: "gr", k: -1, rho: 0, rb: 1, T: 0.8 });
  for (const s of m.data) {
    near(s.a, 1 - s.t, 1e-10);
    near(s.K, 0, 1e-10);
    near(s.mu, 0, 1e-10);
  }
  assert.equal(m.diagnostics.trapped, false);
});
test("Misner–Sharp geometric/source identities, null product, and trace for all k and w", () => {
  for (const k of [-1, 0, 1])
    for (const w of [0, 1 / 3, 0.6]) {
      const r = simulate({
        k,
        w,
        rho: 9,
        spin2: 1.2,
        rb: 0.4,
        T: 0.25,
        tol: 1e-11,
      });
      for (const s of r.data) {
        near(s.mu, s.massMatter, 1e-7);
        near(
          s.thetaPlus * s.thetaMinus,
          (4 * (s.compactness - 1)) / s.R ** 2,
          1e-7,
        );
        near(
          (s.Rscalar - (s.rho - 3 * s.pressure + s.spin2 / 2)) /
            (1 + s.rho + 3 * s.pressure + s.spin2 / 2),
          0,
          1e-8,
        );
        near(s.acc, s.dH + s.H ** 2, 1e-10);
      }
    }
});
test("future trapping differs from anti-trapping at the same compactness", () => {
  const a = surface(1, -2, 0, 1),
    b = surface(1, 2, 0, 1);
  assert.equal(a.classification, "future trapped");
  assert.equal(b.classification, "anti-trapped");
  near(a.compactness, b.compactness);
  assert.equal(surface(1, -1, 0, 1).classification, "marginal outer");
  assert.equal(surface(1, 1, 0, 1).classification, "marginal inner");
});
test("boundary trapping forms and disappears before EC bounce; refined event conditions", () => {
  const r = simulate(),
    enter = r.events.find((e) => e.kind === "trapped-enter"),
    exit = r.events.find((e) => e.kind === "trapped-exit"),
    bounce = r.events.find((e) => e.kind === "bounce");
  assert.ok(enter.t < exit.t && exit.t < bounce.t);
  for (const e of [enter, exit]) {
    near(e.state.thetaPlus, 0, 1e-8);
    assert.ok(e.state.thetaMinus < 0);
    near(e.state.compactness, 1, 1e-8);
    assert.ok(r.data.some((s) => s.t === e.t));
  }
  const small = simulate({ rb: 0.3 });
  assert.equal(small.diagnostics.trapped, false);
  assert.equal(small.diagnostics.bounced, true);
});
test("ordinary and spin invariants; effective mass pressure-work relation", () => {
  const r = simulate({ w: 1 / 3, T: 1 });
  assert.ok(r.diagnostics.matterDrift < 1e-12);
  assert.ok(r.diagnostics.spinDrift < 1e-12);
  const d = r.data.filter((s) => !s.eventSample);
  for (let i = 1; i < d.length - 1; i += 40) {
    const l = d[i - 1],
      s = d[i],
      u = d[i + 1],
      derivative = (u.mu - l.mu) / (u.t - l.t);
    near(derivative, (-s.pEff * s.R ** 2 * s.Rdot) / 2, 1e-3);
  }
});
test("GR/EC comparisons explicitly match density OR velocity", () => {
  const ec = simulate({ T: 0.3 }),
    grDensity = compare(ec, "density"),
    grVelocity = compare(ec, "velocity");
  near(grDensity.p.rho, ec.p.rho);
  assert.notEqual(grDensity.p.H0, ec.p.H0);
  near(grVelocity.p.H0, ec.p.H0);
  assert.notEqual(grVelocity.p.rho, ec.p.rho);
  assert.ok(grVelocity.diagnostics.residual < 1e-7);
});
test("regular collapse/bounce remains stable with half maximum step and tighter tolerance", () => {
  const a = simulate(),
    b = simulate({ tol: 1e-11, maxStep: defaults.T / 1280 });
  const c = convergence(a, b);
  assert.equal(c.passed, true);
  assert.ok(c.error < 1e-6);
  assert.ok(b.stats.accepted > a.stats.accepted);
});
test("GR endpoint threshold is explicitly unresolved, not a computed singularity", () => {
  const r = simulate({ theory: "gr" });
  assert.equal(r.status, "threshold");
  assert.ok(r.data.at(-1).t < 2 / 3);
  assert.ok(r.warnings.some((w) => /threshold|unresolved/.test(w)));
  assert.ok(r.data.every((s) => s.a > 0 && Number.isFinite(s.K)));
});
test("Hashemi Fig.1 parameter reproduction after k normalization; independent quadrature", () => {
  // Original: C=1.11, D=.08, k=2C-D=2.14, a_i=1, v_i=0.
  // Transform a_new=a_old/sqrt(k_old), r_new=sqrt(k_old)*r_old to k_new=+1.
  const p = {
      theory: "ec",
      k: 1,
      a0: 1 / Math.sqrt(2.14),
      rho: 6.66,
      spin2: 0.96,
      rb: 0.5,
      T: 2,
      constraint: "velocity",
      H0: 0,
      tol: 1e-11,
    },
    r = simulate(p),
    e = r.events.find((e) => e.kind === "bounce" && e.t > 0);
  assert.ok(e);
  const A = (r.p.rho * r.p.a0 ** 3) / 3,
    D = (r.p.spin2 * r.p.a0 ** 6) / 12,
    F = (a) => A / a - D / a ** 4 - 1;
  let lo = r.p.a0 * 1e-4,
    hi = r.p.a0 * 0.7;
  for (let j = 0; j < 70; j++) {
    const mid = (lo + hi) / 2;
    if (F(mid) < 0) lo = mid;
    else hi = mid;
  }
  const aB = (lo + hi) / 2;
  near(e.state.a, aB, 1e-8);
  let total = 0,
    N = 20000,
    delta = r.p.a0 - aB;
  for (let j = 0; j < N; j++) {
    const phi = ((j + 0.5) * Math.PI) / (2 * N),
      a = aB + delta * Math.sin(phi) ** 2;
    total +=
      (2 * delta * Math.sin(phi) * Math.cos(phi)) /
      Math.sqrt(Math.max(0, F(a)));
  }
  const tB = (total * Math.PI) / (2 * N);
  near(e.t, tB, 2e-7);
  assert.ok(e.state.K > 0 && Number.isFinite(e.state.K));
});
