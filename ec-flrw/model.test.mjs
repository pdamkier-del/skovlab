import test from "node:test";
import assert from "node:assert/strict";
import {
  simulate,
  setup,
  defaults,
  quantities,
  convergence,
} from "./model.mjs";
const close = (a, b, tol = 1e-6) =>
  assert.ok(Math.abs(a - b) < tol, `${a} vs ${b}`);
test("retained analytic FLRW dust benchmark a³=1+9τ²/4", () => {
  const r = simulate();
  for (const s of r.data) {
    const D = 1 + (9 * s.t * s.t) / 4;
    close(s.a, Math.cbrt(D), 2e-7);
    close(s.H, (1.5 * s.t) / D, 2e-7);
    close(s.dH, (1.5 * (1 - 2.25 * s.t * s.t)) / (D * D), 2e-7);
  }
  assert.ok(r.maxResidual < 1e-7);
  assert.equal(r.events.length, 1);
  close(r.events[0].t, 0);
  close(r.events[0].K, 27);
  close(r.data.at(-1).Nacc, Math.log(4) / 3, 0.012);
});
test("FLRW constraint, alternate initial data and spin scaling", () => {
  for (const w of [0, 1 / 3, 0.8]) {
    const r = simulate({ w, spin: 0.5, branch: "contract", T: 2 });
    assert.ok(r.initial.H < 0);
    assert.ok(r.maxResidual < 1e-5);
    for (const s of r.data) {
      close(s.S * s.a ** 6, 0.5, 1e-6);
      close(s.rho * s.a ** (3 * (1 + w)), 1, 1e-6);
    }
    assert.ok(r.events.some((e) => e.label.includes("bounce")));
  }
});
test("KS equations, constraint and geometric invariants independently evaluated", () => {
  const p = { ...defaults, geometry: "ks", spin: 0.5, T: 1 };
  const m = setup(p),
    r = simulate(p);
  for (const s of r.data) {
    const V = s.X * s.Y ** 2,
      ddY = (-s.Y * (s.ho * s.ho + 1 / s.Y ** 2 + p.w * s.rho - s.S)) / 2;
    const ddX = -s.X * (ddY / s.Y + s.hr * s.ho + p.w * s.rho - s.S);
    close(s.rho * V ** (1 + p.w), m.rho0, 1e-8);
    close(s.S * V ** 2, m.sCoeff, 1e-8);
    close(
      s.K,
      4 *
        ((ddX / s.X) ** 2 +
          2 * (ddY / s.Y) ** 2 +
          2 * (s.hr * s.ho) ** 2 +
          (s.ho * s.ho + 1 / s.Y ** 2) ** 2),
      1e-7,
    );
    close(s.R, s.rho - 3 * p.w * s.rho + 2 * s.S, 1e-6);
    close(s.acc, s.dH + s.H * s.H, 1e-10);
  }
  assert.ok(r.maxResidual < 1e-7);
  assert.ok(r.events.some((e) => e.label.startsWith("Radial")));
  assert.ok(!r.events.some((e) => e.label.startsWith("Volume")));
});
test("independent finite-difference derivative and Ricci identity", () => {
  for (const geometry of ["flrw", "ks"]) {
    const p = { ...defaults, geometry, spin: 0.5, T: 1 },
      m = setup(p),
      q = m.q,
      d = m.derivative(q),
      eps = 1e-6;
    const left = quantities(
        -eps,
        q.map((v, i) => v - eps * d[i]),
        p,
        m,
      ),
      right = quantities(
        eps,
        q.map((v, i) => v + eps * d[i]),
        p,
        m,
      ),
      s = quantities(0, q, p, m);
    close((right.H - left.H) / (2 * eps), s.dH, 1e-7);
    if (geometry === "flrw")
      close(s.R, 3 * ((1 - 3 * p.w) * s.rho + 2 * s.S), 1e-8);
  }
});
test("tolerance / step reduction stabilizes both regular models", () => {
  for (const geometry of ["flrw", "ks"]) {
    const a = simulate({ geometry, T: 1, spin: 0.5, tol: 1e-6 }),
      b = simulate({
        geometry,
        T: 1,
        spin: 0.5,
        tol: 1e-10,
        maxStep: 1 / 1600,
      }),
      c = convergence(a, b);
    assert.ok(c.complete);
    assert.ok(c.error < 1e-5);
    assert.ok(b.maxResidual < 1e-7);
  }
});
test("numerical threshold is not reported as proven singularity", () => {
  const r = simulate({ geometry: "ks", spin: 0, T: 5 });
  assert.ok(r.warnings.some((w) => w.includes("not proof")));
  assert.ok(r.data.every((s) => s.X > 0 && s.Y > 0 && Number.isFinite(s.K)));
  assert.ok(r.data.at(-1).t < 5);
});
test("invalid constraints fail explicitly", () => {
  assert.throws(() => simulate({ spin: 2, branch: "contract" }), /H²/);
  assert.throws(() => simulate({ spin: 0, branch: "bounce" }), /positive spin/);
  assert.throws(
    () => simulate({ geometry: "ks", hr0: 10, ho0: -1, spin: 0 }),
    /positive initial/,
  );
});
test("fast turning points are refined and inserted into the plotted shared time series", () => {
  const r = simulate({ w: 0.8, spin: 0.1, branch: "contract", T: 2 });
  const e = r.events.find((e) => e.label.includes("bounce"));
  assert.ok(e);
  assert.ok(e.dH > 0);
  const s = r.data.find((s) => s.t === e.t);
  assert.ok(s);
  assert.ok(Math.abs(s.H) < 1e-3);
  assert.ok(r.warnings.some((w) => w.includes("numerical divergence")));
});
