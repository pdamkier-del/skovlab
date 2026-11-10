/** Hashemi et al. 1407.4103v2, Eqs. 9, 16–19. Signature translated to (-+++).
 * rho = κL*²ρphysical; spin2 = κ²L*² Sphysical². Thus spin correction = spin2/4.
 */
export function matter(a, p) {
  const ratio = p.a0 / a,
    rho = p.rho * ratio ** (3 * (1 + p.w)),
    spin2 = p.theory === "ec" ? p.spin2 * ratio ** 6 : 0,
    spinCorrection = spin2 / 4,
    pressure = p.w * rho;
  return {
    rho,
    pressure,
    spin2,
    spinCorrection,
    rhoEff: rho - spinCorrection,
    pEff: pressure - spinCorrection,
  };
}
export function conservation(s, p) {
  return {
    matterInvariant: s.rho * (s.a / p.a0) ** (3 * (1 + p.w)),
    spinInvariant: s.spin2 * (s.a / p.a0) ** 6,
  };
}
