# Complexity-class leave-one-out test: protocol (written before any prediction was run)

Date: 2026-10-11. Inputs: SPE paper v3 Tables 8-14 and 22 only. Job 2 literature evidence is NOT yet in
the matrix, so every cell below is marked from v3 text; Job 2 may later upgrade "open" cells.

Caveat on blindness: the v3 outcome tables (tau, EUR/well) were visible when the matrix was built.
To limit that, cell marks use only geological, test and pressure statements (Tables 9, 10, 12, 14),
not tau, EUR, EUR/well or eta_G values (eta_G is production-derived, so it is not used as a score input).

## 1. Challenge columns (reservoir-intrinsic only)
C1 compartments / water-isolated channels
C2 stacked or non-net layers with doubtful connection
C3 channel gas-water contact / early water
C4 damage or completion effectiveness (water-based mud, fracs)
C5 low reservoir energy (measured p_i < 5,000 psia)
Not scored (shown for information): C6 halite/scale/condensate (no v3 evidence: open for all), C7 hub truncation
(TRUNC flag; a data limit, not rock), C8 facility/kh limit (H > 6; a facility property).

## 2. Cell states and score
observed = 1.0 (a measurement or direct test states it); inferred = 0.5 (a model or diagnosis states it);
open = 0 (no evidence either way; NOT the same as absent).
Complexity score = sum of C1..C5.

## 3. Classes (fixed now)
simple: score < 0.5; moderate: 0.5 <= score < 1.5; complex: score >= 1.5.

## 4. Leave-one-field-out (LOFO)
Peers of field i = other fields of the same class, if at least 2 exist; otherwise all other fields (play).
Same rule for the stratigraphic-group baseline (v3 rule). Prediction = geometric mean of peer values.
Sigma (for P90-P10) = sample sd of ln(value) over the peer set when it has >= 3 peers, else the sd over all other fields.
P90-P10 = pred x exp(-/+1.2816 sigma); width = P10/P90; coverage = actual inside.
Targets: tau (13 fields), field EUR = 0.365 x q_ref x tau_pred (13, as v3 Table 16),
EUR per well (12 clean fields, Trent excluded as in v3), RF_eff (8 fields with credible GIIP, Boulton excluded).
Scoring as v3 Table 16: median absolute error, geometric bias, P90-P10 coverage, range width.
Never calibrate to RF on mapped GIIP.
