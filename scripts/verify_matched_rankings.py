from pathlib import Path
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument(
    "--package-root",
    type=Path,
    default=Path(__file__).resolve().parents[1]
)
args = parser.parse_args()

root = args.package_root.resolve()
base = root / "artifacts/corrected_experiment_outputs"
output = root / "regenerated"
output.mkdir(exist_ok=True)

pred = pd.read_csv(
    base / "test_all_method_predictions.csv",
    dtype={"record_id": "string"}
)
saved = pd.read_csv(
    base / "comment4_audit/comment4_verified_matched_counts.csv"
)

keys = ["method", "target_n_accepted"]

if pred.duplicated(["record_id", "method"]).any():
    raise ValueError("Duplicate prediction keys.")

if saved.duplicated(keys).any():
    raise ValueError("Duplicate saved matched-count keys.")

required = ["record_id", "method", "true_label", "prediction", "ranking_score"]

if pred[required].isna().any().any():
    raise ValueError("Missing identifiers, labels, or ranking scores.")

pred["ranking_score"] = pd.to_numeric(
    pred["ranking_score"], errors="raise"
)

if not np.isfinite(pred["ranking_score"]).all():
    raise ValueError("Nonfinite ranking scores.")

if not set(saved["method"]).issubset(set(pred["method"])):
    raise ValueError("Saved table contains an unknown method.")

rows = []

for method, targets in saved.groupby("method"):
    part = pred.loc[pred["method"] == method].copy()

    ranked = part.sort_values(
        ["ranking_score", "record_id"],
        ascending=[False, True],
        kind="mergesort"
    )

    for target_value in sorted(targets["target_n_accepted"].unique()):
        k = int(target_value)

        if k != target_value or not 0 < k <= len(ranked):
            raise ValueError(f"Invalid target: {method}, {target_value}")

        selected = ranked.head(k)
        n = len(ranked)
        correct = int(
            selected["true_label"].eq(selected["prediction"]).sum()
        )

        rows.append({
            "method": method,
            "target_n_accepted": k,
            "N": n,
            "n_accepted": k,
            "n_correct_accepted": correct,
            "n_errors_accepted": k - correct,
            "n_abstained": n - k,
            "coverage": k / n,
            "selective_accuracy": correct / k,
            "accepted_misclassification_rate": (k - correct) / k,
            "forced_accuracy": float(
                ranked["true_label"].eq(ranked["prediction"]).mean()
            ),
            "abstention_penalized_accuracy": correct / n,
            "abstention_penalized_error": 1 - correct / n
        })

regenerated = pd.DataFrame(rows)

regenerated.to_csv(
    output / "matched_rankings_all_targets.csv", index=False
)

comparison = saved.merge(
    regenerated,
    on=keys,
    how="outer",
    suffixes=("_saved", "_regenerated"),
    validate="one_to_one",
    indicator=True
)

if not comparison["_merge"].eq("both").all():
    raise ValueError("Saved and regenerated result keys do not match.")

integer_fields = [
    "N", "n_accepted", "n_correct_accepted",
    "n_errors_accepted", "n_abstained"
]
float_fields = [
    "coverage", "selective_accuracy",
    "accepted_misclassification_rate", "forced_accuracy",
    "abstention_penalized_accuracy", "abstention_penalized_error"
]

checks = []

for field in integer_fields + float_fields:
    a = comparison[f"{field}_saved"]
    b = comparison[f"{field}_regenerated"]

    matches = (
        a.eq(b).to_numpy()
        if field in integer_fields
        else np.isclose(
            a.to_numpy(dtype=float),
            b.to_numpy(dtype=float),
            rtol=0,
            atol=1e-10,
            equal_nan=False
        )
    )

    checks.append({
        "metric": field,
        "rows_compared": len(comparison),
        "mismatched_rows": int((~matches).sum()),
        "max_absolute_difference": float(
            np.max(np.abs(a.to_numpy(dtype=float)
                          - b.to_numpy(dtype=float)))
        )
    })

report = pd.DataFrame(checks)
report.to_csv(
    output / "matched_rankings_agreement_report.csv",
    index=False
)

print("Regenerated rows:", len(regenerated))
print(
    "Targets:",
    sorted(regenerated["target_n_accepted"].unique().tolist())
)
print(report.to_string(index=False))

if report["mismatched_rows"].sum():
    raise RuntimeError(
        "Differences detected. Inspect them without altering source artifacts."
    )

print("PASS: All compared counts and metrics agree within stated tolerance.")
print("Boundary-tie diagnostics and calibration metrics were not compared.")
