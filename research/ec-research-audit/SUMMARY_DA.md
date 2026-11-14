# Kort vurdering af ECD-projektet

**Min anbefaling er at afgrænse det analytiske arbejde, før den store 3D-simulator udvides. Start med at undersøge, hvad seksfeltsmodellens fermiontilstand og energiskala faktisk betyder.**

## Den intuitive fysik

Projektet har opnået mere end blot at tegne et bounce. I har undersøgt, hvornår tidligere stofmodeller fejler, udledt kontrollerbare specialtilfælde og bygget en 3D-prototype. Mine genkørsler understøtter de korte svagfeltsresultater.

Men “Dirac-felt” betyder ikke automatisk “en realistisk sky af fermioner”. En klassisk feltamplitude indeholder ikke i sig selv Paulis udelukkelsesprincip, degenerationspres eller partiklernes vekselvirkninger. Derfor kan en matematisk løsning være korrekt uden at beskrive en kollapsende stjerne.

De forskellige resultater modsiger ikke hinanden:

- Ét bestemt homogent spinorfelt kan ikke vende sit volumenkollaps.
- Det plane lokale eksempel vender på grund af feltets gradienter. Vendingen findes også uden torsion.
- Seks særlige masseløse felter giver et ægte torsionsdrevet kosmologisk bounce i den klassiske model. Det er et univers på en periodisk rumgeometri, ikke en afgrænset sky.
- Ingen af resultaterne viser endnu et regulært bounce af en endelig kollapsende sky med en konsistent yderside og en kontrolleret fysisk fermionbeskrivelse.

Den største videnskabelige hindring er forbindelsen mellem de valgte klassiske felter og fysisk muligt fermionstof. I seksfeltseksemplets enkle normalisering med én besættelse pr. mode ligger bouncet ved en ukontrolleret høj, Plancksk energiskala. At gøre en klassisk amplitude større løser ikke automatisk dette problem.

Modellen er værd at bevare som matematisk laboratorium. Den er endnu ikke grundlag for at konkludere, at torsion redder realistiske sorte huller fra singulariteter.

## Den tekniske vurdering

Den korrigerede action, spinkonnektion og fulde energimomentumtensor hænger sammen i de kontrollerede tilfælde. En ældre fortegnsfejl i torsionens geometriske orientering er allerede rettet i den nuværende formulering.

126 Python-tests og 9 modeltests i Node bestod. Opløsningsforsøget på 9³, 17³ og 33³ punkter gav de gemte resultater igen. Det er god, men begrænset evidens for kort svagfeltsudvikling. Det beviser hverken realistisk fysik eller stabilt stærkt kollaps. Jeg fandt desuden en konkret fejl i partikelantallet på periodiske gitre; simuleringerne er ikke ændret.

Randbetingelserne giver endnu ikke en fysisk vakuumyderside. Der mangler også stærkfeltskontrol og en dokumenteret regulær udvikling af en hel sky. Et lokalt minimum i volumen er ikke det samme som, at hele legemet vender.

## Det næste arbejde

Først bør I skrive en præcis oversættelse mellem seksfeltseksemplets klassiske amplituder og normaliserede fermionmoder: Hvilke arter og besættelser antages, hvilke korrelationer mangler, og hvor er tilnærmelsen gyldig? En vejleder med kvantefeltteori bør kontrollere den del. Et negativt svar er et brugbart forskningsresultat.

Derefter kan I analytisk undersøge, om det klassiske bounce overlever små forskelle mellem de tre rumretninger. Først når spørgsmålet er afklaret, bør I vælge konkrete forbedringer og valideringskrav til solverens videre arbejde.

Lær i denne rækkefølge: Dirac-strøm og bilineærer; Fermi-statistik og normalisering af moder; energimomentumtensor og energibetingelser; FLRW og Friedmann-ligningerne; tetrader og spinkonnektion; derefter ADM-bindinger, Raychaudhuri og anisotropi. Wick-kontraktioner og effektiv feltteori kommer til den afgrænsede kvantedel med vejledning.

**Det mest forsvarlige næste skridt er en lille, skarp undersøgelse af det eksisterende bounces fysiske antagelser. Den kan afgøre, hvad større beregninger overhovedet skal forsøge at besvare.**
