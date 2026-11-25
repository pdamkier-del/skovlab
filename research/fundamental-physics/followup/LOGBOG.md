# Forskningslogbog · Opfølgning

## 25. november 2026

1. Startede fra det lokale checkpoint `b3fa2b3` og fastlåste igen produktionsmotorerne til `cb587788`. Prøvede først at finde sene vinduer i fulde kørsler med konstant klima. Valgte derefter en præcis ordtest og uafhængige train/test-seeds. Omregnede testen af fortegn til eksakt enumeration af hele forløbs orienteringer.
2. Implementerede en diskret variant af Roldán og Parrondos flashing ratchet, løste for stalling og beregnede eksakte skjulte ordsandsynligheder. Stalling gjorde to positionssymboler utilstrækkelige. Forsøget viste, at længere ord har positiv KL eksakt, mens den direkte Monte Carlo-estimator har utilstrækkelig opløsning i de korte ord.
3. Fællesmotoren havde en overraskende stærk sen asymmetri. Gentog fra friske seeds efter 2.400 sweeps, nu med sampling hvert sweep. Faste bins tabte signalet på 20×20. Kvantilbaserede bins og tre separate vinduer gjorde en ren opstartsforklaring mindre sandsynlig. Tog særskilte målinger omkring hvert sweeptrin og fandt en vedvarende cirkulation mellem beholdningerne.
4. Peters sene regime så stationært ud i nogle makrotal og gav stærkt KL. Gik tilbage og målte individuelle højder. Praktisk taget alle levende steder var forsvindende små. To forskudte, konservative højdegrænser fjernede det sene regime. Dette fund blev nedgraderet fra mulig fysisk pil til følsomhed i træreglerne. Vækst-/kampkontrollen med så stor angrebspris ændrer også spredning og kan stadig vise langsom drift.
5. Målte varme hotspots med parrede KMP-opdateringer uden global pulje. Superposition pr. realisation holdt. Adskilte global energirestriktion fra langtrækkende kraft med kanonisk og mikrokanonisk ligevægt.
6. Beregnede den Gaussiske parfri energi, gentog med feltstikprøver og med lokale Gibbs-opdateringer. 2D-kraften overlevede det sidste tjek og var forenelig med determinantresultatet. 3D-signalet ved større afstand faldt under den valgte Monte Carlo-opløsning.
7. I metrikforsøget voksede en lokal superpositionsresidual. Den numeriske test med finere gitter og mindre tidsstep bevarede den. Ved måling af første moment gav fordobling af boksens sidelængde en kraftig reduktion af den tilsyneladende drift. Beholdt lokal omfordeling som resultat og forkastede en tyngdekraftsfortolkning.
8. Testede Barenblatt-profilen mod samme konservative solver. Tilføjede separat reversibel bølgemodel for at skelne rumlig spredningsentropi fra mikroskopisk irreversibilitet. Demonstrerede også sjældne hændelsers betydning for en eksakt fluktuationsrelation.
9. Gemte rådata, afledte data, analyse, uafhængig reproduktionsprocedure og offline-HTML i forskningsmappen. Alle ændringer ligger inden for `research/fundamental-physics/`.

Se [rapporten](RAPPORT.md) for ligninger, parametre, litteratur og kvantitative resultater. Se [README](README.md) for næste sessions indgangspunkter.
10. Validerede alle fire HTML-paneler, parameterændringer og afspilning i Chromium samt med en separat DOM-test. De 24 eksisterende repository-tests bestod. Den komprimerede råfil fra b3fa2b3 gav samme SHA-256 efter dekomprimering.
