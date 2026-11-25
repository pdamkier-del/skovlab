# Skovlaboratoriet som laboratorium for statistisk fysik

Den danske [rapport](RAPPORT.md) samler modelaudit, resultater og tre forskningsprojekter. [Litteraturen](LITTERATUR.md) knytter hvert forsøg til en fagfællebedømt artikel. [Logbogen](LOGBOG.md) registrerer valg, forsøg og forkastede fortolkninger.

## Reproduktion

Kør fra en klon med commit `cb5877888f5dc8fea06b8224f891a04a4be3302d` i historikken. Kræver Git, Node.js, en C++17-kompilator og Python 3 med NumPy, SciPy, pandas og matplotlib. Forsøgsmapperne kan kopieres til en anden klon i samme sti.

```bash
python3 -m pip install -r research/fundamental-physics/requirements.txt
bash research/fundamental-physics/reproduce.sh
```

Et valgfrit argument til scriptet angiver en anden resultatmappe. For hver stokastisk betingelse er seed en statistisk enhed. Postprocesseringen trækker 4.000 bootstrap-stikprøver af seed-gennemsnit og giver marginale 95 %-intervaller uden korrektion for mange sammenligninger. Resultatfiler med enkelt-seed målinger kan analyseres med andre valg.

| Fil i `results/` | En række beskriver |
|---|---|
| `arrow.csv.gz` | Ét snapshot ved en rumlig blokstørrelse. Reserver inkluderer tomme pladser med værdi nul. `pool` og `structure` er pr. gitterplads. `balance` er absolut fortegnet afvigelse fra energiregnskabet. |
| `arrow_seed_scores.csv` | Én testscore på én uafhængig seed for en given tidsmæssig og rumlig indstilling. |
| `pulse.csv` | Respons på én enhed reserveenergi før de øvrige trin. `msd` bruger kvadreret korteste grafafstand. `support` måler længste afstand med positiv reserve. |
| `mixing.csv` | Udjævning i det frosne artsnetværk. `squared` er summen af afvigelser fra 1,5 i anden. |
| `response.csv` | Ændring i probens reserve ved én påvirkning for henholdsvis intakt og fjernet kilde, identificeret af `removed`. |
| `controls.csv` | Parrede probeforskelle med kamp og vækst slået fra via parametre. Indeholder også en deterministisk ligevægt. |
| `superposition.csv` | Maksimal feltresidual af lineær superposition og energisum ved to samtidige pulser. På ringgitteret er `separation` indeksforskellen. |
| `kmp.csv` | Stikprøvemomenter og venstre varmestrøm for én selvstændig KMP-kæde. `arrow` er et antisymmetrisk lagmoment. |
| `spectral.csv`, `green.csv`, `metric.csv` | Deterministiske Fourier- og egenværdiberegninger. `zeta1` og `zeta2` bruger gitterets egenværdier uden længdereskalering. |
| `*_summary.csv` | Grupperede middelværdier, antal seeds og percentilintervaller. |
| `piloter.png`, `spektrum.png`, `metrik.png` | Grafer over henholdsvis simulerede piloter, torusreferencer og den arealvægtede metrik. |

`model.cjs` læser de to originale scripts direkte fra Git. Den fjerner browserens eventregistrering og erstatter tegning og formelstatus med tomme funktioner. Initialisering, parsing af ligninger og dynamik bruger originalkode. Valg af gitterdimensioner uden for sliderens diskrete interval og én startart til det frosne laboratorium foretages ved at sætte konfigurationen efter UI-læsning. `kmp.cpp` og `metric.py` er selvstændige fysiske referencer.

## Fortsat undersøgelse

[Ny rapport, interaktivt laboratorium og rådata](followup/README.md).
