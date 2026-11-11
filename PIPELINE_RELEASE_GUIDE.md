# Pipeline notebook release guide

## Purpose and structure

`revised_risk_aware_hybrid_pipeline_v2.ipynb` is the implementation notebook
prepared for the revision deposit. It retains historical experiments,
corrected revision implementation, and later audit/supplementary sections.
It is not a verified linear Run All workflow.

The initial/legacy configuration and displayed results are not replacements
for the final frozen primary protocol. The authoritative archived evidence is:

- `../artifacts/corrected_experiment_outputs/final_pretest_protocol.json`
- `../artifacts/data_audit/constrained_split_manifest.csv`
- `../artifacts/corrected_experiment_outputs/test_all_method_predictions.csv`
- `../artifacts/corrected_experiment_outputs/test_frozen_CRUS_acceptance_audit.csv`

Existing saved outputs are historical, not results of a new execution of
the portability-prepared notebook.

## Reproduce metrics from saved predictions

Use the standalone scripts and environment instructions in
`../REPRODUCING_RESULTS.md`. From the extracted package root, the documented
primary commands on Windows are:

```powershell
py scripts/regenerate_primary_metrics.py --package-root .
py scripts/verify_matched_rankings.py --package-root .
```

These write regenerated outputs; they do not rerun model inference.
Review their documented output locations before execution.

## Raw inputs and source version

Raw dialogue inputs are omitted from this package selection. Follow
`../DATA_RECONSTRUCTION.md` and the provenance in
`../artifacts/source_data/source_manifest.json`.

Use the recorded source commit and verify input-file checksums. Do not
silently use a different repository version. Consult the source dataset's
licence and attribution requirements separately from this package's code
licence. Omission is not a claim that redistribution is prohibited.

The default raw-input location is:

`<package-root>/local_inputs/MTS-Dialog/Main-Dataset`

That directory must directly contain the training and validation CSVs.

## Configurable paths

Set environment variables before starting the notebook kernel, when needed:

| Variable | Meaning |
|---|---|
| `CRUS_PACKAGE_ROOT` | Extracted package root, containing artifacts and notebooks |
| `CRUS_RAW_DATA_ROOT` | Directory directly containing the two source CSVs |
| `CRUS_MTS_REPO_ROOT` | Local checkout of the recorded dataset repository |
| `CRUS_RUN_OUTPUT_ROOT` | Separate directory for new execution outputs |
| `CRUS_ALLOW_ARTIFACT_COPY` | Set to `1` only when explicitly enabling audit-workspace copying |

Start the notebook frontend from the extracted package using the intended
Python environment. Package discovery can use the current working directory
and its parents, or the explicit package-root variable.

The initial/revision pipeline requires the relevant scientific dependencies.
Syntax validation does not establish that those dependencies are installed
or compatible. Historical notebook installation cells are not a complete
environment lockfile; consult the package environment documentation.

## Section setup and output isolation

Cell numbers are 1-based saved-notebook positions:

- Cell 7 defines package, raw-input, and initial-output paths.
- Cell 41 defines the new revision-pipeline output workspace.
- Cell 110 defines support for later saved-artifact audit paths.

Use the relevant section with its required setup and variables. These
instructions do not assert that arbitrary cells can run independently.

New outputs default to a timestamped directory under `local_runs/`.
Later legacy audit paths are redirected to a separate working copy under:

`<run-output-root>/saved_artifact_audits`

Copying requires explicit opt-in. The helper verifies inventoried source
hashes and copied-file hashes. It refuses to initialise a nonempty audit
workspace in a new session rather than silently reusing modified inputs.

The helper also copies the canonical notebook for source inspection.
That snapshot is not proof that the revised source originally generated
the archived predictions.

Missing checkpoints, raw inputs, intermediate variables, or other omitted
components must be reported. They must not be silently regenerated or
substituted merely to make an audit pass.

## Verification scope: 2026-11-11

Completed checks:

- Notebook structure and IPython-aware syntax: 244 nonempty code cells.
- Stage 2 to Stage 3 normalised algorithm-source comparison.
- Checksums for 260 inventoried artifact files.
- Split manifest: 1,288 records and 1,285 groups, with no cross-split groups.
- Split sizes: train 773, validation 258, test 257.
- Case-level prediction consistency: 2,313 rows.
- Frozen CRUS acceptance consistency:
  SingleStageFull 118, SingleStageTruncated 115,
  Cascade 117, LengthNormLegacy 113 accepted test records.
- Limited execution of path setup and workspace support, including opt-in
  blocking and verification of copied artifacts against originals.

Not established by those checks:

- Full top-to-bottom notebook execution.
- Fresh-environment end-to-end model training or inference.
- Successful execution of every supplementary experiment or historical audit.
- A complete dependency lockfile or verification of every operating system.

## Before publishing the package

Exclude local raw inputs, new experiment outputs, temporary notebook
candidates, backups, helper scripts, and internal repair reports from the
upload selection. Git ignore rules do not remove files from a ZIP archive.

Finalise the package inventories and checksums after selecting the release
files. Then update the README and manuscript Code Availability statement
to match the actual published repository status and DOI.
