# Status efter ni forskningscyklusser

**Fortsættelsen har tilføjet tre cyklusser: en ny rumlig spintilstand, dens 3D-udvikling og en kontrol af, hvad der styrer materialestrømmens volumenændring.**

Spinets retning varierer nu i rummet. Kildetermerne og gravitationens bindinger er kontrolleret uafhængigt, også de spændinger en perfekt-fluid-erstatning ville overse. Startdata og evolution er testet på tre opløsninger. Rumfejlene falder omtrent med anden orden, og den separate tidsforfinelse er forenelig med RK4.

For netop denne familie fortsætter kontraktionen gennem det beregnede interval. Der ses ingen lokal volumenvending. Det er ikke et generelt bevis imod bounces eller for stabilitet ved vilkårlige forstyrrelser.

De fulde felter er nu gemt i 15 tabsfri checkpoints med kontrolsummer. Den fulde torsionskrumning er kontrolleret på genindlæste felter ved tre tidspunkter. De målte værdier er endelige og konvergerer, men tre tidssnit beviser ikke global regularitet eller fravær af en senere singularitet.

Ved sluttidspunktet viser Raychaudhuri-kontrollen en tydelig fokusering: Rotation og acceleration kan modvirke kontraktionen nogle steder, men er langt svagere end de negative bidrag. Kontaktleddets bidrag i den kontrollerede enkeltspinor-identitet er også fokuserende. Dette er en analyse af samme løsning, ikke en sammenligning med en torsionsfri udvikling; konklusionen må ikke overføres til alle ECD-tilstande eller kvantestof.

20 programtests består. Alle nye resultater, fejlmål, checkpoints og begrænsninger er gemt. Der er stadig ikke påvist et bounce af en endelig sky, fysiske volumenoscillationer eller en kontrolleret kvantefysisk fermionbeskrivelse ved disse store krumninger.

**Næste konkrete forsøg øger kun spinretningens amplitude fra 0,2 til 1,0**, mens tæthed, bølgelængde og action beholdes, og bindingerne løses igen. Det undersøger en stærkere forstyrrelse uden at vælge parametre efter et ønsket bounce. NEXT_ACTION.md beskriver præcist fremgangsmåde, stopkriterier og validering.
