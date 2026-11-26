# Evolution og emergent rumtid

## Aktuel forskningsretning · V3 (fastlåst 26. november 2026)

**[Grundmodel V3 — diskret dynamisk rumtid](GRUNDMODEL_V3.md)** er den aktuelle autoritative konceptbeskrivelse og startpunkt for Codex. Knuder og dynamiske forbindelser udgør geometrien; identiske aktive akser bestemmer nabostruktur; Einstein–Hilbert/Regge + skalarfelt og PLA er fundamentet. Blandede lokale topdimensioners fælles virkning er endnu ikke udledt eller verificeret. Se også [samlet forskningsstatus](README_RESEARCH_STATUS_20261126.md) og [numeriske pilotforsøg](DISCRETE_FIELD_GR_PILOT_20261126.md). V1/V2 og tidligere resultater bevares.

## Tidligere forskning og reproduktion
[Dansk forskningsrapport](RAPPORT.md) · [Forskningslogbog](LOGBOG.md) · [H1–H5](HYPOTHESES.md) · [Rådata og figurer](results/)

Rapporten sammenligner kurvatur og effektiv transportdimension på den eksisterende skovmotor og i en særskilt lokal selektionsmodel. [Masse, inerti, Lorentz-symmetri og feltkræfter](../fundamental-physics/matter/README.md) er fysiske referenceforsøg fra samme forskningsrunde.

## Reproduktion

Kør fra repositoryets rod. Den samme Git-historik skal indeholde `cb587788`, som forskningsharnessen bruger til at hente den uændrede skovmotor.

```bash
python3 -m pip install -r research/fundamental-physics/requirements.txt
bash research/evolution-geometry/reproduce.sh
```

Kørslerne med 3D-arkitektur tager længst. Reproduktionsscriptet tager en valgfri outputmappe. Analysekoden læser både gzip- og almindelige råfiler.

| Filer | Indhold |
|---|---|
| `snapshots_*.json.gz` | Graf, strategi-ID, besættelse og energiregnskab for hvert seed på den uændrede skovmotor og for gradmatchede substrater. |
| `forest_geometry.csv`, `forest_summary.csv` | Rå geometrimålinger per graf og seed-bootstrap af målinger og parrede kontraster. |
| `architecture*.csv` | Tidsserier, frekvenser, selektions- og orienteringskontroller, geometrimål og sekvensanalyse for den lokale selektionsvariant. Lange reserverækker er gzip-komprimeret. |
| `architectures*.json.gz` | Egenskaber per celle for et udvalg af 3D-netværk. |
| `calibration.csv` | Kendte dimensioner og samme estimator som i skovforsøgene. |
| `clock_ambiguity.csv` | Sammenligning af signaltid, afstand og urhastighed i to konformt relaterede optiske grafbeskrivelser. |

De store gitre bruger en frøfast stokastisk sporvurdering på de frosne grafer. Bootstrapintervallerne resampler **hele simulationsseeds** og omfatter ikke systematiske afvigelser fra endelig gitterstørrelse. På de originale ringgitre angiver `geometry` simulatorens etiketter −1, 0 og +1. De gradmatchede substrater er `cliques`, `torus` og `regular`.

## PUK

[Forundersøgelse, fire projektkandidater og offline-laboratorium](puk/README.md).

## V2 · Harmonisk Einstein–Klein–Gordon

[Rapport, udledninger, rådata og offline-laboratorium](v2/README.md).
