# Reproduction from saved predictions

Run commands from the repository root.

## Required analysis packages

These scripts use Python, NumPy, pandas, and scikit-learn.
The primary saved protocol records:
- numpy: 2.1.3
- pandas: 2.2.3
- scikit-learn: 1.6.1

The original packaging session successfully ran the primary scripts.

On 2026-11-09, the four standalone saved-prediction scripts also
completed successfully in the local Windows crus-metrics-env
environment after package installation. pip check reported no
broken requirements.

See the local Windows verification section below for results
and scope. This was not an end-to-end model inference test.

## Commands

python scripts/regenerate_primary_metrics.py --package-root .
python scripts/verify_matched_rankings.py --package-root .

## Outputs

The regenerated/ directory contains:
- primary_full_coverage_metrics.csv
- primary_native_acceptance_metrics.csv
- primary_matched_count_metrics.csv
- matched_rankings_all_targets.csv
- matched_rankings_agreement_report.csv

## Verified scope

The matched-ranking script reconstructs selections from saved
ranking scores, sorting by ranking_score descending and record_id
ascending for ties.

It regenerated 45 method/target rows at accepted-case targets
113, 115, 117, 118, and 171.

Eleven count/metric fields agreed with the saved verified summary.
Integer counts matched exactly. Floating-point fields were checked
with absolute tolerance 1e-10 and relative tolerance zero.

The primary regeneration script also checked saved correctness flags
against labels and predictions and reconstructed full-coverage and
native-acceptance metrics.

## Not yet verified

- Automated agreement of all full-coverage/native metrics with summaries.
- Calibration metrics.
- Saved boundary-tie diagnostic fields.
- All manuscript figures.
- All repeated-run metrics.
- Additional revision experiments beyond the Table 13 and operating-point/ranking-curve checks documented below.
- End-to-end model inference in a clean environment.

## Policy distinction

Native CRUS gating and ranking-based top-k acceptance are different
selection rules. Equal accepted-case counts do not imply identical
selected records.

## Environment provenance

The primary protocol records eight package versions.
Six recorded versions match in each repeated-run metadata file.
The repeated-run metadata do not record pandas or scipy versions.
These are partial environment records, not a complete lockfile.

## Local Windows saved-prediction verification - 2026-11-09

Packages were installed in the local crus-metrics-env Python
environment. `python -m pip check` reported:
"No broken requirements found."

The following four scripts completed successfully using
`--package-root` against the extracted package:

- scripts/regenerate_primary_metrics.py
- scripts/verify_matched_rankings.py
- revision_updates/editor_table13_final_cohort_20261029T070537486427Z/regenerate_table13.py
- revision_updates/editor_comment2_consistency_20261029T074417157641Z/verify_operating_points_and_risk_coverage.py

Primary metrics were regenerated and saved correctness flags
were verified against labels and predictions.

Matched-ranking verification passed for all 45 method/target rows
and all 11 compared count/metric fields within the stated tolerance.

Table 13 regeneration verified 257 cases: 181 correct and 76
incorrect predictions. The reported means, mean difference, bootstrap interval,
Mann-Whitney result and rank-biserial effect matched the values
documented in REVISION_UPDATE_GUIDE.md. 
All 10,000 bootstrap replicates were valid.

The operating-point audit verified all saved ranking-curve points
and native-gate decisions against reconstruction. Cascade native
acceptance gave 109 correct and 8 errors among 117 accepted cases;
ranked top-117 selection gave 106 correct and 11 errors.

Both revision scripts accepted local package paths without edits
and reported that original input files remained unchanged.

This verification used saved predictions. It does not establish
end-to-end model inference, complete manuscript/figure agreement,
calibration verification, or repeated-split bootstrap reproduction.