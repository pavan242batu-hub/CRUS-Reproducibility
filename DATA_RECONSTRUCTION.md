# Dataset access and record reconstruction

## Source and recorded version

Repository:
https://github.com/abachaa/MTS-Dialog

Recorded commit:
3ff0801933608d6f570468c13125125fb5cabdea

Use the saved provenance files to identify source artifacts and
verify their recorded checksums. Check the source dataset's applicable
access and redistribution terms separately.

Primary provenance:
artifacts/source_data/source_manifest.json

Additional-MTS provenance:
artifacts/additional_mts_heldout_audit_20261017T085443976861Z/download_provenance.json

Raw dialogue inputs are not distributed in this package selection.
## How to obtain the omitted inputs

Raw dialogue inputs are omitted to avoid duplicating the source
dataset in this code-and-derived-artifact deposit. Their omission
is not a claim that the dataset licence prohibits redistribution.

Obtain the source dataset from the MTS-Dialog repository identified
above. Use the recorded commit
3ff0801933608d6f570468c13125125fb5cabdea rather than assuming that
the current default branch contains identical files.

Locate the source filenames listed below within that recorded
repository version. Use the saved provenance files to check the
recorded source locations and checksums before reconstruction.

The source repository identifies the dataset licence as CC BY 4.0.
Consult its licence and attribution requirements before use or
redistribution. The MIT licence for this package's original
implementation code does not replace the dataset licence.

The source-version licence link and dataset citation are provided
in README.md. If a source file is unavailable or its checksum does
not match the saved provenance, do not silently substitute another
version; report the discrepancy to the package maintainers.

## Primary source files

MTS-Dialog-TrainingSet.csv
MTS-Dialog-ValidationSet.csv

Use files corresponding to the recorded provenance and checksums,
not an unverified current repository version.

## Primary record identifiers

The original code reads each source CSV with pandas.read_csv.

source_row is the zero-based parsed data-row position within that file.
It is not the original dataset ID and is not a physical CSV line number.
CSV headers are not counted as data rows.

record_id is constructed as:

    f"{source_filename}:{source_row}"

For example, source_row 7 refers to dataframe.iloc[7].

Use source_file and source_row from:
artifacts/data_audit/constrained_split_manifest.csv

Do not reset source-row identifiers after filtering or deduplication.

## Dialogue normalization and hashing

The recorded normalization is:

    re.sub(r"\s+", " ", str(text).strip().lower())

dialogue_hash is:

    hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()

For each retained primary record, verify the normalized source
dialogue against dialogue_hash in the supplied manifest.

The classifier input is normalized dialogue. Reference section text
is not used as query input.

## Labels

Use the manifest's retained label and the supplied source/preprocessing
code to verify source-label agreement.

Do not guess label-normalization rules or substitute an unrelated
specialty-label mapping.

## Deduplication, grouping, and filtering

The implementation sorts by source order and source-row position
before choosing representatives of exact dialogue/label duplicates.

Exact normalized-dialogue/label duplicates are reduced to one
representative. Records with the same normalized dialogue but
different labels are retained.

Reviewed near-duplicate pairs can share a group despite having
different dialogue hashes. Therefore, group_id must not be regenerated
from dialogue_hash alone.

Consult:
- final_cleaning_grouping_policy.json
- exact_duplicate_removal_log.csv
- near_duplicate_review_decisions.csv
- retained_conflicting_label_groups.csv
- rare_class_exclusion_log.csv

Use the supplied final manifests as the authoritative assignments
for reproducing reported evaluations.

## Primary and repeated partitions

Primary manifest:
artifacts/data_audit/constrained_split_manifest.csv

The primary cohort contains 1,288 records and 17 retained labels:
773 train, 258 validation, and 257 test.

Repeated manifests:
artifacts/supplementary_repeated_splits/seed_*/split_manifest.csv

Preserve record and group identifiers. Do not create fresh splits
as replacements for reported assignments.

## Additional-MTS evaluation

Source files:
MTS-Dialog-TestSet-1-MEDIQA-Chat-2023.csv
MTS-Dialog-TestSet-2-MEDIQA-Sum-2023.csv

For these additional records, source_csv_row is one-based:
source_csv_row 1 refers to dataframe.iloc[0].

This differs from the primary cohort's zero-based source_row.

Use evaluation_reference.csv for selected record/source mappings.
Use all_400_records_screening_audit__text_excluded.csv for screening
flags and exclusions.

Retain the provided record_id values rather than inventing replacements.
Use run_manifest.json and metrics.json for evaluation scope,
class-probability order, frozen policy, and limitations.

This analysis is an exploratory additional-MTS evaluation and must not
automatically be described as independent cross-dataset validation.

## Perturbation outputs

Files ending __text_excluded.csv omit specified dialogue-text fields.
See manifest/additional_artifact_export_log.json.

Recreating perturbed text requires the original input mapping,
transformation implementation, seeds, and recorded settings.

This guide does not claim that perturbation-text reconstruction
has been independently tested.

## Verification status

Source-mapping conventions were inspected in the implementation.
A fresh reconstruction of all input records from independently
obtained source CSVs has not yet been tested in this packaging workflow.

Historical provenance files are retained unchanged. Their presence
does not, by itself, establish licensing approval or independent
verification of every source byte.
