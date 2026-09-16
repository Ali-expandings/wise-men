# Preliminary Wilcoxon analysis — N=29 (2026-07-06)

**Status: PRELIMINARY. The frozen spec's formal §8 verdict requires N=30 (pilot Q41 outstanding). Every §8 condition nevertheless already holds at N=29, and the conclusion is robust to the only open data flag.**

Method: pure-python Wilcoxon signed-rank (normal approximation, tie + continuity correction), 5-axis composites from `parsed/*.yaml` (Q23 = official per-axis-median values; Q23_tiebreaker artifact excluded). Script: `wilcoxon_n29.py` (per-axis section reconstructs slot→arm from the unsealed blinding-map comments; slot/arm composite cross-checks all passed).

## §8 conditions at N=29

| # | Condition | Result | Pass |
|---|---|---|---|
| 1 | median C > median B | 25 vs 21 | ✅ |
| 2 | median (C−B) ≥ 2 | 4.0 | ✅ |
| 3 | Wilcoxon C>B, one-sided α=0.05 | W+=418.5, z=4.367, **p=6.3e-06** | ✅ |
| 4 | no axis significantly worse (two-sided, Bonferroni α_eff=0.01) | correctness p=0.53 (no diff); insight p=4.2e-07, practical p=2.9e-04, risk p=1.3e-05, dissent p=1.0e-05 — all BETTER | ✅ |
| 5 | Wilcoxon C>A, one-sided | z=4.707, **p=1.3e-06** | ✅ |

Means: C=24.48, B=20.76, A=16.28. C beats B on 28/29.

## Sensitivity — Q09/Q11 chairman-parity flag (HISTORY repair path option c)

Excluding both flagged questions (N=27): means C=24.48 / B=20.93 / A=16.33; median gap 4.0; C beats B 26/27; C>B p=1.4e-05; C>A p=2.8e-06. **Conclusion unchanged → the parity flag is moot for the headline result.** Flag can be closed as "resolved by sensitivity analysis" unless someone wants the chairmen re-run for completeness.

## Remaining for the formal verdict
Q41 clean rerun under frozen v2.3 (protocol preserved verbatim at `eval-data/protocol-v2.3-frozen/`) → N=30 → re-run this script → formal §8 verdict. Given p-values 4-5 orders of magnitude below α, Q41 cannot flip the outcome; it can only complete the protocol.
