# Complexity-class LOFO test: results (2026-10-11, inputs: SPE v3 Tables 9-14, 22; matrix marks from v3 text only)
Script: loo_complexity_test.py; sensitivity.py; protocol_declared_before_run.md; matrix_evidence.md; loo_results.json.
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
