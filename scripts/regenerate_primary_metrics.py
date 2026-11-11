from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

parser = argparse.ArgumentParser()
parser.add_argument(
    "--package-root",
    type=Path,
    default=Path(__file__).resolve().parents[1]
)
args = parser.parse_args()

root = args.package_root.resolve()
artifacts = root / "artifacts"
results = root / "regenerated"
results.mkdir(exist_ok=True)

def read(name):
    return pd.read_csv(
        artifacts / "corrected_experiment_outputs" / name,
        dtype={"record_id": "string"}
    )

def booleans(series, field):
    values = series.astype("string").str.strip().str.lower()
    mapping = {"true": True, "false": False, "1": True, "0": False}
    if not values.isin(mapping).all():
        raise ValueError(f"Invalid or missing Boolean values in {field}")
    return values.map(mapping).astype(bool)

pred = read("test_all_method_predictions.csv")
manifest = pd.read_csv(
    artifacts / "data_audit/constrained_split_manifest.csv",
    dtype={"record_id": "string"}
)

if pred.duplicated(["record_id", "method"]).any():
    raise ValueError("Duplicate prediction keys.")

if pred[["record_id", "method", "true_label", "prediction"]].isna().any().any():
    raise ValueError("Missing prediction identifiers or labels.")

classes = sorted(manifest["label"].dropna().unique())
test_ids = set(
    manifest.loc[manifest["split"] == "test", "record_id"]
)

pred["computed_correct"] = pred["true_label"].eq(pred["prediction"])

if not (
    booleans(pred["correct"], "prediction correct")
    == pred["computed_correct"]
).all():
    raise ValueError("Saved correctness differs from label comparison.")

full_rows = []
for method, part in pred.groupby("method"):
    if set(part["record_id"]) != test_ids or len(part) != len(test_ids):
        raise ValueError(f"Incomplete or unexpected test coverage: {method}")

    full_rows.append({
        "method": method,
        "n_test": len(part),
        "n_correct": int(part["computed_correct"].sum()),
        "accuracy": accuracy_score(part["true_label"], part["prediction"]),
        "macro_f1_all_retained_labels": f1_score(
            part["true_label"],
            part["prediction"],
            labels=classes,
            average="macro",
            zero_division=0
        )
    })

pd.DataFrame(full_rows).to_csv(
    results / "primary_full_coverage_metrics.csv", index=False
)

reference = pred[
    ["record_id", "method", "computed_correct"]
]

def evaluate_audit(filename, policy_columns, output_name):
    audit = read(filename)
    keys = ["record_id", "method"] + policy_columns

    if audit.duplicated(keys).any():
        raise ValueError(f"Duplicate policy keys: {filename}")

    audit["accepted_bool"] = booleans(audit["accepted"], "accepted")

    joined = audit.merge(
        reference,
        on=["record_id", "method"],
        how="left",
        validate="many_to_one",
        indicator=True
    )

    if not joined["_merge"].eq("both").all():
        raise ValueError(f"Unlinked prediction rows: {filename}")

    if "correct" in joined:
        if not (
            booleans(joined["correct"], "audit correct")
            == joined["computed_correct"]
        ).all():
            raise ValueError(f"Correctness mismatch: {filename}")

    group_columns = ["method"] + policy_columns
    rows = []

    for key, part in joined.groupby(group_columns, dropna=False):
        key = key if isinstance(key, tuple) else (key,)
        identifiers = dict(zip(group_columns, key))

        if set(part["record_id"]) != test_ids:
            raise ValueError(f"Incomplete audit coverage: {identifiers}")

        selected = part.loc[part["accepted_bool"]]
        n = len(part)
        accepted = len(selected)
        correct = int(selected["computed_correct"].sum())

        row = {
            **identifiers,
            "n_test": n,
            "n_accepted": accepted,
            "n_correct_accepted": correct,
            "coverage": accepted / n,
            "accepted_accuracy": correct / accepted if accepted else np.nan,
            "selective_risk": (
                1 - correct / accepted if accepted else np.nan
            )
        }

        if "target_n_accepted" in identifiers:
            if accepted != int(identifiers["target_n_accepted"]):
                raise ValueError(
                    f"Accepted count differs from target: {identifiers}"
                )

        rows.append(row)

    pd.DataFrame(rows).to_csv(results / output_name, index=False)

evaluate_audit(
    "test_frozen_CRUS_acceptance_audit.csv",
    [],
    "primary_native_acceptance_metrics.csv"
)

evaluate_audit(
    "test_matched_count_acceptance_audit.csv",
    ["target_n_accepted"],
    "primary_matched_count_metrics.csv"
)

print("Regenerated files:")
for name in [
    "primary_full_coverage_metrics.csv",
    "primary_native_acceptance_metrics.csv",
    "primary_matched_count_metrics.csv"
]:
    print(name)

print("Saved correctness flags verified against labels and predictions.")
print("No model inference executed.")
print("Agreement with manuscript/saved summary values remains to be checked.")
