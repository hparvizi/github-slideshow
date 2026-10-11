# Complexity-class LOFO test: results (2026-10-11, inputs: SPE v3 Tables 9-14, 22; matrix marks from v3 text only)
Script: loo_complexity_test.py; sensitivity.py; 00_protocol_declared_before_run.md; matrix_evidence.md; loo_results.json.
Validation: the stratigraphic baseline reproduces v3 Table 16 (field EUR: 37% median error, -2% bias, 10/13 inside, 3.0x width).

| Target | Peers | n | Median abs error | Geometric bias | Inside P90-P10 | Median width |
|---|---|---|---|---|---|---|
| tau | stratigraphic | 13 | 34.7% | -2.5% | 10/13 | 3.0x |
| tau | complexity | 13 | 37.2% | 0.0% | 8/13 | 2.9x |
| field EUR (0.365 q_ref tau) | stratigraphic | 13 | 36.8% | -2.2% | 10/13 | 3.0x |
| field EUR | complexity | 13 | 37.0% | +0.3% | 8/13 | 2.9x |
| EUR per well | stratigraphic | 12 | 41.8% | +10.4% | 11/12 | 6.3x |
| EUR per well | complexity | 12 | 21.9% | 0.0% | 11/12 | 6.3x |
| RF_eff | stratigraphic | 8 | 25.8% | 0.0% | 6/8 | 3.1x |
| RF_eff | complexity | 8 | 23.1% | +0.5% | 6/8 | 3.1x |

Reading (stated as it came out):
- tau and field EUR: complexity classes do NOT beat stratigraphic groups (37% vs 35-37% error; coverage worse, 8/13 vs 10/13). Random class labels match this: permutation P = 0.70.
- EUR per well: median error falls from 42% to 22% (permutation P = 0.007), but it is fragile: moving the complex threshold from 1.5 to 2.0 gives 33% vs 42%; dropping Murdoch K gives 26% vs 45%; the gain rests on 12 fields, one single-well 282 bcf outlier, and on classes whose "simple" group is mostly "no evidence recorded".
- RF_eff (n=8): 23% vs 26%, permutation P = 0.08: suggestive, not established.
- Range widths are identical because sigma falls back to the play-wide value for small peer sets; the test does not show sharper ranges.
Conclusion for v4: report complexity grouping as a promising, untested-at-scale alternative for EUR per well, not as a replacement for the play-wide range; the evidence for tau is negative. Needs the 30-field set to resolve.
Limits: 13 fields; class rule written after seeing the v3 tables; marks from v3 text only; Job 2 evidence not yet applied.


## ADDENDUM after independent QC (Q: PASS WITH FIXES) and rerun (rerun_qc_fixes.py, output in rerun_qc_fixes_output.txt)
This addendum SUPERSEDES the reading above.
1. Leakage: several matrix marks (Breagh C2, Kilmar C1/C3, C4 for Breagh, Chiswick, Kew, Rita) came from v3 Table 12 diagnoses based on production-derived eta_G / eta_J; Kilmar C3 is a production outcome. The "no outcome-derived marks" statement was wrong.
2. Leakage-free matrix (only measured p_i, the Cavendish DST, and geological stacking descriptions): classes become 9 simple / 3 moderate / 1 complex. EUR per well: 41.0% vs 41.8% for stratigraphic, permutation P = 0.28. tau 38.8% vs 34.7% (P 0.84). RF_eff 34.6% vs 25.8% (P 0.95). The EUR-per-well gain is NOT reproduced: it came from the leaked marks.
3. Original matrix, 20,000 permutations (seed 7): EUR per well P = 0.012 (earlier 0.007 was a favourable seed); tau 0.70; RF_eff 0.088. Not corrected for three targets and several thresholds. Threshold grid on the original matrix: (0.5,1.5) 21.9%; (0.5,2.0) 32.9%; (1.0,1.5) 26.1%; (1.0,2.0) 41.0% (no gain vs 41.8%); Cavendish moderate = the (0.5,2.0) case. tau improves to 30% at (0.5,2.0).
4. Coverage and width: the first run mixed sigma sources. With a common play-wide sigma both groupings give identical widths and similar coverage (tau 9/13 vs 10/13; EUR/well 9/12 each); the test cannot show range sharpness.
5. Other caveats: Murdoch K (single well, 282 bcf) dominates the simple class (without it EUR per well is 25.7% vs 44.7% on the original matrix); six of 13 tau/EUR values rest on a fallback decline that uses an all-field median, so they are not independent targets; six fields are "simple" because v3 records nothing on them.
REVISED CONCLUSION for v4: complexity classes built from evidence that does not depend on production outcomes do not beat stratigraphic grouping on tau, EUR per well or RF_eff for these 13 fields. The earlier EUR-per-well improvement was an artefact of outcome-informed marks. Report the result as negative or inconclusive at n = 13; a fair test needs independent evidence (Job 2 literature, 30-field set).
