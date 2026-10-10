"""Run a provisional, reproducible K-Means experiment on the prepared matrix.

K-Means is implemented directly with NumPy so the script can record inertia
after every Lloyd iteration. The feature matrix is treated as read-only.
"""

import hashlib
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

_MPL_CONFIG_DIR = tempfile.TemporaryDirectory(prefix="cervical_kmeans_mpl_")
os.environ["MPLCONFIGDIR"] = _MPL_CONFIG_DIR.name
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "PROVISIONAL_clustering_features.csv"
RESULTS_DIR = PROJECT_ROOT / "outputs" / "results"
GRAPHS_DIR = PROJECT_ROOT / "outputs" / "graphs"

# Clearly named settings for reproducibility and later comparison.
RANDOM_SEED = 42
CANDIDATE_K_VALUES = [2, 3, 4, 5, 6]
N_INITIALIZATIONS = 10
MAX_ITERATIONS = 300
CENTROID_TOLERANCE = 1e-4

ITERATION_RESULTS_PATH = RESULTS_DIR / "kmeans_iteration_metrics.csv"
RUN_SUMMARY_PATH = RESULTS_DIR / "kmeans_run_summary.csv"
ASSIGNMENTS_PATH = RESULTS_DIR / "kmeans_cluster_assignments.csv"
REPORT_PATH = RESULTS_DIR / "kmeans_experiment_report.md"
MSE_PLOT_PATH = GRAPHS_DIR / "kmeans_mse_by_iteration.png"
SSE_PLOT_PATH = GRAPHS_DIR / "kmeans_inertia_by_k.png"
SILHOUETTE_PLOT_PATH = GRAPHS_DIR / "kmeans_silhouette_by_k.png"


def markdown_table(headers, rows):
    """Create a simple Markdown table using only the standard library."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def sha256_file(path):
    """Hash a file in chunks to verify that inputs were not changed."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_kmeans(matrix, k, rng):
    """Run one Lloyd K-Means initialization and keep metrics each iteration.

    Centroids start at randomly selected input rows. Each iteration assigns
    every row to its nearest centroid, recalculates non-empty centroids as
    arithmetic means, and records SSE and MSE. An empty centroid keeps its
    previous location; its zero-sized cluster is reported explicitly.
    """
    row_count = matrix.shape[0]
    initial_indices = rng.choice(row_count, size=k, replace=False)
    centroids = matrix[initial_indices].copy()
    previous_labels = None
    history = []
    stopping_reason = "maximum iterations reached"

    for iteration in range(1, MAX_ITERATIONS + 1):
        squared_distances = ((matrix[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
        labels = np.argmin(squared_distances, axis=1)

        updated_centroids = centroids.copy()
        cluster_sizes = np.bincount(labels, minlength=k)
        for cluster_id in range(k):
            members = matrix[labels == cluster_id]
            if len(members):
                updated_centroids[cluster_id] = members.mean(axis=0)

        centroid_shift = np.sqrt(((updated_centroids - centroids) ** 2).sum(axis=1)).max()
        assigned_errors = matrix - updated_centroids[labels]
        row_squared_errors = (assigned_errors ** 2).sum(axis=1)
        sse = float(row_squared_errors.sum())
        # MSE here is average squared Euclidean distance per record: SSE / N.
        mse = sse / row_count
        history.append(
            {
                "iteration": iteration,
                "sse_inertia": sse,
                "mse_per_record": mse,
                "max_centroid_shift": float(centroid_shift),
                "nonempty_clusters": int(np.count_nonzero(cluster_sizes)),
            }
        )

        stable_labels = previous_labels is not None and np.array_equal(labels, previous_labels)
        centroids = updated_centroids
        if stable_labels:
            stopping_reason = "assignments unchanged"
            break
        if centroid_shift <= CENTROID_TOLERANCE:
            stopping_reason = "maximum centroid shift at or below tolerance"
            break
        previous_labels = labels.copy()

    # labels and centroids were computed together above; they define this run's
    # returned partition and its recorded final SSE/MSE.
    final_sizes = np.bincount(labels, minlength=k)
    return {
        "labels": labels,
        "centroids": centroids,
        "history": history,
        "iterations": len(history),
        "converged": stopping_reason != "maximum iterations reached",
        "stopping_reason": stopping_reason,
        "cluster_sizes": final_sizes,
        "sse": history[-1]["sse_inertia"],
        "mse": history[-1]["mse_per_record"],
    }


def silhouette_score_euclidean(matrix, labels):
    """Compute mean silhouette with Euclidean distances using NumPy only.

    A singleton cluster receives silhouette 0. The score is undefined when
    there is only one non-empty cluster or every record is its own cluster.
    """
    unique_labels = np.unique(labels)
    row_count = matrix.shape[0]
    if len(unique_labels) < 2 or len(unique_labels) >= row_count:
        return float("nan")

    # Pairwise distances from squared norms and a matrix product, avoiding a
    # three-dimensional temporary array.
    squared_norms = (matrix ** 2).sum(axis=1)
    squared_distances = squared_norms[:, None] + squared_norms[None, :] - 2 * matrix @ matrix.T
    distances = np.sqrt(np.maximum(squared_distances, 0.0))

    masks = {label: labels == label for label in unique_labels}
    scores = np.zeros(row_count, dtype=float)
    for index in range(row_count):
        own_label = labels[index]
        own_mask = masks[own_label]
        own_count = int(own_mask.sum())
        if own_count <= 1:
            scores[index] = 0.0
            continue

        a_value = float(distances[index, own_mask].sum() / (own_count - 1))
        b_value = min(
            float(distances[index, other_mask].mean())
            for other_label, other_mask in masks.items()
            if other_label != own_label
        )
        denominator = max(a_value, b_value)
        scores[index] = 0.0 if denominator == 0 else (b_value - a_value) / denominator

    return float(scores.mean())


def validate_input(data):
    """Check that the prepared matrix is numeric, complete, and finite."""
    if data.empty or data.shape[0] == 0 or data.shape[1] == 0:
        raise ValueError(f"Input matrix is empty: observed shape {data.shape}.")
    if data.columns.duplicated().any():
        raise ValueError("Input has duplicate feature column names.")
    if data.isna().any().any():
        missing = data.isna().sum()
        details = [f"{name}={int(count)}" for name, count in missing.items() if count]
        raise ValueError("Input contains missing values: " + ", ".join(details))

    try:
        matrix = data.to_numpy(dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("All input features must be numeric.") from error
    if not np.isfinite(matrix).all():
        raise ValueError("Input contains non-finite values (NaN or infinity).")
    if not CANDIDATE_K_VALUES:
        raise ValueError("CANDIDATE_K_VALUES must include at least one positive integer.")
    if any(not isinstance(value, int) or value < 2 or value >= len(data) for value in CANDIDATE_K_VALUES):
        raise ValueError("Every K must be an integer from 2 through row_count - 1.")
    if len(CANDIDATE_K_VALUES) != len(set(CANDIDATE_K_VALUES)):
        raise ValueError("CANDIDATE_K_VALUES contains duplicates.")
    if N_INITIALIZATIONS < 1 or MAX_ITERATIONS < 1 or CENTROID_TOLERANCE < 0:
        raise ValueError("Initialization count and iteration limit must be positive; tolerance cannot be negative.")
    return matrix


def save_plots(best_runs, result_rows):
    """Create iteration-MSE and K-Means internal-measure figures."""
    fig, ax = plt.subplots(figsize=(10, 6))
    for k in CANDIDATE_K_VALUES:
        run = best_runs[k]
        iterations = [entry["iteration"] for entry in run["history"]]
        mse_values = [entry["mse_per_record"] for entry in run["history"]]
        ax.plot(iterations, mse_values, marker="o", markersize=3, label=f"K={k}")
    ax.set_title("K-Means MSE by Iteration (Best Initialization per K)")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("MSE = total squared error / number of records")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(title="Candidate setting")
    fig.tight_layout()
    fig.savefig(MSE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)

    ordered = sorted(result_rows, key=lambda row: row["k"])
    ks = [row["k"] for row in ordered]
    sse_values = [row["best_sse_inertia"] for row in ordered]
    silhouette_values = [row["silhouette"] for row in ordered]

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(ks, sse_values, marker="o", color="#4C78A8")
    ax.set_title("K-Means Inertia (SSE) by K")
    ax.set_xlabel("Number of clusters (K)")
    ax.set_ylabel("Inertia / total SSE")
    ax.set_xticks(ks)
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(SSE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(ks, silhouette_values, marker="o", color="#F58518")
    ax.set_title("K-Means Mean Silhouette by K")
    ax.set_xlabel("Number of clusters (K)")
    ax.set_ylabel("Mean silhouette coefficient")
    ax.set_xticks(ks)
    ax.set_ylim(-1.05, 1.05)
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(SILHOUETTE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    if not INPUT_PATH.is_file():
        raise FileNotFoundError(
            f"Prepared feature matrix not found: {INPUT_PATH}\n"
            "Run src/clustering_preprocessing.py first."
        )

    input_hash_before = sha256_file(INPUT_PATH)
    data = pd.read_csv(INPUT_PATH)
    matrix = validate_input(data)
    input_rows, input_features = matrix.shape
    rng = np.random.default_rng(RANDOM_SEED)

    iteration_rows = []
    run_rows = []
    best_runs = {}
    best_rows = []
    assignment_rows = []

    for k in CANDIDATE_K_VALUES:
        runs = []
        for initialization in range(1, N_INITIALIZATIONS + 1):
            run = run_kmeans(matrix, k, rng)
            run["initialization"] = initialization
            runs.append(run)
            for entry in run["history"]:
                iteration_rows.append(
                    {
                        "k": k,
                        "initialization": initialization,
                        **entry,
                    }
                )

            sizes = run["cluster_sizes"]
            run_rows.append(
                {
                    "k": k,
                    "initialization": initialization,
                    "sse_inertia": run["sse"],
                    "mse_per_record": run["mse"],
                    "iterations": run["iterations"],
                    "converged": run["converged"],
                    "stopping_reason": run["stopping_reason"],
                    "nonempty_cluster_count": int(np.count_nonzero(sizes)),
                    "cluster_sizes_in_label_order": ";".join(str(int(size)) for size in sizes),
                }
            )

        best = min(runs, key=lambda candidate: candidate["sse"])
        best_runs[k] = best
        best_silhouette = silhouette_score_euclidean(matrix, best["labels"])
        sizes = best["cluster_sizes"]
        best_row = {
            "k": k,
            "best_initialization": best["initialization"],
            "best_sse_inertia": best["sse"],
            "mse_per_record": best["mse"],
            "silhouette": best_silhouette,
            "iterations": best["iterations"],
            "converged": best["converged"],
            "stopping_reason": best["stopping_reason"],
            "nonempty_cluster_count": int(np.count_nonzero(sizes)),
            "cluster_sizes_in_label_order": ";".join(str(int(size)) for size in sizes),
        }
        best_rows.append(best_row)

        for row_position, cluster_label in enumerate(best["labels"]):
            assignment_rows.append(
                {
                    "input_row_position": row_position,
                    "k": k,
                    "best_initialization": best["initialization"],
                    "cluster_label": int(cluster_label),
                }
            )

    iteration_frame = pd.DataFrame(iteration_rows)
    run_frame = pd.DataFrame(run_rows)
    best_frame = pd.DataFrame(best_rows)
    assignment_frame = pd.DataFrame(assignment_rows)

    # Keep the processed matrix unchanged; only create new result artifacts.
    if sha256_file(INPUT_PATH) != input_hash_before:
        raise RuntimeError("Input feature matrix changed during the experiment.")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    iteration_frame.to_csv(ITERATION_RESULTS_PATH, index=False)
    run_frame.to_csv(RUN_SUMMARY_PATH, index=False)
    assignment_frame.to_csv(ASSIGNMENTS_PATH, index=False)
    save_plots(best_runs, best_rows)

    report_rows = []
    for row in best_rows:
        silhouette = row["silhouette"]
        report_rows.append(
            (
                row["k"],
                row["best_initialization"],
                f"{row['best_sse_inertia']:.8f}",
                f"{row['mse_per_record']:.8f}",
                "undefined" if not np.isfinite(silhouette) else f"{silhouette:.8f}",
                row["iterations"],
                row["nonempty_cluster_count"],
                row["cluster_sizes_in_label_order"],
            )
        )

    report = [
        "# Provisional K-Means Experiment\n\n",
        "> Exploratory syllabus-based experiment on a provisional processed matrix. "
        "No teacher approval is claimed. This is not a medical diagnostic system.\n\n",
        "## Configuration and input\n\n",
        f"- **Input matrix:** `data/processed/{INPUT_PATH.name}`\n",
        f"- **Input dimensions:** {input_rows} rows x {input_features} features\n",
        f"- **Features:** {', '.join(f'`{column}`' for column in data.columns)}\n",
        f"- **Candidate K values:** {', '.join(str(value) for value in CANDIDATE_K_VALUES)}\n",
        f"- **Random seed:** {RANDOM_SEED}\n",
        f"- **Initializations per K:** {N_INITIALIZATIONS}; the run with lowest final SSE is reported as best for that K\n",
        f"- **Maximum iterations:** {MAX_ITERATIONS}\n",
        f"- **Convergence:** stop when labels are unchanged between iterations or maximum centroid shift is at most {CENTROID_TOLERANCE:g}; otherwise stop at the iteration limit\n",
        "- **Initialization:** choose K distinct input rows as initial centroids using NumPy's seeded generator.\n",
        "- **Iteration procedure:** assign each record to its nearest centroid by squared Euclidean distance, recompute each non-empty centroid as the arithmetic mean of its assigned records, then record that iteration's SSE and MSE.\n",
        "- **Empty cluster handling:** retain the previous centroid for an empty cluster and report its zero size; the effective non-empty cluster count is included in the results.\n",
        "- **Input validation:** missing, non-numeric, empty, or non-finite inputs cause a clear error before results are written.\n",
        f"- **Input SHA-256 unchanged:** {sha256_file(INPUT_PATH) == input_hash_before}\n\n",
        "## Metric definitions\n\n",
        "For each record, squared error is the sum of squared Euclidean coordinate differences from its assigned centroid. **Inertia/SSE** is the sum of those squared errors over all records. The plotted **MSE per record** is `SSE / N`, where N is the number of input records; it is the mean squared Euclidean distance per record, not SSE divided by the number of feature cells. Thus, MSE is a scaled version of SSE for this fixed N, while total inertia grows with the number of records.\n\n",
        "The silhouette coefficient is also reported for the best-SSE run per K. It summarizes within-cluster versus nearest-other-cluster Euclidean distances, with values closer to 1 generally indicating better separation, near 0 indicating overlap, and negative values indicating some records are closer on average to another cluster. Singleton clusters receive 0.\n\n",
        "## Best run per K\n\n",
        markdown_table(
            ["K", "Best init", "Inertia / SSE", "MSE per record", "Silhouette", "Iterations", "Non-empty clusters", "Cluster sizes by label"],
            report_rows,
        ),
        "\n\n",
        "## Output files\n\n",
        f"- Iteration history for every initialization: `outputs/results/{ITERATION_RESULTS_PATH.name}`\n",
        f"- Run summary for every initialization: `outputs/results/{RUN_SUMMARY_PATH.name}`\n",
        f"- Assignments from the selected best-SSE run for each K: `outputs/results/{ASSIGNMENTS_PATH.name}`\n",
        f"- Per-iteration MSE plot: `outputs/graphs/{MSE_PLOT_PATH.name}`\n",
        f"- Inertia-by-K plot: `outputs/graphs/{SSE_PLOT_PATH.name}`\n",
        f"- Silhouette-by-K plot: `outputs/graphs/{SILHOUETTE_PLOT_PATH.name}`\n\n",
        "## Interpretation limits and warnings\n\n",
        "- Inertia cannot be compared naively across different K values: it generally cannot increase when K increases, and a larger K often lowers SSE.\n",
        "- Silhouette is an internal geometric measure; it depends on the selected standardized features and Euclidean distance and does not validate medical meaning.\n",
        "- The selected run per K is the lowest-inertia initialization, so its score is an optimization selection, not independent evidence of cluster quality.\n",
        "- The input was already produced using provisional median imputation, exact-duplicate removal, and standardization. Those choices can affect cluster geometry; duplicate removal may especially alter density for the later DBSCAN comparison.\n",
        "- No DBSCAN run or cross-method comparison was performed. Cluster labels are arbitrary grouping identifiers, not diagnoses or risk classes.\n",
    ]
    REPORT_PATH.write_text("".join(report), encoding="utf-8")

    print("K-Means experiment completed.")
    print(f"Input: {input_rows} rows x {input_features} features")
    print(f"Candidate K values: {CANDIDATE_K_VALUES}; initializations per K: {N_INITIALIZATIONS}")
    print(f"Run summary: {RUN_SUMMARY_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Iteration metrics: {ITERATION_RESULTS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Assignments: {ASSIGNMENTS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Report: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Graphs: {MSE_PLOT_PATH.name}, {SSE_PLOT_PATH.name}, {SILHOUETTE_PLOT_PATH.name}")


if __name__ == "__main__":
    main()
