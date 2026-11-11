# Current major-revision update

Submission ID: 86208cd7-779a-4368-982f-188f98cb187a

This directory supplements the previously prepared reproducibility
package. It contains regenerated Table 13 results and an independent
operating-point/risk–coverage audit.

## 1. Table 13: final primary cohort

Folder:
editor_table13_final_cohort_20261029T070537486427Z/

Regeneration script:
regenerate_table13.py

Verified cohort:
- 257 primary-test Cascade forced predictions
- 181 correct predictions
- 76 incorrect predictions

Regenerated results:
- Mean CRUS, correct: 0.103103
- Mean CRUS, incorrect: 0.227043
- Mean difference, incorrect minus correct: 0.12394018348451587
- Conditional 95% group-bootstrap percentile CI:
  [0.10099926008447667, 0.1462303128992902]
- Bootstrap replicates: 10,000
- Bootstrap seed: 20261029
- Assigned test groups: 256
- Mann–Whitney U, incorrect sample first: 11371.0
- Exploratory two-sided p-value: 1.446840361098988e-16
- Signed rank-biserial effect: 0.6532422215760396

The Mann–Whitney p-value is record-level and is not cluster-adjusted.
The group-bootstrap interval conditions on the saved predictions
and excludes model-refitting uncertainty.

These outputs replace the historical 259-case CRUS analysis.

## 2. Operating-point and risk–coverage consistency

Folder:
editor_comment2_consistency_20261029T074417157641Z/

Verification script:
verify_operating_points_and_risk_coverage.py

Verified primary Cascade thresholds:
- tau_c = 0
- tau_u = 0.128165036474669

Verified results:
- SK4 full coverage: 82 correct and 175 incorrect of 257
- Cascade full coverage: 181 correct and 76 incorrect of 257
- Native Cascade gate: 117 accepted, 109 correct, 8 errors
- Ranked Cascade top-117: 106 correct, 11 errors

All saved ranking-curve points agreed with reconstruction.
All saved native-gate decisions agreed with frozen thresholds.

Native-gate evaluation and saved-score ranking are separate policies.

## 3. Repeated-split bootstrap documentation

The Table 7 accuracy means, sample standard deviations and intervals,
including MedCPT, matched the saved summaries at reported precision
and were retained unchanged.

The interval-producing implementation uses:
- 5,000 bootstrap replicates
- Random seed 20261015
- Assigned group_id as the resampling unit
- Union of 866 observed test groups
- Synchronized group multiplicities across methods and repeats
- Equal-weight averaging of the five repeat-specific metrics
- Percentile confidence intervals
- Fixed models, split assignments, policies and original selections

The lightweight summary checks did not independently reproduce the
bootstrap intervals or verify every recorded source-file checksum.

## 4. Running the added scripts

The packaged scripts accept a required --package-root argument.
No Colab-path edits are needed for these script versions.

From the extracted package root, run:

    python revision_updates/editor_table13_final_cohort_20261029T070537486427Z/regenerate_table13.py --package-root .
    python revision_updates/editor_comment2_consistency_20261029T074417157641Z/verify_operating_points_and_risk_coverage.py --package-root .

Use the Python interpreter from the environment where the required
analysis packages are installed.

The scripts read packaged inputs under artifacts/ and write new
outputs to timestamped subdirectories under regenerated/.

Required inputs include the frozen protocol, split manifest,
case-level predictions and acceptance audit. The operating-point
script additionally reads the saved ranking-curve CSV.

Both scripts completed successfully in a local Windows environment
on 2026-11-09. See REPRODUCING_RESULTS.md at the package root for
the verification record and scope.

They regenerate analyses from saved predictions; they do not
retrain models, run model inference or retune thresholds.

The full package has not been independently reproduced from
source data in a clean environment.


## 5. Checksums and historical materials

The copied Table 13 SHA256SUMS.txt describes the files covered when
that analysis output was created; it does not cover subsequently
added scripts or this guide.

A final package inventory and checksum list must be generated after
all files and documentation are finalized.

The earlier archive and its checksum remain historical records.
They do not identify the revised package.