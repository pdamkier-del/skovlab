# Matematiske noter til en uafhængig udledning

## Ét bit, to beholdninger

I den lokale model skifter \(Q_i\to E_i\) med rate \(a_i\) og \(E_i\to Q_i\) med rate \(b\). En åben kant flytter \(D(E_j-E_i)\) ind i \(i\) og det modsatte i \(j\). Det identificerer en eksakt bevaret sum \(\sum_i(E_i+Q_i)\) både for den infinitesimale model og hvert deltrin i koden. Alle genotyper kan kopieres mellem samme faste naboceller. Arveanlægget ændrer kun kanttilladelsen. Afkom arver en bit, og mutation kan vende den.

**To-plads-udledning.** I en stabil komponent med \(D>0\) er \(E_i=E_*\), og \(Q_i=(b/a_i)E_*\). For to pladser med hver starttotal \(T\) er \(E_*=2T/(2+b/a_1+b/a_2)\). Isoleret er \(E_i=a_iT/(a_i+b)\). Den fælles reserve er det harmoniske middel af de to isolerede reserver. Den ligger mellem dem, så den varme plads taber reserve og den kolde vinder. Beviset bruger forsyningssatsen og ikke grafkurvatur. I det fulde gitter kan selektion og rumlig sammensætning afgøre, hvem der bærer tabet ved en åben kanal.

**Skalainvarians.** Alle energitrin er lineære ved en fast genotypetilstand. Sæt \((E,Q)\mapsto \lambda(E,Q)\) og \(\beta\mapsto\beta/\lambda\), hvor kopiering bruger \(p=0,24\,\sigma[\beta(E_j-E_i)]\) og \(\sigma(z)=(1+e^{-z})^{-1}\). Derfor er sandsynligheden identisk. Induktion på sweeps med fælles tilfældige tal holder genotyper og den reskalerede energihistorie identiske. Konstant \(\beta T\) og samme initialfraktioner er den relevante kontrol. En energitærskel, fast absolut fødselsomkostning eller en ikke-lineær transportlov kunne bryde ækvivalensen.

**Transportoperator.** På en periodisk graf med enhedsrate per åben kant findes den effektive diffusionskoefficient ved en korrektorfunktion \(\chi\). For hvert orienteret kantbidrag er forskydningen \(\delta_{ij}+\chi_j-\chi_i\), hvor \(\delta_{ij}\) følger kanten også over periodisk rand. Med én gauge pr. komponent løses \(L\chi_i=\sum_j\delta_{ij}\). Derefter
\[
D_\mathrm{eff}=\frac{1}{|V|}\sum_{\{i,j\}}(\delta_{ij}+\chi_j-\chi_i)
(\delta_{ij}+\chi_j-\chi_i)^\mathsf T.
\]
Her vægtes komponenterne med deres volumen. Det er et minimumsproblem for et kvadratisk udtryk. Det tillader en uafhængig afledning af \(D_x\leq\text{andel åbne x-kanter}\), \(D_y=1\) i én-bit-modellen og \(D_x=0\), når en åbnet komponent slet ingen cykel med x-vinding rummer. Skil dette mål fra hældningen af retursandsynlighed og fra den rumlige dimension af substratet. [Kipnis & Varadhan, additivfunktionaler af reversible Markov-processer](https://doi.org/10.1007/BF00318348)

## Skift krumning uden at skifte grad

Et modul har 16 celler. Begge genotyper har 24 indre energikanter og grad tre. Reserver føres via genotypegrafens Laplacian \(L_g\), mens lokalbeholdninger føres via samme ring \(L_R\) for begge genotyper. Donor og modtager indgår gennem diagonale rater \(A=\mathrm{diag}(a)\), \(B=\mathrm{diag}(b)\):
\[
\begin{pmatrix}\dot E\\\dot Q\end{pmatrix}=
\begin{pmatrix}-D_E L_g-B&A\\B&-D_Q L_R-A\end{pmatrix}
\begin{pmatrix}E\\Q\end{pmatrix}.
\]
Søjlesummer nul og ikke-negative off-diagonaler giver konservativ, positiv dynamik. Sammenhæng og positive udvekslingsrater giver en entydig stationær tilstand ved fast total, svarende til den positive invariantfordeling for en endelig irreducibel Markov-proces. Modulernes arveanlæg ændrer grafen, mens intet trin flytter energi fra ét modul til et andet. En nabo kan overføre sit arveanlæg lokalt, men lader energien i modtagerens eksisterende beholdninger blive i modulet.

Beregn de to positive nulvektorer med samme normering. Deres reserve ved modtageren er den mulige fitnessforklaring. Ved homogen pumpe og vedligehold giver symmetriske, forbundne Laplacianer et homogent felt og ingen routingfordel. Ved heterogenitet kan det modtagne energiniveau afhænge af lokale stier, selv ved samme grad, kantantal og energisum. Kontrast af to grafer holder ikke alle andre netværksmål faste. Derfor kan et fortegn vinde evolutionært, uden at forsøgene alene udpeger kurvaturen som den årsagsmæssige variabel.

## Hvorfor antal kan skjule tidens pil præcist

I den firemoduls Markov-model kan kun én bit ændre sig i hvert spring. Mutationsraten er positiv i alle flipperetninger. Den stationære trafik er \(J_{xy}=\pi_x P_{xy}\). Fuld stiinformation for et enkelt spring måles ved \(\sum_{xy}J_{xy}\ln(J_{xy}/J_{yx})\). Om et net er reversibelt kan testes ved at sammenligne produktet af overgangssandsynligheder mod uret og med uret i en lukket cyklus. En sådan cyklus består her af at flippe bit \(i\), derpå \(j\), derpå \(i\) og \(j\) igen.

Observer alene antallet \(N\) af ét-bits. En observeret overgang går fra \(k\) til \(k+1\), \(k-1\) eller samme k. Stationaritet kræver lige meget samlet trafik over hvert snit \(\{N\le k\}\). Kun overgangen \(k\leftrightarrow k+1\) krydser det snit. Derfor er sandsynligheden af fremadrettede og vendte **to-symbolsord** præcis ens, selv når den fulde kæde har strømme. Dokumentér dernæst hvorfor projektionen generelt ikke er Markovsk, og beregn længere ord ved at multiplicere overgangsmatricen mellem diagonale observationsprojektorer. [Roldán & Parrondo](https://doi.org/10.1103/PhysRevE.85.031129)

## H5 · Brug ure til at gøre en metrik falsificerbar

På en statisk graf med kantlængde \(\ell_{ij}\) og positiv lapse \(N_{ij}\) er en foreskrevet optisk signaltid \(\ell_{ij}/(cN_{ij})\). Begge størrelser kan ganges med samme positive faktor uden ændring af signaltid. En måling af signaltid kan derfor kun identificere deres forhold. Lokal tid \(d\tau=N_i\,dt\) kræver et uafhængigt ur. Hvis valgte oscillatorer er ure, skal deres frekvensændringer kunne beskrives af en fælles lapse. Et separat, lokalt hyperbolsk signal skal derefter have fælles \(c\) efter kalibrering i de samme lokale måleenheder. Det samme gælder to uafhængige prober. Diffusionshastighed og de lokale energibeholderes relaxation er ikke i sig selv sådan en urtest. Den [tidligere optiske beregning](../RAPPORT.md#h5--en-fælles-optisk-metrik-er-mulig-men-signaltid-bestemmer-ikke-egentid-alene) giver et reproducerbart eksempel på tvetydigheden, og [bølgestudiet](../../fundamental-physics/matter/README.md) viser den finite gittergrænse. [Unruh](https://doi.org/10.1103/PhysRevLett.46.1351)
