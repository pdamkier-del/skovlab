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
