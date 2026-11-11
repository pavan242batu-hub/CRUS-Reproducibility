from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform

import numpy as np
import pandas as pd
import scipy
from scipy.stats import mannwhitneyu

# ---------------- Configuration ----------------

import argparse

parser = argparse.ArgumentParser(description="Regenerate final-cohort Table 13 from packaged saved predictions.")
parser.add_argument("--package-root", type=Path, required=True)
args = parser.parse_args()
PACKAGE_ROOT = args.package_root.resolve()
ROOT = PACKAGE_ROOT / "artifacts"
METHOD = "Cascade"

EXPECTED_N = 257
EXPECTED_CORRECT = 181
EXPECTED_INCORRECT = 76

BOOTSTRAP_REPLICATES = 10000
BOOTSTRAP_SEED = 20261029

if not ROOT.is_dir():
    raise FileNotFoundError(f"Missing artifacts directory: {ROOT}")

PRED_PATH = (
    ROOT / "corrected_experiment_outputs"
    / "test_all_method_predictions.csv"
)
CRUS_PATH = (
    ROOT / "corrected_experiment_outputs"
    / "test_frozen_CRUS_acceptance_audit.csv"
)
MANIFEST_PATH = ROOT / "data_audit/constrained_split_manifest.csv"
PROTOCOL_PATH = (
    ROOT / "corrected_experiment_outputs"
    / "final_pretest_protocol.json"
)

for path in [PRED_PATH, CRUS_PATH, MANIFEST_PATH, PROTOCOL_PATH]:
    if not path.is_file():
        raise FileNotFoundError(path)

# ---------------- Helpers ----------------

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def parse_boolean(series, name):
    values = series.astype("string").str.strip().str.lower()
    mapping = {
        "true": True, "false": False,
        "1": True, "0": False,
        "1.0": True, "0.0": False
    }
    require(
        values.isin(mapping).all(),
        f"Invalid or missing Boolean values in {name}."
    )
    return values.map(mapping).astype(bool)

source_paths = {
    "predictions": PRED_PATH,
    "crus_audit": CRUS_PATH,
    "manifest": MANIFEST_PATH,
    "protocol": PROTOCOL_PATH
}
input_hashes = {
    name: sha256(path) for name, path in source_paths.items()
}

# ---------------- Read and verify cohort ----------------

pred_all = pd.read_csv(PRED_PATH, dtype={"record_id": "string"})
audit_all = pd.read_csv(CRUS_PATH, dtype={"record_id": "string"})
manifest = pd.read_csv(
    MANIFEST_PATH,
    dtype={"record_id": "string", "group_id": "string"}
)
protocol = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))

require(
    protocol.get("main_manifest_sha256") == input_hashes["manifest"],
    "Manifest checksum does not match the frozen primary protocol."
)

require(
    not manifest["record_id"].duplicated().any(),
    "Duplicate record IDs in the full manifest."
)
require(
    manifest[["record_id", "group_id", "split", "label"]]
    .notna().all().all(),
    "Missing required manifest values."
)
require(
    manifest.groupby("group_id")["split"].nunique().le(1).all(),
    "A group crosses manifest partitions."
)

test = manifest.loc[
    manifest["split"].eq("test"),
    ["record_id", "group_id", "label"]
].copy()

pred = pred_all.loc[pred_all["method"].eq(METHOD)].copy()
audit = audit_all.loc[audit_all["method"].eq(METHOD)].copy()

require(len(test) == EXPECTED_N, "Unexpected manifest test size.")

test_ids = set(test["record_id"])

for name, frame in [("predictions", pred), ("CRUS audit", audit)]:
    require(
        frame["record_id"].notna().all(),
        f"Missing record IDs in {name}."
    )
    require(
        not frame["record_id"].duplicated().any(),
        f"Duplicate Cascade record IDs in {name}."
    )
    require(
        set(frame["record_id"]) == test_ids,
        f"Cascade IDs in {name} differ from final test IDs."
    )

require(
    pred[["true_label", "prediction"]].notna().all().all(),
    "Missing prediction labels."
)

pred["computed_correct"] = pred["true_label"].eq(pred["prediction"])

require(
    (
        parse_boolean(pred["correct"], "prediction correct")
        == pred["computed_correct"]
    ).all(),
    "Saved prediction correctness disagrees with labels."
)

audit["audit_correct"] = parse_boolean(
    audit["correct"], "CRUS-audit correct"
)

final = (
    test.merge(
        pred[[
            "record_id", "true_label", "prediction",
            "computed_correct"
        ]],
        on="record_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        audit[["record_id", "CRUS", "audit_correct"]],
        on="record_id",
        how="left",
        validate="one_to_one"
    )
    .sort_values("record_id")
    .reset_index(drop=True)
)

require(
    final["label"].eq(final["true_label"]).all(),
    "Prediction reference labels differ from manifest labels."
)
require(
    final["audit_correct"].eq(final["computed_correct"]).all(),
    "CRUS-audit correctness disagrees with final predictions."
)

final["CRUS"] = pd.to_numeric(final["CRUS"], errors="raise")
require(
    np.isfinite(final["CRUS"]).all(),
    "CRUS contains nonfinite values."
)
require(
    final["CRUS"].between(0, 1).all(),
    "CRUS falls outside the documented [0, 1] range."
)

n_correct = int(final["computed_correct"].sum())
n_incorrect = int((~final["computed_correct"]).sum())

require(
    len(final) == EXPECTED_N
    and n_correct == EXPECTED_CORRECT
    and n_incorrect == EXPECTED_INCORRECT,
    (
        f"Unexpected final cohort: N={len(final)}, "
        f"correct={n_correct}, incorrect={n_incorrect}. "
        "Stop and investigate; do not force these counts."
    )
)

# ---------------- Descriptive statistics ----------------

correct_scores = final.loc[final["computed_correct"], "CRUS"].to_numpy()
incorrect_scores = final.loc[~final["computed_correct"], "CRUS"].to_numpy()

summary = pd.DataFrame([
    {
        "subset": name,
        "n": len(values),
        "mean_CRUS": float(np.mean(values)),
        "sd_CRUS": float(np.std(values, ddof=1)),
        "median_CRUS": float(np.median(values)),
        "minimum_CRUS": float(np.min(values)),
        "maximum_CRUS": float(np.max(values))
    }
    for name, values in [
        ("Correct predictions", correct_scores),
        ("Incorrect predictions", incorrect_scores)
    ]
])

delta = float(incorrect_scores.mean() - correct_scores.mean())

# ---------------- Group-bootstrap mean difference ----------------

codes, group_names = pd.factorize(final["group_id"], sort=True)
n_groups = len(group_names)

correct_mask = final["computed_correct"].to_numpy(dtype=bool)
scores = final["CRUS"].to_numpy(dtype=float)

correct_counts = np.bincount(
    codes, weights=correct_mask.astype(int), minlength=n_groups
)
incorrect_counts = np.bincount(
    codes, weights=(~correct_mask).astype(int), minlength=n_groups
)
correct_sums = np.bincount(
    codes, weights=scores * correct_mask, minlength=n_groups
)
incorrect_sums = np.bincount(
    codes, weights=scores * (~correct_mask), minlength=n_groups
)

rng = np.random.default_rng(BOOTSTRAP_SEED)
bootstrap_delta = np.full(BOOTSTRAP_REPLICATES, np.nan)

for b in range(BOOTSTRAP_REPLICATES):
    sampled = rng.integers(0, n_groups, size=n_groups)

    nc = correct_counts[sampled].sum()
    ni = incorrect_counts[sampled].sum()

    if nc > 0 and ni > 0:
        bootstrap_delta[b] = (
            incorrect_sums[sampled].sum() / ni
            - correct_sums[sampled].sum() / nc
        )

valid = bootstrap_delta[np.isfinite(bootstrap_delta)]
require(
    len(valid) >= int(0.99 * BOOTSTRAP_REPLICATES),
    "Too many bootstrap replicates have an empty correctness subset."
)

ci_low, ci_high = np.quantile(valid, [0.025, 0.975])

# ---------------- Mann–Whitney and effect size ----------------

test_result = mannwhitneyu(
    incorrect_scores,
    correct_scores,
    alternative="two-sided",
    method="asymptotic",
    use_continuity=True
)

u_incorrect_first = float(test_result.statistic)
p_value = float(test_result.pvalue)

rank_biserial = (
    2 * u_incorrect_first / (n_incorrect * n_correct) - 1
)

group_sizes = final.groupby("group_id").size()
mixed_groups = (
    final.groupby("group_id")["computed_correct"].nunique() > 1
).sum()

# ---------------- Save new outputs only ----------------

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
OUT = PACKAGE_ROOT / "regenerated" / f"editor_table13_final_cohort_{stamp}"
OUT.mkdir(parents=True, exist_ok=False)

summary.to_csv(OUT / "table13_crus_summary.csv", index=False)

final[[
    "record_id", "group_id", "label", "prediction",
    "computed_correct", "CRUS"
]].to_csv(OUT / "table13_final_case_audit.csv", index=False)

np.savez_compressed(
    OUT / "table13_bootstrap_mean_difference.npz",
    mean_difference=bootstrap_delta
)

metadata = {
    "analysis": "Primary Cascade CRUS by forced-prediction correctness",
    "n_test": len(final),
    "n_correct": n_correct,
    "n_incorrect": n_incorrect,
    "mean_correct": float(correct_scores.mean()),
    "mean_incorrect": float(incorrect_scores.mean()),
    "difference_direction": "incorrect minus correct",
    "mean_difference": delta,
    "mean_difference_95_ci": [float(ci_low), float(ci_high)],
    "bootstrap": {
        "unit": "assigned test group_id",
        "group_sampling": "sample G groups with replacement per replicate",
        "within_group": "retain all records; record-weighted subset means",
        "replicates_attempted": BOOTSTRAP_REPLICATES,
        "replicates_valid": len(valid),
        "replicates_empty_subset": int(
            BOOTSTRAP_REPLICATES - len(valid)
        ),
        "seed": BOOTSTRAP_SEED,
        "interval": "2.5 and 97.5 percentiles; numpy linear quantiles",
        "fixed": "model, split, predictions, correctness, CRUS, group assignments"
    },
    "groups": {
        "n_groups": n_groups,
        "maximum_group_size": int(group_sizes.max()),
        "groups_with_both_correct_and_incorrect": int(mixed_groups)
    },
    "mann_whitney": {
        "first_sample": "incorrect predictions",
        "second_sample": "correct predictions",
        "U": u_incorrect_first,
        "p_two_sided": p_value,
        "method": "asymptotic; tie correction; continuity correction",
        "scope": (
            "Exploratory record-level test; assumes independent samples; "
            "not cluster-adjusted and not multiplicity-adjusted."
        )
    },
    "rank_biserial": {
        "value": float(rank_biserial),
        "formula": "2*U_incorrect_first/(n_incorrect*n_correct)-1",
        "positive_direction": "higher CRUS among incorrect predictions"
    },
    "input_sha256": input_hashes,
    "versions": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__
    },
    "limitations": [
        "Post-test descriptive/exploratory analysis.",
        "Conditional group-bootstrap interval excludes model-refitting uncertainty.",
        "Assigned groups may not capture all related-record dependence.",
        "Mann–Whitney p-value is not a group-adjusted inferential result.",
        "Correctness separation does not establish optimal weights or clinical utility."
    ]
}

(OUT / "table13_analysis_metadata.json").write_text(
    json.dumps(metadata, indent=2), encoding="utf-8"
)

table_lines = [
    r"\begin{table}[ht]",
    r"\centering",
    (
        r"\caption{CRUS by forced-prediction correctness for Cascade "
        r"on the final primary test cohort ($N=257$). "
        r"All cases are included, irrespective of acceptance.}"
    ),
    r"\label{tab:crus}",
    r"\begin{tabular}{lrr}",
    r"\hline",
    r"Subset & Mean CRUS & Number of cases \\",
    r"\hline",
    f"Correct predictions & {correct_scores.mean():.6f} & {n_correct}" + r" \\",
    f"Incorrect predictions & {incorrect_scores.mean():.6f} & {n_incorrect}" + r" \\",
    r"\hline",
    r"\end{tabular}",
    r"\end{table}"
]

(OUT / "table13_replacement.tex").write_text(
    "\n".join(table_lines), encoding="utf-8"
)

direction = (
    "higher" if delta > 0 else "lower" if delta < 0 else "equal"
)

paragraph = (
    f"The final primary test cohort comprised 257 Cascade forced "
    f"predictions, including {n_correct} correct and {n_incorrect} incorrect "
    f"predictions. Mean CRUS was {correct_scores.mean():.6f} for correct "
    f"predictions and {incorrect_scores.mean():.6f} for incorrect predictions. "
    f"The mean difference (incorrect minus correct) was {delta:.6f}, "
    f"with a conditional 95% group-bootstrap percentile interval of "
    f"[{ci_low:.6f}, {ci_high:.6f}] based on {len(valid):,} valid replicates. "
    f"An exploratory two-sided Mann–Whitney comparison, with incorrect "
    f"cases as the first sample, gave U={u_incorrect_first:.6f}, "
    f"p={p_value:.6g}, and signed rank-biserial effect "
    f"r={rank_biserial:.6f}. The record-level p-value is not cluster-adjusted. "
    f"Observed mean CRUS was {direction} among incorrect predictions. "
    f"This analysis characterizes association with prediction correctness "
    f"within the fixed primary evaluation; it does not establish optimal "
    f"weights, independent external validity, or clinical harm reduction."
)

(OUT / "crus_signal_quality_replacement.txt").write_text(
    paragraph, encoding="utf-8"
)

response = (
    "Thank you for identifying the historical-result inconsistency. "
    "We regenerated Table 13 and the CRUS Signal Quality analysis from "
    "the final primary Cascade case-level predictions, verifying "
    "257 unique test records: 181 correct and 76 incorrect forced predictions. "
    f"The regenerated means are {correct_scores.mean():.6f} and "
    f"{incorrect_scores.mean():.6f}; the mean difference (incorrect minus "
    f"correct) is {delta:.6f}, with a conditional 95% group-bootstrap "
    f"interval [{ci_low:.6f}, {ci_high:.6f}]. "
    f"The exploratory two-sided Mann–Whitney statistic is "
    f"U={u_incorrect_first:.6f}, p={p_value:.6g}, with signed rank-biserial "
    f"effect r={rank_biserial:.6f}. The resampling unit, test convention, "
    "and conditional/dependence limitations are documented. "
    "[After editing the manuscript, confirm: We replaced the obsolete "
    "259-case table and historical inferential values and revised all "
    "associated interpretations.]"
)

(OUT / "editor_response_draft.txt").write_text(
    response, encoding="utf-8"
)

# Verify that source files have not changed.
require(
    all(sha256(path) == input_hashes[name]
        for name, path in source_paths.items()),
    "An input file changed during analysis."
)

checksum_lines = [
    f"{sha256(path)}  {path.name}"
    for path in sorted(OUT.iterdir())
    if path.is_file()
]

(OUT / "SHA256SUMS.txt").write_text(
    "\n".join(checksum_lines) + "\n", encoding="utf-8"
)

print("FINAL COHORT CHECK: PASSED")
print("N:", len(final))
print("Correct:", n_correct)
print("Incorrect:", n_incorrect)
print("Assigned test groups:", n_groups)
print("Maximum group size:", int(group_sizes.max()))
print("\nREGENERATED TABLE 13")
print(summary.to_string(index=False))

print("\nINFERENTIAL / EFFECT SUMMARY")
print("Mean difference, incorrect minus correct:", delta)
print("95% group-bootstrap CI:", [float(ci_low), float(ci_high)])
print("Valid bootstrap replicates:", len(valid))
print("Mann–Whitney U, incorrect sample first:", u_incorrect_first)
print("Two-sided exploratory p-value:", p_value)
print("Signed rank-biserial effect:", rank_biserial)

print("\nOUTPUT DIRECTORY:", OUT)
print("Original source files unchanged.")
print("No model inference or threshold selection performed.")