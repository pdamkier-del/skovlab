# Forskningslogbog

## 25. november 2026

1. Klonede det offentlige repository separat. Fastlåste fælles og udgivet Peter-model ved `cb5877888f5dc8fea06b8224f891a04a4be3302d`. Sammenlignede de to samarbejdsbranches og kortlagde model-, test- og forskningsfilerne. Audit af skovreglerne står i rapporten. De selvstændige Einstein–Cartan-laboratorier blev kortlagt på dokumentations- og testniveau.
2. Forkastede idéen om at måle gravitation ved at følge centroiden for to overlappende diffusionspakker. Overlap kan flytte maxima uden reel vekselvirkning. Valgte superposition som nulhypotese og en fjern lokal probe til at isolere puljens rolle.
3. Udformede holdout-test af tidens retning med reservefelter, konstant klima, lag 4/20/80, tre blokstørrelser og en kontrol med tilfældig tidsorden. De sene vinduer er operationelle tidsvinduer og indebærer ingen antagelse om stationaritet.
4. Matchede faktisk diffusionskode mod frosne grafers analytiske identiteter. Bruger grafafstand til ringgitterforsøg, da skærmprojektionen ændrer afstande. Behandler en deterministisk impuls som deterministisk, selv om den er genkørt med flere seeds.
5. Kørte lokal KMP-varmeudveksling med lige og ulige reservoirtemperaturer og omvendt gradient. Indførte et eksakt numerisk andetmomentssystem for at kunne skelne finite-size-effekter fra estimatorstøj.
6. Tilføjede torusreferencer for varmespor, zeta, Green-funktion og en Gaussisk Casimir-analog samt en statisk arealvægtet konform metrik til at afprøve den tidligere metrikhypotese på en konsistent operator.
7. JavaScript-harnessen fejlede første gang, fordi browserens script er pakket i en funktion. Lukkede funktionen efter måle-hooket og genkørte. Ingen data fra den afbrudte kørsel indgår. Eksisterende `npm test` gav 24 beståede tests.
8. Opstartssignalet var stærkt ved konstant klima. Det sene signal afhænger af simulator og lag, og 80-sweep-signalet i Peters udgave var foreneligt med tilfældighed på 24×24. Forkastede derfor en generel påstand om robust sen klassifikation.
9. To-puls-residualen nåede højst 8,9×10⁻¹⁶. Fulde sweeps med kamp gav brede fjernresponsintervaller. En kontrolleret intervention, der gjorde kamp ubetalelig, gav ved 12×12 en målelig fjernrespons med forventning fra puljen. Det gør en afstandsfortolkning overflødig for dette signal.
10. KMP-kovariansen var tydelig i den korteste kæde. Ved N=64 var usikkerheden større end effekten. Den lukkede momentberegning fastholdt den positive forventning og gav et mål for den nødvendige statistiske styrke.
11. Begge fulde kørsler bestod energitolerancen. Impulserne matchede det analytiske flade spektrum. En separat, valgfri Chromium-krydstest af fire snapshots med standard-UI nåede tidsgrænsen i Cloud. Den numeriske harness blev verificeret med invariants og analytiske kontroller.

## Opfølgning samme dag

Undersøgelsen fortsatte fra `b3fa2b3` med stationær tidspil, fluktuationsinducerede kræfter, konservativ metrikfeedback og en reversibel bølgereference. Se [den fortsatte forskningslogbog](followup/LOGBOG.md) og [rapporten](followup/RAPPORT.md). Den første rundes store råfil er komprimeret tabsfrit i denne opfølgning.
