# Tidens pil, fluktuationskræfter og energiafhængig geometri

*Skovlaboratoriet · Opfølgning på de første 288 simulationer · 25. november 2026*

**Tre hovedfund.** Den fælles skovmotor har en målbar tidspil i reserveenergien langt efter opstart, i vinduer med tilnærmelsesvis stabile observerede fordelinger. Et separat klassisk felt giver en målbar Casimir-kraft mellem to bindinger, selv når feltets opdatering kun bruger naboer. En konservativ energiafhængig metrik bryder lineær superposition og ændrer to energipakkers profiler, mens det meste af et tilsyneladende centroidskift forsvinder i en større boks. Sammen giver forsøgene en måde at skelne en målt tidspil, en korrelation, en formændring og en fysisk kraft.

## A. Kan klokken aflæses efter opstart?

### Måling og stationaritet

Vi kørte fem betingelser på to gitterstørrelser med 16 seeds per betingelse og størrelse. To betingelser er de udgivne motorer med konstante klimakoefficienter. Tre Peterscenarier har højdeloft 8, højdeloft med nul diffusion, eller højdeloft med praktisk ubetalelig angrebs- og spredningspris. Spontan etablering og mutation er slået fra i batchen. Standard børnemutation er bevaret. Kørsel og opdeling bruger original motor fra `cb587788`. De første 1.600 sweeps for de to udgivne modeller og de første 1.000 for ablationerne indgår ikke i hovedtesten. Ændring i reserve, strukturenergi, pulje, levende andel og højde blev derefter vurderet over fire 200-sweep-vinduer. Vi krævede, at seed-bootstrapintervaller for forskelle hele tiden lå inden for de deklarerede margener, 0,28 energienheder per celle, 0,30 i højde og 0,025 i levende andel. Disse tal er en praktisk screening af udvalgte marginaler.

Et ord \(w=(x_1,\ldots,x_m)\) er \(m\) symboler fra den grovkornede reserve eller en anden skalarmåling. Vi beregner \(P_R(w)=P_F(w^{\mathrm{rev}})\) og tester
\[
D_m=\sum_w P_F(w)\ln\frac{P_F(w)}{P_R(w)}.
\]
Grænserne mellem symboler og de to ordmodeller læres kun fra træningsseeds. Med en halv pseudoobservation per ord evalueres \(\ln[\widehat P_F(w)/\widehat P_F(w^{\mathrm{rev}})]\) på uafhængige testseeds. Resultatet er en holdout-logscore for KL-målet. Den har endelig stikprøveusikkerhed og kan være negativ, selv om den eksakte KL-divergens er ikke-negativ. Intervaller bruger seed som replikationsenhed. Orienteringstesten vender hele testforløb og opregner alle fortegnskombinationer. Det bevarer den inden-for-seed autokorrelation under den reversible nulmodel. De mange udforskede observationsvalg gør en uafhængig replikation vigtig.

### Fællesudgaven består den uafhængige gentagelse

Vi genkørte 24 yderligere fulde simulationer med friske seeds til sweep 3.600 og aflæste hvert sweep fra 2.400. Træning og test brugte hver seks af de nye seeds per størrelse. Et ord med tre reserveobservationer ved et lag på ét sweep gav:

| Gitter | Kvartiler, nat per ord | Tertiler, nat per ord | Faste energigrænser 0,75, 1, 1,25 |
|---|---:|---:|---:|
| 10×10 | 1,032 [0,988–1,077] | 0,520 [0,492–0,546] | 0,075 [0,048–0,103] |
| 20×20 | 0,147 [0,127–0,162] | 0,089 [0,073–0,103] | −0,00013, interval omfatter nul |

Intervallerne er 95 % seed-bootstrap. Ved lag to og kvartiler forekom ordet 321, tre høje til lavere reserveklasser, i 4,36 % af ordene fremad og 0,61 % efter tidsvending på det lille testgitter. Det større gitter havde 2,27 % mod 1,11 %. Reservens middel ved 20×20 var 1,0340, 1,0364 og 1,0364 over tre sene vinduer. Standardafvigelserne var 0,0612, 0,0630 og 0,0630. På hvert seed lå gennemsnitlig Wasserstein-afstand til det første vindue under 0,01 ved 20×20 for de to senere vinduer, efter gennemsnit over seeds. Opstart, sampling hver anden sweep og et enkelt sæt binningsgrænser forklarer derfor ikke hele signalet. Fast binning på 20×20 taber det. Resultatet vedrører den observerede proces på de afprøvede sene tidshorisonter. Langsomme skjulte variable kan stadig ændre fuldtilstandens fordeling.

Vi instrumenterede 3.200 sene sweeps på 10×10 uden at ændre dynamikken. Per gittercelle og sweep flyttede optag i gennemsnit 0,323 fra \(Q\) til reserve. Vedligehold og død flyttede 0,321 tilbage til \(Q\), heraf omkring 0,041 fra struktur. Konkurrencetrinnet skabte netto 0,041 i struktur, og diffusion flyttede samlet reserve med afrundingsnul. Der er altså en vedvarende rettet cyklus gennem de bogførte beholdninger, selv om deres middelværdier stort set står stille. Et afsluttet sweep har en fast intern rækkefølge. Død sletter information, struktur bygges ved enrettet vækst, og artsregistret vokser ved mutation. Disse regler har almindeligvis andre eller ingen umiddelbare inverse overgange. Størrelsen af hver regels isolerede bidrag til fællesudgavens observerede KL er endnu ikke bestemt. I Peters variant overlevede et talmæssigt KL-signal ved \(\alpha=0\), men i et problematisk regime beskrevet nedenfor.

### Peters sene signal fejler en fysisk kontrol

Ved 20×20 passerede flere Peter-scenarier de valgte driftsmargener og gav høj holdout-score. En ekstra måling viste, at praktisk taget alle registrerede levende steder sent i højdeloftsforsøget havde højde under \(10^{-8}\). For otte seeds på hvert gitter var middelhøjden over de sidste målte vinduer omkring \(5\times10^{-197}\) ved 10×10 og \(7\times10^{-186}\) ved 20×20. Spredning halverer både moderens og afkommets højde, mens \(\ln(1+h)\) i standardens vedligeholdelsesudtryk afrunder til nul ved meget små højder. Eksakt aritmetik ville også give aftagende vedligehold ved \(h\to0\); afrundingen forstærker problemet. Både en tærskel på \(10^{-12}\) og \(10^{-8}\), hvor energien returneres til puljen ved fjernelse, gav tomme gitre i de sidste vinduer. Kontrollen er en modelændring, og dens vigtigste resultat er følsomheden. Den oprindelige Peter-score er derfor svag evidens for en tidspil i en fysisk meningsfuld stationær skov. Under dyr kamp og spredning drev flere makrostørrelser stadig.

### Roldán og Parrondo og en særskilt fluktuationstest

Vi byggede en seks-tilstands flashing ratchet med tre positioner og et tændt/slukket potentiale. Nabohop har forholdet \(k_{ij}/k_{ji}=\exp[(V_i-V_j+f\Delta x)/(k_BT)]\). Vi målte stationær fordeling og fuld stientropi samt tegnsekvenser, når feltets tilstand er skjult. Ved den kraft, hvor positionsstrømmen er nul til numerisk præcision, er den fulde eksakte KL-rate stadig **0,02529 nat per trin**. Holdout for to fuldt observerede tilstande gav **0,02487** [0,02419–0,02576]. Med kun position er eksakt \(D_2\) nul ved stalling, mens eksakt \(D_8\) er \(1,10\times10^{-4}\) nat per ord. Den lille positionsasymmetri blev fundet ved eksakt optælling af ord. De korte positionssekvenser alene gav ikke statistisk sikker måling af stallsignalet. Den reversible kontrol gav eksakt nul. Det reproducerer mekanismen, hvor skjulte tilstande undertrykker lavordenssignalet, og højere ord kan afsløre dissipation uden netto observeret strøm. Den diskrete uniformisering og parametrene er vores referencevalg. [Roldán & Parrondo 2010](https://doi.org/10.1103/PhysRevLett.105.150607) · [Roldán & Parrondo 2012](https://doi.org/10.1103/PhysRevE.85.031129)

For en anden ringproces med sandsynligheder \(p,q\) for højre/venstre er \(S=J\ln(p/q)\). Eksakt konvolution bekræftede både \(P(S)/P(-S)=e^S\) og \(\langle e^{-S}\rangle=1\). Ved \(p=0,55\), \(q=0,15\) og 160 trin var \(P(J<0)=1,96\times10^{-11}\). Medianen af 16 Monte Carlo-estimater med 20.000 baner endte på \(2,93\times10^{-19}\) for et gennemsnit, der eksakt er 1. Det er en direkte illustration af, hvorfor eksponentialestimater kan lyve overbevisende ved utilstrækkelig sampling. Fysisk entropiproduktion i træmotoren kræver stadig et termodynamisk mål og en understøttet reverse-protokol. [Lebowitz & Spohn](https://doi.org/10.1023/A:1004589714161) · [Seifert](https://doi.org/10.1103/PhysRevLett.95.040602)

## B. Kan lokale fluktuationer give en kraft?

### To energitoppe, uden pulje og uden empirisk kraft

I en periodisk KMP-kæde udveksler kun et tilfældigt nabopar energi. Med samme tilfældige kant og samme delingsfraktion er hvert enkelt trin en lineær operator i energierne. Vi kørte 768 parrede realisationer per afstand og størrelse, fra flad profil, to separate hotspots og begge samlet. Selv om de enkelte felter fluktuerer kraftigt, fulgte de superposition i hver realisation med maksimal fejl \(1,25\times10^{-14}\). Den ene pakke kan varme det område op, hvor den anden startede, men de ændrer ikke hinandens transportkoefficienter. Her er en rumlig respons uden en særskilt parinteraktion.

Et ekstra tjek viste, at et lokalt system kan have afstandsuafhængige korrelationer blot ved valg af ensemble. Den kanoniske kontrol har uafhængige eksponentialenergier. Ved fast totalsum er en ensartet fordeling af fraktionerne, Dirichlet med alle parametre 1, invariant for KMP. Med middelenergi 1 er \(\operatorname{Cov}(E_i,E_j)=-1/(N+1)\) for enhver forskellig plads. På \(N=32\) ved afstand 16 måltes −0,0288 mod −0,0303. Globalt fastholdt totalenergi giver således en langtrækkende statistisk binding uden en lokal fjernvirkningsregel eller en kraft.

### En målbar, fluktuationsinduceret kraft fra en lokal Hamiltonian

Sæt \(k_BT=1\). Et klassisk felt med \(K=m^2I+\mathsf L\) har kinetisk irrelevant Gibbs-vægt \(\exp[-\phi^TK\phi/2]\). To lokale, kvadratiske bindinger med styrke \(k\) dæmper feltet ved pladserne 0 og \(r\). Efter at have trukket enkeltbindingernes frie energi fra er
\[
F_{\mathrm{int}}(r)=\frac12\ln\left[1-
\left(\frac{G(r)}{k^{-1}+G(0)}\right)^2\right],\qquad G=K^{-1}.
\]
På gitteret er kraften ved en flytning udad givet ved \(F_{\mathrm{int}}(r)-F_{\mathrm{int}}(r+1)\). Dette er respons på en mekanisk kontrolkoordinat. Feltets kvadratiske lokale observabel \(\phi_i^2/2\) har derimod kovarians \(G(r)^2/2\), som kan være positiv også med bindingsstyrke nul og kraft nul.

Vi beregnede den eksakte endelige torus i 1D, 2D og 3D med tre feltmasser og tre gitterstørrelser. Vi kontrollerede kraften både gennem Gaussiske prøver og med **lokale termiske Gibbs-opdateringer**, hvor hver feltværdi kun ser sine naboer. For 2D, \(L=20,m=0,3,k=1,r=4\) gav den lokale simulering **−0,000443** [−0,000695; −0,000191] i \(k_BT\) per gitterenhed mod eksakt **−0,000343**. Monte Carlo-intervaller her bruger 32 uafhængige kæder. For 64 i sidelængde, \(m=0,12\), \(k=1\), \(r=4\), gav den direkte feltprøve henholdsvis −0,03235, −0,001570 og −0,000018 i 1D, 2D og 3D. Ved afstand 8 var signalet i 3D for lille til sikker Monte Carlo-detektion. Større feltmasse dæmper den rumlige Green-funktion og korter rækkevidden af. Geometrien, ikke den historiske skovpulje, bestemmer feltets rækkevidde.

Bindingerne er eksplicit koblet til feltet. Der er intet direkte led mellem deres positioner i energien. Kraften kommer fra ændringen af feltets tilgængelige fluktuationer og blev målt med en frienergiforskel. Det er en klassisk termisk Casimir-analog. Der er ingen kvantevakuumenergi i forsøget. Glatte selvgående trætoppe i de eksisterende regler har ingen tilsvarende bevægelig probe eller Gibbs-mål. [Dean & Gopinathan](https://doi.org/10.1103/PhysRevE.81.041126)

## C. Når energien ændrer geometrien

Vælg en lokal konform 2D-metrik \(g_{ab}=A(u)\delta_{ab}\), \(A=1+\beta u\), hvor \(u\) er energi per referenceareal. Der er ingen global normalisering af arealet. I to dimensioner er \(\sqrt{g}g^{ab}=\delta^{ab}\), så en konservativ fluxdiskretisering svarer til
\[
 \partial_t u=\Delta f(u),\qquad f(u)=\frac{u}{1+\beta u}.
\]
Her er \(f\) energitætheden per fysisk areal. På gitteret føres lige meget ud af den ene celle og ind i naboen. I 1D brugte vi samme fluxlov som en kontrol af dimensionseffekten. Den er dér en transportanalog og bruger ikke den 2D-konforme identitet.

Ved \(\beta=0\) var parresidualen \(u_{AB}-u_A-u_B+u_0\) afrundingsnul. Ved \(\beta=4\), afstand 6 og tid 4 var dens relative \(L^2\)-norm **1,205 %** på 96×96. Den blev **1,2048 %** med mindre trin og **1,208 %** med 128×128. Ved tid 32 var den **9,07 %** i den normale boks og **9,36 %** i en boks med dobbelt sidelængde ved samme cellebredde. Øget afstand reducerede signalet ved samme tid. Energiens total var bevaret inden for \(10^{-9}\).

En tilsyneladende bevægelse af den anden top mod den første var afhængig af, hvordan position måles. Ved tid 32 blev et lineært første moment på den lille torus forskudt −0,228. I den dobbelt så brede boks blev samme mål kun −0,00286. Et cirkulært moment gav fortsat en større forskydning, fordi det er følsomt for formændringer. Det lokale overskud på siden mod den anden top bestod derimod boksforstørrelsen. På en stor flade med aftagende perturbation følger \(d\int x u\,dx/dt=\int x\Delta f(u)\,dx=0\) efter integration ved dele. Det forklarer forskellen mellem asymmetrisk omfordeling og transport af en pakkes samlede første moment.

\(f'(u)>0\) giver et maksimumsprincip. Desuden gælder
\[
\frac{d}{dt}\int\tfrac12 u^2\,dx=-\int f'(u)|\nabla u|^2\,dx\leq0.
\]
Et stationært felt i en forbundet periodisk boks må være uniformt. Den høje top kan derfor holde sig markant længere end ved lineær diffusion, men den viste koblingslov kan hverken understøtte en permanent isoleret koncentration eller give en kraftlov mellem frie partikler. En kobling, som gør \(f'<0\), ville allerede have baglæns diffusion i den lokale linearisering. Det ville give vækst, der bliver hurtigere ved gitterforfinelse, og er derfor en dårlig positiv kontrol for fysisk selvlokalisering.

Som reference integrerede vi også \(\partial_t u=\Delta(u^2)\) fra en kompakt Barenblatt-profil. Den har radius proportional med \(t^{1/(d+2)}\). Forfining fra \(L=64\) til 192 reducerede profilfejlen ved samme sluttid fra **0,183 % til 0,043 %** i 1D og fra **0,603 % til 0,051 %** i 2D. Den validerer solverens behandling af en kendt ikke-lineær transportlov. Barenblatt-pakken breder sig langsomt med kompakt støtte. Det er en anden PDE end vores metrikfeedback. [Lee & Vázquez](https://doi.org/10.1512/iumj.2003.52.2200)

## D. En makroskopisk pil med reversibel mikrodynamik

I en lokal harmonisk kæde udviklede vi en kompakt pakke med en symmetrisk velocity-Verlet-opdatering. Opdateringen har en eksakt diskret afhængighedskegle på højst én nabo per trin. Kompakt støtte blev kontrolleret numerisk under fremadforløbet. Efter 18 tidsenheder var pakkens rumlige energientropi steget omkring **0,712 nat** i eksempelkørslen. Vend alle hastigheder, og løsningen følger præcis den modsatte vej: den oprindelige pakke vender tilbage med relativ feltfejl under \(8,3\times10^{-15}\) i alle 48 kørsler. Den korrigerede kvadratiske diskrete energi holdt sig inden for \(4,6\times10^{-15}\) relativt. Det konservative bølgesystem viser, hvordan asymmetrisk makroskopisk forberedelse kan give en observerbar pil under en reversibel regel. Keglen her er virkningen af et lokalt opdateringsskema. Der er ingen dynamisk horisont eller relativistisk geometri.

## Fysisk prioritering

| Fund | Fysisk betydning og overraskelse | Matematik og numerisk evidens | Forbindelse til Oskars idé, videre arbejde og visualisering |
|---|---|---|---|
| **1. Feltfluktuationer giver en kraft** | En kraft mellem objekter kan opstå ved at ændre feltets fluktuationer. | Frienergi fra en determinant og uafhængig lokal Monte Carlo. Stor evidens for den specifikke klassiske model. | Lokal udveksling er fælles idé. Felt og flytbart objekt er nye fysiske variable. Afstand og dimension kan ændres i laboratoriet. |
| **2. Stationær tidspil med nul strøm** | Fravær af synlig netto transport er utilstrækkeligt til at slutte ligevægt. | Eksakt stisandsynlighed og holdout med fuld tilstand. Svagt positionssignal ved korte ord. | Relevant metode for skjulte energifaser. En god næste prøve er at måle sekvenser af lokale energistrømme. |
| **3. Sen tidspil i fællesudgaven** | Genkendelig tidspil efter opstart i de observerede marginaler. | To seedfamilier, flere binninger, målt energicyklus. Høj evidens for den observerede asymmetri. Fuld stationaritet er åben. | Direkte fra skovmotoren. Den bedste bro mellem oprindelig model og stokastisk termodynamik. Ordsandsynligheder ses i HTML. |
| **4. Tidsvending af en spredt bølge** | En makroskopisk pil kan forsvinde, når de mikroskopiske hastigheder vendes. | Eksakt diskret symmetri og genopbygning ved maskinpræcision. | Separat lokal bølgemodel. Egnet til visuelt at forklare kausalitet, initialbetingelser og reversibilitet. |
| **5. Geometri ændrer energiens vekselvirkning** | En konservativ regel kan skabe asymmetrisk respons uden en parvis tiltrækningslov. | Konvergent superpositionsbrud. Faldende maksimum og et første-moment-tjek udelukker flere stærke fortolkninger. | Tættest på den oprindelige diffusionsligning. En bedre næste variant har et selvstændigt dynamisk geometrifelt med sit eget energiregnskab. |

Ud over den observerede tidspil i fællesudgaven er de robuste fysiske reproduktioner specifikke for deres referenceprocesser. Under de testede skovregler kan vi endnu ikke tilskrive en målt kraft, en gravitationel lov, en relativistisk horisont eller en kvanteeffekt til træernes energi. Den mest oplagte næste hypotese er, at en **lokal, reversibel energimodel med bevægelige sonder** kan bevare Oskars energiregnskab og samtidig bære en målbar, fluktuationsinduceret kraft. Den klassiske feltmodel giver allerede en kvantitativ reference, som sådan en variant kan falsificeres imod.
