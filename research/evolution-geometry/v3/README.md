# Grundmodel V3 · Lorentzisk Regge-checkpoint

[Dansk rapport](RAPPORT.md) · [Matematisk udledning](MATEMATIK.md) · [Logbog](LOGBOG.md) · [Offline HTML](lab.html) · [Rådata og figur](results/)

Udgangspunktet er det fastlåste [V3-koncept](../GRUNDMODEL_V3.md). Fuld variational dynamik er verificeret i en **periodisk homogen ansats**. Hurtige checks og generel akse-/kantalgoritme virker ved flere faste dimensioner. Den frie inhomogene slab og blandede topdimensioner har eksplicit dokumenterede begrænsninger.

## Reproduktion

```bash
python3 -m pip install -r research/fundamental-physics/requirements.txt
bash research/evolution-geometry/v3/reproduce.sh
```

To valgfrie argumenter giver alternativ resultatmappe og HTML-sti. Hver af forskningsprotokollerne kan køres uafhængigt, fx:

```bash
OPENBLAS_NUM_THREADS=1 python research/evolution-geometry/v3/experiments.py /tmp/skov-v3 --section mesh
```

Gyldige sektioner er `mesh`, `wave`, `homogeneous`, `slab` og `all`. En fuld kørsel tager længst i de frie slab-forsøg. Programmet løser lineære og ikke-lineære systemer i SciPy. Forskellige BLAS-versioner kan ændre de sidste cifre og stopiterationen nær en acceptgrænse.

- `mesh.py` finder faktiske kuber og triangulerer en ren rumtidssektion. `metric_intervals` accepterer en udskiftelig funktion \(x\mapsto g(x)\).
- `Regge.evaluate(s, phi, Gnewton=..., model=(V, Vprime), matter="axial")` evaluerer virkningen og gradienterne i det valgte kausale kammer. Det tager delte, signerede kvadrerede intervaller som input.
- `solve_slab` accepterer randfelter og -metrik i inputarrays og kan holde geometrien fast. Tjek altid `stationary` og residualerne.
- `Frusta.start([a0,phi0], phidot0, h0)` løser første lapse og feltimpuls. `Frusta.step(older, left, old_h)` løser næste plades DEL og lapse og returnerer både kandidat og residual. De afprøvede udvidende grene har harmonisk, masseløst eller kvartisk potentiale. Et brugerdefineret par \(V,V'\) kan udskiftes.
- `homogeneous.csv` indeholder accepterede plader. `homogeneous_rejections.csv` registrerer stop ved afvisning. `fixed_time_convergence.csv` registrerer en anden protokol, hvor lapse kontrolleres og ikke løses.
- `slab_attempts.csv` indeholder negative inhomogene forsøg. `discarded_modes.csv` måler de uafhængige kantrester på to accepterede homogene plader. `verification.csv`, `cone.csv`, `controls.csv`, `dispersion.csv` og `wave.csv` indeholder de tilsvarende kontroller.

Download `lab.html` og åbn det i en browser. Det har alle nødvendige data indlejret og kan vises offline. Halve plader og afviste løsninger bruges kun på den måde, som råtabellerne angiver.

## Produktreduktion og inhomogene variationer

Se [det nye V3-checkpoint](reduction/README.md) og [offline-forsøgene](reduction/lab.html) for produktfaktorisering, radionligningen, randresidualer og skæve gitre.
