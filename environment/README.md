# Recorded environment information

The JSON files in this directory were extracted from saved experiment
protocols, not from the current packaging runtime.

requirements-recorded-candidate.txt is an untested candidate list.
It is not a complete dependency lockfile.

Before using it:
- Verify that entries are Python distribution names, not import aliases.
- Separate Python/runtime versions from pip-installable packages.
- Check missing dependencies and installation-specific packages.
- Document the required Python version and hardware/runtime details.
- Test installation and metric regeneration in a separate environment.
- Do not change frozen experimental artifacts to match a new environment.


## Repeated-run environment records

Additional package-version records were located in each seed's
experiment_outputs/retrieval_initialization_metadata.json and copied
unchanged into the package.

primary_vs_repeated_recorded_versions.csv compares these records with
the primary protocol. MATCH means the recorded version strings agree;
it does not establish a complete or tested environment specification.
MedCPT baseline environment records are separate and are not used to
infer the main experiment environment.
