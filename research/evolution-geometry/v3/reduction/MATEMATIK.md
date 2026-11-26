# Produktreduktion og den ekstra Einstein-ligning

Brug signatur ((-+cdots+)), (c=1), (kappa=8pi G_{D+1}). (D) tæller rumtid. Lad (y) have periode 1 og antag en ortogonal, uvriddet cirkelfiber med nulmoder for metrik og reelt skalarfelt. (L(x)>0) er omkredsen.

```text
ds² = gμν dxμ dxν + L(x)² dy²
R_high = R − 2 □L/L,   √|g_high| = L√|g|
X = gμν ∂μΦ ∂νΦ
```

Christoffelsymbolerne ud over dem for g er (Gamma^y_{mu y}=partial_muln L) og (Gamma^mu_{yy}=-L
abla^mu L). De giver (R_{mu
u}^{high}=R_{mu
u}-
abla_mu
abla_
u L/L) og (R^{high}_{yy}=-LBox L). For en ikke-null vertikal rand med normalkvadrat (epsilon) giver den højere Gibbons–Hawking–York-term (L(K+ncdotpartialln L)). Det sidste bidrag ophæver integralet af (-Box L/kappa) inklusive (epsilon) i divergensteoremet. Ved vertikale hjørner bevares vinklen og målet multipliceres med L. Skalar-Dirichletdata kræver intet ekstra randled. Ved fri skalarvariation fremkommer den vægtede normalflux.

```text
S = ∫ √|g| L [(R − 2Λ)/(2κ) − X/2 − V(Φ)]
    + (1/κ) ∫_∂ ε √|h| LK + vertikale hjørneled.
```

Ved konstant (L_0) fås (G_D=G_{D+1}/L_0), (phi=sqrt{L_0}Phi) og (V_D(phi)=L_0 V(phi/sqrt{L_0})). Massen er uændret for et kvadratisk potentiale. Den kanonisk normerede kvartiske koefficient divideres med (L_0). Ved variation af (L) holdes det højere felt (Phi) fast.

## Variation før fastlåsning

```text
L (Gμν + Λ gμν) + (gμν □ − ∇μ∇ν)L = κ L Tμν
∇μ(L ∇μ Φ) − L V′(Φ) = 0
R − 2Λ − κ(X + 2V) = 0
(D−1) □L = −2L (Λ + κV)
```

Den tredje linje er den uafhængige fiberligning. Den sidste følger ved at indsætte fiberligningen i sporet af metrikkens ligning. På en løsning af det fastfrosne D-dimensionelle system ved (D>2) er venstresiden i fiberligningen (4(Lambda+kappa V)/(D-2)). Derfor er et masseløst nulmodefelt og (Lambda=0) konsistent ved konstant L, også med feltgradienter. Et varieret massivt felt fejler generelt. En konstant (V) kan ophæve (Lambda), hvis skalarfeltets egen ligning også er opfyldt. Ved (D=2) kan Einstein-tensorens spor ikke bestemme R. Fiberligningen skal stadig kontrolleres uafhængigt. Blandede (ymu)-ligninger er nul i den uvriddede nulmodesektor. De er relevante, hvis KK-vektor eller fiberafhængig impuls aktiveres.

I Einstein-rammen (g_E=(L/L_0)^{2/(D-2)}g) fås for (D>2) det gravitationelle led (-[(D-1)/(D-2)](partialln L)^2) under den sædvanlige præfaktor (1/(2kappa_D)). En dynamisk radius tilføjer en fysisk skalarmode, hvis normaldata også skal specificeres. For en flad, uvriddet m-torus med konstante længder erstatter (mathcal V=prod_a L_a) overalt (L_0) i kobling og feltnormalisering. Alle ekstra diagonale ligninger har samme konstant-radius-betingelse. Med dynamiske torusmoduler optræder både volumen- og formmoder. For diagonale faktorer (L_a(x)) giver den sporvendte interne ligning (Boxln L_a+partiallnmathcal Vcdotpartialln L_a=-2(Lambda+kappa V)/(D+m-2)). Summen giver (Boxmathcal V=-2mmathcal V(Lambda+kappa V)/(D+m-2)).

Den homogene kontrol bruger (n=D-1) lige store basisretninger med Hubbleparameter H og fiberretning (J=dot L/L). Den uafhængige begyndelsesconstraint er (n(n-1)H^2/2+nHJ=kappa(dotPhi^2/2+V)+Lambda). Hver retningsrate følger (dot H_i+(nH+J)H_i=2(Lambda+kappa V)/n). Dermed kan variationen af L måles med (J(0)=0) og en constraint-konsistent start.

## Regge-produkt

Hver D-simpleks ganges med et interval og trianguleres via de D+1 trapper i en fælles, global toppunktsorden. En cirkel består af mindst tre intervaller. Intrinsiske kvadrerede intervaller er (s_{uv}+ell_j^2) for tværgående diagonal, (s_{uv}) horisontalt og (ell_j^2) vertikalt, (sum_jell_j=L). Afstande gælder i den lokale prismecelle. For et ægte basishinge (h) har (h	imes I_j) samme to-dimensionelle normalplan, så vinkeldefekten er uændret og de triangulerede hinge-mål summerer til (|h|ell_j). Nye hinges væk fra basishinges har fladt normalplan. Dette gælder også det vertikale Dirichlet-randled, hvor halvlinket er bevaret. For en åben fiber er de ortogonale kapper ekstrinsisk flade, men samlingen af kappe og siderand har et hjørneled. Med V3's reelle Lorentz-konvention giver tidagtige hjørner (pi/2); ortogonale hjørner med Lorentzisk normalplan har nul real boost. De afprøvede kapper genskaber forskellen i den samlede virkning.

Det affine nulmodefelt har ingen fiberafledt og bevarer sin basisgradient på hver delprisme. For nodal potentialekvadratur har de lige store delprismer tilsammen samme vægt for hvert toppunkt i basis. Aksial faktorisation gælder når trappen har de oprindelige basisben samt ét fiberben med nul feltforskel. Derfor er (S_{D+1}=LS_D) ved samme G og samme unormaliserede felt, og de tilbageførte basisgradienter er præcis (L
abla S_D). Med kanonisk felt og konverteret G er de to virkninger identiske. Fast L reproducerer derfor eksisterende V3's ligninger i basissektoren. Derivationen gælder produktunderfamilien og produktvariationerne. Individuelle højere diagonalvariationer kan stadig have residualer.

En samlet (dS/dL=S_D) varierer også randdata og tester derfor ikke den lokale Einstein-ligning. I `local.py` varierer fiberlængder i den indre tidsskive, ved et eksplicit midpoint-ansatz for de tværgående diagonaler. Det måler en markeret retning i det fulde kantgradientrum. Generel dynamik og rumlig konvergens for dette ansatz er åbne.

## Lokale overgange

En kompaktificeret cirkel har positiv omkreds og en højere geometrisk dimension, også når kun nulmoder er excitérbare. En fastfrosset cirkel har yderligere en fastholdt fysisk omkreds. En fundamentalt fraværende cirkel har ingen fiberdata eller variationsligning. Grænsen (L\to0) gør den viste produktmetrik degenereret. En glat lukning kan findes i andre lokale ansatzer, fx ved en akse hvor omkreds over proper radialafstand går mod (2pi). Så kræves selvstændige regularitets- og topologidata.

Israel-betingelser sammenligner den inducerede metrik og dens kanoniske normalimpuls på hypersurfaces af samme dimension med en specificeret overfladestress. En lokal blandet overgang kan afprøves ved at reducere den høje side til fælles randgeometri. Den reducerede normalimpuls indeholder både (L(K_{ab}-Kh_{ab})) og et led proportionalt med (h_{ab}ncdotpartial L). Skalarens flux vægtes med L. Fri radiusvariation bærer desuden en egen randkoefficient (i Jordan-formen proportional med K ved fastholdt induceret basis-metrik). En lav sektor uden radion skal derfor levere en radius-randbetingelse eller et overgangsled, der bestemmer denne koefficient. Ligestilling af (G_D) fastsætter kun den fælles sektors kobling på produktstykket. Den tidligere stratificerede virkning er den mere generelle ramme. Produktet begrænser dens sektor- og randled, hvor en fiber faktisk er til stede. En kanonisk regel for arbitrære blandede komplekser følger endnu ikke.
