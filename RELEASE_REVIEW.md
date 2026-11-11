\# Release preparation review



Review date: 2026-11-09



\## Archive status



Zenodo DOI reserved: 10.5281/zenodo.24084026



At the time of this review, the Zenodo record is a draft.

DOI reservation does not establish publication or public access.



\## Completed package checks



\- Both implementation notebooks were backed up outside the package.

\- Both notebooks have no saved code-cell outputs or execution counts.

\- Notebook-level widget metadata is absent.

\- Comparison against the backups confirmed that notebook cells were

&#x20; preserved; only widget metadata was removed where present.



\- The frozen protocol and separately saved validation policies were

&#x20; inspected. All nine policy entries, policy-selection settings,

&#x20; and uncertainty configurations agreed in the inspected contents.



\- The primary split manifest contains 1,288 records and includes

&#x20; record identifiers, source mappings, labels, dialogue hashes,

&#x20; group identifiers, and split assignments.

\- The calibration manifest contains 773 records and includes

&#x20; record identifiers, group identifiers, labels, and fold assignments.

\- Both manifest SHA-256 hashes match the frozen protocol.



\- Each of nine methods in the primary prediction CSV has exactly

&#x20; 257 unique test record identifiers.

\- Each of four methods in the native acceptance audit has exactly

&#x20; 257 unique test record identifiers.

\- No missing, non-test, or duplicated identifiers were found

&#x20; within those method-specific checks.



\- All eight CSV columns flagged in the historical sharing report

&#x20; were identified as dialogue\_hash columns. All their values

&#x20; passed a 64-character hexadecimal-format check.

\- All 16 current text-excluded CSVs lack columns named dialogue,

&#x20; query, or perturbed\_text.

\- The corresponding original CSVs and files named

&#x20; inference\_inputs.csv were not found under artifacts/.



\## Scope and limitations



These are limited release-preparation checks, not comprehensive

privacy, security, legal, or scientific validation.



Historical array-schema reports were inspected. This does not

constitute a fresh inspection of every current array value.



Notebook source, Markdown, metadata, attachments, JSON values,

and all other artifact contents have not been comprehensively

cleared for sharing by the checks recorded here.



Machine-specific notebook paths remain. The notebooks are historical

implementation materials, not a tested Run all workflow.



The package must not be described as fully independently reproduced

or as a verified clean-environment end-to-end inference release.



Historical reports under manifest/ are retained as provenance and

may describe earlier package states.



\## GitHub public-access check



On 2026-11-09, the depositor opened

https://github.com/pavan242batu-hub/CRUS-Reproducibility

in a signed-out private/incognito browser window.



The repository and updated README were visible. The README

displayed reserved Zenodo DOI 10.5281/zenodo.24084026 and

identified the Zenodo record as an unpublished draft.



This confirms GitHub repository and README accessibility only.

It does not confirm publication of the Zenodo deposit, access

to its final files, or completion of sharing review.



\## Remaining release tasks



\- Resolve the remaining manual sharing and distribution review.

\- Finalize README access and release-status statements.

\- Add the archive DOI to the manuscript Code Availability section.

\- Refresh the final inventory and checksums after all file edits.

\- Create and inspect the final archive.

\- Upload and publish the final Zenodo deposit.

\- Test public access to the published record and files.

\- After Zenodo publication, update the GitHub README, manuscript

&#x20; availability statement, and reviewer response to identify the

&#x20; published deposit and confirmed access.

## Notebook preparation addendum ? 2026-11-11

This addendum updates the notebook-preparation scope. It does not certify
publication, manual sharing/privacy review, or full scientific reproduction.

Both canonical implementation notebooks were prepared and provided with
specific release guides. Temporary preparation copies and repair reports
were retained outside the release package.

Completed checks:

- Main pipeline: structure and IPython-aware syntax for 244 nonempty code cells.
- External-transfer notebook: structure and IPython-aware syntax for
  324 nonempty code cells.
- Main pipeline Stage 2 to Stage 3 path/service-normalised source comparison.
- External notebook: 252 original shared cells verified; 243 shared updated
  code cells compared excluding its extended helper; 79 external-tail code
  cells compared after intended path/service normalisation.
- Complete guarded external prediction function preserved unchanged.
- Frozen split manifest: 1,288 records, 1,285 groups, no cross-split groups.
- Split sizes: train 773, validation 258, test 257.
- Case-level prediction consistency: 2,313 rows.
- Frozen CRUS acceptance consistency: SingleStageFull 118,
  SingleStageTruncated 115, Cascade 117, LengthNormLegacy 113 accepted
  primary-test records.
- Checksums verified for 260 inventoried artifact files.
- Limited setup/helper execution passed, including opt-in copying guards,
  working-copy checksums, canonical notebook inspection snapshots, and
  explicit local-file selection using a synthetic CSV.

Historical saved outputs were not regenerated. No training or external
prediction was executed during these checks. Missing raw inputs,
checkpoints, or intermediate runtime state must not be silently substituted.

The machine-readable scope is recorded in
`manifest/notebook_preparation_validation.json`.

Historical `manifest/package_status.json` and
`manifest/consistency_validation.json` are retained unchanged as provenance.
Their earlier flags must not be interpreted as a current comprehensive
assessment, nor automatically changed to True because narrower checks passed.

Still pending for final deposit preparation: final release-file inventory
and checksum refresh, manual sharing review, confirmation of online access
statements, archive publication, and DOI/public-access verification.

## Sharing-review follow-up ? 2026-11-11

The uploader reported visual review of all four packaged risk--coverage
PNG/PDF files with no patient details, credentials, or confidential
annotations identified.

The two table-source contents supplied in conversation contained aggregate
research statistics and LaTeX formatting. The two flagged JSON `note`
values matched the expected explanatory metadata. The local 386-record
prediction JSONL matched the inspected source copy.

The uploader then confirmed:
"Sharing permissions reviewed?no unresolved restrictions."

The scope and reviewed-file hashes are recorded in
`manifest/sharing_review.json`. This follow-up records the reported review
outcome; it does not assert institutional approval, exhaustive inspection
of every possible disclosure, independent legal clearance, or complete
scientific reproduction.

Earlier pending-review statements in this document describe the state
before this follow-up and should be read chronologically. Historical
status JSON records are retained unchanged.

Online publication and public-access verification remain separate steps.
