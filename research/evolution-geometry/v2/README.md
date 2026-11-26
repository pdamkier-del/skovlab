# Evolutionær rumtid V2

[Dansk rapport](RAPPORT.md) · [Matematiske udledninger](MATEMATIK.md) · [Forskningslogbog](LOGBOG.md) · [Offline-laboratorium](lab.html) · [Rådata og figur](results/)

Denne særskilte forskningsmappe tager udgangspunkt i den fastlåste harmoniske [Grundmodel V2](../GRUNDMODEL_V2.md) og målene [H1–H5](../HYPOTHESES.md). Download HTML-filen og åbn den lokalt. De fire paneler viser fri spredning, homogen EKG, radial svagfeltsbinding og en kompakt cirkel.

## Selvstændig reproduktion

Fra repositoryets rod:

```bash
python3 -m pip install -r research/fundamental-physics/requirements.txt
bash research/evolution-geometry/v2/reproduce.sh
```

Scriptet tager en alternativ resultatmappe og HTML-sti som første og andet argument. Koden er deterministisk. Valg af fase, tolerance, step, radius, normalisering og dimension er parametre og ligger i råtabellerne. For en første selvstændig kontrol er det nok at udlede og integrere tærskelprofilen i [binding.py](binding.py).

| Fil | Forsøg |
|---|---|
| `flrw.csv.gz`, `constraints.csv` | Homogen EKG ved forskellige dimensioner, rumlig krumning, begyndelsesdata og normalisering. |
| `circle.csv.gz` | Bianchi I med foreskrevet cirkeltopologi, dynamisk radius og frossen rumlig varmeprobning. |
| `free_moments.csv`, `free_profiles.csv` | Minkowski-kontrol med Fourier-baseret energi og moment, samt uafhængig radial kvadratur. |
| `radial_sp.csv`, `sp_profiles.csv`, `sp_evolution.csv` | Stationært og tidsafhængigt radialt Schrödinger–Poisson, med konvergens- og perturbationskontroller. |
| `critical6.csv`, `width.csv` | Eksakt tærskelprofil integreret numerisk, og variational Gaussisk breddeansats, som er en selvstændig legetøjsmodel. |

Tolerancer og trinoplysninger hører til det enkelte forsøg. En åbent/logaritmisk grænse i lav dimension er ikke automatisk Newton-grænsen i V2.
