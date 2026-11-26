# Einstein–Klein–Gordon ved vilkårlig fast dimension

Brug \(D=n+1\), \(c=\hbar=1\), signatur \((-+\dots+)\), \(\kappa_D=8\pi G_D\) og \(\Lambda=0\). Start med den uændrede [Grundmodel V2](../GRUNDMODEL_V2.md). Ved Dirichlet-metrikdata på en ikke-null rand tilføjes det sædvanlige Gibbons–Hawking–York-led. Alternativt kan variationerne have kompakt støtte, så randleddene bortfalder.

## Variation, kausalitet og energiregnskab

Variation i \(\phi\), efter integration ved dele, giver \(\Box_g\phi-m^2\phi=0\). Ved metrisk variation anvendes \(\delta\sqrt{-g}=-\sqrt{-g}\,g_{\mu\nu}\delta g^{\mu\nu}/2\). Resultatet er
\[
 G_{\mu\nu}=\kappa_D T_{\mu\nu},\quad
 T_{\mu\nu}=\partial_\mu\phi\partial_\nu\phi-
 \tfrac12g_{\mu\nu}\big[(\partial\phi)^2+m^2\phi^2\big].
\]
Det harmoniske potentiale og gravitation er begge fastholdt. For \(D>2\) giver sporet de nyttige identiteter
\[
 R=\kappa_D[(\partial\phi)^2+\tfrac{D}{D-2}m^2\phi^2],\qquad
 R_{\mu\nu}=\kappa_D[\partial_\mu\phi\partial_\nu\phi+
 \tfrac{m^2\phi^2}{D-2}g_{\mu\nu}].
\]
\(\nabla_\mu T^{\mu\nu}=(\Box_g\phi-m^2\phi)\nabla^\nu\phi\) viser lokal bevarelse. Den forudsiger ikke en almindelig bevaret integralenergi på en vilkårlig foliering. En timelig Killing-vektor \(\xi\) giver \(\nabla_\mu(T^{\mu\nu}\xi_\nu)=0\), og den tilsvarende ladning bevares ved passende randflux. I asymptotisk flad gravitation kan en total ADM-energi defineres med de relevante asymptotiske betingelser. Energi inden for en endelig boks kan ændres af flux og af den valgte observatør.

Den karakteristiske kegle følger \(g^{\mu\nu}k_\mu k_\nu=0\); massen ændrer bølgepakker og deres gruppehastighed, mens fronten har lokal hastighed \(c\). Egentiden er \(d\tau^2=-g_{\mu\nu}dx^\mu dx^\nu/c^2\) langs timelige baner. I FLRW med lapse 1 måler et medfølgende ur \(t\); radiale nullstråler går med \(d\chi/dt=1/a\) i radial geodætisk koordinat. Et lokalt henfald eller faseudsving alene måler ikke \(d\tau\).

På en rumlig skive er Hamilton-constrainten \({}^{(n)}R+K^2-K_{ij}K^{ij}=2\kappa_D\rho\). Med \(K_{ij}=-\mathcal L_n h_{ij}/2\) og \(j_i=-h_i{}^\mu T_{\mu\nu}n^\nu\) er momentum-constrainten \(D_j(K^j{}_i-\delta^j{}_i K)=\kappa_D j_i\). Den homogene sektor har \(j_i=0\); et generelt inhomogent gitter kræver begge constraints og gauge-kontroller.

## Lave dimensioner og enhedsvalg

- **\(n=1\).** Einstein-tensoren er identisk nul i 2D rumtid. Standard Einstein–Hilbert-leddet har ingen bulk-metrikdynamik. For en ikke-negativ harmonisk energi tvinger \(T_{\mu\nu}=0\) et regulært reelt massivt felt til vakuum. Den frie KG-kontrol i 1+1 har en foreskrevet Minkowski-metrik. Dilatongravitation ville være en ændret virkning.
- **\(n=2\).** 2+1-Einstein kan have materiekrumning, men ingen lokale vakuumgravitoner. Et statisk, trykløst objekt kan give en global konisk geometri; den sædvanlige lineære Newton-tiltrækning fra hvileenergi forsvinder. For en langsom, trykløs kilde giver sporligningen \(R_{00}\simeq\kappa_D\rho(n-2)/(n-1)\). Dette er ikke en generel nulkrumningspåstand for et oscillerende felt. En 2D-logaritmisk Poisson-kraft med uafhængig kobling er en anden model.
- I enhederne ovenfor har \(G_D\) enhed \(L^{n-1}\), \(\phi\) enhed \(L^{-(n-1)/2}\) og \(\rho\) enhed \(L^{-(n+1)}\). Relevante sammenligninger bruger fx \(G_Dm^{n-1}\), \(mR\), \(\chi=\kappa_D\rho/m^2\) og \(\mathcal C\sim G_D M/R^{n-2}\) for \(n>2\), med den n-afhængige sfæreflade i en præcis massedefinition. Samme numeriske værdi af en dimensionfuld \(G_D\) på tværs af n er ingen fysisk normalisering.

## Eksakt homogen EKG og stort n

For \(n\ge 2\), \(\rho=(\dot\phi^2+m^2\phi^2)/2\), \(p=(\dot\phi^2-m^2\phi^2)/2\) og \(H=\dot a/a\) gælder
\[
 \tfrac12n(n-1)(H^2+k/a^2)=\kappa_D\rho,\quad
 \dot H=k/a^2-\tfrac{\kappa_D}{n-1}\dot\phi^2,\quad
 \ddot\phi+nH\dot\phi+m^2\phi=0.
\]
\(\dot\rho=-nH(\rho+p)\), eller \(d(\rho a^n)=-p\,d(a^n)\). Ved \(nH/m\ll1\) giver periodegennemsnit \(\langle p\rangle\simeq0\), \(\rho\propto a^{-n}\) og flad \(a\propto t^{2/n}\). Ved flad, fast \(\chi\) er \(nH/m=\sqrt{2\chi n/(n-1)}\), så \(H/m\sim\sqrt{2\chi}/n\) og lokalfeltets friktion \(nH/m\) forbliver endelig. Ved fast \(H/m\) skalerer starttætheden i stedet som \(n(n-1)\). \(1/n\) er derfor en veldefineret baggrundslov under den første restriktion. Den giver ingen evolutionær præference. [Turner](https://doi.org/10.1103/PhysRevD.28.1243)

På \(\mathbb R^2\times S^1\) i Bianchi I med homogen isotrop spænding, \(H_i=H+\sigma_i\), \(\sum_i\sigma_i=0\), gælder \(\dot\sigma_i=-3H\sigma_i\) og \(3H^2=\kappa\rho+\frac12\sum_i\sigma_i^2\). Cirklen har fysisk radius \(R(t)\). Ved frossen skive har dens spektrum \(j^2/R^2\), så \(d_s(u)=2+2u\langle j^2/R^2\rangle_u\). For \(u\ll R^2\) ser proben tre rumlige dimensioner, ved \(u\gg R^2\) to. Radiusændring er dynamisk løsning; kompakttopologien er på forhånd valgt. Selv på samme skive kan to prober nå forskellige resultater ved forskellig opløsning.

## Binding ved svagt felt: to forskellige kritiske dimensioner

I svagt, langsomt felt, \(|\Phi|\ll1\), \(|\partial_t\psi|\ll m|\psi|\), \(|\nabla\psi|\ll m|\psi|\), brug \(\phi=(\psi e^{-imt}+\psi^*e^{imt})/\sqrt{2m}\). Periodegennemsnit giver \(\rho\simeq m|\psi|^2\),
\[
 i\partial_t\psi=-\Delta\psi/(2m)+m\Phi\psi,\quad
 \Delta\Phi=\kappa_D\tfrac{n-2}{n-1}m|\psi|^2,\quad n>2.
\]
De hurtige harmoniske komponenter, relativistisk stråling og dynamisk gravitation er uden for denne ledende orden. Aproksimationen bruger en elliptisk potentialeligning. Den er derfor uegnet til at teste fundamentale rejsetider eller superluminale signaler. Efter reskalering til \(i\dot u=-\Delta u/2+Uu\), \(\Delta U=|u|^2\), sammenlignes dimensionerne først som matematiske modeller med samme definerede balance mellem spredning og binding. Den valgte radiale normering \(u(0)=1\) er ikke en sammenligning af samme fysiske kompakthed.

Med bevaret \(M=\int |u|^2\), \(T=\int |\nabla u|^2/2\) og \(W=\int U|u|^2/2<0\), giver \(u_R(x)=R^{-n/2}u(x/R)\) energien
\[
 E(R)=T R^{-2}+W R^{-(n-2)}.
\]
Stationaritet kræver \(2T+(n-2)W=0\). Så er \(E''(1)=2(4-n)T\). For \(n=3\) er dette en positiv skalastivhed; ved fire er den neutral og alle skalamedlemmer har samme norm. Over fire er der en energisænkende sammentrækning eller udvidelse ved fast norm. Dette er en variational skalatest, ikke en generel nonlineær stabilitetssætning. Ved fri tidsudvikling kan man som ekstra kontrol udlede \(I''=4T+2(n-2)W\), \(I=\int r^2|u|^2\), under passende forfald.

For egenløsningen \(u(t,x)=e^{-i\mu t}f(x)\) giver multiplikation med \(f\) en anden identitet, \(\mu M=T+2W=(n-6)T/(n-2)\). En stationær, aftagende profil med \(\mu<0\) kan således kun høre til \(n<6\), under identiteternes finite-energi/randantagelser. Ved \(n=6\) findes en eksplicit tærskelprofil
\[
 f(r)=\frac{12\sqrt2}{(1+r^2)^2},\qquad U=-f/\sqrt2,
 \qquad \mu=0.
\]
Den har endelig norm og algebraisk hale. Indsæt i \(\Delta f=-2f^2/\sqrt2\) for at tjekke begge ligninger. Den er en tærskel, ikke en stabil eksponentielt lokaliseret pakke. [Fodor, Forgács & Mezei](https://doi.org/10.1103/PhysRevD.81.064029)

En Gaussisk breddeansats med kvadratisk fase giver den enklere, dimensionløse bredde-ODE \(\ddot R=R^{-3}-qR^{1-n}\) med \(q=(n-2)|W(1)|/(2T(1))\). Lineariser ved \(q=1,R=1\): \(\delta\ddot R=(n-4)\delta R\). Ved stort n, \(R=1+x/n\), bliver \(R^{1-n}\to e^{-x}\). Breddemodellen viser et \(1/n\)-grænselag, som følger af gravitationens r-afhængighed. Det siger intet om stabilitet af fuld relativistisk dynamik ved stort n. Den fulde radiale Schrödinger–Poisson-integration i denne forskningsmappe bruger ingen Gaussisk breddeansats.
