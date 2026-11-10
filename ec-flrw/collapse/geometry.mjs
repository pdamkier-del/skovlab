/** Pure FLRW metric diagnostics. Dimensionless lengths R/L*, time t/L*, Gm/L*. */
export function surface(a, v, k, r) {
  if (!(a > 0 && r > 0 && 1 - k * r * r > 0))
    throw Error(
      "Surface requires a > 0, r > 0 and 1 − kr² > 0 in this regular FLRW chart.",
    );
  const R = a * r,
    H = v / a,
    sqrt = Math.sqrt(1 - k * r * r),
    outgoing = H * R + sqrt,
    ingoing = H * R - sqrt;
  const compactness = (v * v + k) * r * r,
    thetaPlus = (2 * outgoing) / R,
    thetaMinus = (2 * ingoing) / R,
    eps = 1e-9 * (1 + Math.abs(H * R) + sqrt);
  let classification = "untrapped";
  if (Math.abs(outgoing) <= eps && ingoing < 0)
    classification = "marginal outer";
  else if (Math.abs(ingoing) <= eps && outgoing > 0)
    classification = "marginal inner";
  else if (outgoing < 0 && ingoing < 0) classification = "future trapped";
  else if (outgoing > 0 && ingoing > 0) classification = "anti-trapped";
  const ahSquared = v * v + k;
  return {
    R,
    Rdot: v * r,
    compactness,
    thetaPlus,
    thetaMinus,
    outgoing,
    ingoing,
    classification,
    mu: (R * compactness) / 2,
    rAH: ahSquared > 0 ? 1 / Math.sqrt(ahSquared) : null,
  };
}
export function diagnose(t, q, p) {
  const [a, v] = q,
    m = p.matter(a),
    H = v / a,
    acc = -(m.rho + 3 * m.pressure - m.spin2) / 6,
    dH = acc - H * H;
  const s = surface(a, v, p.k, p.rb),
    constraint = H * H + p.k / (a * a) - m.rhoEff / 3,
    den = H * H + Math.abs(p.k / (a * a)) + (m.rho + m.spinCorrection) / 3;
  const massMatter = (s.R ** 3 * m.rhoEff) / 6,
    scale = a / p.a0;
  return {
    t,
    a,
    v,
    H,
    acc,
    dH,
    scale,
    volume: scale ** 3,
    ...m,
    ...s,
    massMatter,
    constraint,
    residual: Math.abs(constraint) / Math.max(1e-30, den),
    massResidual: Math.abs(s.mu - massMatter) / (1 + Math.abs(massMatter)),
    Rscalar: 6 * (acc + H * H + p.k / a ** 2),
    K: 12 * (acc ** 2 + (H * H + p.k / a ** 2) ** 2),
  };
}
