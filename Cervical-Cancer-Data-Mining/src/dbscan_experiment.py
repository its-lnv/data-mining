"""Run a provisional DBSCAN parameter-grid experiment.

The script reads the same standardized feature matrix as the K-Means study and
writes result artifacts only. It does not change either input CSV.
"""

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

_MPL_CONFIG_DIR = tempfile.TemporaryDirectory(prefix="cervical_dbscan_mpl_")
os.environ["MPLCONFIGDIR"] = _MPL_CONFIG_DIR.name
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "PROVISIONAL_clustering_features.csv"
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
RESULTS_DIR = PROJECT_ROOT / "outputs" / "results"
GRAPHS_DIR = PROJECT_ROOT / "outputs" / "graphs"

# Illustrative parameter values from the existing study plan, used here as a
# provisional grid because the matrix is standardized. They remain configurable.
EPS_VALUES = [1.0, 1.5, 2.0, 2.5]
MIN_SAMPLES_VALUES = [5, 10]
RANDOM_SEED = 42  # DBSCAN has no random_state; row order is kept fixed.
METRIC = "euclidean"
ALGORITHM = "auto"
N_JOBS = 1
EXPECTED_ROWS = 835
EXPECTED_FEATURES = 9

PARAMETER_RESULTS_PATH = RESULTS_DIR / "dbscan_parameter_results.csv"
ASSIGNMENTS_PATH = RESULTS_DIR / "dbscan_cluster_assignments.csv"
REPORT_PATH = RESULTS_DIR / "dbscan_experiment_report.md"
CLUSTER_COUNT_PLOT_PATH = GRAPHS_DIR / "dbscan_cluster_count_by_parameters.png"
NOISE_PLOT_PATH = GRAPHS_DIR / "dbscan_noise_percentage_by_parameters.png"
SILHOUETTE_PLOT_PATH = GRAPHS_DIR / "dbscan_silhouette_by_parameters.png"


def sha256_file(path):
    """Return a SHA-256 digest by reading a file in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_table(headers, rows):
    """Build a Markdown table without optional dependencies."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def validate_input(data):
    """Require the exact prepared matrix dimensions and complete finite values."""
    if data.shape != (EXPECTED_ROWS, EXPECTED_FEATURES):
        raise ValueError(
            f"Expected the K-Means feature matrix to be {EXPECTED_ROWS} x "
            f"{EXPECTED_FEATURES}; found {data.shape[0]} x {data.shape[1]}."
        )
    if data.columns.duplicated().any():
        raise ValueError("Input feature matrix contains duplicate column names.")
    if data.isna().any().any():
        missing = data.isna().sum()
        details = [f"{name}={int(count)}" for name, count in missing.items() if count]
        raise ValueError("Input feature matrix contains missing values: " + ", ".join(details))
    try:
        matrix = data.to_numpy(dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Input feature matrix must contain only numeric values.") from error
    if not np.isfinite(matrix).all():
        raise ValueError("Input feature matrix contains non-finite values.")
    if not EPS_VALUES or any(not np.isfinite(value) or value <= 0 for value in EPS_VALUES):
        raise ValueError("EPS_VALUES must contain positive finite values.")
    if len(EPS_VALUES) != len(set(EPS_VALUES)):
        raise ValueError("EPS_VALUES contains duplicates.")
    if not MIN_SAMPLES_VALUES or any(
        not isinstance(value, int) or value < 1 for value in MIN_SAMPLES_VALUES
    ):
        raise ValueError("MIN_SAMPLES_VALUES must contain positive integers.")
    if len(MIN_SAMPLES_VALUES) != len(set(MIN_SAMPLES_VALUES)):
        raise ValueError("MIN_SAMPLES_VALUES contains duplicates.")
    return matrix


def evaluate_silhouette(matrix, labels):
    """Return non-noise silhouette and a clear reason when it is undefined."""
    assigned_mask = labels != -1
    assigned_labels = labels[assigned_mask]
    nonnoise_cluster_count = len(np.unique(assigned_labels))
    assigned_count = int(assigned_mask.sum())

    if nonnoise_cluster_count < 2:
        return float("nan"), "undefined: fewer than two non-noise clusters"
    if assigned_count <= nonnoise_cluster_count:
        return float("nan"), "undefined: requires more assigned records than clusters"

    score = silhouette_score(
        matrix[assigned_mask],
        assigned_labels,
        metric=METRIC,
    )
    return float(score), "valid; calculated on non-noise records only"


def run_experiment(data, matrix):
    """Fit every configured parameter pair and collect summaries/labels."""
    result_rows = []
    assignment_rows = []

    for min_samples in MIN_SAMPLES_VALUES:
        for eps in EPS_VALUES:
            model = DBSCAN(
                eps=float(eps),
                min_samples=int(min_samples),
                metric=METRIC,
                algorithm=ALGORITHM,
                n_jobs=N_JOBS,
            )
            labels = model.fit_predict(matrix)
            noise_mask = labels == -1
            noise_count = int(noise_mask.sum())
            noise_percent = noise_count / len(labels) * 100.0
            nonnoise_labels = labels[~noise_mask]
            unique_clusters = np.unique(nonnoise_labels)
            cluster_sizes = {
                str(int(cluster_id)): int((labels == cluster_id).sum())
                for cluster_id in unique_clusters
            }
            cluster_count = len(unique_clusters)
            silhouette, metric_status = evaluate_silhouette(matrix, labels)

            result_rows.append(
                {
                    "eps": float(eps),
                    "min_samples": int(min_samples),
                    "cluster_count_excluding_noise": int(cluster_count),
                    "noise_count": noise_count,
                    "noise_percentage": noise_percent,
                    "non_noise_record_count": int(len(labels) - noise_count),
                    "cluster_size_distribution": json.dumps(cluster_sizes, sort_keys=True),
                    "silhouette_score": silhouette,
                    "silhouette_points": "non-noise records only" if np.isfinite(silhouette) else "not calculated",
                    "silhouette_status": metric_status,
                    "limitation_or_invalid_case": (
                        "all records are noise" if noise_count == len(labels)
                        else "one non-noise cluster; silhouette undefined" if cluster_count < 2
                        else "none beyond noise-excluded silhouette limitations"
                    ),
                }
            )

            for row_position, cluster_label in enumerate(labels):
                assignment_rows.append(
                    {
                        "input_row_position": row_position,
                        "eps": float(eps),
                        "min_samples": int(min_samples),
                        "cluster_label": int(cluster_label),
                        "is_noise": bool(cluster_label == -1),
                    }
                )

    return pd.DataFrame(result_rows), pd.DataFrame(assignment_rows)


def create_plots(results):
    """Plot how eps and min_samples affect cluster and noise summaries."""
    eps_order = sorted(float(value) for value in EPS_VALUES)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for min_samples in MIN_SAMPLES_VALUES:
        subset = results[results["min_samples"] == min_samples].sort_values("eps")
        ax.plot(
            subset["eps"],
            subset["cluster_count_excluding_noise"],
            marker="o",
            label=f"min_samples={min_samples}",
        )
    ax.set_title("DBSCAN Cluster Count by eps and min_samples")
    ax.set_xlabel("eps (Euclidean radius in standardized feature space)")
    ax.set_ylabel("Clusters (noise excluded)")
    ax.set_xticks(eps_order)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CLUSTER_COUNT_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for min_samples in MIN_SAMPLES_VALUES:
        subset = results[results["min_samples"] == min_samples].sort_values("eps")
        ax.plot(
            subset["eps"],
            subset["noise_percentage"],
            marker="o",
            label=f"min_samples={min_samples}",
        )
    ax.set_title("DBSCAN Noise Percentage by eps and min_samples")
    ax.set_xlabel("eps (Euclidean radius in standardized feature space)")
    ax.set_ylabel("Noise points (% of all records)")
    ax.set_ylim(-2, 102)
    ax.set_xticks(eps_order)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(NOISE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for min_samples in MIN_SAMPLES_VALUES:
        subset = results[results["min_samples"] == min_samples].sort_values("eps")
        scores = subset["silhouette_score"].astype(float)
        ax.plot(
            subset["eps"],
            scores,
            marker="o",
            label=f"min_samples={min_samples}",
        )
    ax.set_title("DBSCAN Non-noise Silhouette by Parameters")
    ax.set_xlabel("eps (Euclidean radius in standardized feature space)")
    ax.set_ylabel("Silhouette (non-noise records only)")
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(eps_order)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(SILHOUETTE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    if not INPUT_PATH.is_file():
        raise FileNotFoundError(
            f"Prepared feature matrix not found: {INPUT_PATH}\n"
            "Run src/clustering_preprocessing.py first."
        )
    if not RAW_PATH.is_file():
        raise FileNotFoundError(f"Raw source CSV not found: {RAW_PATH}")

    input_hash_before = sha256_file(INPUT_PATH)
    raw_hash_before = sha256_file(RAW_PATH)
    data = pd.read_csv(INPUT_PATH)
    matrix = validate_input(data)
    results, assignments = run_experiment(data, matrix)

    if sha256_file(INPUT_PATH) != input_hash_before:
        raise RuntimeError("Processed input matrix changed during the DBSCAN experiment.")
    if sha256_file(RAW_PATH) != raw_hash_before:
        raise RuntimeError("Raw source CSV changed during the DBSCAN experiment.")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(PARAMETER_RESULTS_PATH, index=False)
    assignments.to_csv(ASSIGNMENTS_PATH, index=False)
    create_plots(results)

    table_rows = []
    for row in results.to_dict(orient="records"):
        score = row["silhouette_score"]
        table_rows.append(
            (
                f"{row['eps']:g}",
                row["min_samples"],
                row["cluster_count_excluding_noise"],
                row["noise_count"],
                f"{row['noise_percentage']:.2f}%",
                row["cluster_size_distribution"],
                "undefined" if pd.isna(score) else f"{score:.6f}",
                row["silhouette_points"],
                row["limitation_or_invalid_case"],
            )
        )

    report = [
        "# Provisional DBSCAN Experiment\n\n",
        "> Exploratory syllabus-based experiment on the same provisional feature matrix used by K-Means. "
        "No teacher approval is claimed, and this report does not declare DBSCAN better than K-Means.\n\n",
        "## Input and reproducibility\n\n",
        f"- **Input matrix:** `data/processed/{INPUT_PATH.name}`\n",
        f"- **Input shape:** {data.shape[0]} records x {data.shape[1]} features\n",
        f"- **Features:** {', '.join(f'`{column}`' for column in data.columns)}\n",
        f"- **Input validation:** missing={int(data.isna().sum().sum())}; all values finite={bool(np.isfinite(matrix).all())}\n",
        f"- **Scikit-learn:** {sklearn.__version__}; DBSCAN uses `algorithm='{ALGORITHM}'`, `metric='{METRIC}'`, `n_jobs={N_JOBS}`\n",
        f"- **Grid:** `eps` = {', '.join(str(value) for value in EPS_VALUES)}; `min_samples` = {', '.join(str(value) for value in MIN_SAMPLES_VALUES)}\n",
        f"- **Random seed setting:** {RANDOM_SEED} is recorded for consistent project configuration, but DBSCAN has no random-state parameter. Input row order is unchanged and fixed.\n",
        f"- **Raw CSV SHA-256 unchanged:** {sha256_file(RAW_PATH) == raw_hash_before}\n",
        f"- **Processed matrix SHA-256 unchanged:** {sha256_file(INPUT_PATH) == input_hash_before}\n\n",
        "DBSCAN forms density-connected clusters using the radius `eps` and minimum neighborhood count `min_samples`; it does not require a predefined cluster count. Label `-1` denotes noise. The tested parameter values follow the illustrative ranges in the study plan; they are not approved or guaranteed to suit this representation.\n\n",
        "## Results for every parameter combination\n\n",
        "Cluster sizes list only non-noise clusters. `silhouette_score` excludes noise points; the score is undefined when fewer than two non-noise clusters remain or the calculation is otherwise mathematically invalid.\n\n",
        markdown_table(
            ["eps", "min_samples", "Clusters (no noise)", "Noise count", "Noise %", "Cluster sizes (label:count)", "Silhouette", "Silhouette records", "Limitation / invalid case"],
            table_rows,
        ),
        "\n\n",
        "## Metric and comparison limitations\n\n",
        "- Silhouette is computed only on non-noise records. A high score can reflect a small subset if many records are noise; interpret it alongside noise count and percentage.\n",
        "- A silhouette value is undefined for one cluster or all noise. Such configurations remain in the result table with the reason stated rather than being assigned a score.\n",
        "- Parameter settings can yield different numbers and sizes of clusters, and silhouette is conditional on each resulting partition and its included records. Do not rank settings by silhouette alone.\n",
        "- Results depend on the standardized feature space, Euclidean distance, and provisional median imputation and duplicate removal. Exact duplicate removal can alter DBSCAN neighborhood density.\n",
        "- These results are internal geometric summaries. No outcome or diagnosis field was used as an input or evaluation label, and clusters are not diagnoses or medical risk categories.\n",
        "- K-Means results are not compared here. Comparative analysis should wait until both result sets are reviewed using the shared feature representation and with the different metric/noise limitations made explicit.\n\n",
        "## Output files\n\n",
        f"- Parameter results: `outputs/results/{PARAMETER_RESULTS_PATH.name}`\n",
        f"- Assignments for every configuration: `outputs/results/{ASSIGNMENTS_PATH.name}`\n",
        f"- Cluster-count plot: `outputs/graphs/{CLUSTER_COUNT_PLOT_PATH.name}`\n",
        f"- Noise-percentage plot: `outputs/graphs/{NOISE_PLOT_PATH.name}`\n",
        f"- Non-noise silhouette plot: `outputs/graphs/{SILHOUETTE_PLOT_PATH.name}`\n",
        f"- Detailed report: `outputs/results/{REPORT_PATH.name}`\n\n",
        "Preprocessing choices remain provisional. This educational data-mining project is not a clinical diagnostic system.\n",
    ]
    REPORT_PATH.write_text("".join(report), encoding="utf-8")

    print("DBSCAN experiment completed.")
    print(f"Input: {data.shape[0]} rows x {data.shape[1]} features; missing=0; finite=True")
    print(f"Parameter combinations: {len(results)}")
    print(f"Parameter results: {PARAMETER_RESULTS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Assignments: {ASSIGNMENTS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Report: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Graphs: {CLUSTER_COUNT_PLOT_PATH.name}, {NOISE_PLOT_PATH.name}, {SILHOUETTE_PLOT_PATH.name}")


if __name__ == "__main__":
    main()
