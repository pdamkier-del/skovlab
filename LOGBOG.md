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

Med T₀=1 og C=10000000 i standardopsætningen.

**Energibogføring:** Den eksisterende sum E_disponibel + Q er bevaret. Reservoirets initiale termiske energi er antaget U₀=C T₀, som er en uændret reference. Den fulde idealiserede energisum er E_disponibel + (U₀+Q) = E_initial + U₀. Numerisk vises den forskydningsfri sum E_disponibel+Q på skærmen.

**Begrænsninger:** Vi har modelleret én termodynamisk entropistørrelse, nemlig reservoirets ΔS_bad, *ikke* træernes termodynamiske entropi eller hele det isolerede systems ΔS_total. Der er ingen detaljeret balance, eksplicit mekanisk energi, stokastisk termodynamisk log-ratio for baner, eller fysisk mikromodel for træernes indre tilstande. Modellen kan derfor endnu ikke bruges til en uafhængig test af anden hovedsætning. ΔS_bad er ikke sammenlignelig i numerisk størrelse med Shannon-entropier målt i nat og må ikke summeres med disse.

**Opfølgende problemstilling:** Kan vi tilføje en mikrofysisk termodynamisk beskrivelse af træernes energi og ressourceomsætning, så hele systemets entropibalance bliver defineret? Det kræver større modelændringer, og bør ske først efter kontrolberegninger og test af de nuværende målinger.

### Kvalitetskontrol

- HTML/JavaScript er blevet kontrolleret for syntaktisk gyldig JavaScript, ingen dublerede DOM-id'er og ingen referencer til ikke-eksisterende element-id'er.
- Fuld browserinteraktion og fysisk validering af modellen er endnu ikke gennemført i denne ændring.

### Eksekveret funktionstest af denne version

JavaScript-koden blev evalueret i en mocket DOM/canvas med de faktiske standardindstillinger og 20 sweeps. Resultaterne før justeringen af standard-C fra 1000 til 100000 (der kun ændrer reservoirets termiske respons, ikke skovdynamikken):

- Start: E_disponibel=100000 og Q=0.
- Efter 20 sweeps: E_disponibel≈30101,588 og Q≈69898,412.
- Bevarelsesfejl: \(E_{disponibel}+Q-E_{initial}\approx4,6\cdot10^{-9}\) modelenergienheder.
- Artsentropi: fra ca. 2,30232 til 2,28929 nat.
- Reservoirets entropi steg fra nul til 4261,25 for den daværende C=1000; efter C-ændringen bliver det numeriske resultat anderledes efter samme hændelsesforløb.

Testen kontrollerede også, at nye entropital og artsenergibjælker blev skrevet til brugerfladen. Det er en **funktionstest med simuleret DOM**, ikke en visuel test i en rigtig browser. De termodynamiske antagelser er fortsat idealiserede.


## 7. november 2026 — Indre termisk entropi og entropibalancen

**Nyt spørgsmål:** Brugeren ønsker ikke blot Shannon-artsentropi og reservoirets termodynamiske entropi, men de termiske bidrag *inde ved træerne* og summen, som kan bruges til at illustrere anden hovedsætning.

### Nyt fysisk modelvalg (eksplicit idealisering)

Hvert gittersted får en lokal termisk beholder med **fast** varmekapacitet \(c>0\), også hvis stedet er tomt. Den termiske energi på stedet kan fortolkes som varme i træ/umiddelbar jord og omgivelser. Et træ kan dø eller blive overtaget, mens varmen bliver på gitterstedet; derfor er denne termiske beholder **ikke et vedvarende træindivid**. Et fælles varmereservoir har varmekapacitet \(C>0\).

Alle termiske beholdere starter ved \(T_0=1\) i modeltemperaturenheder. Varme er ikke en ny form for disponibel energi, men den energi, som efter vores regler omdannes fra træernes disponible energipakker. For hver dissipativ hændelse med energi \(q\ge0\):
- \(q_{lokal}=\alpha q\) føres til varmebeholderen på hændelsens gittersted;
- \(q_{bad}=(1-\alpha)q\) føres til det fælles reservoir.

\(\alpha\) er den brugerbestemte lokale varmeandel (standard 0,5). Vi antager ingen varmeledning, tilbageførsel af varme til træernes disponible energi eller ændring i varmekapacitet. Den termiske del er derfor en **ensrettet dissipationsmodel**, ikke mikroskopisk reversibel dynamik.

### Entropiformler

For hvert sted \(i\), hvor \(Q_i\) er den akkumulerede varme over starttilstanden:

\[
T_i=T_0+\frac{Q_i}{c},\qquad \Delta S_i = c\ln\left(1+\frac{Q_i}{cT_0}\right).
\]

Fælles bad, akkumuleret varme \(Q_B\):

\[
T_B=T_0+\frac{Q_B}{C},\qquad \Delta S_B=C\ln\left(1+\frac{Q_B}{CT_0}\right).
\]

Summen for **alle modellerede termiske beholdere** er

\[
\Delta S_{termisk}=\sum_{i\in levende\ steder}\Delta S_i+
\sum_{i\in tomme\ steder}\Delta S_i+\Delta S_B.
\]

Både den samlede lokale varme, varme ved aktuelle levende træsteder og varme i tomme områder vises. Den lokale termiske entropi grupperes også efter den art, som **aktuelt** optager stedet; dette er en klassifikation af steder, ikke artens hele historiske entropi.

**Energibalance:**

\[
E_{disponibel}+\sum_i Q_i+Q_B=E_{disponibel,0}.
\]

De termiske beholderes referencenergi \((N c+C)T_0\) er konstant og udeladt på begge sider af dette forskydningsregnskab.

### Hvad fortæller det om anden hovedsætning?

Fordi \(q\ge0\) og alle termiske beholdere varmes op fra en positiv starttemperatur, bliver \(\Delta S_{termisk}\) ikke-faldende i denne model. Det er en kontrol af **vores eksplicitte dissipative regler**, ikke et uafhængigt eksperimentelt bevis for anden hovedsætning eller en fuld beregning af skovens fysiske entropi. Vi mangler bl.a. træernes kemiske/konfigurationelle mikrostadier, termiske frihedsgrader, kemiske potentialer og reversible energikanaler.

De tre Shannon-mål (arts-, lokal arts- og energiandel-entropi) er fortsat særskilte statistiske størrelser. De er **ikke** termodynamiske bidrag, der skal lægges til \(\Delta S_{termisk}\).

### Metode og mulige videre tests

- Kontroller totalenergi numerisk efter hvert sweep.
- Kontroller at summen af de termiske entropibidrag er lig den viste samlede termiske entropi.
- Kontroller at beregnet \(\Delta S_{termisk}\) er ikke-faldende ved \(\alpha\in[0,1]\), forskellige \(\eta\) og ved dødelighed.
- Undersøg om Shannon-artsentropi falder, mens den modellerede termiske entropi stiger.
- Næste fysisk mere krævende skridt ville være at modellere virkelig varmeudveksling, temperaturafhængige overgange og lokal detaljeret balance; først derefter kan spørgsmål om reversibel mikrodynamik og stokastisk termodynamisk entropiproduktion adresseres ordentligt.

**Kodekontrol:** Termiske bidrag efter aktuelle artsbesatte steder kan undersøges i fold-ud-tabellen i HTML. Der er endnu ingen særskilt model for kemisk entropi i et træ, og det skal ikke forveksles med en beregnet størrelse.


### Funktionstest af termisk delmodel — 7. november 2026

JavaScript blev eksekveret med simuleret DOM og canvas. Fire testscenarier blev kørt, hver i 60 sweeps på et 20×20-gitter med 5 arter og samme seed:

| Scenarie | α lokal | η erobring | Dødelighed/sweep | Fald i beregnet ΔS_total over tid | Maks. energifejl | Slut-ΔS_termisk |
|---|---:|---:|---:|---:|---:|---:|
| Standardvariation | 0,5 | 0,8 | 0 | 0 | <2×10⁻¹¹ | 3290,994 |
| Al varme lokalt | 1 | 0 | 0 | 0 | 0 | 2683,662 |
| Al varme til bad | 0 | 0 | 0,1 | 0 | 0 | 3922,071 |
| Fuld erobringsoverførsel | 0,5 | 1 | 0,1 | 0 | 0 | 3404,943 |

I alle fire scenarier var forskellen mellem den beregnede termiske total og summen af \(\Delta S_{levende\ steder}+\Delta S_{tomme\ steder}+\Delta S_{bad}\) nul ved den målte numeriske præcision. Der fandtes ingen referencer til manglende eller dublerede DOM-id'er.

**Vigtig fortolkning:** Disse tests demonstrerer konsistens med de *valgte* dissipative antagelser, ikke en afledning af anden hovedsætning fra mikroskopisk reversible love. Visualiseringen er ikke afprøvet i en rigtig browser ved denne test.


## 7. november 2026 — Skoven løber tør for energi: åben model med sollys

**Observation:** Brugeren rapporterede "de uddør". I energiudgaven havde hvert træ kun en endelig startenergi, og vækst og kamp omdannede energi ensrettet til varme. Uden energitilførsel kunne den disponible energi derfor blive udtømt, så vækst og formering gik i stå. Dette er ikke nødvendigvis bogstavelig død af alle træer, da der ikke var indbygget sultedød, men det var en central biologisk og økonomisk modelbegrænsning.

**Ændring:** Indfør brugerparameteren `enSunlight` (standard 1,5 modelenergienheder per levende træ per sweep, nul tilladt). Ved begyndelsen af hvert sweep får *eksisterende levende* træer `sunlight` ekstra disponibel energi. Træer, der fødes i dette sweep, får først solenergi fra næste sweep. Dette er en bevidst deterministisk energitilførsel; ingen ny artsmutation, spontan genoplivning eller genindvandring er indført.

**Åbent energiregnskab:**

\[
E_{disponibel}(t)+Q_{lokal}(t)+Q_{bad}(t)
=
E_{start}+E_{sol,ind}(t).
\]

Dermed skal den gamle lukkede balance modificeres; det er *ikke* korrekt længere at forvente konstant energi inde i skoven uden at tælle solinput.

**Entropi og anden hovedsætning:** De beregnede entropistørrelser for lokal varme og reservoiret beskriver stadig kun den idealiserede termiske del. Med solenergi er systemet åbent, og solkildens egen entropi er **ikke** inkluderet. En virkelig test af anden hovedsætning for det komplette system kræver, at energikilden, dens temperatur og den relevante entropistrøm også medtages.

**Numeriske funktionstests:** 20×20 gitter, 5 arter, 100 sweeps, seed=2. Med solinput 1,5 og ingen dødelighed endte 369 levende træer og 34.364,16 tilgængelige energienheder, med kumulativ soltilførsel 54.450. Maksimal fejl i åben energibalance <3×10⁻¹⁰. Uden sollys blev kun 167,10 disponibel energi tilbage; det demonstrerer hvorfor gammel model kan gå i stå. Med solinput og 2% tilfældig dødelighed var den maksimale energibalancefejl <4×10⁻¹⁰.

**Vigtigt:** Sollys forhindrer energisult, men stopper ikke artsudryddelse gennem konkurrence. Uddøde arter kan ikke komme igen med modellens nuværende regler; mutation eller indvandring ville være et selvstændigt nyt modelvalg, ikke en bugrettelse.


## 7. november 2026 — Konservativ energioverførsel som standard

**Brugerobservation og hypotese:** Når træerne fortløbende mister disponibel energi til varme, bliver modellen afhængig af kontinuerlig solenergi. Brugeren foreslår i stedet at bruge overførsler, hvor energien forbliver blandt de levende træer, som ved en idealiseret elastisk proces.

**Præcis terminologi:** Vi har implementeret *konservativ overførsel af disponibel energi*; det er **ikke** et mekanisk elastisk sammenstød. I elastiske sammenstød bevares kinetisk energi, mens vores træer ikke har en modelleret hastighed, impuls eller kinetisk energi.

**Regler i ny standardtilstand:**
1. Hvert levende træ starter med \(E_0=10\) energienheder.
2. Ingen soltilførsel: \(E_{sol}=0\).
3. Ingen energiomdannelse til varme ved kamp: \(\eta=1\).
4. Vækst ændrer højden, men **koster ingen energi**. Dette er en bevidst forenkling — ikke biologisk realistisk.
5. Ved reproduktion overføres \(E_{fødsel}\) fra forælder til afkom. Summen bevares.
6. Ved konflikt tager vinderen hele taberens disponible energi. Hvis angriberen vinder, overføres den besejrede celles energi til angriberens afkom; hvis forsvareren vinder, absorberer den taberens energi.
7. Tilfældig død er slået fra i denne tilstand. Ellers skulle energien hos et træ, der dør uden at blive besejret, omplaceres efter en særskilt regel. Artsudryddelse under konkurrence er fortsat mulig.
8. Den tidligere dissipative model med varme, reservoir og solinput er bevaret som et **valgfrit sammenligningsforsøg**.

**Energibalance:**
\[
\boxed{\sum_{i\in levende\ træer}E_i(t)=\sum_{i\in starttræer}E_i(0)}
\]
for den konservative tilstand, uden varme eller eksterne kilder.

**Entropi og anden hovedsætning:** Artenes Shannon-entropi, lokal Shannon-entropi og energiandel-entropi kan stadig ændre sig. Derimod er det *ikke muligt* at beregne træernes fulde termodynamiske entropi ud fra energibevarelsen alene. Den termiske entropivisning skjules derfor i konservativ tilstand. Der må ikke vises en konstant \(\Delta S=0\) som om dette var et fysisk udledt resultat. I den dissipative tilstand kan den idealiserede varmeentropi fortsat undersøges.

**Funktionstests:** 20×20 gitter, 5 arter, seed=2, 100 sweeps.
- Konservativ: levende træers disponible energi: 4000,00 både før og efter; total energi-fejl 0. Slutantal levende træer 367.
- Konservativ med dødsparameter forsøgt sat til 0,2: død er blokeret; samme energibevarelse og resultat.
- Dissipativ tilstand med solinput 1,5: åbent energiregnskab testet, maksimal afvigelse \(2,62\times10^{-10}\) modelenergienheder.

**Åbent forskningsspørgsmål:** Om vi bør indføre realistisk energibehov ved vækst, metabolisme og død, og hvordan energi i så fald kan skifte fra kemisk til termisk form. Et fuldt fysisk studie af anden hovedsætning vil kræve flere modellerede frihedsgrader.


## 7. november 2026 — Sollys, død og konstant samlet energi; mikrotilstands-entropi

**Problem:** Brugeren ønsker at undersøge både solenergi og naturlig død, men stadig bevare energien, samt få en fysisk begrundet entropi ved træerne.

### Nyt valg: internt energikredsløb (standard)

Vi indfører et *endeligt* fælles energilager med energi \(E_L\), initialt \(E_{L,0}=N_{træer,0} E_{lager\ per\ træ}\), og levende træer med energier \(E_i\).

- **Soloptag:** Hvert træ får ved sweepets start højst \(I\) energienheder **fra lageret**, dvs. faktisk optag \(\min(I,E_L)\). Dette er ikke en ekstern, uudtømmelig sol og må snarere forstås som en idealiseret ressource- eller lysenergi-beholder.
- **Tilbageførsel:** Ved samme sweep returneres op til \(R\) af træets disponible energi til lageret.
- **Naturlig død:** Med dødsrate \(p=1-\exp(-\lambda)\) flyttes hele træets restenergi tilbage til lageret. Cellen bliver tom. Træer, som er døde, kan ikke uden videre vende tilbage som samme individ.
- **Konkurrence:** Vinderen modtager taberens energi fuldt ud, uden omdannelse til varme.
- **Formering:** Energien til et nyt træ flyttes fra dets forælder; ingen energi skabes.
- **Vækst:** Højden kan vokse uden energiforbrug i denne simplificerede, konservative modus.

Det lukkede regnskab er

\[
\boxed{E_{total}=E_L+\sum_{i\in levende}E_i=\mathrm{konstant}.}
\]

Træernes energi **alene** er ikke konstant: den flytter mellem træerne og lageret. Dette valg er eksplicit, og det er vigtigt ikke at forveksle bevaret \(E_{total}\) med et krav om konstant \(E_{træer}\).

### Boltzmann-entropi fra en defineret mikromodel

Energibevarelse alene fastlægger ikke temperatur eller entropi. Som første kvantitativ model antager vi **to grupper af idealiserede Einstein-oscillatorer**, én for energien i træ-puljen og én for energien i lageret. Hver gruppe har et fast antal oscillatorer \(n=L^2\) (modelkonvention) og fordeler et helt antal energikvanta \(q\) med energikvant \(\varepsilon=1\) modellenhed.

\[
\Omega(q,n)=\binom{q+n-1}{q},
\qquad
S(q,n)=k_B\ln\Omega(q,n).
\]

Simulationens kontinuerte energi rundes til nærmeste hele kvant i **målingen**, ikke i den underliggende trædynamik. Den viste entropi er

\[
S_{mikro}=S(E_{træer}/\varepsilon,n)+S(E_L/\varepsilon,n),
\]

med separate kurver for træ- og lagerbidrag samt deres sum. Temperatur eller virkelige kemiske mikrostadier er ikke introduceret i denne kvantiserede proxy. Gruppens oscillatorantal er fast og repræsenterer **ikke antallet af aktuelle træindivider**. Træernes fordeling *inden for* træ-puljen og hver enkelt arts biologiske indre entropi er heller ikke beregnet.

**Helt afgørende:** Fordi træernes tilfældige op-eller-ud-/konkurrence- og dødsregler ikke er afledt fra mikroskopisk reversible hastigheder eller lokal detaljeret balance, behøver dette \(S_{mikro}\) **ikke være ikke-faldende**. En negativ ændring er derfor ikke en empirisk overtrædelse af anden hovedsætning. Et fysisk konsistent stokastisk-termodynamisk studie ville inkludere systemets og omgivelsernes entropi samt overgangsrater og deres baglæns sandsynligheder.

Kilder:
- [Gould og Tobochnik: Einstein Solid Entropy (ComPADRE)](https://www.compadre.org/STPBook/statistical-mechanics-1/ex4_2.cfm)
- [Udo Seifert, *From Stochastic Thermodynamics to Thermodynamic Inference* (2019)](https://doi.org/10.1146/annurev-conmatphys-031218-013554)
- [Seifert, Entropy Production along a Stochastic Trajectory (2005)](https://doi.org/10.1103/PhysRevLett.95.040602)

### Metode og funktionstest

Fem tests à 150 sweeps, hver på 20×20-gitter med fem arter, kontrollerede energiregnskabet.

| Opsætning | Startenergi inkl. lager | Træenergi slut | Lager slut | Maks. fejl |
|---|---:|---:|---:|---:|
| Kredsløb, I=1,5; R=0,5; død=0,01 | 8000 | 7941 | 59 | 0 |
| Kredsløb, høj død=0,08 | 8000 | 1493,5 | 6506,5 | 0 |
| Kredsløb, ingen sol | 8000 | 0 | 8000 | 0 |
| Konservativ uden lager | 4000 | 4000 | 0 | 0 |
| Dissipativ med ekstern sol | 4000 + soltilførsel | ca. 33431,1 | 0 (særskilt varmeregnskab) | under 3×10⁻¹⁰ |

Mikromodellens entropi faldt i 81 af 150 kredsløbssweeps i standardtestopsætningen (målt for hele systemets modeldefinerede mikroentropi), og ændringen fra start blev negativ. Dette er en konsekvens af overgangsreglerne og den valgte makrotilstandsopdeling, og må ikke udlægges som et brud på anden hovedsætning.

**Åbne spørgsmål:** Skal sollys tilføres fra en virkelig ekstern sol-reservoir med særskilt udgående varme og entropiflux? Skal træernes egen termiske/kemiske entropi behandles med stokastisk termodynamik, hvor overgangsrater respekterer lokal detaljeret balance? Skal vi sammenligne energikonservering i total-puljen med en regulator, der holder træpuljens energi konstant ved at overføre overskud tilbage til lageret?


### Rettelse og udvidelse — entropi for individuelle træsteder

Den første mikrotilstandsversion beregnede én stor Einstein-solid for hele træernes disponible energi. Det viste sig at være utilstrækkeligt til at undersøge **indre entropi ved træerne individuelt**, fordi en energiflytning mellem to træer med fast samlet \(E_{træer}\) da ikke ændrede denne måling. Denne definition er nu **erstattet** — tidligere omtale af to faste grupper med \(n=L^2\) gælder ikke længere for træbidraget.

Aktuel definition: Hvert gittersted har \(m=3\) idealiserede oscillatorer og \(q_i=\mathrm{round}(E_i/\varepsilon)\) kvanta, hvor \(\varepsilon=1\) modellenhed. Tomme steder har \(q_i=0\). Lageret har \(n_L=3L^2\) oscillatorer og \(q_L=\mathrm{round}(E_L/\varepsilon)\). Vi måler

\[
\frac{S_{træer}}{k_B}=\sum_{i\in levende} \ln \Omega(q_i,3),
\quad
\frac{S_{lager}}{k_B}=\ln \Omega(q_L,3L^2),
\quad
S_{mikro}=S_{træer}+S_{lager}.
\]

Der vises også \(S_{art}=\sum_{i\in art} k_B \ln\Omega(q_i,3)\) for hver art. \(S_{mikro}\) er altså en summeret **mikrotilstands-proxy**. Ved at antage adskilte, uafhængige oscillatorer på de enkelte steder undgår vi dobbeltoptælling mellem denne træ-entropi og lagerentropien. Men den faktiske træmodel har ikke tre fysiske oscillatorer pr. træ, og kvantiseringen anvendes kun til statistik. \(S_{mikro}\) er derfor ikke en empirisk, fuldstændig termodynamisk entropi for et skovøkosystem.

**Opdaterede funktionstests:** Fire scenarier af 120 sweeps på 20×20 gitter med fem arter, inklusive direkte kontrol af summen af indre artsentropier.

| Scenarie | E ved start | E_træer slut | E_lager slut | Negativt mikro-ΔS i antal sweeps | Samlet mikro-ΔS/kB |
|---|---:|---:|---:|---:|---:|
| Sol 1,5, returnering 0,5, død ~0,01 | 8000 | 7915 | 85 | 65/120 | -2739,389 |
| Sol 1, returnering 0,5, død ~0,08 | 8000 | 1561,5 | 6438,5 | 61/120 | -365,076 |
| Ingen sol, død ~0,01 | 8000 | 0 | 8000 | 84/120 | -923,201 |
| Kun konservativ energi mellem træer | 4000 | 4000 | 0 | 67/120 | -692,901 |

Den samlede energifejl var numerisk 0 i disse scenarier; summen af artsvise indre entropier afveg højst \(5,3\times10^{-12}\) fra \(S_{træer}/k_B\). Kodens syntaks og referencer til HTML-elementer bestod også funktionstesten med simuleret DOM/canvas.

**Forskningsfortolkning:** Antallet af negative ændringer viser, at disse ad hoc-evolutionære overgangsregler **ikke er termodynamisk konsistente bare fordi de bevarer energi**. Vi kan bruge resultatet til at stille næste forskningsspørgsmål om at konstruere overgangsrater med lokal detaljeret balance, ikke til at påstå at anden hovedsætning er falsk.


## 7. november 2026 — Fluktuationsaudit af energikredsløbet (10 seeds × 4 scenarier)

**Formål:** Undersøge hvilke mål i den eksisterende model der fluktuerer, om der er et langsigtet driftssignal, og hvordan energibevarelse relaterer sig til entropi og selektion.

**Metode:** Der er kørt 40 egentlige skovforløb med 320 sweeps hver (12.800 sweeps i alt), gitter 20×20, fem arter, fuld startdækning og seeds 1–10. Det er den eksisterende JavaScript-dynamik fra `index.html`, eksekveret i et mocket DOM/canvas-miljø. Udvalgte tilstande er registreret for hver sweep, og både middelværdi over seeds, standardafvigelse mellem seeds og tidslig standardafvigelse i det sidste vindue på 100 sweeps er undersøgt. Tidslig standardafvigelse betyder ikke nødvendigvis en stationær fluktuation: der kan stadig være drift.

**Forsøg** (I=soloptag pr. træ/sweep; R=tilbageførsel; p=dødsandsynlighed):

1. Energikredsløb: I=1,5, R=0,5, p=0,01.
2. Energikredsløb uden død: I=1,5, R=0,5, p=0.
3. Konservativ energi kun i træerne: ingen sol, p=0.
4. Energikredsløb med høj død: I=1,5, R=0,5, p=0,08.

### Målinger (middel ± standardafvigelse på tværs af 10 seeds ved sweep 320)

| Måling | Kredsløb p=0,01 | Kredsløb p=0 | Konservativ | Kredsløb p=0,08 |
|---|---:|---:|---:|---:|
| Levende træer | 364,5 ± 13,1 | 370,4 ± 9,4 | 368,3 ± 8,2 | 344,7 ± 23,2 |
| Antal arter | 3,7 ± 0,8 | 4,0 ± 0,5 | 3,8 ± 0,8 | 2,0 ± 0,9 |
| Energi hos træer | 7974,0 ± 29,7 | 8000,0 ± 0 | 4000,0 ± 0 | 3906,8 ± 357,2 |
| Energi i lageret | 26,1 ± 29,7 | 0 ± 0 | 0 ± 0 | 4093,3 ± 357,2 |
| Artsentropi H (nat) | 0,970 ± 0,248 | 1,092 ± 0,266 | 1,057 ± 0,237 | 0,403 ± 0,407 |
| Lokal artsentropi (nat) | 0,465 ± 0,153 | 0,590 ± 0,137 | 0,570 ± 0,139 | 0,177 ± 0,183 |
| Energiandel-entropi (nat) | 0,982 ± 0,361 | 1,088 ± 0,248 | 0,993 ± 0,209 | 0,423 ± 0,398 |
| Mikrotilstandsproxy S/kB | 1511,3 ± 137,5 | 1192,4 ± 71,7 | 948,9 ± 36,2 | 4149,1 ± 60,3 |
| Dominerende arts andel | 0,612 ± 0,140 | 0,467 ± 0,128 | 0,530 ± 0,129 | 0,802 ± 0,225 |

*Bemærk:* De fire scenarier har ikke samme totalenergi. Kredsløb har startenergi 8000 fordelt ligeligt mellem træer og lager; konservativ har 4000 alene hos træer. Mikro-S kan derfor **ikke** sammenlignes direkte på tværs af scenarier som en kontrolleret effekt af dødelighed eller energioverførsel. En parret kontrol med identisk E_total og matched initialbetingelser kræves.

### Tidslige udsving i sidste 100 sweeps (gennemsnitlig tidslig SD inden for hvert run)

| Måling | Kredsløb p=0,01 | Kredsløb p=0,08 |
|---|---:|---:|
| Antal træer | 5,55 | 7,09 |
| E_træer = −E_lager i ændringer | 90,15 | 199,27 |
| Artsentropi H (nat) | 0,037 | 0,038 |
| Energiandel-entropi (nat) | 0,048 | 0,042 |
| Mikrotilstandsproxy S/kB | 217,08 | 29,47 |

**Energi:** E_total var eksakt konstant på simulationsprecision i alle disse forløb (maksimal rapporteret afvigelse 0). Energien i træer og lager er fuldstændigt antikorrelateret i niveau og ændringer, da \(E_L=E_{total}-E_{træer}\).

**Entropiens fluktuationer:** I det almindelige kredsløb var \(\Delta S_{mikro}<0\) for gennemsnitligt 54,1 % af de 320 sweep-overgange (spænd 50,9–59,1 % over seeds). Det viser **ikke** en verificeret termodynamisk entropiproduktion, men en proxy, der fluktuerer og også har stærk langsigtet drift. I konservativ model var andelen 52,2 %. Den målte tidslige SD af mikro-S i almindeligt kredsløb er stor, fordi lageret er næsten tømt og kraftigt følsomt over for relativt små energioverførsler.

**Artsselektionsdrift:** Antal arter kan kun falde eller forblive konstant, fordi modellen ikke har mutation, immigration eller spontan artsopståen. Derfor er artsentropiens fald ikke blot fluktuation omkring en fast værdi. Høj dødelighed (p=0,08) gav kun gennemsnitligt 2 arter tilbage ved sweep 320; der er stadig væsentlig seed-variation.

**Potentiel modellåsning:** Uden død blev det endelige energilager helt tømt i alle 10 seeds, fordi hver tree hvert sweep returnerer højst 0,5 og derefter modtager op til 1,5. Med p=0,01 var gennemsnitslageret ca. 26 ud af 8000 ved sweep 320. Dette kan skabe kunstig lagermangel og er en vigtig mangel ved den valgte energicyklus, **ikke evidens for termodynamisk ligevægt**.

**Ikke påvist:** Ingen test af autokorrelation, spektraltoppe, karakteristisk oscillationsperiode, konvergens til stationær fordeling eller skalalov er endnu udført. Korte op-og-ned-udsving alene dokumenterer ikke periodiske svingninger.

**Anbefalet næste metode:** (1) langtidstest og lag-/autokorrelationsanalyse for lagerenergi og population, (2) justér soloptagsreglen, så lageret ikke systematisk tømmes (eller undersøg netop denne faseovergang), (3) paired-seed- og matched-energy-forsøg over varierende død og tilbageførsel, (4) særskil dynamisk entropiproduktion fra definitionen af tilstandsentropi og prøv lokal detaljeret balance.


## 7. november 2026 — Langtidsundersøgelse af fluktuationer og entropimængder

**Formål:** Test om fluktuationerne i skovens energier, population, artsentropi og idealiseret mikroentropi er stationære, periodiske eller påvirket af langsigtet selektionsdrift.

**Metode:** 36 uafhængige runs: 12 seeds × 3 parameteropsætninger, hver med 1.000 sweeps, 20×20 gitter, 5 arter, samme startenergi E_total=8.000 i alle tre kredsløbsopsætninger. Målinger efter hvert sweep. Langtidsvindue sweeps 500–1.000. Autokorrelation for lag 1, 10 og 50, tidslig standardafvigelse i vinduet samt middelværdi i halvdelene 500–750 versus 750–1.000. Analysen bruger faktisk JavaScript fra GitHub `index.html` med mocket DOM/canvas (ikke en browser-visuel test).

**Opsætninger:**
- A: standardkredsløb: soloptag I=1,5; retur R=0,5; p_død=0,01 pr. sweep (i beregning, ikke λ).
- B: balanceret I=0,5; R=0,5; p_død=0,01.
- C: høj død I=1,5; R=0,5; p_død=0,08.

### A: Standardkredsløb — entropiens størrelse i tidsforløbet

| Mål | Sweep 0 | 500 | 1.000 |
|---|---:|---:|---:|
| Artsentropi H_art (nat) | 1,605 | 0,790 | 0,466 |
| Lokal artsentropi H_lokal (nat) | 1,534 | 0,362 | 0,207 |
| Energiandel-entropi H_E (nat) | 1,605 | 0,857 | 0,427 |
| Rumlig forskel H_art − H_lokal (nat) | 0,071 | 0,428 | 0,259 |
| Indre træ-mikroentropi S_træ/kB | 1.676 | 1.467 | 1.518 |
| Lager-mikroentropi S_lager/kB | 2.803 | 281 | 199 |
| Sum-mikroentropi S_total/kB | 4.479 | 1.748 | 1.718 |

Alle værdier er gennemsnit på tværs af 12 seeds; første fire mål er Shannon i **nat**, de sidste tre i den antagne Einstein-oscillator-model i **kB**-enheder. Tallene har forskellige skalaer og kan ikke summeres på tværs af definitioner.

Ved sweep 1.000 var der i snit 379,6 træer, 2,33 arter, E_træ≈7.940 og E_lager≈59,8. E_total=8.000 i alle runs med nul opgjort numerisk energifejl.

### Autokorrelation i vindue 500–1.000 (middel over seeds)

| Mål | Lag 1 | Lag 10 | Lag 50 |
|---|---:|---:|---:|
| E_træ | 0,131 | −0,010 | 0,005 |
| Antal træer | 0,790 | 0,270 | 0,131 |
| H_art | 0,985 | 0,925 | 0,808 |
| S_mikro | 0,255 | 0,106 | 0,017 |

Energi- og mikrostørrelserne har meget kort autokorrelationshukommelse, hvorimod artsdiversitet er stærkt persistent, til dels fordi den driver nedad. Der er ikke påvist en robust periodisk oscillation. En fuld frekvens-/spektralanalyse mangler stadig.

### Tidslige standardafvigelser i sidste halvdel (gennemsnit på tværs af seeds)

| Mål | A: standard p=0,01 | B: I=R=0,5 | C: høj død p=0,08 |
|---|---:|---:|---:|
| E_træ | 94,6 | 25,6 | 211,9 |
| Antal træer | 5,55 | 39,67 | 7,47 |
| H_art (nat) | 0,107 | 0,226 | 0,052 |
| H_E (nat) | 0,138 | 0,230 | 0,056 |
| S_mikro/kB | 224,0 | 42,1 | 30,2 |

**Vigtigt om standardafvigelse:** Disse tal kan inkludere *drift*; især setup B er ikke stationært. De er ikke alle rene ligevægtsfluktuationer.

### B: I=R=0,5 — sammenbrud trods konstant energi

Start E_træ=4.000, E_lager=4.000; ved sweep 1.000 var E_træ≈4,04 og E_lager≈7.995,96; der var kun ca. 7,5 levende træer i gennemsnit. Et af 12 runs havde nul levende træer. Dødelighed returnerer al træenergi til lageret; lige store tilførsels- og returrater er ikke tilstrækkelige til at kompensere dødelighed. \(E_{total}\) er stadig nøjagtigt konstant.

Dette betyder, at sol-/energikredsløbet i denne udgave ikke automatisk giver en robust livsbærende ligevægt.

### C: p=0,08 — stærk selektion og større energifluktuationer

Ved sweep 1.000 var E_træ≈3.902,9, E_lager≈4.097,1 og der var i gennemsnit 353,4 træer, men kun ca. 1,17 arter. Kun to af 12 runs havde mere end én art tilbage. I den sene periode var tidslig energi-SD omkring 211,9 mod 94,6 i standardforsøget. H_art≈0,047 nat og H_E≈0,046 nat: artsmæssig dominans trods fortsatte population- og energifluktuationer.

### Entropifluktuationer og anden hovedsætning

I setup A havde den *konstruerede* mikrotilstandsproxy negativ ændring i 52,3 % af sweep-overgangene, gennemsnit på tværs af 12 runs. I setup B 42,6 %, C 50,5 %. Dette er ikke et termodynamisk brud; modellen mangler dynamisk konsistente overgangsrater, mikroskopiske udvekslingsmekanismer og produktion af miljøentropi. Det viser forskel mellem en valgt tilstandsentropi \(k_B\ln\Omega\) og den totale stokastisk-termodynamiske entropiproduktion.

**Status:** Delvis korttidstilpasning af E_træ og S_mikro i A/C, men vedvarende artsselektion, så der er ingen påvist fuld stationær ligevægt. Robust periode ikke påvist; længere runs og spektraltests er stadig ønskelige.

**Anbefaling:** En paret, matched-energy analyse over f.eks. \(I/R\)-rater og dødelighed, samt kvantificering af entropiflux/produktion med lokalt detaljeret balance, ville være næste fysiske udvikling. Separér stationære udsving fra irreversibel udryddelsesdrift i plottet.


## 7. november 2026 — Tidens pil, version 1 (bygget og testet)

**Motivation:** Flyt fokus fra alene at plotte entropi som funktion af tid til at teste, om et forløbs retning kan udledes statistisk af observerede tilstande.

### Implementering i den eksisterende webapp

Der er tilføjet et nyt panel **Tidens pil** i `index.html`. Brugeren kan optage et fuldt forward-forløb med 200, 500 eller 1000 sweeps fra det valgte seed og regelsæt. Antallet af gemte frames begrænses automatisk til højst omtrent 150 med mellemliggende observationer. Hver frame gemmer skovens faktiske arter pr. gittercelle samt træantal, levende artsantal, arts-Shannon-entropi, tilgængelig energi hos træerne og mikrotilstands-entropi, når den er defineret. Selve simulationen kører hele sweeps; den hopper ikke over dynamik, selvom nogle frames springes over ved optagelsen.

Afspilleren har en frem-/tilbage-knap, en tids-skyder, start/pause og en graf over det valgte mål med markering af den aktuelle frame. Tidsvendt afspilning viser **samme lagrede tilstande i omvendt rækkefølge**; den beregner ikke sandsynligheden for en fysisk tidsvendt overgang og udgør ikke en dynamisk reversibilitetstest i sig selv.

### Mål for observeret tidsasymmetri

Vælg en af: træernes disponible energi, antal træer, artsentropi eller den idealiserede mikroentropi. Den scalar tidsserie, samplet på optagelsens frames, opdeles i fire lige brede intervaller mellem observeret min og max. Observerede tretrinsekvenser \(a\to b\to c\) sammenlignes med omvendte \(c\to b\to a\). Den viste målestørrelse er Jensen–Shannon-divergensen:

\[
\mathrm{JSD}(P_F,P_R)=\frac12 D_{KL}(P_F\Vert M)+\frac12 D_{KL}(P_R\Vert M),\qquad M=\frac{P_F+P_R}{2}.
\]

Den måles i nat, ligger mellem 0 og \(\ln 2\), og nul betyder symmetri i **den valgte observerede tretrinsfordeling**. Mængden er ikke nødvendigvis nul for en kort, finit tilfældig tidsserie, selv under en tidsreversibel kontrol. Den er følsom for binning, sampling, antal frames og en mulig tidslig drift. Den må **ikke** kaldes faktisk fysisk entropiproduktion eller en verificeret sandsynlighed for frem-/baglæns baner.

**Særligt problem i denne skov:** Artsudryddelse er en indbygget ensrettet regel. Den udryddede art kan ikke genopstå spontant uden mutation/immigration. Denne irreversibilitet er derfor triviel i en artshistorik og siger ikke i sig selv noget fundamentalt om tidens pil.

### Funktionstest

Den konkrete JavaScript-kode blev eksekveret i et mocket DOM/canvas-miljø (ikke en rigtig browser). På 20×20 gitter med 5 arter, seed 2, 100 sweeps og ét frame pr. 5 sweeps:

- Der blev gemt 21 snapshots, start ved sweep 0 og slut ved sweep 100.
- Energiregnskabet var eksakt bevaret i modelprecision: E_total = E_initial = 8000.
- Det beregnede tidsasymmetrimål for træernes energi var JSD = 0,109444 nat.
- Spoling tilbageviste det gemte snapshot fra sweep 100 korrekt.
- For en eksplicit tids-symmetrisk testserie (palindrom) var JSD = 0.
- For en konstant testserie var JSD = 0.
- JavaScript-syntaksen bestod, og der var ingen dublerede eller manglende direkte DOM-id'er.

**Næste metodiske trin:** Sammenlign med kontrolleret, tidsreversibel Markov-dynamik med kendt detaljeret balance; anvend flere uafhængige forløb og bootstrap/blokbootstrap eller passende nulmodel; undersøge stationaritet, spektralanalyse og skelnen mellem irreversibel selektion og fysisk termodynamisk entropiproduktion. Først efter en sådan validering kan forhold mellem observeret tidsasymmetri og entropiproduktion studeres kvantitativt.


### Tidens pil — reversibel kontrol versus drevet Markovkæde

For at give JSD-målet en fysisk kalibrering blev en **separat, analytisk håndterbar kontrolmodel** tilføjet til Tidens pil-panelet.

**Fire tilstande på en ring**, med overgangssandsynligheder \(p_+\) (med uret), \(p_-\) (mod uret) og \(p_0=1-p_+-p_-\) (uændret). Systemet startes i en uniform tilstand, og dets stationære fordeling er uniform for begge parameteropsætninger.

- **Reversibel ligevægt:** \(p_+=p_-=0,45\), \(p_0=0,1\). Detaljeret balance er opfyldt. Teoretisk middel-entropiproduktion er 0.
- **Drevet ikke-ligevægt:** \(p_+=0,8\), \(p_-=0,1\), \(p_0=0,1\). Den stationære sandsynlighedsstrøm er ikke nul. Under en fortolkning med lokal detaljeret balance er den gennemsnitlige entropiproduktion i \(k_B\)-enheder pr. trin:
\[
\sigma=(p_+-p_-)\ln(p_+/p_-)=0,7\ln8\approx1,455609.
\]

For en konkret bane optælles \(+\ln(p_+/p_-)\) for hvert fremadgående spring og det negative beløb for hvert tilbagespring; uændret tilstand bidrager nul.

**Funktionstest** af 12.000 trin med seed 234:

| Model | JSD for 3-trinsmønstre (nat) | Målt middel \(\Sigma/k_B\) pr. trin | Teoretisk |
|---|---:|---:|---:|
| Reversibel ring | 0,000104 | 0 | 0 |
| Drevet ring | 0,456073 | 1,447118 | 1,455609 |

Den tidsreversible kontrol har statistisk JSD tæt ved nul, mens den drevne ring viser klar asymmetri. Denne kontrol er **ikke samme dynamik som skoven**; skovens JSD kan stadig skyldes selektionsdrift eller regelbaserede irreversible udryddelser. Målet er kun at illustrere og teste metodeforskellen mellem reversibel og drevet dynamik.

**Yderligere kontrol:** Den eksisterende skovoptagelse på 100 sweeps med 21 snapshots gav JSD=0,109444 nat; HTML-elementer og JS-funktioner havde ingen manglende eller dublerede referencer, og den testede konservative energibalance var konstant. Der er endnu ingen browserbaseret billed- eller iPhone-test, kun JS-eksekvering med simuleret DOM/canvas.


## 16. november 2026 — Ny fokuseret model A og oprydning af hjemmesiden

Brugeren valgte at videreudvikle energikredsløbet (A), og bad om at fjerne ubrugte funktioner fra HTML. Den tidligere blanding af konservativ, cirkulerende og dissipativ energimodel, tilfældig død, varme- og tidens-pil-paneler er erstattet af én mindre, selvstændig implementering af skovmodellen. Tidligere historiske beskrivelser i denne logbog er derfor **ikke alle gældende regler**. Denne sektion beskriver den aktuelle version.

### Gældende regler

- Et L × L-gitter; K arter med en fast strategi s i intervallet [0,1]. Et sweep behandler træer i tilfældig rækkefølge; nyfødte træer handler først næste sweep.
- Et træ forsøger som udgangspunkt vertikal vækst med sandsynlighed 1-s eller angreb/spredning med sandsynlighed s.
- **Vækst koster** en konfigurerbar mængde disponibel energi g. Beløbet går til det fælles lager. Hvis et træ ikke kan vokse, enten på grund af højdelimit eller manglende energi til g, forsøger det i stedet angreb med **100 % sandsynlighed**.
- Angreb kræver mindst en reproduktionspakke b. Hvis der ikke er nok til b, kan træet ikke angribe, selv om det er tvunget til at forsøge. Dette er en handlingsbegrænsning, ikke død.
- Ved etablering overføres b fra modertræ til afkom. Et nyt træ har normalt højde 1.
- Kamp mellem forskellige arter: Vælg enten højdebaseret sandsynlighed P(A vinder)=h_A/(h_A+h_B) eller energibaseret sandsynlighed P(A vinder)=E_A/(E_A+E_B), beregnet før afkommets energi trækkes fra angriberen.
- Taberen i en kamp dør. Angriberen fjernes fra egen celle, hvis den taber; hvis forsvareren taber, erstattes den af angriberens afkom.
- **Ingen tilfældig naturlig død**: Et træ dør af energimangel kun ved E=0 (i numerikken E <= 10⁻¹⁰ for at undgå floating-point restværdier), eller hvis det taber i kamp. Ved enhver død returneres dets resterende disponible energi til fælleslageret.
- Energi i kredsløb: Ved starten af hvert sweep returnerer hvert allerede levende træ højst r energienheder til lageret og får derefter højst s_sun fra lageret. Hvis lageret er tomt, kan det ikke betale fuld energitilførsel.
- Total tilgængelig energi bevares: E_total = sum_i E_i + E_lager. Der er intet termisk entropiregnskab i denne version. Energi skal fortolkes som **disponible modelressourcer**, ikke bogstavelig gravitationel potentiel energi.

### Standardparametre

L=100, K=10, fuld startdækning, startenergi 10 pr. træ, lagerenergi 10 pr. indledende træ, lager→træ 1,5 pr. sweep, træ→lager 0,5 pr. sweep, vækstomkostning 1, reproduktionspakke 2. Højdebaseret kamp er standard; energibaseret kamp kan vælges i HTML. Maksimal højde er som udgangspunkt slået fra.

### UI og validering

Ny selvstændig og forenklet \`index.html\` viser: skoven, population og artsdiversitet, tidsserie for artsentropi/rumlig naboblanding/antallet af arter, træ- og lagerenergi, energibalance, artsoversigt og de relevante kontroller. Den tidligere store kode og paneler for de andre modeller er fjernet fra den aktuelle HTML.

Eksekveret 200 sweeps på 20×20-gitter med 5 arter for begge konkurrenceregler. Højdebaseret: 220 træer, 4 arter tilbage. Energibaseret: 307 træer, 1 art tilbage. Maksimal målt energibalanceafvigelse var **0** i begge testforløb ved JS-flydetalspræcision; ingen negative energier blev observeret. Disse resultater er enkeltstående tests af kodekonsistens og må **ikke** fortolkes som statistisk sammenligning mellem kampregler.

Denne logbog bevares som historik; den aktuelle HTML er endnu ikke manuelt browser-testet.

## 16. november 2026 — Gratis kolonisering af tomme nabofelter

Når et træ vælger at sprede sig og det udvalgte nabofelt er tomt, etableres et nyt træ **uden energioverførsel**. Det nye træ starter med E=0 og får mulighed for at optage energi fra fælleslageret ved begyndelsen af næste sweep. Hvis energitilførslen ikke løfter det over nul, dør det ved næste handling. Kravet om energipakken b og energioverførsel ved sejr gælder fortsat for angreb på besatte felter. Reglen om, at et træ som ikke kan betale højdevæksten forsøger spredning med 100 % sandsynlighed, er bevaret.

Funktionstest: to kampmåder, 150 sweeps på 20×20 gitter med 40 % startdækning. Ingen negative energier, og energiregnskabsafvigelsen var 0 i begge forsøg. Testet i simuleret JavaScript DOM; endnu ikke visuelt gennemset i en browser.


## 16. november 2026 — Reproduktionsenergi og energiudligning i sammenhængende artsgrupper

**Aktuel ændring:** Uanset om nabofeltet er tomt eller besat, skal vellykket spredning overføre en fast energipakke \`b\` (standard 2) fra modertræet til det nye træ. At kolonisere et tomt felt har **ingen ekstra angrebsomkostning**, men den overførte pakke på 2 skal være til rådighed. Et nyfødt træ starter derfor med E=2, ikke E=0, medmindre brugeren ændrer \`b\`.

Hvert sweep deles den **disponible energi** ligeligt inden for hver sammenhængende komponent af levende træer af **samme art**. Komponenterne bestemmes af 4 eller 8 nabofelter alt efter valg, inklusive periodiske kanter hvis de er aktive. To adskilte kolonier af samme art deler **ikke** energi direkte. Den samlede energi i komponenten er uændret efter fordeling: \(E_i \leftarrow (\sum_{j\in C}E_j)/|C|\). JavaScript-koden fordeler afrundingsresten til den sidste celle.

**Opdateringsrækkefølge:** (1) hvert træ, der lever ved sweepets begyndelse, udveksler energi med fælleslageret; (2) sammenhængende artsgrupper udligner energi; (3) træerne handler i tilfældig rækkefølge; (4) grupperne udligner energien igen; (5) træer, som stadig har E=0, dør. Tab i kamp medfører fortsat straks død og overførsel af taberens disponible energi til fælleslageret.

**1. hovedsætning i vores idealiserede ressourcebogføring:**
\[
E_{\mathrm{total}}=\sum_{\text{levende træer}}E_i+E_{\mathrm{fælleslager}}
\quad\text{(konstant).}
\]
Energideling, formering, vækst og død er interne overførsler. Den beregnede disponible modelenergi er ikke en komplet fysisk termodynamisk beskrivelse; især mangler varme, temperatur og entropiproduktion.

**Funktionstest:** 20×20 gitter med 5 arter og 40 % startdækning, 180 sweeps med henholdsvis højde- og energibaseret kamp. Energibalancens maksimale absolutte afvigelse var 5,92×10⁻¹¹ og 4,37×10⁻¹¹ modelenergienheder; der forekom ingen negative energiresultater. De to testforløb er ikke statistisk dokumentation for en bestemt evolutionær fordel.

**Vigtigt historisk:** Logbogens tidligere afsnit, hvor tomme felter fik et nyt træ med E=0, er overskrevet af denne regel.


## 16. november 2026 — Lokal, gradvis energitransport (erstatter øjeblikkelig udligning)

Den tidligere regel om øjeblikkelig ligelig deling af energi inden for en hel sammenhængende artskoloni er **erstattet**. Nu udføres ét **synkront, lokalt transporttrin** pr. sweep mellem par af nabotræer af samme art:

\[
\Delta E_{i\to j}=\alpha(E_i-E_j).
\]

Alle par-fluxe beregnes ud fra energierne før transporttrinnet og summeres først derefter, så energien ikke springer øjeblikkeligt på tværs af kolonien. Naboer defineres ved 4 eller 8 forbindelser efter det valgte gitter; de periodiske kanter respekteres. Kontrolparameteren **α kan vælges 0,00–0,12**, standard 0,10, hvilket holder det eksplicitte trin stabilt og ikke-negativt selv ved 8 naboer. Transporten finder sted efter energiudveksling med fælleslageret og før vækst-/angrebshandlingerne. Nul-energi-død kontrolleres ved afslutningen af et sweep; et træ, der taber i kamp, dør straks. Formering kræver fortsat overførsel af 2 energienheder også ved kolonisering af tomt felt.

Validering af JavaScript-reglerne: 20×20 gitter, 5 arter, 40 % startdækning, 160 sweeps i hver af kombinationerne (højde-/energikamp) × (4/8 naboer) ved α=0,12. Største absolutte afvigelse fra startenergien var 1,23×10⁻¹¹ modelenergienheder; ingen negative energiresultater. Ingen browser-visuel test endnu. Modellen er energibevarende, men dette alene dokumenterer ikke en fysisk termodynamisk første-hovedsætning med alle former for energi repræsenteret.


## 16. november 2026 — Fjernet fast tilbageførsel af energi pr. sweep

Energi returneres ikke længere automatisk fra levende træer til fælleslageret i hvert sweep. Hvert levende træ kan fortsat modtage op til den angivne energimængde fra lageret ved sweepets begyndelse, forudsat at lageret har energi nok. Energi går **tilbage til lageret ved vertikal vækst** (den betalte vækstenergi) og **ved død** (eventuel resterende disponibel energi). Den lokale energitransport mellem nabotræer af samme art og overførslen af 2 energienheder fra modertræ til afkom er fortsat interne overførsler. Energibalancen forbliver E_total = sum E_træ + E_lager.

Indstillingen 'Energi retur fra træet pr. sweep' er fjernet fra både HTML og simulationens beregninger.

Funktionstest: 20×20 gitter, fem arter, startdækning 40 %, 150 sweeps med henholdsvis højde- og energibaseret konkurrence. Maksimal energibalanceafvigelse: 5,92×10⁻¹² henholdsvis 6,37×10⁻¹² modelenergienheder. Ingen negative energier registreret.


## 16. november 2026 — Tre samtidige statistiske mål for skoven

Det nye panel **Entropi og energifordeling** viser tre tidsserier: (1) arts-Shannon-entropi H_art = −Σ_k p_k ln(p_k); (2) energi-Shannon-entropi H_E = −Σ_i q_i ln(q_i), hvor q_i = E_i/Σ_j E_j for levende træer og fælleslageret er udeladt; og (3) Pearson-korrelationen r_E mellem disponible energier i nabopar af levende træer. Rumlig korrelation beregnes for vandrette og lodrette nabopar, uanset om konkurrence foregår med 4 eller 8 naboer. Periodiske kanter respekteres.

Ved graftegning normaliseres H_art med ln(K), H_E med ln(N_levende), og r_E afbildes som (r_E+1)/2, så alle tre kan vises på 0–1-akse. De rå værdier vises særskilt. Det understreges på siden, at hverken energi-Shannon-entropi eller energikorrelation i sig selv er termodynamisk entropi. Ved ingen træenergi eller utilstrækkelig variation er relevante mål udefinerede; kurven afbrydes for manglende værdier frem for at tegne nul.

Kontrol: 150 sweeps på 20×20-gitter, 5 arter, 40 % startdækning med begge kampformer. Ingen negative energier, og energibalancens største absolutte afvigelse var under 7×10⁻¹². Browser-visuel kontrol udestår.


## 16. november 2026 — Konsolideret entropivisning og afgrænsning af termodynamisk S

Det overflødige panel "Evolution og diversitet" er fjernet, fordi H_art allerede blev vist i "Entropi og energifordeling". Den samlede visning hedder nu "Evolution, entropi og energifordeling" og har kun ét sæt tal og kurver for H_art, energi-Shannon-entropi H_E og rumlig Pearson-energikorrelation r_E. Browser-referencer og JavaScript-syntaks er kontrolleret.

Vi har diskuteret en mulig **fremtidig, separat termodynamisk kontrolmodel**: To varmebeholdere med definerede temperaturer og varmekapaciteter, med varmeoverførsel fra varm til kold. Entropien kan da regnes som ΔS = Σ C_i ln(T_{i,f}/T_{i,i}). Dette er **ikke implementeret**. Vores nuværende træenergi er en idealiseret disponibel ressource uden temperatur, varme og specificeret antal mikrotilstande. H_E er derfor ikke termodynamisk entropi, og en invariant E_total alene garanterer ikke anden hovedsætning.


## 16. november 2026 — Angreb kun fra klumpens rand

**Ny gældende regel:** Hver sammenhængende klump af en art træffer ét valg per sweep efter artens faste strategi s: vækst med sandsynlighed 1−s, angreb med s. Ved vækst får hvert træ med tilstrækkelig **egen** disponibel energi lov til at vokse én højdeenhed, mens energifattige træer står stille. Kun hvis ingen træer i klumpen har råd til vækst eller har plads under højdegrænsen, vælger klumpen automatisk angreb. Enkeltstående energimangel tvinger **ikke** hele klumpen til angreb.

**Kun randtræer angriber:** Et træ på klumpens rand er et træ med mindst ét nabofelt (4 eller 8 efter indstilling), der enten er tomt eller tilhører en anden art. Randtræet vælger tilfældigt blandt netop de mulige ydre nabofelter og forsøger kun angreb/spredning, når det kan overføre den konfigurerede energipakke (standard 2). Træer helt omgivet af deres egen art angriber ikke. Angrebets udfald følger fortsat den valgte højde- eller energiformel, og døde træer afleverer deres resterende energi til fælleslageret.

Alle træer beholder egen energi, lokal gradvis energitransport og individuel død ved E=0. Nyfødte træer kan ikke handle før næste sweep.

**Kodevalidering:** 20×20, 5 arter, 40 % startdækning, 200 sweeps per kombination af højde-/energikamp og 4/8 naboer. Maksimal absolut energibalanceafvigelse under 1,1×10⁻¹¹ modelenergienheder; ingen negative energier. Dette er kontrol af numerik, ikke en garanti for oscillationer eller for populationsmæssig persistens.

## 16. november 2026 — Undgå unødvendige inaktive klumper

I den kollektive klumpdynamik var en mulig kilde til tilsyneladende stilstand, at en klump kunne vælge angreb, selv om ingen randtræer kunne angribe et fremmed/tomt nabofelt. Nu trækkes fortsat et fælles vækst-/angrebsvalg med sandsynlighederne 1−s og s, men hvis denne handling ikke kan gennemføres og alternativet kan, bruges alternativet. Hvis ingen træer kan vokse, forsøger klumpen angreb; hvis ingen kan angribe, vokser de individuelt vækstkompetente træer. Er begge umulige, vil klumpen stadig kunne forblive statisk, hvilket er en reel konsekvens af modellen. Individuel energidød og lokal energitransport er uændret.

Funktionstest: 20×20 med 5 arter, 40 % startdækning, 200 sweeps, begge konkurrenceformer. Maksimal numerisk energibalanceafvigelse under 3×10⁻¹²; ingen negative energier. I begge enkeltforløb endte én art med at dække hele gitteret — et eksempel på mulig evolutionær fiksering, ikke et bevis for universel opførsel.


## 16. november 2026 — Energiomdannelse Q → E → U og kombineret kampstyrke

Implementeret idealiseret energiregnskab: E_total = Q + Σ_i (E_i + U_i). E_i er individuelt disponibel energi, som stadig transporteres lokalt mellem nabotræer af samme art. Højdebundet U_i beregnes som growthCost × (h_i−1); h=1 svarer til U=0. Når et træ vokser, flyttes vækstomkostningen fra E_i til U_i, ikke til Q. Ved død frigives træets resterende E_i+U_i til Q.

Angreb: E+U er standardkampstyrke; E alene og U alene kan vælges som kontrol. En kamp mod en fremmed art koster særskilt attackCost=1 fra E til Q, uanset udfald. Angriberen skal samtidig kunne overføre birthCost=2 til et eventuelt nyt træ. Spredning til en tom celle koster ingen ekstra kampomkostning. Ved almindeligt nyt træ (h=1) frigives den besejrede forsvarers U til Q. Hvis den nye celle arver forsvarerens højde, flyttes tilsvarende U fra Q til det nye træ. Ved valg af angriberens højde skal modertræet selv betale disponibel E svarende til barnets U; ellers bliver det nye træ højde 1. Klumpens fælles vækst-/angrebsvalg, randbegrænsede angreb og individuel død ved E=0 er bevaret.

Modellens U er en effektiv højdeafhængig investering, ikke nødvendigvis fysisk tyngdepotentiale mgh. Q er et genanvendeligt lager, ikke i sig selv varme med temperatur eller termodynamisk entropi S.

Numeriske tests: 18 kombinationer af E+U/E/U-kamp, 4/8 naboer og de tre fødselshøjder, hver i 120 sweeps på 15×15, 5 arter, 50 % startdækning. Maksimal absolut energibalanceafvigelse 6,9×10⁻¹³. Alle E>=0 og U svarede præcist til growthCost×Σ(h−1). Visuel browserkontrol ikke udført.


## 16. november 2026 — To valgbare vedligeholdelsesmodeller

Indført vedligeholdelse af hvert levende træ pr. sweep som energioverførsel E_i → Q, begrænset til det faktisk tilgængelige E_i: paid = min(E_i, m_i). Standard er **konstant m_i = 0,10**. Alternativet er **højdeafhængigt m_i = m0 + m1·h_i** med standard m0=0,05 og m1=0,02. Alle parametre kan redigeres, og den aktive model vælges i energireglerne.

Vedligeholdelse køres efter tilførsel fra Q og lokal energitransport, men før klumpernes kollektive vækst-/angrebsvalg. Dermed betaler et nyfødt træ først næste sweep. Træer med E_i=0 dør individuelt og frigiver U_i til Q; de kan ikke overleve uendeligt med en positiv restenergi, hvis de ikke får tilførsel. Det er ikke en fast aldersgrænse.

Tests: 20×20 gitter, 5 arter, 50 % startdækning, 150 sweeps for hver kombination af de to vedligeholdelsesmodeller og tre kampformer. Højeste observerede højde i disse seks forløb var h=59 (konstant) og h=38 (højdeafhængig); alle energier var ikke-negative. Maksimal energibalanceafvigelse < 2,1×10⁻¹¹ for Q + Σ(E+U). Browser-visuel kontrol ikke udført.

## 16. november 2026 — Artsoversigt ved gitteret

Tilføjet en responsiv oversigt direkte ved siden af skovgitteret med artsnummer, artens farve og dens faste strategi s (sandsynlighed for angreb). Oversigten opdateres ved tegning og nedtoner uddøde arter uden at fjerne deres s-værdi. På smalle skærme vises oversigten under gitteret i flere kolonner. Simulationens dynamik er uændret. Kontrolleret JavaScript-kørsel, alle UI-referencer og energibalance i 60 sweeps; ingen browser-visuel test udført.


## 16. november 2026 — Tilbage til enkel højdebaseret Up or out-model

På brugerens ønske er den komplekse Q/E/U-energimodel, energilager, vedligeholdelse, energibaseret kamp, energi-entropi, energigrafer og relaterede kontroller fjernet helt fra HTML og simulationskoden. Modellen bruger nu **kun højden h** som kampstyrke: P(A vinder) = h_A / (h_A + h_B). Ved sejrrigt angreb overtages feltet med et nyt træ i højde 1; ved tabt angreb dør angriberen. Kun randtræer angriber. Hver sammenhængende artsklump træffer stadig én vækst-/angrebsbeslutning efter sin arts faste s. Ved vækst vokser alle medlemmer én højdeenhed, forudsat eventuel højdegrænse. Den anden handling forsøges, hvis den først valgte er umulig.

**Diffusion er bevaret som en åbenlys abstraktion**, ikke som skjult energi: en lokal symmetrisk udjævning af højdeforskelle mellem nabotræer af samme art. For hvert nabopar overføres en højdeandel α(h_i−h_j), med synkron opdatering og 0≤α≤0,12. Det bevarer summen af træhøjder under selve udjævningstrinnet, men kan give decimalhøjder og repræsenterer **ikke fysisk transport af træhøjde**. Som kontrol kan α sættes til 0, hvor hver vækst igen er et helt højdetrin. Dette er en modelantagelse til undersøgelse, ikke en biologisk etableret mekanisme.

Appen er ryddet til skovgitter (vis art, højde eller kombination), arts- og s-oversigt, én graf for artsdiversitet og få forsøgsindstillinger. Mobiltilpasset layout bibeholdt. Numerisk kørselskontrol: 8 kombinationer af 4/8 naboer, α=0/0,1 og startdækning 100 %/40 %, hver 140 sweeps. Ingen ugyldige eller negative højder, ingen runtime-fejl, korrekt initialiseret artsoversigt. Visuel test i rigtig browser er endnu ikke udført.


## 16. november 2026 — Δs i den eksisterende højdemodel

Den eksisterende gittermodel **beholder højden** og alle de hidtidige regler om kollektivt valg, randangreb og lokal abstrakt højdeudjævning. Der er nu en justerbar skelnegrænse Δs med standardværdi 0,01. Kun hvis |s_A−s_B| > Δs må et randtræ fra A forsøge angreb mod B; lige eller næsten lige strategier giver intet kampforsøg. Tomme celler kan stadig koloniseres. Når kampen er tilladt, er sejrssandsynligheden fortsat h_A/(h_A+h_B). Δs er altså en **separat tolerance på strategiforskellen**, ikke et alternativ til højdebaseret kamp. Ingen mutation er tilføjet.

Test: JavaScript kunne køres for Δs=0, 0,01 og 0,20 i 150 sweeps på et 20×20-gitter; uden ugyldige højder eller manglende UI-referencer. Når tolerancen var større, var flere arter tilbage i det testede eksempel. Ingen visuel browserkontrol udført.


## 16. november 2026 — Valg af latticens krumning k = −1, 0, +1

Tilføjet en geometrivælger til den eksisterende højdebaserede skovsimulation:
- **k = 0:** det tidligere kvadratiske gitter, med valgfri periodiske kanter.
- **k = +1:** lukket, sfærisk-lignende ringgraf med celleantal proportionalt med sin(breddegrad), aftagende mod to poler; vist som udfoldet længde-/breddekort. Naboforbindelserne lukkes rundt om ringene og sammenkobles mellem ringe.
- **k = −1:** åben, hyperbolsk-lignende ringgraf med celleantal proportionalt med sinh(radial afstand), voksende mod skivens rand; vist i en diskmodel.

**Præcisering:** Disse er *kombinatoriske tilnærmelser til positiv/negativ krumning*, ikke eksakte tesselleringer af flader med konstant Gaussisk krumning K=±1, og diskens billedgeometri er ikke en metrisk isometri. Antallet af celler er L² i alle tre tilfælde; selve nabografen ændres, så geometri påvirker kamp, koloniforbindelse og lokal højdeudjævning. 4/8-nabovalget bestemmer, hvor mange radiale nabokoblinger der tilføjes i krummede tilfælde; gradtallet er ikke nødvendigvis præcis 4 eller 8. Krumningen ændres ved at geninitialisere forsøget. Periodiske kanter er kun relevante i den flade version.

Kontrol: 20×20, 5 arter, 70 % startdækning, 100 sweeps for alle seks kombinationer af k∈{−1,0,+1} og 4/8 nabovalg. Ingen ugyldige/negative højder og alle kombinationer gennemførte uden kodefejl; de krummede grafer har præcis L² celler. Browservisuel kontrol er ikke gennemført.


## 16. november 2026 — Interaktiv 3D-sfære ved k=+1

For **k=+1** er den tidligere udfoldede 2D-projektion erstattet af en drejelig, perspektivlignende **ortografisk 3D-projektion af en sfære** i samme canvas. En pixel i den synlige halvkugle beregnes ved invers sfæreprojektion og henføres til præcis én eksisterende celle i den sfæriske ringgraf. Bagsiden dækkes af forsiden. Der er lys/skygge for rumlig form, men artsfarver og den valgte højdevisning fungerer fortsat.

Interaktion: træk med mus eller finger for rotation om to akser; zoom med musehjul eller +/−; knap til nulstilling. k=0 beholder det kvadratiske gitter; k=−1 beholder den flade hyperbolske skiveprojektion. **Simulationsregler og nabograf er uændrede**. Projektionen er en visuel sfære, ikke et bevis for at den diskrete ringgraf er en eksakt sfærisk tessellering med konstant lokal krumning.

JavaScript-test: k=−1,0,+1 i 40 sweeps på 20×20, inklusive kald af rotations-, zoom- og nulstillingshændelser for k=+1; ingen runtime-fejl. Visuel test i rigtig browser ikke udført.


## 16. november 2026 — Kontinuerlig evolution: børnemutation og spontan mutation

Begge mutationsveje er implementeret i den eksisterende højdebaserede skovmodel med Δs-tolerance, lokal højdeudjævning og k=−1/0/+1, inklusive drejelig 3D-sfære for k=+1. Intet optimum for s er programmeret. Mutationer går tilfældigt i begge retninger og begrænses til intervallet [0,1].

**Børnemutation:** Hver vellykket fødsel (overtagelse af tomt eller besat nabofelt) har standardmæssigt 1 % sandsynlighed for at få en strategi s' = s ± dε. Uden mutation arves forælderens art/strategi. **Spontan mutation:** Uafhængigt af fødsler har hver sweep 1 % sandsynlighed for, at én tilfældig levende celle får s' = s ± dε. Gennemsnitligt én spontan mutation pr. 100 sweeps i hele skoven. Standard dε=0,01. Alle tre værdier er justerbare i panelet Mutation og evolution. En mutant får et unikt arts-id og kan selv få efterkommere, så selektion kan ændre den dominerende strategi.

Appen viser antal mutationer af hver type, dominerende levende arts s og de op til 24 mest talrige levende arter; nye mutanter får deterministiske artsfarver. Artsentropi H normaliseres nu til ln(antal levende træer), og grafens anden kurve er største arts andel i stedet for det gamle antal arter / startantal, fordi artsmængden nu er dynamisk. Andelen af fremmede nabopar måles langs faktisk valgt geometris kanter.

**Vigtig begrænsning:** Δs-reglen er stadig en hård spærring, hvis |s_i−s_j|≤Δs. En mutation på præcis 0,01 med Δs=0,01 kan derfor normalt ikke angribe sin moderlinje direkte. Det kan forsinke selektionen. Mutationer garanterer variation, men hverken permanent aktivitet eller at systemet konvergerer mod én optimal strategi.

Kørselstest i JavaScript for k=−1,0,+1, hver 100 sweeps på 20×20 med maksimalt mutationstryk (10 % ved fødsel og 100 % spontan pr. sweep) for at belaste systemet. Der blev registreret hundrede spontane mutationer i hvert forsøg og hundredvis af børnemutationer, ingen ugyldige artshenvisninger eller højder og ingen manglende UI-elementer. Ægte browser-visuel validering ikke udført.


## 2026-11-16 — Peters private Skovlab: forsøg A/B/C og energiregler

Der er oprettet et tilvalg af dimensionsløs energi i `peter-dev/index.html` og en separat offentlig kopi på `main/peter/index.html`, som kan åbnes på https://pdamkier-del.github.io/skovlab/peter/. **Den fælles simulation i `main/index.html` er uændret.**

Tre forskningspaneler: **A** (energitilførsel, populationstæthed, aktivitet, mulige kritiske tilstande), **B** (periodisk energitilførsel og populationsvægtet strategi) samt **C** (Shannon-artsentropi, dominans og dødsfald). Grafer viser tidsserier, ikke automatiske påstande om faseovergange eller tilpasning. I særdeleshed er Shannon-entropi og dødstællinger **ikke termodynamisk entropiproduktion**.

Justerbare energiparametre: middeltilførsel Q0, amplituden a, perioden T, **vækstomkostning pr. træ**, **angrebsomkostning pr. forsøg**, **energioverførsel til afkom fra forælderen**, vedligeholdelse, startenergi og maksimumreserve. Før hver sweep modtager levende træer Q(t)=Q0[1+a sin(2πt/T)] og betaler vedligeholdelse; ved underskud dør de. En handling kræver tilstrækkelig reserve. Succesfuld kolonisering betaler afkommets startenergi fra forælderen. Der er ingen energiudveksling gennem tomme celler, og ingen varme-/reservoirregnskab. Energimodellen kan slås fra, så den oprindelige dynamik kan bruges som kontrol. Modelparametre genstarter for reproducerbare forsøg.

Kørselskontrol via den faktiske JavaScript-kode: 20×20, 150 sweeps, Q0=0/0,4/1,3/2,2; ingen ikke-finite energier/højder. Ved lave Q0 blev alle træer uddøde, ved højere Q0 overlevede træer med fortsat aktivitet. Dette er kun en funktionstest og ikke evidens for en kritisk faseovergang. Separat kontrol med energimodel slået fra gennemført. Visuel browser-test og live GitHub Pages-servering ikke uafhængigt verificeret.


## 2026-11-16 — Oprydning i Peters lab og samlet model

Egen HTML i `peter-dev/index.html` og webkopien på `main/peter/index.html` er konsolideret. Fælles `main/index.html` er ikke ændret. En synlig modeloversigt angiver én samlet simulation og kæden: periodisk ekstern energitilførsel → fælles pulje → optag og vedligeholdelse → vækst/angreb/død. Klimaet påvirker **kun tilførslen til energipuljen**, ikke angrebssandsynlighed eller andre mikroskopiske regler direkte. Kontrolpanelet angiver formel `Q(t)=Q0[1+a sin(2πt/T)]`, aktuelle værdier, interval og fase, inklusive forklaring af `Q0`, `a` og `T`.

A/B/C vises nu som *analysefaner for den samme model* (A energipulje og aktivitet, B miljø og strategi, C Shannon-entropi og mutation). Dobbeltmålinger i den gamle separate udviklingssektion er fjernet. Variabler er omgrupperet til Simulation, Miljø/fælles energi, Træernes handlinger, Mutation/strategi og Gitter/geometri; avancerede indstillinger er sammenklappelige. Eksisterende id'er og den fysiske dynamik er bevaret.

Automatiseret JS-runtimetest med mock DOM og samtlige nødvendige felter: fladt, sfærisk-lignende og hyperbolsk-lignende gitter, flere tilførsler, 100 sweeps pr. kombination (9 forsøg); maksimal absolut energibalancefejl ca. 3.8e-9 energienheder. Dette er ikke en ægte visuel browser-test. Det numeriske energiregnskab er i abstrakte modelenheder og ikke et termodynamisk entropiregnskab.


## 2026-11-16 — Konservativ pulje Q og højdebaserede angreb (Peters lab)

Personlige versioner på `peter-dev/index.html` og `main/peter/index.html` opdateret. Kampvinder afhænger fortsat af højde `P(A vinder)=h_A/(h_A+h_B)=U_A/(U_A+U_B)` med fælles `U=κh`, standard κ=2. Træernes reserver starter på 10. Angrebspris er 1 og returneres til Q; vedligehold returneres ligeledes; død frigiver restreserve og U til Q. Afkom får reserver og strukturel energi finansieret af forælderen. Periodisk variation regulerer loftet for optag fra Q, ikke tilførsel af ny energi. Parvis konservativ energidiffusion sker over nabokanter mellem træer med samme art eller strategiforskel højst Δs; den tidligere abstrakte højdeudjævning er erstattet. Hvis et træ ingen angrebsbare naboer har, kan gruppen kun vokse, hvis energien rækker. Start-Q sat til 2 pr felt så periodisk uddeling har effekt. Puljetab standard 0. Energiregnskab er `Q+Σ(E+U)+kumulativt tab = startenergi`. Test: 3 geometrier × 3 amplituder × 180 sweeps; maksimal absolut balancefejl < 2e-10 energienheder i test. Ved amplituden 1 blev fuld udryddelse observeret i test med positiv pulje tilbage; uden træer findes ingen mekanisme til spontan genkolonisering. Ikke evidens for faseovergang. Browser-visning ikke valideret separat.


## 18. november 2026 — Implementeret bet-hedging og uforudsigeligt klima uden artsimmunitet

**Brugerbestilling:** Erstat beskyttelse af ens/lignende arter med almindelig konkurrence, og tilføj både arvelig bet-hedging og et uforudsigeligt miljø. Formålet er at undersøge løbende evolutionær omsætning af angrebsstrategier, uden at artsdiversitet bliver påtvunget.

### Den nye dynamik

- **Ingen Δs-immunitet:** Den tidligere skelnegrænse og dens input er fjernet. Nabotræer kan angribes uanset genotype eller fænotype, også hvis de kommer fra samme art. Energiforbrug, højdeafhængig vinderchance og regler for formering er stadig gældende.
- **Diversified bet-hedging:** Genetisk slægtlinje `a` har arvelig middelstrategi `μ_a` i `strategies[a]` og arvelig variationsbredde `σ_a` i `sigmas[a]`. Hvert træ har en individuel, varig fænotype `s_i` i `phenotypes[i]`, sampled ved etablering som `clip(μ_a + U[-σ_a,σ_a],0,1)`. Frie afkom og afkom efter kamp nedarver arts-id (medmindre fødselsmutation laver ny slægtlinje), men får deres egen fænotype. På hver fødsel kan mutation, hvis aktiveret, lave en ny slægtlinje med ændret `μ` eller `σ`. Spontan mutation på levende træ ændrer også arvelig slægtlinje og genprøver fænotypen. Bet-hedging kan slås fra, hvorefter alle træer i en art har `s_i = μ_a` og den gamle artsgruppebaserede handlingsbeslutning bruges.
- **Individuelle valg:** Med bet-hedging aktiveret beslutter træet at vokse eller angribe med sin egen `s_i`, så fænotypevariation faktisk kan påvirke konkurrencen. Uden bet-hedging beslutter en sammenhængende artsgruppe samlet som tidligere.
- **Uforudsigelige klimachok:** En særskilt seed-baseret hash giver én pseudotilfældig multiplikativ faktor pr. klimaperiode på *den planlagte energioptagskapacitet fra Q*. `climateNoise` er styrken 0–1; faktoren er `1 + noise × U[-1,1]`. Det er ikke ekstern energi: hvert optag flytter som hidtil energi fra Q til E, og Q+Σ(E+U) bevares. Klimatidsserien kan gentages ved samme seed. Basisformlen kan stadig redigeres i formelfeltet; den grønne periodekurve viser aktuelt realiseret optagskapacitet inkl. chok.
- **Diversitetsmål:** Shannon-artsentropi H fra slægtlinje-andele holdes adskilt fra fænotypisk strategientropi, beregnet på ti s-intervaller. Forskningspanel viser også gennemsnitlig arvelig σ og en ny tidsserie med fordelinger mellem lave, mellem og høje angrebsstrategier.

### Metodiske forbehold

Dette er en **testbar bet-hedging-hypotese**, ikke endnu dokumentation for at bet-hedging vinder: der skal sammenlignes med `betHedging=0` og `climateNoise=0` under parrede seeds samt måles langsigtet overlevelse og slægtlinjeudskiftning. Stokastiske klimafaktorer er her uafhængige *mellem perioder* men konstante i hver periode. Fordelingssamplingen er uniform og klippet ved grænserne, ikke en normalfordeling. Interne fænotyper hører til samme genetiske art; derfor kan strategientropi stige uden at artsentropien stiger. Der er ingen belønning for sjældne arter eller beskyttede angrebsmål.

### Verifikation

Browserbaserede mekaniktests findes i `scripts/peter-hedging.test.cjs` og er koblet på `scientific-labs.yml`. De kontrollerer angrebsadgang mellem selv identiske arter, afkoms variationsgrænser, klimachoks reproducerbarhed og aktivering, deterministisk genstart med samme seed, energibevarelse under 400 sweeps på tre geometrier samt korrekt energi-/slægtsarv ved spredning og de nye grafer. Den 18. november 2026 bestod disse tests sammen med de øvrige videnskabelige tests i GitHub Actions workflow **44345250744**.


## 25. november 2026 — Ny forskningsretning: zeta, statistiske energifordelinger og spektral geometri

**Status:** Hypoteser og pilotdesign. Eksisterende simulationsmekanik bevares uændret; eksterne scripts måler den faktiske `peter-dev/index.html` via `window.__skovTest`. Ingen antagelse om en priori potenslov, kritikalitet eller kobling til Riemanns nulpunkter.

### Audit af den aktuelle model
- To forskellige energibegreber: reserve `E_i=en[i]`, strukturenergi `U_i=u[i]`. Puljen `Q=pool` indgår i `Q+Σ(E_i+U_i)` (konstant op til numerisk afrunding). Klimaet ændrer *kapaciteten til optag fra Q*, ikke tilførsel af ekstern energi.
- Bet-hedging: `strategies[a]=μ_a` og `sigmas[a]=σ_a`, individuelt `phenotypes[i]=s_i` for hvert træ. Angreb på træer af samme art er fortsat tilladt i den nuværende implementering. **Ingen modelregler ændres** i dette forsøg.
- Diffusion: `en_i ← en_i + d Σ_{j~i, levende og samme art}(en_j-en_i)`, `d=min(alpha,.45/maxDegree)`. Tomme celler og kanter mellem forskellige arter leder ikke diffusion. Den aktive graf består af artsafgrænsede levende komponenter. Gitterets graf alene er en reference og ikke den faktisk anvendte diffusionsgraf.
- Geometrierne `k=+1` og `k=-1` er diskrete ringgitter-approksimationer og må **ikke** ukritisk tolkes som eksakte konstantkrumme flader.
- `H=-Σp_a ln p_a` er Shannon-artsentropi, **ikke** termodynamisk entropi.

### Forskningshypoteser og forudregistrerede checks

**H1 (energifordeling):** Rangeret reserveenergi `E_(r)` kan over et afgrænset interval følge `A r^{-alpha}`. Nulhypotese: den ikke-lineære rangkurve beskrives bedre af fx lognormal- eller eksponentialfamilier eller viser systematisk krumning. Måle både `E_i` og `E_i+U_i` ved flere sweeps, seeds, størrelser. Log-log OLS og høj R² er **kun en screening**, ikke en goodness-of-fit test. Ved senere konfirmation: distributionsbaseret MLE, estimering af `x_min`, KS-bootstrap, log-likelihood-ratio/Vuong mod lognormal, eksponential og stretched exponential, samt held-out seeds. Varierende positiv støtte og reserve på nul skal håndteres eksplicit. Rapporter exponentens usikkerhed på seed-niveau, ikke som om tidslige snapshots er uafhængige.
**H2 (endelig størrelse):** Test gitter `L=10,20,30`, fast 8 startarter, startdækning 0,55, seed 11,23,37,47, miljøstøj 0 vs 0,6 og diffusion 0 vs 0,1. Ingen manipulerede energiregler. 500 sweeps og snapshots efter 300/400/500. I alt 48 uafhængige kørsler, tre tidskorrelerede snapshots per kørsel. Samme seed parres mellem betingelser. Vurder `alpha`-variation og kumulativ top-10%-energiandel; sammenlign log-rank potensmodel med kurvet log-rank og eksponentiel rangmodel. Dette er **pilot**, ikke et bevis for asymptotisk form.
**H3 (spektral geometri):** Den faktiske diffusionsoperator er `I-d L_aktiv(t)` ved et fast frozen snapshot. Det relevante spektrum er det af `L_aktiv`, ikke kun den statiske graf-Laplacian. Ved flere isolerede komponenter er der flere nul-eigenværdier. For positive eigenværdier defineres `ζ_skoven(s;t)=Σ_{λ_j(t)>0} λ_j(t)^{-s}`. Sammenlign nulmoders antal, mindste positive egenværdi, diffusionsrelaksation og `ζ(1),ζ(2)`; baseline for fladt periodisk 4-nabo-gitter har eksakt `λ_{kl}=4-2cos(2πk/L)-2cos(2πl/L)`. Tilføj senere konkret spektrum for aktivt artsnetværk og ringgeometrier, med tomme og fulde netværk som kontroller.
**H4 (kritikalitet):** Ingen identifikation af SOC alene ud fra potenslov i E eller arters antal. Kræv blandt andet definerede kaskadehændelser (udryddelses-/dødsklynger), finite-size scaling, systemstørrelsesafhængige cutoffs og robust parameterområde uden finjustering. Udviklings-/miljøtidsserier er autokorrelerede og periodiske; blokbootstrap eller uafhængige seeds kræves.
**H5 (ægte talteori):** Riemanns klassiske zeta `ζ(α)` kan opstå som matematisk *beskrivelse* af en hypotetisk uendelig Zipf-række. For endelig N er den rigtige sum `H_N^(α)`. Primtalsenergier og Eulerprodukter følger ikke af skovens nuværende regler; Riemann-gassen med `E_p=ε ln p` er kun en eventuel fremtidig **kontrastmodel**, ikke en påvisning af talteoretisk struktur.

### Centrale kilder
- Clauset, Shalizi & Newman (2009), *Power-law distributions in empirical data*, SIAM Review 51(4), 661–703, DOI 10.1137/070710111: https://arxiv.org/abs/0706.1062
- Newman (2005), *Power laws, Pareto distributions and Zipf’s law*: https://arxiv.org/abs/cond-mat/0412004
- Friedli & Karlsson (2014), *Spectral zeta functions of graphs and the Riemann zeta function in the critical strip*: https://arxiv.org/abs/1410.8010
- Karlsson (2019), *Spectral zeta functions*: https://arxiv.org/abs/1907.01832
- Pruessner (2012)/review (2015), *25 Years of Self-Organized Criticality: Concepts and Controversies*: https://doi.org/10.1007/s11214-015-0155-x
- Julia/Bost-Connes primon gas theory context: https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/physics2.htm

### Reproducerbare pilotmålinger
`scripts/peter.number-theory-pilot.cjs` producerer seed-/størrelsesstratificerede rank-fits og eksakte statiske torus-eigenværdier via GitHub Actions `scientific-labs.yml`. Ikke konkludér fra graf eller fit alene. Resultater, herunder negative fund, tilføjes i en separat logbogssektion efter vellykket kørsel.


## 25. november 2026 — Faktiske numeriske resultater: rangeret energi og zeta-reference

**Kørslen:** GitHub Actions `45655852924`, gennemført med success. `node scripts/peter.number-theory-pilot.cjs` på den *uændrede* `peter-dev/index.html`. Alle 7 mekaniktests, 24 andre tests og eksisterende browserchecks bestod.

### Protokol
48 uafhængige runs = 3 gitterstørrelser (10,20,30) × 4 seeds (11,23,37,47) × klimastøj (0,0.6) × diffusion (0,0.1). Hvert forløb = 500 sweeps. Snapshots ved sweep 300, 400 og 500: **144 tidskorrelerede målinger, ikke 144 uafhængige replikater**. Øvrige værdier fastholdt: 8 startarter, dækning 0.55, beta-hedging aktiv, variationsbredde .25, mutation 0.1 % pr. fødsel, 4 naboer, flad geometri, periodisk rand, energioptag 1, klimaamplitude .5, klimaperiode 80, vedligeholdelse .1, angrebspris 1, vækstpris 2. Observeret energi-balancefejl under 7e−9 i alle betingelser.

Enkel *beskrivende* regressionsscreening på rangordnede positive reserveenergier `en[i]`:
- Potenslov: OLS `log E_r = a - α log r`;
- Alternativ A: krum `log E_r = a+b log r+c(log r)^2`;
- Alternativ B: eksponentiel rangkurve `log E_r = a+b r/n`.
Der sammenlignes gennemsnitlig RMSE på *samme* data. En eksponentiel rangkurve svarer ikke i sig selv til en eksponentialfordeling af råenergierne; denne screening er **ikke** Clauset-MLE, KS eller test af et probabilistisk distributionsvalg.

### Samlet negativt fund
**Den eksponentielle rangkurve havde lavere log-RMSE end potensloven i ALLE 12 parameterkombinationer**, og lavere end den krumme log-rank-model i alle 12. For 20×20, klimastøj=0, diffusion=0, var RMSE: potenslov 0.6901, krum log-rank 0.4927, eksponentiel rangkurve 0.3864. Tilsvarende var mean R² for potenslov blot ca. 0.529 (deskriptivt og ikke særligt overbevisende).

Gennemsnitlig OLS-rangeksponent `α` for reserver:
| L | Klimastøj | Diffusion 0 | Diffusion .1 |
|--|--:|--:|--:|
| 10 | 0 | 0.8848 | 0.7537 |
| 10 | .6 | 0.6463 | 0.6983 |
| 20 | 0 | 0.8094 | 0.7246 |
| 20 | .6 | 0.6893 | 0.6369 |
| 30 | 0 | 0.7818 | 0.7120 |
| 30 | .6 | 0.6485 | 0.6731 |

Alle gennemsnit <1, og ingen tydelig tiltrækning til α=1. Eksempel på kontrast ved L=30, α_diff=0: klimastøj 0 med `α_rank≈.782`, støj .6 med `α_rank≈.649`. Men der er kun 4 uafhængige seeds og 500 sweeps; dette må ikke fortolkes som verificeret kausal effekt eller universel exponent.

**Størrelse / diversitet:** Ved klima=0, diffusion=0 var gennemsnitligt antal overlevende arter: L10 = 1.167; L20 = 3.500; L30 = 5.250. Shannon H: 0.0932; 0.7567; 0.8322. En oplagt alternativ forklaring er *langsommere artstab i store gitre* og ikke en faseovergang. Tætheden lå omkring 0.53–0.56; sammenlign derfor også occupancy, ikke blot arternes absolutte antal. Højere genetisk artsrigdom med L alene er ikke bevis på kritikalitet.

**Reserver vs totaltræenergi:** Der findes også rangregressionsestimater for `en[i]+u[i]` i råoutputtet, og disse er typisk lidt større end reservernes rangeksponent i de 12 forhold. Forskellen understreger behovet for præcis energidefinition.

### Den *statiske*, eksakt beregnede flade gitterreferences spektral-zeta

Referencegraf: 4-nabo periodisk `L×L` kvadratisk gitter, **ikke den faktiske dynamiske diffusionsgraf**. Eksakte analytiske egenværdier:
`λ_{kl}=4−2cos(2πk/L)−2cos(2πl/L)`, (k,l) ikke begge nul.

| Side L | Pos. egenværdier | λ_min(>0) | ζ_graph(1) | ζ_graph(2) |
|---|---:|---:|---:|---:|
| 10 | 99 | 0.381966 | 41.495383 | 43.633036 |
| 20 | 399 | 0.097887 | 210.191558 | 644.063612 |
| 30 | 899 | 0.043705 | 531.045602 | 3196.522121 |

Disse værdier er en **matematisk kontrol for gitteret**, ikke et emergent evolutionært resultat: spektral-zeta følger direkte af den valgte geometri. Den voksende ζ(2) med L kan skyldes lavfrekvente diffusionsmodi, men beviser ikke, at skoven er kritisk.

### Foreløbig fortolkning
**Ingen påvist spontan Zipf- eller Riemann-zeta-struktur i reserverne.** De enkle screeningmodeller taler imod en enkel global potenslov. Vi har endnu ikke testet en *afgrænset høj-energi-hale* med korrekt MLE/x_min/KS eller holdout-data, så det er ikke legitimt at udelukke enhver form for lokal skaleringslov. Den næste prioritet er faktisk spektrum for den artsafhængige levende diffusionsgraf (script `scripts/peter.spectral-pilot.cjs`) og stærkere distributionsinferens.


## 25. november 2026 — Faktiske dynamiske Laplace-spektre på skovens levende artsnetværk

**Kørslen:** GitHub Actions `45656392947`, success. Script `scripts/peter.spectral-pilot.cjs` diagonaliserer de *eksakte endelige matricer* numerisk med symmetriske Jacobi-rotationer. Egenværdier valideret med `tr(L)=2m` til ~1e−13 og ingen betydelige negative eigenværdier. Ingen simulationregler ændret.

### Protokol
27 frosne grafer = geometrier 0,+1,−1 × seeds 11,23,37 × t=0,150,300, gitter L=10 (100 knuder), otte initialarter, klimaNoise .6, diffusion .1, betHedging til, øvrige parametre fastholdt. Der blev dannet to Laplace-matricer for hvert sample: (1) **statisk nabogeometri** med alle 100 knuder og enhver underliggende geometri-kant; (2) **dynamisk diffusiv graf**, der kun bevarer kanter mellem to *levende* nabotræer af samme art, nøjagtigt som originalfunktion `diffuseEnergy()`. Isolerede og ubeboede felter bevares som nulegenværdier i hele 100×100-operatoren. `ζ_G(s)=Σ_{λ>0}λ^{-s}` med eigenværdier fra den unormaliserede kombinatoriske Laplacian. Den virkelige Euler-diffusion har yderligere faktor `d=min(alpha,.45/maxDegree)`, hvilket skal med ved absolutte relaxationshastigheder.

### Målinger: middel over 3 seeds, t=300
| Geometri | Antal statiske kanter | Aktive kanter | Nulmodi (aktive graf) | mindste λ>0 | ζ_aktiv(1) | Levende arter |
|---|---:|---:|---:|---:|---:|---:|
| k=0 | 200 | 61.333 | 49.667 | 0.082291 | 99.789 | 1.667 |
| k=+1 | 196 | 53.667 | 55.667 | 0.064240 | 56.968 | 2.333 |
| k=−1 | 175 | 48.333 | 58.000 | 0.035191 | 81.959 | 2.000 |

Underliggende geometriers statiske spektrum (identisk på tværs af seeds, samme L=10):
| Geometri | λ_min(>0), statisk | ζ_statisk(1) | nullitet |
|--|--:|--:|--:|
| k=0 | 0.381966 | 41.495383 | 1 |
| k=+1 | 0.154434 | 47.639678 | 1 |
| k=−1 | 0.085349 | 68.045430 | 1 |

### Interne tidsændringer (flad geometri, middel over 3 seeds)
- Ved t=0: 6.333 aktive kanter, 93.667 nulmodi, 8 levende arter; meget få nabopar har samme art i tilfældigt startet skov.
- Ved t=150: 51 aktive kanter, 53.667 nulmodi, 2.333 levende arter, ζ_aktiv(1)≈83.37.
- Ved t=300: 61.333 aktive kanter, 49.667 nulmodi, 1.667 levende arter, ζ_aktiv(1)≈99.79.

Dette er et **matematisk observerbart negativt fund** i forhold til antagelsen om at det fulde gitter direkte styrer energidiffusionen: den virkelige diffusion foregår i stærkt opdelte, artsafgrænsede komponenter. Antallet af nulmodi er en direkte netværkstopologisk invariant. Den voksende aktive kantandel fra start til t=300 følger bl.a. vækst af monokulturlignende klynger og behøver ikke betyde mere artsdiversitet.

**Forbehold:** Kun 3 seeds og 300 sweeps, ingen signifikans- eller kausaltest. De dynamiske `ζ(1)`-tal domineres potentielt af få næsten-nul eigenværdier og er ikke direkte sammenlignelige på tværs af forskellige nulliteter uden passende normalisering/conditionering. Den valgte grafoperator beskriver *kun diffusionstrinnet på et frosset snapshot*, ikke alle processer i modellen og ikke stabiliteten af den fulde evolutionære dynamik. De positive/negative geometrier er algoritmiske ringgitter, ikke nøjagtige konstantkrumme flader. Næste skridt: fra-til-seed holdout, L=10–30 med sparse eigensolver, dynamikkomponenters andel af levende træer, nullitet uden tomme knuder, diffusion-only perturbationstest og prædiktion af efterfølgende H/strategiombytning med tidsforskudt regression.

### Hypotesestatus efter to pilotundersøgelser
- **Global Zipf i reserveenergi:** foreløbig *ikke understøttet* (anden rangfunktion bedre; endnu ingen formel tailsammenligning).
- **Riemann ζ(α) som faktisk fysisk energifordelingslov:** *ikke understøttet*. Den endelige sum `H_N^(α)` er fortsat matematisk korrekt ved antaget ranglov, men ikke empirisk bekræftet.
- **Spektral zeta for aktiv skovdiffusion:** **beregnet og matematisk veldefineret**, stærkt afvigende fra statisk gitter-zeta. **Ingen kausal forbindelse til artsdiversitet endnu.**
- **SOC/kritiske eksponenter/faseovergange:** endnu *ikke testet tilstrækkeligt*, kræver finite-size scaling og kaskadeanalyse.
- **Primtal/Eulerprodukt/Lee–Yang-nulpunkter:** ingen fund; spekulativt i denne model uden pålagt struktur.

### Genkørsel
`node scripts/peter.number-theory-pilot.cjs` og `node scripts/peter.spectral-pilot.cjs` med statisk server på port 8000 og Playwright Chromium; GitHub workflow `scientific-labs.yml` kører begge og eksisterende tests. Resultaterne mærkes `SKOV_ZETA_PILOT_START/END` og `SKOV_SPECTRAL_PILOT_START/END` i CI logs. De enkelte per-seed resultater findes der og skal opbevares som grundlag for konfidensintervaller og ekstern reproduktion.


## 25. november 2026 — Kan diffusionsnetværket forudsige fremtidig artsdiversitet?

**Videnskabeligt spørgsmål:** Forbedrer observeret aktuel diffusionsnetværksstruktur en `H(t+100)`-prognose ud over `H(t)`, det levende artsantal, trædækningen, gennemsnitlig individuel s, L, klimastøj og tidspunkt? Dette er en egentlig tidsforskudt holdout-test, men endnu ikke en kausalitetstest.

### Reproduktion
Faktisk browsermotor, **ingen regler ændret**, GitHub Actions `45658728471` på hovedanalysen i `scripts/peter.spectral-prediction.cjs`. 20 uafhængige seeds × 2 størrelser L=10 og 20 × 2 støjniveauer 0 og 0.6 = **80 kørsler**. Hver simulation løber til 400 sweeps; prædiktorer ved t=100,200,300; respons ved t+100. **240 tidskorrelerede observationer fra 80 runs**. Holdout opdelt efter seed for at undgå den groveste pseudoreplikation: 12 træningsseeds og 8 helt nye testseeds; test-sættet har 96 observationer fra 32 uafhængige forløb. Samme seed parres mellem størrelse og klimabetingelse.

Betingelser: startdækning 0.55, K=8, 4 naboer, periodisk fladt gitter, alpha=0.1, betHedging til, hedgeWidth .25, climateAmplitude .5, period 80, birthMutation=0.1%, spontane mutationer fra, øvrige parametre som seneste model. `Q+Σ(E+U)` kontrolleres med afvigelse < 1e-6.

**Prædiktormodeller:** Simpel ridge-OLS (straffeparameter 5, standardiserede features kun fra train); baseline features: H(t), artsantal(t), levende andel(t), s(t), L, klimastøj, t. Eksperiment model: samme + tre topologiske mål `activeEdgeFraction`, `componentPerTree`, `largestComponentShare`. Ingen mål fra fremtiden anvendes som input. Den passive baseline `H(t+100)=H(t)` testes også. Netværksfeatures er **topologiske mål**, ikke endnu numeriske Laplace-egenværdier. Antal komponenter er dog Laplace-nullitet for live-grafen, hvilket gør det til et direkte spektralt relateret mål. Netværket er artsafgrænset præcis som den faktiske `diffuseEnergy`.

### Resultater på helt nye seeds (96 korrelerede holdout-snapshots)
| Metode | MAE for H(t+100) | RMSE |
|---|---:|---:|
| Ren vedvaren: H(t+100)=H(t) | 0.288540 | 0.421829 |
| Baseline med aktuelle miljø-/artsdata | **0.212007** | **0.285641** |
| Baseline plus diffusionsnetværkets 3 mål | 0.215780 | 0.290526 |
| Baseline plus 2 mål uden største komponent | 0.217061 | 0.291038 |

Netværksvariablerne gør her fejlmålet **ca. 1.8% dårligere** i MAE sammenlignet med rimelig baseline; ingen påvist ekstra prognosekraft. Ved L=10 er MAE .16658 baseline mod .17451 udvidet; ved L=20 .25743 mod .25705 (meget lille forbedring, ikke robust). Ved klima 0: baseline .21681, udvidet .21850; ved klima .6: baseline .20721, udvidet .21306. Konklusionen om den samlede pilot er derfor negativ.

Gennemsnit over de 240 snapshots: 25.58% af alle underliggende kanter er aktive same-species-diffusionsforbindelser, 27.45 levende komponenter, største sammenhængende diffusionsgruppe dækker ca. 38.99% af levende træer (bemærk dette mål kan være stor selv når monodominans forekommer).

**Fejlkilder / ikke konkluder:**
- Der er kun otte holdout-seeds og tre korrelerede tidspunkter per forløb. Det er en intern numerisk pilot uden konfidensinterval eller test på nye klima-/geometrifamilier.
- At netværksmålene afhænger af *nuværende* artsmærkater gør dem stærkt kollineære med H og artsantal. En negativ mer-værdi betyder ikke at spektral information generelt er ubrugelig.
- Modellen har ikke direkte testet eigenværdier ved tid t mod fremtidigt H — kun tre billige grafmål. Tidligere `peter.spectral-pilot.cjs` diagonaliserede de aktuelle Laplace-matricer, men uden tidsforskudt prediktion.
- Hurtig evolutionær artsudryddelse uden ekstra nye arter (lav fødselsmutationsrate) kan dominere. Forudsigelser ved t=300 har ofte H=0 senere.
- MAE vs RMSE og penaliseringsstyrke er ikke optimeret med en separat validation split; parameter-scan og tidslag skal forudregistreres ved stærkere replikation.

### Minimal HTML-visning til forståelse (kun måling, ingen regelændringer)
`peter-dev/index.html` har nu et sammenklappeligt afsnit `Forskning · energinetværk og artsdiversitet` i eksisterende Forskningsområdet:
- andel levende same-species diffusionskanter ud af underliggende kanter,
- største sammenhængende live-energifællesskab som andel af levende træer,
- antal separate levende energifællesskaber,
- tidsserie af de første to mål, forklaring på deres betydning og tydelig advarsel om at kurverne **ikke** er en prædiktion.
Tidsserien samples ca. hver 20 sweeps, og de aktuelle tal opdateres på præcis aktuel sweep, når panelet er åbent. Energiregnskab, konkurrencemekanik og afkomsbet-hedging er uændrede.

**Forskningens videre prioritet:** Validér på større og andre geometrier; mål frosset spektralt gap for største live-komponent, varighed af energifelter og artsid-strukturer, kontroller for blot artstilhørsforhold ved ompermution af artslabels under fast populationstæthed. Overvej om netværk mere naturligt kan forudsige *energiudjævning/overlevelsesrisiko* end artsdiversitet, da Laplace-operatoren direkte bestemmer diffusionsdynamik, mens artstab også styres af angreb, vedligeholdelse og mutation.

**Kilder i bredere forskning:** Nyere oversigter om økologiske early warning signals fremhæver at faresignaler kræver uafhængig prædiktiv validering frem for efterfølgende korrelation, og at ikke alle kollaps har robuste varsler (f.eks. Boettiger 2013 DOI 10.1007/s12080-013-0192-6; oversigt 2026 DOI 10.3390/e28060628). Grafspektralt gap styrer diffusionens relaxationshastighed på en frosset sammenhængende graf; det er ikke automatisk et signal for evolutionært kollaps.
