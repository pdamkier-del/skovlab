import { simulate, initialData } from "./model.mjs";
export function screen(
  parameters,
  { n = 5, spinMax = 2.4, radiusMax = 1.4 } = {},
) {
  if (
    ![5, 8].includes(n) ||
    !Number.isFinite(spinMax) ||
    spinMax < 0 ||
    !Number.isFinite(radiusMax) ||
    radiusMax <= 0
  )
    throw Error(
      "Screen requires 5×5 or 8×8 points, nonnegative spin maximum and positive radius maximum.",
    );
  const base = initialData(parameters),
    rows = [];
  for (let j = 0; j < n; j++)
    for (let i = 0; i < n; i++) {
      const spin2 = (spinMax * j) / (n - 1),
        rb = (radiusMax * (i + 1)) / n,
        p = {
          ...base,
          theory: "ec",
          constraint: "density",
          rho: base.rho,
          spin2,
          boundary: "comoving",
          rb,
        };
      try {
        const r = simulate(p),
          unresolved =
            r.status !== "completed" || r.diagnostics.residual > 1e-6,
          bounce = r.diagnostics.bounced,
          recollapse = r.diagnostics.recollapsed,
          initialTurning = r.events.some((e) => e.key === "turn" && e.t === 0),
          trapped = r.diagnostics.trapped;
        rows.push({
          spin2,
          rb,
          code: unresolved
            ? 4
            : bounce
              ? trapped
                ? 2
                : 1
              : recollapse || initialTurning
                ? 3
                : 0,
          label: unresolved
            ? "Numerically unresolved / stopping threshold"
            : bounce
              ? trapped
                ? "Bounce; future trapping in interval"
                : "Bounce; no future trapping in interval"
              : initialTurning
                ? "Initial imposed turning point; no later bounce detected"
                : recollapse
                  ? "Recollapse / turning behaviour"
                  : "No bounce in simulated interval",
          trapped,
          bounce,
          recollapse,
          initialTurning,
          status: r.status,
          residual: r.diagnostics.residual,
          actualEnd: r.data.at(-1).t,
          parameters: r.p,
        });
      } catch (e) {
        rows.push({
          spin2,
          rb,
          code: 5,
          label: "Inadmissible initial data",
          error: e.message,
          parameters: p,
        });
      }
    }
  return {
    version: 1,
    created: new Date().toISOString(),
    base: base,
    grid: { n, spinMax, radiusMax },
    rows,
    interpretation:
      "Exploratory finite-interval screen, not a physical phase boundary. Initial H is derived at each point. No trapping means none detected in this interval; no event horizon computed. Validate selected cells with half-step comparison.",
  };
}
