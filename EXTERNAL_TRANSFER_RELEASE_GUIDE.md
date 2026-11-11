# External-transfer implementation notebook: release guide

## Purpose and structure

`CRUS_R1_5_External_Transfer.ipynb` retains the shared pipeline, external-transfer
implementation, and historical audit, inspection, and packaging sections.

It is not a verified linear Run All workflow. The historical packaging cells
are retained source, not instructions to recreate or replace the current
release package. Review section dependencies before execution.

The complete guarded `predict_external_cascade` implementation is preserved
in saved cell 272. The preceding bodyless duplicate declaration was replaced
with comments; no placeholder prediction implementation was introduced.

## Shared setup

Consult `PIPELINE_RELEASE_GUIDE.md` for environment variables, raw-input
requirements, output isolation, and the supporting pipeline's verification
limits. That guide's cell numbers refer to the supporting notebook.

In this external-transfer notebook, saved 1-based positions are:

- Cell 8: package, raw-input, and initial-output paths.
- Cell 42: revision-pipeline output workspace.
- Cell 111: saved-artifact workspace support.
- Cell 272: complete guarded external prediction function.

No cells were inserted or removed during this preparation.

New outputs are separate from the deposited artifacts. Later historical
paths resolve to a working copy of inventoried artifacts. Copying requires
`CRUS_ALLOW_ARTIFACT_COPY=1` before kernel startup.

The extended helper snapshots both canonical implementation notebooks for
source inspection. These snapshots do not independently prove historical
execution provenance.

## Local file inspection

The schema-inspection section can use an explicit `INPUT_PATHS` list.

Alternatively, before starting the kernel, set `CRUS_INSPECTION_FILES` to a
JSON list of local filenames. For example, using an actual file you intend
to inspect:

```powershell
$env:CRUS_INSPECTION_FILES = '["C:/path/to/your/file.csv"]'
```

Replace that example path. No browser upload or automatic dataset download
is performed by the local selection helper. Selected files are read into
memory, so avoid unnecessarily large files.

The notebook-source selection cell uses this package's canonical external
notebook rather than requiring an upload from a browser.

## Data and frozen evidence

Follow `../DATA_RECONSTRUCTION.md` for the recorded primary dataset version
and checksum verification. Raw dialogue inputs are omitted from the package
selection; this is not a claim that redistribution is prohibited.

External datasets, model checkpoints, runtime variables, and intermediate
artifacts required by particular sections may need separate acquisition
or reconstruction. Do not silently substitute missing components.

Use the deposited frozen configurations, split/group assignments,
case-level predictions, and acceptance decisions as the archived evidence.
Use `../REPRODUCING_RESULTS.md` for standalone saved-prediction metric
regeneration. Shared historical configuration values are not substitutes
for the final frozen primary protocol.

## Checks completed on 2026-11-11

- Structure and IPython-aware syntax: 324 nonempty code cells.
- Original shared-prefix verification: 252 cells.
- Shared updated-code comparison, excluding the extended helper:
  243 code cells.
- External-tail path/service-normalised comparison: 79 code cells.
- Complete external prediction implementation preserved unchanged.
- Explicit artifact-copy opt-in blocking.
- Working-copy and archived-original checksum checks for 260 files.
- Inspection snapshots of both canonical notebooks matched their sources.
- Explicit local-file selection tested with a synthetic CSV.
- Missing local-file selection correctly rejected.

Limited path-setup/helper code was executed. Training, external prediction,
and the full notebook were not executed in these checks.

Not established: full external-transfer reproduction, fresh-environment
end-to-end inference, every historical audit, or all supplementary workflows.

Historical saved outputs were not regenerated. No claims of new model
performance follow from these preparation checks.
