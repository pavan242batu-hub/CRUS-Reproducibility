from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="Verify operating points and ranking curves from packaged saved outputs.")
parser.add_argument("--package-root", type=Path, required=True)
args = parser.parse_args()
PACKAGE_ROOT = args.package_root.resolve()
ROOT = PACKAGE_ROOT / "artifacts"
BASE = ROOT / "corrected_experiment_outputs"

FILES = {
    "protocol": BASE / "final_pretest_protocol.json",
    "predictions": BASE / "test_all_method_predictions.csv",
    "gates": BASE / "test_frozen_CRUS_acceptance_audit.csv",
    "saved_curves": BASE / "test_ranking_risk_coverage_curves.csv",
    "manifest": ROOT / "data_audit/constrained_split_manifest.csv",
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def as_bool(series):
    values = series.astype("string").str.strip().str.lower()
    mapping = {
        "true": True, "false": False,
        "1": True, "0": False,
        "1.0": True, "0.0": False
    }
    require(
        values.isin(mapping).all(),
        f"Invalid Boolean values in {series.name}."
    )
    return values.map(mapping).to_numpy(dtype=bool)

for path in FILES.values():
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing saved input: {path}\n"
            "Locate the saved file; do not regenerate model predictions."
        )

input_hashes = {
    name: sha256(path) for name, path in FILES.items()
}

protocol = json.loads(
    FILES["protocol"].read_text(encoding="utf-8")
)

require(
    input_hashes["manifest"] == protocol["main_manifest_sha256"],
    "Manifest checksum differs from the frozen protocol."
)
require(
    protocol["ranking_ties"] == "score descending; record ID ascending",
    "Unexpected ranking tie rule. Inspect the frozen protocol."
)

pred = pd.read_csv(
    FILES["predictions"],
    dtype={
        "record_id": "string",
        "method": "string",
        "true_label": "string",
        "prediction": "string",
    }
)
gates = pd.read_csv(
    FILES["gates"],
    dtype={"record_id": "string", "method": "string"}
)
manifest = pd.read_csv(
    FILES["manifest"],
    dtype={
        "record_id": "string",
        "label": "string",
        "split": "string",
    }
)
saved_curves = pd.read_csv(FILES["saved_curves"])

require(
    manifest[["record_id", "label", "split"]].notna().all().all(),
    "Missing manifest fields."
)
require(
    manifest["record_id"].is_unique,
    "Duplicate manifest IDs."
)

test = manifest.loc[
    manifest["split"].str.strip().str.lower().eq("test")
].set_index("record_id")

N = len(test)
require(
    N == 257 and N == int(protocol["split_sizes"]["test"]),
    "Unexpected primary test cohort."
)

required_pred = [
    "record_id", "method", "true_label",
    "prediction", "correct", "ranking_score"
]
require(
    set(required_pred).issubset(pred.columns),
    "Required prediction columns are missing."
)
require(
    pred[required_pred].notna().all().all(),
    "Missing prediction values."
)
require(
    not pred.duplicated(["method", "record_id"]).any(),
    "Duplicate method/record predictions."
)
require(
    not gates.duplicated(["method", "record_id"]).any(),
    "Duplicate native-gate audit records."
)

pred["ranking_score"] = pd.to_numeric(
    pred["ranking_score"], errors="raise"
)
require(
    np.isfinite(pred["ranking_score"]).all(),
    "Nonfinite ranking scores."
)

full_rows = []
curve_parts = []
prediction_groups = {}

# Reconstruct all ranking curves from the saved ranking score.
for method, part in pred.groupby("method", sort=True):
    part = part.copy()

    require(
        len(part) == N and set(part["record_id"]) == set(test.index),
        f"{method}: test IDs or size differ."
    )

    truth = test.loc[part["record_id"], "label"].to_numpy(dtype=str)

    require(
        np.array_equal(
            part["true_label"].to_numpy(dtype=str), truth
        ),
        f"{method}: reference labels disagree with manifest."
    )

    part["recomputed_correct"] = (
        part["prediction"].to_numpy(dtype=str) == truth
    )

    require(
        np.array_equal(
            as_bool(part["correct"]),
            part["recomputed_correct"].to_numpy()
        ),
        f"{method}: saved correctness disagrees with labels."
    )

    prediction_groups[method] = part.set_index("record_id")

    n_correct = int(part["recomputed_correct"].sum())

    full_rows.append({
        "method": method,
        "N": N,
        "correct": n_correct,
        "incorrect": N - n_correct,
        "accuracy": n_correct / N,
        "error": (N - n_correct) / N
    })

    ranked = part.sort_values(
        ["ranking_score", "record_id"],
        ascending=[False, True],
        kind="mergesort"
    )

    k = np.arange(1, N + 1)
    cumulative_correct = (
        ranked["recomputed_correct"].astype(int).cumsum().to_numpy()
    )

    curve_parts.append(pd.DataFrame({
        "method": method,
        "n_accepted": k,
        "n_correct_accepted": cumulative_correct,
        "n_errors_accepted": k - cumulative_correct,
        "coverage": k / N,
        "selective_accuracy": cumulative_correct / k,
        "risk": (k - cumulative_correct) / k,
        "abstention_penalized_accuracy": cumulative_correct / N
    }))

full = pd.DataFrame(full_rows)
curves = pd.concat(curve_parts, ignore_index=True)

require(
    {"Cascade", "SK4"}.issubset(prediction_groups),
    "Cascade or SK4 is missing."
)

# Check saved curves against independent reconstruction.
keys = ["method", "n_accepted"]
require(
    not saved_curves.duplicated(keys).any(),
    "Duplicate points in saved ranking curves."
)

old = saved_curves.set_index(keys).sort_index()
new = curves.set_index(keys).sort_index()

require(
    old.index.equals(new.index),
    "Saved and reconstructed curve keys differ."
)

curve_fields = [
    "n_correct_accepted", "n_errors_accepted",
    "coverage", "selective_accuracy", "risk",
    "abstention_penalized_accuracy"
]

for field in curve_fields:
    np.testing.assert_allclose(
        old[field].to_numpy(dtype=float),
        new[field].to_numpy(dtype=float),
        rtol=0,
        atol=1e-12,
        err_msg=f"Saved ranking curves disagree for {field}."
    )

# Verify every saved native CRUS gate.
gate_rows = []

for method, part in gates.groupby("method", sort=True):
    require(
        method in prediction_groups,
        f"Gate method {method} missing from predictions."
    )
    require(
        len(part) == N and set(part["record_id"]) == set(test.index),
        f"{method}: gate IDs or size differ."
    )

    pg = prediction_groups[method].sort_index()
    part = part.set_index("record_id").loc[pg.index].copy()
    policy = protocol["frozen_policies"][f"{method}:CRUS"]

    tc = float(policy["tau_c"])
    tu = float(policy["tau_u"])

    require(
        np.isfinite([tc, tu]).all(),
        f"{method}: invalid frozen thresholds."
    )

    for field in ["confidence", "CRUS", "tau_c", "tau_u"]:
        part[field] = pd.to_numeric(part[field], errors="raise")
        require(
            np.isfinite(part[field]).all(),
            f"{method}: invalid {field}."
        )

    np.testing.assert_allclose(
        part["tau_c"], tc, rtol=0, atol=1e-12
    )
    np.testing.assert_allclose(
        part["tau_u"], tu, rtol=0, atol=1e-12
    )

    accepted = (
        part["confidence"].ge(tc) & part["CRUS"].le(tu)
    ).to_numpy()

    require(
        np.array_equal(accepted, as_bool(part["accepted"])),
        f"{method}: saved acceptance differs from frozen policy."
    )

    correct = pg["recomputed_correct"].to_numpy(dtype=bool)

    require(
        np.array_equal(correct, as_bool(part["correct"])),
        f"{method}: gate-audit correctness differs."
    )

    a = int(accepted.sum())
    ca = int((accepted & correct).sum())
    ea = int((accepted & ~correct).sum())

    gate_rows.append({
        "method": method,
        "tau_c": tc,
        "tau_u": tu,
        "N": N,
        "accepted": a,
        "correct_accepted": ca,
        "accepted_errors": ea,
        "abstained": N - a,
        "coverage": a / N,
        "selective_accuracy": ca / a if a else np.nan,
        "selective_error": ea / a if a else np.nan,
        "penalized_accuracy": ca / N,
        "penalized_error": (ea + N - a) / N
    })

native = pd.DataFrame(gate_rows)
cascade = native.loc[native["method"].eq("Cascade")]
require(len(cascade) == 1, "Missing or duplicate Cascade gate.")
cascade = cascade.iloc[0]

require(
    np.isclose(cascade["tau_c"], 0, rtol=0, atol=1e-15)
    and np.isclose(
        cascade["tau_u"], 0.128165036474669,
        rtol=0, atol=1e-15
    ),
    "Unexpected primary Cascade thresholds."
)

require(
    (
        int(cascade["accepted"]),
        int(cascade["correct_accepted"]),
        int(cascade["accepted_errors"]),
        int(cascade["abstained"])
    ) == (117, 109, 8, 140),
    "Unexpected Cascade native-gate counts."
)

sk4 = full.loc[full["method"].eq("SK4")].iloc[0]
cascade_full = full.loc[full["method"].eq("Cascade")].iloc[0]

require(
    int(sk4["correct"]) == 82,
    "Unexpected SK4 full-coverage correct count."
)
require(
    int(cascade_full["correct"]) == 181,
    "Unexpected Cascade full-coverage correct count."
)

K = int(cascade["accepted"])
matched = curves.loc[curves["n_accepted"].eq(K)].copy()

cascade_ranked = matched.loc[matched["method"].eq("Cascade")].iloc[0]
require(
    int(cascade_ranked["n_correct_accepted"]) == 106,
    "Unexpected Cascade ranked top-117 result. Inspect the saved ranking."
)

# Save new audit outputs; never overwrite original results.
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
OUT = PACKAGE_ROOT / "regenerated" / f"editor_comment2_consistency_{stamp}"
OUT.mkdir(parents=True, exist_ok=False)

full.to_csv(OUT / "verified_full_coverage.csv", index=False)
native.to_csv(OUT / "verified_native_operating_points.csv", index=False)
curves.to_csv(OUT / "verified_ranking_curves.csv", index=False)
matched.to_csv(OUT / "verified_ranked_matched_count.csv", index=False)

fig, ax = plt.subplots(figsize=(9, 6))

for method, part in curves.groupby("method", sort=True):
    ax.plot(
        100 * part["coverage"],
        100 * part["risk"],
        label=method,
        linewidth=1.5
    )

ax.scatter(
    [100 * cascade["coverage"]],
    [100 * cascade["selective_error"]],
    color="black",
    marker="X",
    s=100,
    zorder=10,
    label="Cascade native CRUS gate (separate policy)"
)

ax.set_xlabel("Coverage (%)")
ax.set_ylabel("Selective misclassification rate (%)")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(alpha=0.25)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "risk_coverage_verified.pdf")
fig.savefig(OUT / "risk_coverage_verified.png", dpi=300)
plt.close(fig)

metadata = {
    "N": N,
    "ranking": protocol["ranking_ties"],
    "native_gate": "confidence >= tau_c AND CRUS <= tau_u",
    "source_sha256": input_hashes,
    "checks": {
        "manifest_matches_protocol": True,
        "all_prediction_ids_and_labels_verified": True,
        "all_saved_ranking_curve_points_verified": True,
        "all_saved_native_gate_decisions_verified": True
    },
    "scope": (
        "Numerical operating-point and ranking-curve audit only. "
        "Not a complete manuscript, threshold-sweep, or figure-asset audit."
    )
}

(OUT / "audit_metadata.json").write_text(
    json.dumps(metadata, indent=2), encoding="utf-8"
)

require(
    all(
        sha256(path) == input_hashes[name]
        for name, path in FILES.items()
    ),
    "An original input changed during the audit."
)

print("COMMENT 2 NUMERICAL AUDIT: PASSED")
print("\nFROZEN CASCADE THRESHOLDS")
print("tau_c =", repr(float(cascade["tau_c"])))
print("tau_u =", repr(float(cascade["tau_u"])))

print("\nFULL-COVERAGE RESULTS")
print(full.to_string(index=False))

print("\nNATIVE CRUS OPERATING POINTS")
print(native.to_string(index=False))

print("\nRANKED MATCHED-COUNT RESULTS")
print(
    matched[
        ["method", "n_accepted", "n_correct_accepted",
         "n_errors_accepted", "coverage", "risk"]
    ].to_string(index=False)
)

print("\nSK4 full-coverage error (%):", 100 * sk4["error"])
print("All saved ranking-curve points agree with reconstruction.")
print("All saved native gates agree with frozen thresholds.")
print("Original input files unchanged.")
print("No model training, inference, or threshold selection performed.")
print("Output directory:", OUT)