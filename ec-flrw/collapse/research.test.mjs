import test from "node:test";
import assert from "node:assert/strict";
import { screen } from "./research.mjs";
import { defaults } from "./model.mjs";
test("screen enforces density constraints and finite-interval / invalid / unresolved labels", () => {
  const r = screen(defaults, { n: 5, spinMax: 16, radiusMax: 1.4 });
  assert.equal(r.rows.length, 25);
  assert.ok(r.rows.some((c) => c.code === 5));
  assert.ok(r.rows.some((c) => c.code === 4));
  assert.ok(r.rows.some((c) => c.bounce));
  assert.ok(r.rows.some((c) => c.initialTurning && c.code === 3 && !c.bounce));
  assert.ok(r.rows.some((c) => c.bounce && !c.trapped));
  for (const cell of r.rows.filter((c) => c.code !== 5)) {
    const p = cell.parameters;
    assert.ok(
      Math.abs(p.H0 ** 2 + p.k / p.a0 ** 2 - (p.rho - p.spin2 / 4) / 3) < 1e-10,
    );
    assert.equal(p.rho, defaults.rho);
    assert.ok(cell.actualEnd <= p.T);
  }
});
test("screen validates grid controls instead of running unbounded batches", () => {
  assert.throws(() => screen(defaults, { n: 100 }), /Screen requires/);
  assert.throws(() => screen(defaults, { spinMax: -1 }), /Screen requires/);
});
