# PUK-forundersøgelse · Evolution og emergent rumtid

[Dansk rapport og fire projektkandidater](RAPPORT.md) · [Interaktivt laboratorium](lab.html) · [Matematiske noter](MATEMATIK.md) · [Pilotdata og figurer](results/) · [Logbog](LOGBOG.md)

Download HTML-filen og åbn den i en browser. Den kan køres offline og indeholder fire forsøg om transportretninger, grafkurvatur, tidspil og ures målinger.

## Genkør forsøgene

Fra repositoryets rod:

```bash
python3 -m pip install -r research/fundamental-physics/requirements.txt
bash research/evolution-geometry/puk/reproduce.sh
```

Scriptet accepterer en alternativ resultatmappe og en alternativ HTML-sti som henholdsvis første og andet argument. Den lange kørsel gemmer råresultater fra alle seeds. Til en første uafhængig reproduktion er to små forsøg nok:

```bash
python3 research/evolution-geometry/puk/motifs.py /tmp/puk-test
python3 research/evolution-geometry/puk/markov.py /tmp/puk-test
```

`motif_equilibria.csv` viser den lokale stationære løsning for alle 240 ordnede placeringer af donor og modtager. Fokuser først på donor 0 og modtager 3 eller 8. `motif_population.csv` sammenligner fuld adiabatik med 12 lokale energitrin mellem reproduktionsrunder, med 20 seeds samt neutrale, frosne, frakoblede og mutationsfri kontroller. `markov.csv` er eksakt lineær algebra med 16 tilstande og positive mutationsrater, uden samplingstøj.

`minimal.csv.gz` indeholder de enkelte forløb for et gitter med ét arveligt bit. Brug `minimal_contrasts.csv` for parrede seedintervaller. `minimal_networks.json.gz` gemmer de aktive masker til `conductance.csv`. `interfaces.csv` sammenligner én ressourcezone med gentagne zoner. `two_sites.csv` kontrollerer den analytiske to-plads-løsning. `*_summary.csv` bruges af HTML. `minimal-og-krumning.png` viser de to vigtigste simulationspaneler.

De oprindelige skovsimulatorer, 3D-forsøg, brede kurvaturmålinger og optiske identifikationskontroller er beskrevet i [foregående rapport](../RAPPORT.md). [Feltreferencerne](../../fundamental-physics/matter/README.md) forklarer den selvstændige bølge- og Lorentz-kalibrering.
