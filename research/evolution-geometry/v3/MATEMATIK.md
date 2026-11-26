# Grundmodel V3 · Fra aktive akser til Lorentzisk variation

[Det fastlåste koncept](../GRUNDMODEL_V3.md) · [H1–H5](../HYPOTHESES.md)

## 1. Konstruktion og uafhængige data

Brug heltalskoordinater som labels. En aksial kant \((v,v+e_i)\) findes præcis, hvis begge hjørner tillader akse \(i\). For hver delmængde af akser testes alle hjørner og parallelle kanter i den tilsvarende kube. Behold desuden maksimale celler af lavere dimension. Det er nødvendigt for at opdage en linje hæftet til en flade. Algoritmen forudsætter et koordinatlattice og bygger ingen kuber ud fra knudernes dimensionstal alene.

I et rent rumligt kompleks af dimension \(n\) bruges én tidskant per tidsinterval og konstant maskemønster gennem hvert interval. Hver rumtidskube opdeles ved alle permutationer af tilgængelige aksetrin, en Freudenthal-triangulering. De kumulative hjørner af hver permutation danner en simplex. Begrænsningen af trianguleringen til en fælles flade er den samme fra begge sider. Det giver ét variabel-id for hvert uordnet kantpar. Rumlige aksialkanter kan initialiseres til fælles \(\ell_0\), mens diagonaler initialiseres fra valgt metrisk felt og aldrig bliver ekstra aksialkanter. Simplexgene kan også leveres direkte, som i kegletesten.

I en simplex med topdimension \(D=n+1\) er de uafhængige intervaller \(s_{ij}\) signerede andenpotenser. Referér til hjørne 0:
\[
G_{ab}=\tfrac12(s_{0a}+s_{0b}-s_{ab}),\quad
V_D=\sqrt{|\det G|}/D!.
\]
En ikke-degenereret Lorentz-simplex kræver netop én negativ egenværdi. Fælles kanter giver en fælles induceret Gram-metrik på alle delte facetter. Motoren kræver højst to topceller per facet og en sammenhængende sti/ring i hvert hinge-link. Det er nyttige lokale checks; vilkårlige input får ikke dermed certifikat for en global manifold.

## 2. Lorentzisk Regge-virkning

Sæt \(c=1\) og brug signaturen \((-+\cdots+)\). Et hinge har dimension \(D-2\). Ortogonalprojektion af de to resterende hjørnevektorer til normalplanet giver normerne \(a,b\) og prikprodukt \(d\). De findes med Schur-komplementet af hinge-Gram-blokken. Definér den ikke-nulle vinkel på den analytiske gren
\[
 \theta=-i\log\left(\frac{d+i\sqrt{ab-d^2}}{\sqrt a\sqrt b}\right),\qquad
 \delta_h=C_h-\sum_{\sigma\supset h}\theta_{\sigma h}.
\]
Her er \(C_h=2\pi\) i bulk og \(\pi\) på randen. For timelige hinges er normalplanet euklidisk, og \(\theta\in[0,\pi]\). For rumlige hinges er der en Lorentz-normalplan. Grenen følger positiv imaginær kvadratrod ved negativ norm. Realdele 0, \(\pi/2\), \(\pi\) tæller passager af nullretninger. Vi kræver nul realdel af bulkdefekten ved rumlige hinges. Det svarer til en regulær normal lysekegle. Input med null- eller degenererede Gram-blokke, null-wedge-stråler og uregelmæssige bulkhinges afvises.

Sæt \(B_h=V_h\) for rumlige og \(B_h=iV_h\) for timelige hinges. Virkningen på den valgte reelle Lorentz-gren er
\[
 A_g=\frac{1}{8\pi G_D}\left[
 \operatorname{Im}\sum_h B_h\delta_h-\Lambda\sum_\sigma V_D\right].
\]
Den reelle orienterede defekt, som rapporteres, er \(\operatorname{Re}\delta_h\) for timelige hinges og \(\operatorname{Im}\delta_h\) for rumlige. Randhinges tager det diskrete ydre vinkelled med. Randintervaller fikseres ved Dirichlet-variation. Randsystemer med ændret kausal gren ligger uden for den gennemførte implementering. Fortegnet er kontrolleret mod den negative gravitationelle kinetiske term i den flade FLRW-reduktion. [Regge](https://doi.org/10.1007/BF02733251) · [Sorkin, Lorentziske vinkler](https://arxiv.org/abs/1908.10022) · [Asante, Dittrich & Padua-Argüelles](https://arxiv.org/abs/2112.15387)

## 3. Skalarfeltet og den aksiale begrænsning

Det affine P1-felt har \(w_a=\phi_a-\phi_0\). På simplexen er gradienten konstant og dens norm \(w^TG^{-1}w\). Med knudekvadratur for potentialet:
\[
 A_\phi^\text{affin}=\sum_\sigma V_D\left[-\tfrac12 w^TG^{-1}w
 -\frac1{D+1}\sum_{v\in\sigma}V(\phi_v)\right].
\]
Dette er den præcise affine kinetiske term på en fuld Regge-metrik. Dens nodale operator kan koble hjørner over en geometrisk diagonal, når de rekonstruerede metriske krydsled er forskellige fra nul. Koden bruger den som særskilt continuumkontrol. Dens generelle stencil præsenteres ikke som V3's rene aksekobling.

Den aksiale variant bruger den samme fysiske simplex-volumen, men approksimerer det kontravariante kinetiske led i simplexens staircase-basis ved den diagonale metriks inverse. I den basis måles feltforskellene langs simplexens \(D\) **faktiske** aksial-/tidsben. Det giver
\[
 A_\phi^\mathrm{akse}=\sum_\sigma V_D\left[
 -\tfrac12\sum_{l\in\mathrm{stair}(\sigma)}
 \frac{(\phi_{l,+}-\phi_{l,-})^2}{s_l}
 -\frac1{D+1}\sum_{v\in\sigma}V(\phi_v)\right].
\]
På ortogonale gitre er kinetiske led identiske. Volumen afhænger fortsat af *alle* geometriske intervaller. Derfor kan geometri koble akserne, selv om den direkte feltoperator kun kobler faktiske ben. På stærkt ikke-ortogonal geometri er den anden form en fysisk diskretiseringsantagelse, og dens effektive feltkegle behøver ikke være den fulde metriks kegle. Motoren validerer ikke fuld Einstein–skalar-konvergens for vilkårlige ikke-ortogonale løsninger. Forsøgene sammenligner begge stencils under raffinement.

Her er potentialet et funktionspar \(V,V'\), således at masseløs, harmonisk, kvartisk og konstant del kan udskiftes. En konstant \(V_0\) er ækvivalent med \(\Lambda\mapsto\Lambda+8\pi G_DV_0\), hvilket testes numerisk. Den kan tælles enten som feltets konstante værdi eller som kosmologisk konstant.

## 4. Variationen og de resterende constraints

På et fast, regulært kausalt kammer siger Schläfli-identiteten \(\sum_{h\subset\sigma}B_h d\theta_{\sigma h}=0\). Derved kræves ingen numerisk differentiering af vinklerne til første variation:
\[
 \delta A_g=(8\pi G_D)^{-1}
 \left[\operatorname{Im}\sum_h\delta_h\, dB_h-\Lambda\sum_\sigma dV_D\right].
\]
\(dV_D=\tfrac12 V_D\operatorname{tr}(G^{-1}dG)\) med analog formel for hinge-volumen og \(dG\) lineær i \(ds_e\). I det affine feltled differentieres \(w^TG^{-1}w\) gennem \(dG^{-1}=-G^{-1}dGG^{-1}\). I det aksiale led giver \(d(\Delta\phi^2/s)\) et kantbidrag med fortegn \(-\Delta\phi^2 ds/s^2\). Gradienten ved en knude er summen af tilstødende signerede feltstrømme plus \(-V_D V'(\phi_v)/(D+1)\). Således er både stress og feltets tilbagekobling variationer af *samme* diskrete virkning.

Med Dirichlet-randdata kræves \(\partial A/\partial s_e=0\) for alle frie kanter og \(\partial A/\partial\phi_v=0\) for alle indre knuder. De timelige kantligninger er med i den generelle residual, heller ikke når de er næsten afhængige på flad baggrund. En lille reduceret residual i en ansats kan ikke i sig selv erstatte de uafhængige kantligninger. Tilsvarende giver vertex-translationer på flad baggrund nær-singulære Hessianer; en numerisk mindste-kvadraters stopkode er ikke en løsningsattest. [Dittrich & Höhn, kanonisk Regge og constraints](https://doi.org/10.1088/0264-9381/27/15/155001)

### Periodisk, homogen tidsdynamik

For en regulær kubisk rumlig periode initialiseres en hel flade med samme sidelængde \(a\). Næste flade har \(b\). Én Minkowski-frustum per kube kan indlejres lokalt med halvkoordinater \(\pm a/2,\pm b/2\) og ortogonal tidsafstand \(h\). På tværs af en tidsplade, med \(d\) ændrede rumlige hjørnetegn, er
\[
 s=-h^2+\tfrac14[(n-d)(b-a)^2+d(a+b)^2].
\]
På en rumlig side er \(s=d a^2\) eller \(d b^2\). Samme tal passer på nabokubens fælles flade. Hjørnets strut-egentid er \(\tau_{\rm strut}=\sqrt{h^2-n(b-a)^2/4}\). Den er forskellig fra den ortogonale separation \(h\). Den sidste er tiden, vi sammenligner med homogen FLRW.

Evaluér Regge og skalaren på trianguleret, rumligt periodisk frustum. Del med antal rumceller og kald resultatet \(L(q_j,q_{j+1},h_j)\), \(q=(a,\phi)\). Når to plader sys sammen, bliver deres to \(\pi\)-led et bulkled med \(2\pi\). Kædereglen fra de individuelle kantgradienter giver
\[
 D_2L_{j-1}+D_1L_j=0,\qquad \partial_{h_j}L_j=0.
\]
Den sidste er den reducerede lapse-constraint og er løst sammen med felt og skala på de accepterede plader. Startpladen bruger kanonisk feltimpuls \(-D_{1,\phi} L_0=\ell_0^n\dot\phi_0\) og lapse-constraint. Hele feltet har én værdi per tidsskive i denne løsning, og længder følger frustumformen. Den uafhængige kantmotor har flere frihedsgrader end denne ansats.

Ved \(a=b\) og \(h\) lille giver den aksiale feltvirkning den vanlige lokale endelige-difference KG-ligning. Med konstant metrisk gitter, forskydning nul og harmonisk potentiale opfylder den
\[
 \left[2\sin(\omega\Delta t/2)/\Delta t\right]^2
 =m^2+4\sum_k \sin^2(q_k\Delta x/2)/\Delta x^2.
\]
Computergitterets én-kant-afhængighed pr. trin er en stencilgrænse; den fysiske signalkegle kommer fra den rekonstruerede Lorentz-metrik. En given global nodetid kan testes via \(d t^TG^{-1}dt<0\) i hver simplex. Det er tilstrækkeligt til en stigende tid på fremadrettede kurver i det valgte kompleks, og det erstatter ikke en generel kontrol af numerisk feltpropagation. Vi tester konvergens af dispersionsloven og den præcise skyggeenergi for den lineære, stationære stencil.

## 5. Hvorfor blandet lokal topdimension endnu ikke er en V3-virkning

En kantmaske kan give en rumlig flade med en ekstra linje hæftet på et hjørne eller en kant. Opgaven ved en overgang er fysisk, ikke kun kombinatorisk:

1. **Måleproblemet.** En \(D\)-sektors EH-led integrerer en \(D\)-volumen, mens en lavere gren har nul mål i den høje volumen. Et ekstra lavdimensionelt led giver selvstændig dynamik, men kræver egne koblinger med forskellige enheder \([G_D]=L^{D-2}\). Der følger ingen relativ normalisering af en simpel liste over fælles akser.
2. **Junction-problemet.** Hinges er \(D-2\)-celler med et todimensionalt normalplan *inden for hver topdimension*. En overgang kan være randfacet på den ene side, en topcelle på den anden eller højere kodimension. Der findes ingen fælles mangelvinkel \(2\pi-\sum\theta\), der automatisk virker på tværs af disse tilfælde. Selv to ens-D manifolder med en tilslutningsspænding behøver induceret metrik og en passende junction-ligning.
3. **Variationsproblemet.** En sum af sektorspecifikke handlinger med tvungent fælles intervaller vil give en algebraisk sum af randmomenta, men selve identifikationen, vægte og eventuel overgangsvirkning er nye fysiske valg. For skalaren kan fælles spor og en fluxbalance udledes *efter* at sektormål og matchende spor er valgt. At bruge identiske aktive akser fastlægger tilladte forbindelser, ikke disse vægte eller gravitationelle randbetingelser.
4. **Lavdimensionel degeneration.** I \(D=2\) har punkt-hinges konstant volumen. Gravitationsleddet giver ingen bulkvariation for faste kausale/topologiske data. Ikke-triviel materiestress kan derfor ikke behandles som ordinær tovejs Einstein-gravitation i den rene 1+1-sektor.

En mulig særskilt kandidat er et stratificeret kompleks, hvor hver stratum har egen virkning og overgangsfladen får en specificeret induceret metrik, feltspor og junction-handling. For \(D_1\neq D_2\) skal man vise, at dens variation er veldefineret også ved forskellig kodimension, at flux og dimensionsenheder er konsistente, og at den reducerer til standard Regge, når \(D_1=D_2\). Det er ikke afledt fra den fastlåste konstruktion. Koden registrerer de faktiske maksimale dimensioner og afviser samlet fast-D variation på dette input. Ingen tvungen lavdimensionel omkostning eller ekstra kraftregel indføres.
