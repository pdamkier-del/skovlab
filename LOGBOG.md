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

## 7. november 2026 — Entropityper og artsopdelt energiregnskab

**Formål:** Gøre forbindelsen mellem evolution, rumlig organisering og energi synlig, uden at sammenblande informationsentropier med fysisk termodynamisk entropi.

### Definitioner (alle logaritmer naturlige)

1. **Artsentropi** (H_{art}=-\sum_i p_i\ln p_i), hvor (p_i=n_i/N_{levende}). Måler diversitet blandt levende træer.
2. **Lokal artsentropi** (H_{lokal}=\sum_b (N_b/N_{levende}) H_b), hvor gitteret opdeles i op til 4×4 blokke; (H_b) er Shannon-entropien i blok b, og tomme celler ignoreres. Måler variation **inden for** områder. Den afhænger af blokstørrelsen.
3. **Energiandel-entropi** (H_E=-\sum_i q_i\ln q_i), hvor (q_i=E_{i,disponibel}/\sum_j E_{j,disponibel}). Den er kun defineret, når energitilvalget er aktivt og den samlede disponible energi er positiv; hvis alle træers disponible energi er nul, viser modellen 0 som en eksplicit konvention.
4. **Rumlig forskel** (H_{art}-H_{lokal}\ge0): forskel mellem artsusikkerhed uden og med viden om en celles blok. Udtrykker rumlig organisering, men er **ikke** termodynamisk entropi.

Kurver vises normaliseret med \(\ln K\), hvor K er det oprindelige antal arter; tallene ved siden af viser rå entropi i nat.

### Artsopdelt energi

Der vises pr. art (a) antal levende træer, (b) **aktuel** disponibel energi, (c) gennemsnitlig energi pr. træ, (d) artens andel af træernes samlede disponible energi, (e) kumuleret energi modtaget ved erobringer og (f) kumuleret energi overført fra arten til fælles reservoir pga. kamp, vækst eller død.

**Afgørende skelnen:** Tilgængelig energi er en beholdning; modtaget og afgivet energi er historiske strømme (kumulative summer). De må ikke lægges sammen som tre beholdninger. Energi i reservoiret tilhører ikke længere arten; kolonnen 'til reservoir fra art' er blot oprindelsesbogføring.

Modellen har ikke mekanisk/kemisk/termisk energiform som særskilt mikroskopisk tilstand, og der beregnes fortsat **ikke termodynamisk entropiproduktion** eller temperatur.

### Kontroller og hypoteser

- Kontrol: Summen af energibeholdning på alle levende træer og samlet reservoir skal være lig startenergien inden for afrundingsfejl.
- Kontrol: Summen af artsopdelte reservoirbidrag skal være lig reservoirbeholdningen.
- Kontrol: Lokal artsentropi må ikke overstige global artsentropi ud over numerisk afrunding.
- Hypotese: Selektion kan sænke artsentropien, mens lokale områder forbliver stærkt blandede, eller omvendt.
- Hypotese: Energiandel-entropi kan udvikle sig anderledes end artsentropi, fordi energien fordeles forskelligt mellem træer.
- Afgrænsning: Gentagne batchforsøg er stadig slået fra i energitilstand, da den særskilte batchmotor endnu kun er valideret for grundmodellen.


## 7. november 2026 — Simplificeret layout og idealiseret termodynamisk entropi

**Brugerønske:** Et mere forståeligt interface med færre sekundære paneler og en egentlig fysisk entropistørrelse, der kan holdes op imod artsdiversitet og energifordeling.

### Design og implementering

- Skov og to entropigrafer er nu hovedvisningen. Individuelle populationskurver, avancerede regler, artsvise bidrag til Shannon-entropi, batchforsøg og lange metodeafsnit findes under fold-ud-paneler.
- Den aktuelle disponible energi for hver art vises som et sæt søjler; den fulde artsvise balance kan åbnes separat.
- Energi er slået til i den foreslåede standardopsætning, mens den oprindelige Up or out-model fortsat kan køres med energiafbryderen slået fra.
- Standardværdier i energi-eksperimentet: η = 0,8; vækstomkostning 0,5; startenergi pr. træ 10. Parametrene er illustrative, ikke empirisk kalibrerede.

### Termodynamisk antagelse — begrænset varmereservoir

Et homogent varmereservoir antages at være i intern ligevægt med konstant positiv varmekapacitet C. Starttemperaturen er T₀ = 1 i modeltemperaturenheder. Energi som tidligere flyttedes til 'reservoir' fortolkes nu eksplicit som akkumuleret tilført **varme** Q, med Q ≥ 0.

Vi beregner

\[
T = T_0 + Q/C, \qquad
\Delta S_{bad} = \int_0^Q \frac{dQ'}{T_0+Q'/C}
= C\ln\!\left(1+\frac{Q}{CT_0}\right).
\]

Med T₀=1 og C=1000 i standardopsætningen.

**Energibogføring:** Den eksisterende sum E_disponibel + Q er bevaret. Reservoirets initiale termiske energi er antaget U₀=C T₀, som er en uændret reference. Den fulde idealiserede energisum er E_disponibel + (U₀+Q) = E_initial + U₀. Numerisk vises den forskydningsfri sum E_disponibel+Q på skærmen.

**Begrænsninger:** Vi har modelleret én termodynamisk entropistørrelse, nemlig reservoirets ΔS_bad, *ikke* træernes termodynamiske entropi eller hele det isolerede systems ΔS_total. Der er ingen detaljeret balance, eksplicit mekanisk energi, stokastisk termodynamisk log-ratio for baner, eller fysisk mikromodel for træernes indre tilstande. Modellen kan derfor endnu ikke bruges til en uafhængig test af anden hovedsætning. ΔS_bad er ikke sammenlignelig i numerisk størrelse med Shannon-entropier målt i nat og må ikke summeres med disse.

**Opfølgende problemstilling:** Kan vi tilføje en mikrofysisk termodynamisk beskrivelse af træernes energi og ressourceomsætning, så hele systemets entropibalance bliver defineret? Det kræver større modelændringer, og bør ske først efter kontrolberegninger og test af de nuværende målinger.

### Kvalitetskontrol

- HTML/JavaScript er blevet kontrolleret for syntaktisk gyldig JavaScript, ingen dublerede DOM-id'er og ingen referencer til ikke-eksisterende element-id'er.
- Fuld browserinteraktion og fysisk validering af modellen er endnu ikke gennemført i denne ændring.
