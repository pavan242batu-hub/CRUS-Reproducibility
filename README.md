# CRUS implementation and reproducibility materials

Implementation and reproducibility materials for clinical section routing.

## Status and access

This repository is publicly accessible and contains CRUS implementation
and reproducibility materials.

The final revision package is being prepared for archival deposit in
Zenodo under reserved DOI:

    10.5281/zenodo.24084026

The Zenodo record is currently an unpublished draft. DOI reservation
does not establish publication or public access to the final archive.

Manual sharing review of the final revision package remains pending.
Public availability does not establish privacy clearance,
redistribution permission, or a fully verified clean-environment,
end-to-end inference release.

## Existing revision snapshot — 30 October 2026

The existing downloadable revision snapshot is:

[Download the 30 October revision package](crus_review_revised_20261030T090211792719Z.zip)

[Download its SHA-256 checksum](crus_review_revised_20261030T090211792719Z.zip.sha256)

Recorded SHA-256:

    c23e1e01e48783723c191b5cfac0b0401209252fc518d4f56bc9140cf809391c

This archive superseded the earlier package at the time it was uploaded.
Earlier archives are retained as historical snapshots.

The 30 October archive does not include the subsequent local
release-preparation edits being prepared for the Zenodo deposit.
It must not be treated as the forthcoming final Zenodo archive.

After extracting this snapshot, begin with its README.md and:

    revision_updates/REVISION_UPDATE_GUIDE.md

The snapshot includes the final-cohort Table 13 analysis, the
operating-point/risk–coverage audit, their scripts and outputs,
and implementation-notebook and reviewer documentation.

The recorded checksum identifies this specific archive. It does not
establish scientific validity, privacy clearance, redistribution
permission, or successful end-to-end execution.

## Final revision package being prepared for Zenodo

The package being prepared includes:

- Implementation notebooks with saved code-cell outputs cleared.
- Recorded configurations and frozen thresholds and policies.
- Primary and repeated-split identifiers and group assignments.
- Cleaning and grouping audits.
- Case-level predictions and acceptance decisions.
- Supporting additional-analysis and MedCPT artifacts.
- Scripts for regenerating specified metrics from saved predictions.
- Dataset-access and record-reconstruction instructions.
- Environment records.
- Artifact inventories, export logs, and checksums.
- A release-preparation review record describing completed checks
  and their limitations.

Final archive contents, inventories, and checksums will be finalized
before publication.

## Documentation and reproduction scope

Within the package, begin with:

1. README.md
2. REVIEWER_GUIDE.md
3. REPRODUCING_RESULTS.md
4. DATA_RECONSTRUCTION.md
5. revision_updates/REVISION_UPDATE_GUIDE.md

The final deposit candidate additionally includes RELEASE_REVIEW.md,
which records the scope and limitations of the current
release-preparation checks.

The metric-regeneration scripts operate on supplied saved predictions
and analysis artifacts. They do not perform fresh model inference.

The matched-ranking regeneration script reconstructed 45 method/target
rows across 11 compared count/metric fields, with zero mismatches
within the documented tolerance.

Other checks and their limitations are described in the package
documentation. Not all supplied summaries, figures, or additional
analyses have been independently regenerated.

The package must not be described as fully independently reproduced.
A complete clean-environment, end-to-end model-inference reproduction
has not been established.

## Implementation notebooks

The package includes:

- notebooks/CRUS_R1_5_External_Transfer.ipynb
- notebooks/revised_risk_aware_hybrid_pipeline_v2.ipynb

These are historical implementation notebooks containing multiple
experiments, audits, intermediate working cells, and machine-specific
paths. Their inclusion does not establish a tested Run all workflow.

Notebook Markdown and intermediate cells may describe historical
development results and release-preparation tasks. They must not be
substituted for the authoritative final-revision results or current
release status identified in the package documentation.

## Dataset access and omitted inputs

Raw MTS-Dialog dialogue inputs are not included in the distributed
package.

Obtain the dataset from its original repository:

https://github.com/abachaa/MTS-Dialog

The recorded source commit is:

    3ff0801933608d6f570468c13125125fb5cabdea

Use DATA_RECONSTRUCTION.md and the supplied provenance files for
source-file locations, recorded checksums, row-index conventions,
normalization and hashing, and authoritative split and group
assignments.

Do not substitute fresh random splits or assume that the current
dataset repository version is identical to the recorded source version.

Raw inputs are omitted to avoid duplicating the source dataset in
this code-and-derived-artifact deposit. Their omission is not a claim
that the dataset licence prohibits redistribution.

Dataset attribution:

Ben Abacha, A., Yim, W.-w., Fan, Y., and Lin, T. (2023).
An Empirical Study of Clinical Note Generation from Doctor-Patient
Encounters. Proceedings of the 17th Conference of the European
Chapter of the Association for Computational Linguistics,
pp. 2291–2302.
DOI: 10.18653/v1/2023.eacl-main.168

The source repository identifies MTS-Dialog as licensed under
Creative Commons Attribution 4.0 International (CC BY 4.0).

Source licence at the recorded commit:

https://github.com/abachaa/MTS-Dialog/blob/3ff0801933608d6f570468c13125125fb5cabdea/LICENSE.txt

Consult the dataset's own licence and attribution requirements before
using or redistributing it.

## Code licence and third-party materials

The original implementation code owned by Pavankumar Dattatray
Paikrao is released under the MIT License, as documented in the
package's LICENSE file.

This licence does not relicense third-party datasets, software,
model weights, or third-party code incorporated in or referenced
by the notebooks and scripts.

Those materials remain subject to their respective licences and
attribution requirements. Existing third-party copyright and
licence notices must be retained.

## Integrity and provenance

For the final revision package, use its package-root files:

- REVISION_FILE_INVENTORY.csv
- REVISION_SHA256SUMS.txt

These files will be refreshed after the final package edits.

Historical inventories, status reports, export logs, and checksums
under manifest/ are retained as provenance. Their coverage may
predate later revision additions and release-preparation edits.

A checksum applies only to the exact file for which it was generated.
The checksum of an earlier archive must not be used to verify the
forthcoming Zenodo archive.

## Remaining publication steps

- Resolve the remaining manual sharing and distribution review.
- Finalize package documentation and release identification.
- Refresh the final inventory and checksums.
- Create and inspect the final archive.
- Upload and publish the final Zenodo deposit.
- Test public access to the published record and files.
- Update this README and the manuscript's Data and Code Availability
  section to reflect the actual published deposit.
