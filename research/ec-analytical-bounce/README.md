# Analytisk undersøgelse af bounce i klassisk ECD

**Resultat:** Den generelle klassiske enkeltspinor-ECD-teori udelukker ikke alle **lokale volumenbounces**. Vi konstruerer analytiske, rumligt varierende startdata, der opfylder alle fire Einstein-constraints og giver en regulær lokal overgang fra kontraktion til ekspansion. Konstruktionen er lokal og planarsymmetrisk; den er ikke en afgrænset sky eller et komplet sort-hul-rumtidseksempel.

**Den viser ikke et torsionsudløst bounce.** Samme datafamilie giver også lokale bounces i torsionsfri Einstein–Dirac. Med constraints løst på ny for hver teori reducerer ECD-kontaktleddet de beregnede vendeaccelerationsrater i denne familie.

[Dansk PDF](rapport.pdf) · [LaTeX](rapport.tex) · [Fuld udledning](DERIVATION.md) · [Lokal eksistens og begrænsninger](EXISTENCE_AND_SCOPE.md) · [Kildekontrol](SOURCES.md)

## Hvad er faktisk vist?

| Spørgsmål | Analytisk resultat |
|---|---|
| Tvinger generel klassisk ECD altid kontraktion til at fortsætte? | Nej; et lokalt modeksempel er konstrueret med constraints opfyldt. |
| Findes der en no-bounce-klasse? | Ja: tilstrækkelige fokuseringsbetingelser udledes; den homogene, rumligt flade strømtilpassede klasse har desuden et stærkere vendepunktsforbud. |
| Kan et lokalt bounce ske med positiv lokal energitæthed? | Ja i eksemplet. Men det bryder den longitudinale nulenergibetingelse; positiv tæthed alene er ikke fysisk tilstrækkeligt. |
| Er eksemplet et realistisk positivfrekvent fermionstof? | Det er ikke etableret. En tilhørende flad, periodisk reference indeholder en stor negativfrekvent sektor. Ingen kvantestatistisk tilstand er konstrueret. |
| Er torsion årsagen til eksemplets bounce? | Nej. Den torsionsfri sammenligning bouncer også; kontaktkorrektionen dæmper vendingen i denne familie. |
| Bouncer en hel gravitationelt kollapset sky eller et sort hul? | Uafklaret. Ingen global fortid, vakuummatching, trapped-surface-konstruktion eller fuld skyvolumen er konstrueret. |

## De vigtigste ligninger

For ét regulært klassisk spinorfelt sættes $u=j/n$, $n=\sqrt{-j^2}>0$, $S=\bar\psi\psi$ og $G_A=3\kappa/16$. Lad $\mathcal G$ være den rumlige trace af den kinetiske Dirac-stress i strømrammen. Den er bestemt af feltets kovariante afledte, ikke en fri væskevariabel. Den fulde stress giver præcist

$$\epsilon=mS+G_A n^2+\mathcal G,\qquad P=G_A n^2+\mathcal G/3,$$
$$\epsilon+3P=mS+4G_A n^2+2\mathcal G.$$

Ved $\Theta=0$ er den nødvendige og, sammen med regulær lokal fortsættelse, tilstrækkelige lokale vendebetingelse

$$u\cdot\nabla\Theta=-\sigma_{\mu\nu}\sigma^{\mu\nu}+\omega_{\mu\nu}\omega^{\mu\nu}-\frac\kappa2(mS+4G_A n^2+2\mathcal G)+\nabla_\mu a^\mu>0.$$

Ingen universel fortegnsregel for alle leddene følger af Dirac-ligningen. At vælge dem uafhængigt er heller ikke tilladt; derfor konstrueres selve feltdataene og geometrien i udledningen.

Et eksplicit lokalt eksempel giver ved vendepunktet

$$\epsilon_0=\frac{5m^2}{48\kappa}>0,\quad \partial_n\Theta_n=\frac{m^2}{24}>0,\quad u\cdot\nabla\Theta_u=\frac{287m^2}{96}>0.$$

De to ekspansionsafledte er forskellige, selv om stof og normaler har samme hastighed i startøjeblikket: stoffets acceleration har en ikke-nul divergens. En uafhængig differentiering af Dirac-ligningen kontrollerer strømresultatet. Ingen tidsintegration eller søgning over kollapsparametre bruges.

## Reproduktion

Med de eksisterende forskningsafhængigheder:

~~~sh
python -m unittest discover -s research/ec-analytical-bounce/tests -v
bash research/ec-analytical-bounce/build_pdf.sh
python research/ec-analytical-bounce/validation/run_checks.py --record
~~~

Symbolsk algebra er en uafhængig kontrol af den dokumenterede udledning. Den er ikke en erstatning for den, en tidsudviklet kollapssimulering eller en garanti for en realistisk materietilstand. Simulatorerne er ikke ændret.
