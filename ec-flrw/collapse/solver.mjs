/** Dormand–Prince 5(4), seven-stage embedded adaptive method.
 * Coefficients: Dormand & Prince, J. Comp. Appl. Math. 6 (1980) 19–26.
 * State-independent event functions; roots refined by reintegration inside accepted steps.
 */
export function step(q, h, f, t = 0) {
  const A = [
      [],
      [1 / 5],
      [3 / 40, 9 / 40],
      [44 / 45, -56 / 15, 32 / 9],
      [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
      [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656],
      [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84],
    ],
    C = [0, 1 / 5, 3 / 10, 4 / 5, 8 / 9, 1, 1];
  const B = [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0],
    E = [
      35 / 384 - 5179 / 57600,
      0,
      500 / 1113 - 7571 / 16695,
      125 / 192 - 393 / 640,
      -2187 / 6784 + 92097 / 339200,
      11 / 84 - 187 / 2100,
      -1 / 40,
    ];
  const k = [];
  for (let j = 0; j < 7; j++)
    k.push(
      f(
        q.map((x, i) => x + h * A[j].reduce((v, a, n) => v + a * k[n][i], 0)),
        t + C[j] * h,
      ),
    );
  return {
    q: q.map((x, i) => x + h * B.reduce((v, b, j) => v + b * k[j][i], 0)),
    error: q.map((_, i) => h * E.reduce((v, b, j) => v + b * k[j][i], 0)),
  };
}
export function integrate({
  q0,
  f,
  end,
  tol = 1e-9,
  maxStep = end / 640,
  samples = 640,
  events = [],
  guard = () => null,
  maxAttempts = 100000,
  minStep = 1e-13,
}) {
  if (
    !Number.isFinite(end) ||
    end <= 0 ||
    !Number.isFinite(tol) ||
    tol <= 0 ||
    !Number.isFinite(maxStep) ||
    maxStep <= 0
  )
    throw Error("Invalid integration interval, tolerance or step cap.");
  let q = q0.slice(),
    t = 0,
    h = Math.min(maxStep, end / 100),
    attempts = 0,
    accepted = 0,
    rejected = 0,
    minAccepted = Infinity,
    status = "completed",
    detail = "Requested interval completed.";
  const data = [{ t: 0, q: q.slice() }],
    roots = [];
  const finish = () => ({
    data,
    events: roots,
    status,
    detail,
    stats: {
      attempts,
      accepted,
      rejected,
      minStep: accepted ? minAccepted : 0,
      lastTime: t,
    },
  });
  const initialGuard = guard(q, 0);
  if (initialGuard) {
    status = initialGuard.kind;
    detail = initialGuard.message;
    return finish();
  }
  outer: for (let i = 1; i <= samples; i++) {
    const target = (end * i) / samples;
    while (target - t > 1e-13 * Math.max(1, end)) {
      if (++attempts > maxAttempts) {
        status = "work-limit";
        detail = "Integrator attempt limit reached.";
        break outer;
      }
      h = Math.min(h, maxStep, target - t);
      if (h < minStep) {
        status = "step-failure";
        detail = "Required step below minimum; numerical evolution unresolved.";
        break outer;
      }
      const trial = step(q, h, f, t),
        error = Math.max(
          ...trial.error.map(
            (e, j) =>
              Math.abs(e) /
              (tol * (1 + Math.max(Math.abs(q[j]), Math.abs(trial.q[j])))),
          ),
        );
      if (
        !trial.q.every(Number.isFinite) ||
        !Number.isFinite(error) ||
        error > 1
      ) {
        rejected++;
        h *= Number.isFinite(error) ? Math.max(0.1, 0.85 * error ** -0.2) : 0.1;
        continue;
      }
      const stop = guard(trial.q, t + h);
      if (stop) {
        status = stop.kind;
        detail = stop.message;
        break outer;
      }
      for (const event of events) {
        const l = event.value(q, t),
          r = event.value(trial.q, t + h);
        if (
          !Number.isFinite(l) ||
          !Number.isFinite(r) ||
          !((l < 0 && r >= 0) || (l > 0 && r <= 0))
        )
          continue;
        let low = 0,
          high = 1;
        for (let n = 0; n < 38; n++) {
          const fraction = (low + high) / 2,
            mid = step(q, h * fraction, f, t).q,
            v = event.value(mid, t + h * fraction);
          if (v > 0 === l > 0) low = fraction;
          else high = fraction;
        }
        const fraction = (low + high) / 2,
          rootTime = t + h * fraction,
          rootQ = step(q, h * fraction, f, t).q;
        if (
          !roots.some(
            (e) => e.key === event.key && Math.abs(e.t - rootTime) < 1e-10,
          )
        )
          roots.push({
            key: event.key,
            t: rootTime,
            q: rootQ,
            direction: r > l ? 1 : -1,
          });
      }
      q = trial.q;
      t += h;
      accepted++;
      minAccepted = Math.min(minAccepted, h);
      h *= error === 0 ? 2 : Math.min(2, 0.9 * error ** -0.2);
    }
    data.push({ t: target, q: q.slice() });
  }
  if (Math.abs(data.at(-1).t - t) > 1e-13) data.push({ t, q: q.slice() });
  return finish();
}
