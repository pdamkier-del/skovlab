# Skovlaboratoriet — forskningslogbog

**Opdateret: 7. november 2026**  
**Udgangspunkt:** Oskar Struer Lunds *Up or out* (træmodel)  
**Formål:** Forstå samspillet mellem selektion, statistisk orden, information, energiressourcer og på længere sigt ikke-ligevægtstermodynamik.

## Projektets historie og idéer

1. **Oprindelig idé:** Hvert træ har en artsbestemt strategi `s` for højde versus udbredelse. Konkurrence mellem arter afhænger af højde. Den originale model er stokastisk.
2. **Fundamental fysik som motivation:** Interesse for entropi, tidens pil, emergens og forholdet mellem mikroskopiske regler og makroskopisk udvikling. Kosmologi og sorte huller er langsigtet inspiration, ikke påståede beskrivelser i træmodellen.
3. **Coarse-graining:** Idé fra statistisk fysik og Rovellis diskussion af tidsretning: Valget af observerbare størrelser ændrer, hvad vi ser. Vi har ikke testet Rovellis hypotese.
4. **Evolution og entropi:** Artsentropi kan falde når en art dominerer, uden at dette modsiger termodynamikkens anden hovedsætning.
5. **Energiressourcer:** Ny hypotese: Ressourcer og overførselseffektivitet kan ændre den evolutionært dominerende strategi.

## Hvad der måles i HTML

- Artsandel `p_i = n_i/N_levende`.
- Shannon-entropi `H_art = -sum_i p_i ln(p_i)`, samt normaliseret `H_art / ln(K)`.
- Nabopar med forskellige arter som proxy for rumlig blanding.
- Middelstrategi `s`, dominerende art, højde.
- Ved tilvalg: disponibel energi i træer, energi i reservoir og samlet modelenergi.

## Modelvarianter

### A. Originalmodellen (kontrol)

Oskars regler bevares. I ét sweep får hvert levende træ højst én aktivering. Med sandsynlighed `1-s` øges højden, med sandsynlighed `s` forsøges nabospredning. Ved kamp er sandsynligheden for angriberens sejr `h_angriber/(h_angriber+h_forsvarer)`. Dødelighed og højdecap kan aktiveres separat.

### B. Energi-udvidelse (eksperimentel)

Nye, valgfri antagelser:

- Hvert levende træ starter med `E0` enheder disponibel energi.
- Et nyt træ får energibeløbet `b` fra modertræet. Uden mindst `b` kan modertræet ikke formere sig.
- Højdevækst koster `c`, som flyttes fra træets disponible energi til et samlet energireservoir.
- Ved kamp går en andel `eta` af den besejrede celles disponible energi til vindersiden; resten går til reservoiret.
- Tilfældig død flytter træets resterende disponible energi til reservoiret.
- **Bevarelse:** `E_total = sum E_træer + E_reservoir` skal forblive konstant. Der kommer ingen energi udefra.
- `eta = 1` er *fuld overførsel af disponibel modelenergi*, ikke et elastisk mekanisk sammenstød. Ved `eta < 1` bliver energi utilgængelig for træerne, men den samlede energi forsvinder ikke.

Ingen fysisk temperatur eller reservoir-mikrotilstande er defineret; det er derfor **ikke** endnu en model for termodynamisk entropiproduktion. Skoven kan ophøre med at vokse, når den disponible energi slipper op.

## Første testbare hypotese

**H1:** Når vækst og formering kræver en begrænset disponibel energiresource, ændres fordelingen af vinderstrategier sammenlignet med originalmodellen.

Forsøgsmetode:

1. Vælg samme gitter, antal arter, seed og artsstrategier.
2. Kør originalmodel og energimodel med samme indstillinger, bortset fra energireglerne.
3. Mål dominerende strategi, artsentropi, rumlig blanding og energi over tid.
4. Gentag på tværs af uafhængige seeds. Samme seed er ikke i sig selv ens underliggende stokastisk historik, når dynamikken ændres.
5. Kontroller numerisk energibevarelse i energi-varianten, og lad konklusioner afhænge af flere gentagelser.

**Vigtigt:** HTML'ens batchfunktion gælder foreløbig kun originalmodellen. En statistisk sammenligning af energi-varianter kræver en senere batchimplementering, før vi kan rapportere resultater.

## Åbne spørgsmål

- Skal ressourcer være lokale, så et træ må konkurrere om energi i sin celle?
- Skal der være en energikilde (f.eks. sollys), så en stationær ikke-ligevægtstilstand kan opstå?
- Skal energi påvirke kampchancen, eller kun evnen til at vokse/spredes?
- Hvordan kan en fremtidig fysisk temperatur og entropiproduktion defineres uden at kalde artsdiversitet for termodynamisk entropi?
- Hvordan sikres, at eventuelle nye effekter ikke blot kommer fra ændret vækstbegrænsning?

## Status

- [x] Oprindelig træmodel og entropy-/strukturmålinger.
- [x] Eksplicit Shannon-entropiberegning.
- [x] Valgfri, energibevaret ressourceudvidelse i HTML.
- [ ] Batchanalyse for energivarianten.
- [ ] Kvantitativ undersøgelse af H1.
- [ ] Fysisk model for åbent system og reservoir-entropi.
- [ ] Litteraturreview af relevante økologiske / ikke-ligevægtsmodeller.

## Arbejdsgang

Hver gang modellen ændres: 1) nedskriv antagelsen, 2) noter præcis ændring, 3) kontroller invarians/balancer, 4) sammenlign med en kontrolmodel, 5) registrer resultater og begrænsninger. Bevar en originaltilstand til sammenligning.