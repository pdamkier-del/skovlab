# Skovlaboratoriet 🌳

Interaktiv gittermodel til undersøgelser af evolutionær selektion, artsdiversitet, rumlig orden og energiressourcer.

## Åbn simulatoren

**[Skovlaboratoriet som hjemmeside](https://pdamkier-del.github.io/skovlab/)** — linket virker, når GitHub Pages er aktiveret.

## Aktiver GitHub Pages

1. Åbn **Settings → Pages** i dette repository.
2. Under **Build and deployment**: vælg **Deploy from a branch**.
3. Vælg **main** og mappen **/(root)**, og klik **Save**.

Herfra vil opdateringer til `index.html` på `main` automatisk blive publiceret på samme adresse.

## Projektfiler

- [index.html](index.html) — hele simulatoren i én selvstændig HTML-fil.
- [LOGBOG.md](LOGBOG.md) — forskningslogbog, hypoteser, antagelser, kontrolberegninger og videre planer.

## Videnskabelig afgrænsning

Artsentropi måles med Shannon-entropi. Den valgfrie energivariant fører bog over disponibel energi og et reservoir med konstant total modelenergi. Det giver **ikke i sig selv** en temperatur eller en fysisk entropiproduktion.

Oprindelige skovregler er udgangspunktet; energimodellen er en eksperimentel udvidelse.

## Næste planlagte trin

1. Batchkørsler for både kontrolmodel og energivariant.
2. Sammenligning af vinderstrategier for forskellige energiomkostninger og overførselseffektiviteter.
3. Følsomhedstests og logning af numeriske kontrolberegninger.

## EC Collapse Laboratory

[EC Collapse Laboratory](https://pdamkier-del.github.io/skovlab/ec-flrw/) investigates homogeneous GR/EC collapse, using a documented averaged Weyssenhoff spin-fluid closure. It includes curvature k = −1, 0, +1; constraint-satisfying initial conditions; shared-time playback; Misner–Sharp effective mass; future null expansions; trapping events; GR/EC comparisons; and reproducible exports. The stable `ec-flrw/` route and free GitHub Pages hosting are preserved.

[Theory, conventions and validation](ec-flrw/collapse/THEORY.md) documents the first deliverable and the published-reference benchmark. The [retained KS geometry explorer](https://pdamkier-del.github.io/skovlab/ec-flrw/geometry-lab.html#ks) remains separate. The parameter screen is exploratory; exterior matching, radial inhomogeneity and thermodynamics are not implemented. An interior bounce or trapped surface does not establish a global event horizon or baby universe.

Run `npm ci`, `npm test`, and `npm run serve`. With Chromium installed, run `npm run test:browser`; set `CHROMIUM_PATH` if necessary, or use `npx playwright install chromium`. After editing the theory Markdown, regenerate the static page with `npm run docs`. GitHub Actions runs the equation/solver tests, checks the generated documentation and exercises both interfaces in Chromium.
