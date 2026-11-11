# Additional-analysis artifact exports

Files were selected from additional_analysis_candidates.csv.

CSV derivatives ending __text_excluded.csv omit only the columns
listed in manifest/additional_artifact_export_log.json.
Source experimental files remain unchanged.

inference_inputs.csv is not included because its query field contains
input text. Dataset reconstruction/access instructions remain required.

The JSONL prediction file was checked for expected top-level fields
in every nonempty record. This is a schema check, not a privacy audit.

Unchanged JSON metadata may reference checksums of source files that
are excluded or represented by derivatives. Those historical checksum
references remain intact. The export log records derivative checksums.

All included analyses still require manuscript mapping and sharing review.
Copying an artifact does not establish that its metrics were regenerated.
