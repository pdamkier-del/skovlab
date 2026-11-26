# Skovlaboratorium — aktuel forskningsarkitektur 2026-11-26
Læs dette ved genoptagelse. V1/V2 er frosne referencer; dette er aktuel syntese, ikke verificeret ny teori.
## Formål
Undersøg om energi, transport og gravitation favoriserer dimensionalitet uden forudbestemt optimum, fitnessfunktion eller kunstig dimensionsomkostning. H1 effektiv geometri, H2 krumning, H3 dimensionalitet (primær), H4 statistisk tidspil, H5 rumlige og tidslige egenskaber. Se HYPOTHESES.md og MEASUREMENT_PROTOCOL.md. Fysisk stabilitet er selektionsanalogi, ikke nødvendigvis Darwinisme. Zeta kun eksplorativt.
## Fastlagt
- Celler er lokale knudepunkter/energifrihedsgrader i fælles geometri, ikke nødvendigvis miniuniverser. Forbindelserne selv er del af rumtiden.
- Heltallige aktive akser [x,y,z,...], n_i. Abstrakte koordinater i N_max; 2n_i potentielle naboer. Kant langs k kun hvis begge ender har k aktiv og er koordinatnaboer langs k. x til x, y til y osv.; ingen direkte krydsaksekant. Intern gravitation kan stadig koble akser. Faktisk grad kan være mindre. Nummerering er ikke afstand.
- Alle aktive rumlige kanter starter med samme proper længde ell_0; omtrent ens initial energi med små variationer. Normalisering af energi kontra densitet/volumen og G_D skal kontrolleres; initialdata skal opfylde constraints.
- Individuelt skalarfelt phi_i og impuls. Ingen kunstig E(n). Udskiftelig lokal metrik som input, fx ds²=-N_i²dt²+sum_k a_ik² dx_k²; diagonal ansatz ikke fuld GR. Skeln fast baggrund fra dynamisk metrik. Lokalt c og kausal transport.
- Einstein–Hilbert plus felt i D=n+1: A=integral sqrt(-g)[(R-2Lambda)/(16pi G_D)-g^munu partial_mu phi partial_nu phi/2-V(phi)]. Stationær virkning (PLA), ikke automatisk energiminimering. Vakuum uden felt; masseløst V=0; massivt m²phi²/2; kvartisk lambda phi^4/4; konstant V eller Lambda (undgå dobbelttælling).
- Fast motor, udskiftelig metrik/ansatz, potentiale, initialdata; HTML visualiserer verificeret motor.
## Regge calculus: næste spor
Knuder og kanter er geometriens skelet; højere simplicer/facetter og incidens skal specificeres. Simplex flad indvendig, krumning i hinges D-2. Euklidisk bulk A_R=sum_h Vol(h) epsilon_h/(8pi G_D), epsilon=2pi-sum dihedralvinkler; relevante randled, Lambda og materie tilføjes. Lorentzisk version til fysisk tid. Valgt metrik kan initialisere simplexintervaller s_ab=Delta x^mu g_munu Delta x^nu ved konstant lokal metrik. Fælles kant har ét interval. Aksekanter alene bestemmer ikke generel simplexgeometri; geometriske hjælpediagonaler er ikke automatisk nye direkte felttransportkanter.
Standard Regge har fast topdimension D: 3+1 hinges trekanter, 4+1 tetraedre. Blandede simplicial complexes er mulige men standard EH giver ikke automatisk overgangsvirkning. Projektion/pullback på fælles akser er kandidat, ikke udledning. Undersøg knudepunkter i ét kompleks med aktive akser, fælles intervaller og højere celler. Sammenlign A: fast maksimal topdimension med variable aktive transportretninger (kontrol, ikke erstatning for H3) og B: ikke-rent kompleks med forskellige maksimale simplex-dimensioner. B kræver eksplicit overgangsvirkning, rand/junction-led, normalisering og constraints. Referencer: https://academic.oup.com/imajna/article/44/5/2698/7502804 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC5253799/ ; https://doi.org/10.1007/JHEP09(2023)069.
## Faktiske resultater
- GRUNDMODEL_V1.md, GRUNDMODEL_V2.md: frosne referencer.
- v2/RAPPORT.md og MATEMATIK.md: fast-n EKG/Schroedinger-Poisson, skaleringsstivhed 2(4-n)T, ikke dimensionsselektion.
- DISCRETE_FIELD_GR_PILOT_20261126.md: fast geometri, L=sum_i(M_i dotphi²/2-M_i V)-sum_edges K_ij(phi_i-phi_j)²/2. 625 knuder, n=1..4, 8 seeds, t=20, middelenergi .857,.960,1.048,1.128; relativ energifejl max 2e-5, reversibel. Ingen GR i grafen. Separat radial Einstein-skalar pilot n=3,4,5 med ens initial kompakthed, ikke ens absolut energi; foreløbig. Ingen samlet model.
- Lokal akselab.html er naboprototype med ikke-Einstein kantdynamik; IKKE fysisk forskningsmotor. Produktion uberørt.
- DIMENSION_AMPLITUDE_IDEA_20261126.md og DIMENSION_PATH_INTEGRAL_IDEA_20261126.md: kvanteidéer parkeret. P(n) ikke energifraktion, PLA giver ikke sandsynligheder, unitær dynamik ikke automatisk selektion.
## Næste arbejde
1. Fast-D Regge med brugerdefineret metrik/initialintervaller; flad og kendt krum geometri.
2. Diskret feltvirkning, variation af fælles intervaller inkl. tidskanter/lapse, randled og constraints. Ingen ad hoc fjedre som EH-erstatning.
3. Ens dimension: Minkowski, vakuum, kendt Einstein-skalar løsning, mesh-konvergens, constraints, kausalitet og relevant energiregnskab (ikke generel global GR-energi).
4. Blandede akser og kompleks: eksplicit overgangsvirkning eller dokumenter manglende input. Faste n først. Fast-geometri kontrol, match dimensionløse koblinger, variér faser, potentialer, størrelse, tid, N_max. Mål effektiv dimension, energi, krumning, entropi, tidsskalaer. Shannon ikke automatisk termodynamisk entropi.
5. Først derefter dimensionsændringer og eventuel kvantisering med fælles tilstandsrum, mål, randbetingelser.
6. HTML viser validering og hypoteser. Bevar fælles app og historik.
## Arbejdsstil
Enkelt dansk, gentag ikke afklaret naboregel. Skeln koncept, udledning, implementering, numerisk og fysisk verifikation. Rapportér negative resultater. Ingen påstand om fuld mixed-D Einstein-model endnu.
