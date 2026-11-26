# V3 · Produktreduktion og inhomogene variationer

[Matematik](MATEMATIK.md) · [Litteratur](LITTERATUR.md) · [Rådata](results/) · [Offline-laboratorium](lab.html)

## Resultater

**Regge-produkt.** Med samme unormaliserede felt og G reproducerer et periodisk produktgitter (S_{D+1}=LS_D) og alle tilbageførte basisgradienter til omtrent (10^{-14}) for (D=2,3,4). Det gælder også på krumme, perturbede gitre og for begge feltoperatorer i deres respektive ansatzer. To cirkler giver produktet af omkredsene. Åbne fibre giver målbare hjørnebidrag på ca. 0,77, 3,06 og 1,15 i de tre konkrete forsøg. Den uafhængigt beregnede sum af timelike hjørnemål gange (pi/2) med Regge-præfaktor genskaber afvigelsen. Feltgradienten faktoriserer også her. Med de åbne randbetingelser har kantgradienten desuden gradienten af hjørneleddet.

**Udeladt ligning.** Den fastlåste radius er konsistent i den kontinuerte nulmodesektor for (D>2), når (Lambda+8pi G_{D+1}V=0) langs løsningen. Radion-integrationen verificerer Hamilton-constrainten for 2, 3 og 4 basisrumretninger med absolut drift under (2	imes10^{-11}). Den masseløse kontrol holder omkredsen på 0,8. En masse eller en positiv kosmologisk konstant får omkredsen til at ændre sig fra samme startlængde og nul initial radiusfart. I den diskrete pilot for to basisrumretninger varierer vi lokalt kun fiberlængder på den indre tidsskive. Ved fælles raffinering falder det volumennormerede masseløse residual fra (4,57	imes10^{-4}) ved (ell=1,h=0,08) til (3,05	imes10^{-5}) ved (ell=0,25,h=0,02). Det massive residual ligger omkring 0,054. Kontinuum for disse begyndelsesdata giver (2V_{high}simeq0,0531) i samme normalisering. Tidsraffinering alene fjerner ikke det masseløse residual. Den rumlige prøve skalerer den periodiske celles fysiske størrelse og dermed hele torussen ved fast antal celler. Det er en lokal skala-test. Konvergens ved fastholdt fysisk domæne og stationaritet i samtlige højere kantvariationer er stadig åbne.

**Inhomogen dynamik.** For flad vakuum er der ni Hessian-singularværdier under (10^{-11}), mens den næste er omkring 0,016. Den lineære afbildning fra alle toppunktsforskydninger med nul variation af de faste randkanter har netop rang ni i de frie intervaller. Den omfatter bevægelser af centrale randpunkter i normalretningen, som førsteordens randlængder ikke registrerer. (|H Q|_2 < 10^{-11}) for en ortonormal basis Q. På den krumme boks er næsten hele den tilbageværende kantresidual ved fastholdt rand projiceret på det flade nulrum. Det giver en diagnose af nær-degeneration og følsomhed for randdata. Det flade nulrum er kun en reference, så en stor projektion identificerer hverken eksakt gauge i den krumme model eller en bestemt brudt constraint. Ved perturbation 0,003 falder største kantresidual fra (2,88	imes10^{-5}) til (1,87	imes10^{-6}) ved justerbar rand. Ved 0,02 er det stadig (4,87	imes10^{-5}). De justerede kanter vælges ved vægtet pivot-QR, og residualerne reevalueres på alle frie kanter og feltnoder. Det valgte randproblem og dets kausale kammer er registreret. En fri stationær løsning til (10^{-8}) er endnu ikke opnået. Startdata kommer fra et homogent kontinuumforløb interpoleret til de åbne V3-rande. Den særskilte periodiske test starter på den verificerede diskrete homogene gren og måler begge slags residual der.

**Kausalitet på skæve gitre.** For (ds^2=-dt^2+(dx+eta,dt)^2+dy^2) har kontinuums null-mode frekvens (|k|-eta k_x). Den affine operators Fourier-symbol konvergerer omtrent anden orden for begge retninger i den valgte prøve. Den aksiale operator konvergerer mod (sqrt{1-eta^2}|k|), da den bruger enkeltbenenes intervaller og derfor udelader blandingsleddet (g_{tx}). Afvigelsen fra den fysiske frekvens er endelig ved fast (eta) og forsvinder i den ortogonale kontrol. Det er en lavfrekvent test af det karakteristiske symbol i en plan baggrund. Numerisk domæneafhængighed og stabilitet af alle højfrekvente grene af et frit koblet tidsskridt er åbne.

**Lokal overgang.** Reduktionen bestemmer koblingen i et regulært produkt, hvor fiberen findes. En overgang til en intrinsisk lavere sektor kræver yderligere rand- eller lukkedata for radius og metrikimpuls. Dynamisk radius genindsætter den manglende ligning, mens en regulær grænseflade stadig skal udledes. [Udledning](MATEMATIK.md)

H1–H5 videreføres i [hypoteseloggen](../../HYPOTHESES.md). Alle beregnede dimensioner er forudsatte i geometri eller produktansatz. Forsøgene demonstrerer derfor hverken evolutionær selektion af dimension eller emergent rumtid.

## Reproduktion

Fra rodmappen med Python 3, NumPy og SciPy:

```bash
python3 -m pip install -r research/fundamental-physics/requirements.txt
bash research/evolution-geometry/v3/reduction/reproduce.sh
```

`product_mesh.py` bygger geometrien og tilbagefører de fulde gradienter. `run.py` skriver produkt-, hjørne- og kontinuumkontrollerne. `local.py` afprøver den udeladte lokale ligning. `inhomogeneous.py` gemmer Hessianspektrum, rumlige og timelige residualer, alle de frie kantintervaller og Fourier-rødder. `build_lab.py` indlejrer tabellerne i den selvstændige HTML. For små residualer kan de sidste cifre og optimeringstrinnet variere med SciPy og BLAS.
