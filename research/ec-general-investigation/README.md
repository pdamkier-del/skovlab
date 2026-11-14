# Generel ECD-undersøgelse: kollaps, regularitet og e-folds

**Undersøgelsen er generel i geometrien og feltkomponenterne. Den er ikke en fuldstændig klassifikation af alle globale ECD-løsninger.** En action fastlægger ligningerne, men ikke et universelt bounce eller ét bestemt antal e-folds uden fysiske startdata, randdata og et defineret slutpunkt.

Vi beholder minimal klassisk ECD som udgangspunkt, undersøger også den præcise udvidelse til flere Dirac-felter og skelner det fra kvantestatistisk fermionstof. Ingen ny tilstandsligning eller bouncekraft er tilføjet. De eksisterende simulatorer er uændrede; den nye kode måler strømkinematik og e-folds passivt på den eksisterende 3D-feltudvikling.

[Dansk rapport](rapport.pdf) · [Generelle feltligninger og afgrænsning](GENERAL_ECD.md) · [E-folds uden FLRW](EFOLDS.md) · [Regularitet og bounce](REGULARITY_AND_BOUNCE.md) · [Eksakt flerefelts-benchmark](CHIRAL_MULTIFIELD_BENCHMARK.md) · [Status og åbne problemer](STATUS_AND_NEXT.md) · [Kilder](SOURCES.md)

## De vigtigste generelle resultater

1. Langs en regulær, bevaret, timelig Dirac-strøm er de lokale volumen-e-folds præcist

   $$N_u=\frac13\int\Theta_u\,d\tau=-\frac13\ln(n/n_0).$$

   Det kræver ingen homogenitet, isotropi eller FLRW-metrik. Strømmen og referencebegivenhederne skal være erklæret.
2. Et fulgt volumen på ADM-snittene giver et andet mål, når strømmen hælder i forhold til normalerne:

   $$N_\Sigma=N_u-\frac13\ln(W/W_0),\qquad W=-u\cdot n_{ADM}.$$

   Retningsbestemte e-folds kræver deformationen af fulgte nabobaner. Positivt gennemsnit betyder ikke, at alle retninger udvider sig.
3. For **ét regulært klassisk spinorfelt**, med fast masse og minimal EC-kobling, gælder den eksakte spor-ligning

   $$R=\kappa m\bar\psi\psi-2\kappa G_A n^2,\qquad |\bar\psi\psi|\leq n.$$

   Derfor giver fortsat kompression med $N_u\to-\infty$ ubegrænset Ricci-skalar og torsionsinvariant. ECD garanterer ikke automatisk et regulært bounce før nulvolumen. Et endeligt-propertidsforløb mod denne grænse har invariant krumningsdivergens; dette viser ikke, at alle data faktisk når grænsen.
4. Flere felter og kvantetilstande kræver særskilt behandling: den samlede aksiale strøm opfylder ikke generelt enkeltspinorens Fierz-relation. Den ovenstående tæthedsbaserede krumningskonklusion må derfor ikke overføres automatisk til dem.
5. Det tidligere analytiske lokale bounce for særlige feltdata står ved magt. Det er også muligt uden torsion, bryder en energibetingelse og bestemmer ikke en hel skys efterfølgende ekspansion eller dens antal e-folds.

## Et eksakt, særligt kosmologisk eksempel med torsionsdrevet bounce

Seks uafhængige masseløse felter med samme kiralitet og balancerede planbølger giver en timelig samlet aksial strøm. Direkte kontrol af alle Dirac-ligninger og den fulde stress giver et regulært kosmologisk bounce med

$$a(\eta)=\sqrt{a_b^2+q^2\eta^2},\qquad N_{acc}=\tfrac12\ln2\simeq0,3466.$$

Det er antallet af **accelererede** e-folds efter dette bestemte bounce. Den senere samlede ekspansion er ubegrænset, men bliver decelereret og strålingslignende. Uden torsionsleddet har den tilsvarende model et strålings-crunch. Dermed er vendingen faktisk torsionsdrevet i dette klassiske flerefelts-benchmark.

Konstruktionen er et eksakt, særligt FLRW-metrikeksempel med seks fulde feltløsninger, ikke den generelle 3D-solver eller en afgrænset sort-hul-sky. En illustrativ Pauli-normalisering placerer dens bounce ved ukontrolleret høj krumning; kvantetilstand, stabilitet og fysisk realisme er ikke etableret. Se [den fulde udledning](CHIRAL_MULTIFIELD_BENCHMARK.md).

## Hvad er faktisk beregnet med 3D-motoren?

[Den gemte sporing](tracked-example.json) følger tre lokale Dirac-strømbaner i en kort, inhomogen svagfeltsløsning. Den måler egentid, materialestrømmens e-folds, normalernes e-folds, volumen-Jacobian, hovedstrækninger og fejl i strømbevarelsen. På de finere af de afprøvede gitre er de lokale netto-e-folds omkring **0,00013–0,00019** over koordinattiden 0,02. Normalmålene er samtidig negative. Dette er forskellige kongruenser, ikke en modstrid.

[Opløsningskontrollen](tracking-refinement.json) viser fortsat mærkbare rekonstruktions-/bevarelsesfejl. Der påstås **ikke** et konvergeret fysisk e-foldtal, et globalt bounce eller inflation. Geometrisk konsistens ved maskinpræcision er ikke det samme som fysisk nøjagtighed. Nogle markører har både små kontraktions- og ekspansionsbidrag; der registreres ingen verificeret bouncebegivenhed.

## Reproduktion

Med de eksisterende NumPy/SciPy/SymPy-afhængigheder:

~~~sh
python -m unittest discover -s research/ec-general-investigation/tests -v
python research/ec-general-investigation/track.py --output tracked-efolds.json
python research/ec-general-investigation/refine_tracking.py
bash research/ec-general-investigation/build_pdf.sh
python research/ec-general-investigation/validation/run_checks.py --record
~~~

Det eksakte benchmark og dets figur kan gendannes med `chiral_benchmark.py` og `plot_chiral.py` i denne mappe.

Figuren kan gendannes med `python research/ec-general-investigation/plot.py`; dens særskilte plotafhængighed er angivet i `requirements-plot.txt`.

De nye resultater omfatter kinematiske identiteter, spor-/torsionsbeviser og en kort numerisk målemetode. Stærkt kollaps, fysiske kvantetilstande, konsistent vakuumyderside og generelle singularitets-/bouncekonklusioner for afgrænsede skyer forbliver særskilte forskningsproblemer.
