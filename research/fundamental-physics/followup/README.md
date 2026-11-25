# Tidens pil, fluktuationskræfter og lokal geometri

- [Dansk forskningsrapport](RAPPORT.md)
- [Interaktivt laboratorium](lab.html). Download HTML-filen og åbn den i en browser. Den indeholder alle data til visningen og kan åbnes offline.
- [Forskningslogbog](LOGBOG.md)
- [Data og scripts](results/)

Bygger videre på lokal forskningscommit `b3fa2b3`. Skovmotorerne læses fra Git ved den oprindelige version `cb5877888f5dc8fea06b8224f891a04a4be3302d`. Simulationsstørrelser og ablationer sættes i forskningsharnessen. Produktfiler og workflow ligger uden for undersøgelsen.

## Gentag forsøget

Installer Python-versionerne i [requirements.txt](../requirements.txt). Kør derefter

```bash
bash research/fundamental-physics/followup/reproduce.sh
```

Scriptets valgfrie argumenter er en resultatmappe og en sti til den genererede HTML. Det fulde skovforsøg er den langsomme del. Man kan køre `forest.cjs` med en resultatmappe og et scenarienavn som separate argumenter for at køre scenarier uafhængigt. De fem store skov-CSV'er og de to uafhængige fællesforløb gemmes med tabsfri gzip. Python-analyserne accepterer også ukomprimerede CSV'er.

| Filer | Indhold |
|---|---|
| `shared_original`, `peter_*`, `shared_validation_*` | Tidsserier eller afledte statistikfiler, med særskilte seed- og tidspunktrækker i de komprimerede CSV'er. |
| `stationarity.csv`, `forest_kl.csv` | Driftscreening over fire vinduer, holdout KL-logscore og orienteringstest. |
| `shared_validation_kl.csv`, `shared_validation_stationarity.csv`, `shared_words.csv` | Uafhængig replikation, marginalfordelinger og målte ordsandsynligheder. |
| `height_*.csv`, `sweep_flux.csv` | Målinger af mikroskopiske højder og nettooverførsler ved hver fase af et sweep. |
| `ratchet.csv`, `fluctuation.csv` | Eksakte og simulerede resultater for skjulte tilstande og fluktuationsrelationer. |
| `casimir.csv`, `casimir_mc.csv`, `local_gibbs.csv` | Eksakt Fourier-reference, Gaussiske prøver og selvstændig lokal termisk dynamik. |
| `hot_exchange.csv`, `exchange_cov.csv` | Lokalt konservativ stokastisk energiudveksling og kontrol af mikrokanoniske korrelationer. |
| `metric_feedback.csv`, `metric_frames.json`, `barenblatt.csv` | Ikke-lineære metrikforsøg, billeddata og en konvergensreference for porøsmedieligningen. |
| `wave.csv`, `wave_profiles.csv` | Målinger og energiprofiler før og efter tidsvending. |
