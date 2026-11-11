# Reviewer guide

## 1\. Purpose and status

This package provides implementation notebooks, saved configurations, split identifiers, case-level outputs, and supporting analysis artifacts.

It is not yet a verified clean-environment, end-to-end inference release. The verification scope and limitations are stated below.

\#\# Current revision additions

&nbsp;

For the corrected final-cohort Table 13 analysis and the

operating-point/risk–coverage audit, begin with:

&nbsp;

revision\_updates/REVISION\_UPDATE\_GUIDE.md

&nbsp;

That guide identifies the added scripts, saved outputs, input-path

requirements and verification limitations.

&nbsp;

The two added standalone scripts accept --package-root and read
inputs from the extracted package's artifacts/ directory.
No Colab-path adaptation is needed for these script versions.
Both completed successfully in a local Windows environment on
2026-11-09. See REPRODUCING_RESULTS.md for the verification record
and revision_updates/REVISION_UPDATE_GUIDE.md for commands and scope.
This verification used saved predictions, not fresh model inference.

&nbsp;

## 2\. Start here: regenerate metrics from saved predictions

From the repository root, using the Python interpreter from your
analysis environment, run each command separately:

```bat
python scripts/regenerate_primary_metrics.py --package-root .
python scripts/verify_matched_rankings.py --package-root .
```

These scripts do not run model inference or require raw dialogue inputs.

Outputs are written to regenerated/.

See REPRODUCING\_RESULTS.md for metric definitions and verification scope.

## 3\. Verified results

- The primary metric script regenerated full-coverage classification and native-acceptance metrics and checked saved correctness flags.  
- The matched-ranking script reconstructed all 45 method/target rows from saved ranking scores.  
- Eleven count/metric fields agreed with the saved verified summary.  
- Integer counts matched exactly.  
- Floating-point comparisons used absolute tolerance 1e-10.

These checks do not establish reproduction of every manuscript result.

## 4\. Implementation notebooks

notebooks/CRUS\_R1\_5\_External\_Transfer.ipynb notebooks/revised\_risk\_aware\_hybrid\_pipeline\_v2.ipynb

These are output-cleared historical implementation notebooks. They retain original path references and multiple revision analyses. Do not execute all cells indiscriminately.

A tested section-by-section execution map for fresh model inference has not yet been supplied.

## 5\. Configurations and split identifiers

Primary configuration and policies: artifacts/corrected\_experiment\_outputs/final\_pretest\_protocol.json artifacts/corrected\_experiment\_outputs/validation\_selected\_policies.json

Primary split: artifacts/data\_audit/constrained\_split\_manifest.csv

Repeated splits: artifacts/supplementary\_repeated\_splits/seed\_\*/split\_manifest.csv

Calibration-fold assignments are provided separately.

Use supplied split assignments when reproducing reported analyses; do not generate new splits as substitutes.

## 6\. Data access and reconstruction

Raw input dialogue files are not included in this package selection.

See DATA\_RECONSTRUCTION.md for the recorded source version,

source-row conventions, record identifiers, normalization, grouping,

and primary/additional-MTS reconstruction instructions.

A fresh reconstruction from independently obtained source files

has not been tested in this packaging workflow. Perturbation-text

reconstruction also remains untested.

- Original dataset access location and version.  
- Source CSV filenames and source-row indexing convention.  
- Record-ID construction.  
- Text normalization, cleaning, and filtering.  
- Group construction and duplicate handling.  
- Reconstruction of selected additional-MTS records.  
- Perturbation generation and seeds.

Do not guess source-row indexing or substitute a different dataset version.

## 7\. Text-excluded derivatives

Files ending \_\_text\_excluded.csv omit the columns listed in: manifest/additional\_artifact\_export\_log.json

Their filenames and checksums differ from the original artifacts. Historical metadata can still refer to original-file checksums.

The query-text file inference\_inputs.csv is not distributed here.

## 8\. Additional analyses

Additional-analysis artifacts are included as supporting outputs. Their presence does not mean all metrics were independently regenerated.

See ADDITIONAL\_ARTIFACTS.md and the export logs.

The additional-MTS analysis must not automatically be interpreted as independent cross-dataset validation. Consult its saved scope and limitation fields.

## 9\. MedCPT baseline

See MEDCPT\_ARTIFACTS.md.

Primary and repeated-run configurations, predictions, selections, and summaries are provided. Training embeddings are excluded.

MedCPT metrics have not been independently regenerated in this packaging workflow.

## 10\. Environment records

See environment/.

Recorded versions are partial historical snapshots, not a complete, tested dependency lockfile.

Six recorded package versions match between the primary run and each repeated run. pandas and scipy versions are not recorded in the repeated-run retrieval metadata.

Do not infer the main-run environment from a separate baseline.

\#\# 11\. Integrity and provenance

&nbsp;

For this revision, use the package-root files:

&nbsp;

\- REVISION\_FILE\_INVENTORY.csv

\- REVISION\_SHA256SUMS.txt

&nbsp;

The inventory lists package files excluding itself and the revision

checksum list. The revision checksum list covers the inventory and

all other package files, excluding itself.

&nbsp;

The manifest/ directory retains historical inventories,

transformation logs and checksums. Their coverage may predate

the current revision additions.

&nbsp;

Checksums identify file contents; they do not establish scientific

validity, privacy compliance or execution success.

&nbsp;

## 12\. Outstanding release tasks

- Complete manual sharing and redistribution review.  
- Complete dataset-access/reconstruction instructions.  
- Document fresh-inference execution order and dependencies.  
- Map final manuscript tables/figures to artifacts and commands.  
- Refresh final inventories/checksums after all edits.  
- Arrange and test editor/reviewer access.