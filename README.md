# Skovlaboratoriet 🌳

Interaktiv gittermodel til undersøgelser af evolutionær selektion, artsdiversitet, rumlig orden og energiressourcer.

## Åbn simulatoren

**[Skovlaboratoriet som hjemmeside](https://pdamkier-del.github.io/skovlab/)** — linket virker, når GitHub Pages er aktiveret.

## Aktiver GitHub Pages

1. Åbn **Settings → Pages** i dette repository.
2. Under **Build and deployment**: vælg **Deploy from a branch**.
3. Vælg **main** og mappen **/(root)**, og klik **Save**.

Herfra vil opdateringer til `index.html` på `main` automatisk blive publiceret på samme adresse.

## Projektfiler

- [index.html](index.html) — hele simulatoren i én selvstændig HTML-fil.
- [LOGBOG.md](LOGBOG.md) — forskningslogbog, hypoteser, antagelser, kontrolberegninger og videre planer.

## Videnskabelig afgrænsning

Artsentropi måles med Shannon-entropi. Den valgfrie energivariant fører bog over disponibel energi og et reservoir med konstant total modelenergi. Det giver **ikke i sig selv** en temperatur eller en fysisk entropiproduktion.

Oprindelige skovregler er udgangspunktet; energimodellen er en eksperimentel udvidelse.

## Næste planlagte trin

1. Batchkørsler for både kontrolmodel og energivariant.
2. Sammenligning af vinderstrategier for forskellige energiomkostninger og overførselseffektiviteter.
3. Følsomhedstests og logning af numeriske kontrolberegninger.
