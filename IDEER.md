# Parkerede ideer

## 16. november 2026 — Dynamisk fitnessstyret mutationsretning

**Status: Ikke implementeret.** Peter vil gemme ideen til senere diskussion med William.

Mulig videreudvikling af de eksisterende spontane mutationer og børnemutationer: i stedet for kun symmetrisk `s' = s ± dε` kan mutationsretningen bias'es efter en **løbende observeret lokal fitnessgradient**, f.eks. afkom pr. træ eller nettovækst over flere sweeps. Optimum skal **ikke være hardcodet** og må kunne flytte sig med populationssammensætning, højder, Δs og lattice-geometri.

**Videnskabeligt forbehold:** Fitnessrettet mutation er en adaptiv heuristik, ikke almindelig retningsneutral mutation efterfulgt af naturlig selektion. Der er ikke besluttet fitnessdefinition, målevindue, gradientestimator eller styrke. Mutationer på dε ≤ Δs kan desuden bremses af den nuværende hårde angrebsgrænse. Neutrale mutationer bør indgå som kontrol, før der konkluderes noget om optimum.

Ingen HTML-ændring er foretaget for denne ide.
