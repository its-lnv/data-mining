"""Compare saved K-Means and DBSCAN partitions on one shared feature matrix.

This script does not refit either clustering algorithm. It loads the saved
assignments, verifies their alignment to the shared matrix, and computes
descriptive cluster-balance and silhouette measures for comparison.
"""

import hashlib
import json
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score

_MPL_CONFIG_DIR = tempfile.TemporaryDirectory(prefix="cervical_compare_mpl_")
os.environ["MPLCONFIGDIR"] = _MPL_CONFIG_DIR.name
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
FEATURES_PATH = PROJECT_ROOT / "data" / "processed" / "PROVISIONAL_clustering_features.csv"
RESULTS_DIR = PROJECT_ROOT / "outputs" / "results"
GRAPHS_DIR = PROJECT_ROOT / "outputs" / "graphs"

KMEANS_RUNS_PATH = RESULTS_DIR / "kmeans_run_summary.csv"
KMEANS_ASSIGNMENTS_PATH = RESULTS_DIR / "kmeans_cluster_assignments.csv"
KMEANS_REPORT_PATH = RESULTS_DIR / "kmeans_experiment_report.md"
DBSCAN_PARAMS_PATH = RESULTS_DIR / "dbscan_parameter_results.csv"
DBSCAN_ASSIGNMENTS_PATH = RESULTS_DIR / "dbscan_cluster_assignments.csv"
DBSCAN_REPORT_PATH = RESULTS_DIR / "dbscan_experiment_report.md"

COMPARISON_PATH = RESULTS_DIR / "clustering_comparison_metrics.csv"
CLUSTER_SIZES_PATH = RESULTS_DIR / "clustering_comparison_cluster_sizes.csv"
REPORT_PATH = RESULTS_DIR / "clustering_comparison_report.md"
BALANCE_PLOT_PATH = GRAPHS_DIR / "clustering_balance_comparison.png"
COVERAGE_PLOT_PATH = GRAPHS_DIR / "clustering_coverage_and_noise.png"
SILHOUETTE_PLOT_PATH = GRAPHS_DIR / "clustering_silhouette_vs_coverage.png"

EXPECTED_ROWS = 835
EXPECTED_FEATURES = 9


def sha256_file(path):
    """Hash a file in chunks without changing it."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_table(headers, rows):
    """Create a Markdown table using only the standard library."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def validate_files():
    """Fail early if any required input artifact is missing."""
    required = [
        RAW_PATH,
        FEATURES_PATH,
        KMEANS_RUNS_PATH,
        KMEANS_ASSIGNMENTS_PATH,
        KMEANS_REPORT_PATH,
        DBSCAN_PARAMS_PATH,
        DBSCAN_ASSIGNMENTS_PATH,
        DBSCAN_REPORT_PATH,
    ]
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("Required comparison input(s) missing: " + ", ".join(missing))


def cluster_balance(sizes):
    """Return minimum/maximum size ratio and normalized Shannon entropy."""
    values = np.asarray(list(sizes.values()), dtype=float)
    if len(values) == 0 or values.sum() == 0:
        return float("nan"), float("nan")
    ratio = float(values.min() / values.max())
    if len(values) == 1:
        return ratio, 0.0
    proportions = values / values.sum()
    entropy = -float(np.sum(proportions * np.log(proportions)))
    normalized_entropy = entropy / float(np.log(len(values)))
    return ratio, normalized_entropy


def validate_matrix_and_assignments(matrix_df, kmeans_assignments, dbscan_assignments):
    """Check dimensions, complete numeric data, and positional alignment."""
    if matrix_df.shape != (EXPECTED_ROWS, EXPECTED_FEATURES):
        raise ValueError(
            f"Expected the shared matrix to be {EXPECTED_ROWS} x {EXPECTED_FEATURES}; "
            f"found {matrix_df.shape[0]} x {matrix_df.shape[1]}."
        )
    if matrix_df.isna().any().any():
        raise ValueError("The shared feature matrix contains missing values.")
    try:
        matrix = matrix_df.to_numpy(dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("The shared feature matrix must be numeric.") from error
    if not np.isfinite(matrix).all():
        raise ValueError("The shared feature matrix contains non-finite values.")

    expected_positions = set(range(len(matrix_df)))
    for name, frame in (("K-Means", kmeans_assignments), ("DBSCAN", dbscan_assignments)):
        if "input_row_position" not in frame.columns:
            raise ValueError(f"{name} assignments lack input_row_position.")
        groups = frame.groupby(
            [col for col in frame.columns if col in {"k", "eps", "min_samples"}],
            dropna=False,
        )
        for key, group in groups:
            positions = group["input_row_position"].astype(int).tolist()
            if len(positions) != EXPECTED_ROWS or set(positions) != expected_positions:
                raise ValueError(
                    f"{name} configuration {key} does not contain exactly one assignment "
                    f"for each of the {EXPECTED_ROWS} input positions."
                )
    return matrix


def calculate_summary(matrix, labels, method, configuration, silhouette_noise_excluded=False):
    """Summarize one saved partition without rerunning its clustering method."""
    labels = np.asarray(labels, dtype=int)
    total_rows = len(labels)
    if total_rows != len(matrix):
        raise ValueError(f"{method} label count {total_rows} does not match matrix rows {len(matrix)}.")

    if method == "DBSCAN":
        noise_mask = labels == -1
        noise_count = int(noise_mask.sum())
        cluster_labels = sorted(int(label) for label in np.unique(labels) if label != -1)
        silhouette_mask = ~noise_mask
        silhouette_note = "non-noise rows only"
    else:
        noise_mask = np.zeros(total_rows, dtype=bool)
        noise_count = 0
        cluster_labels = sorted(int(label) for label in np.unique(labels))
        silhouette_mask = np.ones(total_rows, dtype=bool)
        silhouette_note = "all rows"

    sizes = {str(label): int(np.sum(labels == label)) for label in cluster_labels}
    cluster_count = len(cluster_labels)
    covered_count = int((~noise_mask).sum())
    noise_percent = noise_count / total_rows * 100.0
    coverage_percent = covered_count / total_rows * 100.0
    ratio, entropy = cluster_balance(sizes)

    scored_labels = labels[silhouette_mask]
    unique_scored = np.unique(scored_labels)
    silhouette_valid = len(unique_scored) >= 2 and len(unique_scored) < len(scored_labels)
    if silhouette_valid:
        score = float(
            silhouette_score(
                matrix[silhouette_mask],
                scored_labels,
                metric="euclidean",
            )
        )
        silhouette_status = "valid"
    else:
        score = float("nan")
        silhouette_status = (
            "undefined: fewer than two clusters in scored rows"
            if len(unique_scored) < 2
            else "undefined: requires more scored rows than clusters"
        )

    return {
        "method": method,
        **configuration,
        "record_count": total_rows,
        "cluster_count_excluding_noise": cluster_count,
        "cluster_size_distribution": json.dumps(sizes, sort_keys=True),
        "cluster_size_min_max_ratio": ratio,
        "cluster_size_normalized_entropy": entropy,
        "clustered_record_count": covered_count,
        "coverage_percentage": coverage_percent,
        "noise_count": noise_count,
        "noise_percentage": noise_percent,
        "silhouette_score": score,
        "silhouette_records": silhouette_note,
        "silhouette_record_count": int(silhouette_mask.sum()),
        "silhouette_status": silhouette_status,
    }, sizes


def build_comparison(matrix, kmeans_runs, kmeans_assignments, dbscan_params, dbscan_assignments):
    """Reuse saved configurations/labels and construct comparable summaries."""
    expected_best = (
        kmeans_runs.sort_values("sse_inertia")
        .groupby("k", as_index=False)
        .first()[["k", "initialization", "sse_inertia"]]
        .rename(columns={"initialization": "best_initialization", "sse_inertia": "kmeans_sse_inertia"})
    )
    best_k_configs = set(
        zip(expected_best["k"].astype(int), expected_best["best_initialization"].astype(int))
    )
    saved_k_configs = set(
        zip(
            kmeans_assignments["k"].astype(int),
            kmeans_assignments["best_initialization"].astype(int),
        )
    )
    if best_k_configs != saved_k_configs:
        raise ValueError("Saved K-Means assignments do not match the lowest-SSE initialization per K.")

    rows = []
    size_rows = []
    for (k, initialization), group in kmeans_assignments.groupby(["k", "best_initialization"]):
        labels = group.sort_values("input_row_position")["cluster_label"].to_numpy(dtype=int)
        run_info = expected_best.loc[
            (expected_best["k"] == int(k))
            & (expected_best["best_initialization"] == int(initialization))
        ].iloc[0]
        summary, sizes = calculate_summary(
            matrix,
            labels,
            "K-Means",
            {
                "k": int(k),
                "best_initialization": int(initialization),
                "eps": np.nan,
                "min_samples": np.nan,
                "kmeans_sse_inertia_method_specific": float(run_info["kmeans_sse_inertia"]),
            },
        )
        rows.append(summary)
        for label, count in sizes.items():
            size_rows.append(
                {
                    "method": "K-Means",
                    "configuration": f"K={int(k)}",
                    "cluster_label": int(label),
                    "cluster_size": count,
                    "is_noise": False,
                }
            )

    param_pairs = set(zip(dbscan_params["eps"].astype(float), dbscan_params["min_samples"].astype(int)))
    assignment_pairs = set(
        zip(dbscan_assignments["eps"].astype(float), dbscan_assignments["min_samples"].astype(int))
    )
    if param_pairs != assignment_pairs:
        raise ValueError("DBSCAN parameter results and assignment configurations do not match.")

    for (eps, min_samples), group in dbscan_assignments.groupby(["eps", "min_samples"]):
        group = group.sort_values("input_row_position")
        labels = group["cluster_label"].to_numpy(dtype=int)
        # Validate the saved noise flag against label -1.
        if not np.array_equal(group["is_noise"].astype(bool).to_numpy(), labels == -1):
            raise ValueError(f"DBSCAN noise flags disagree with labels for eps={eps}, min_samples={min_samples}.")
        summary, sizes = calculate_summary(
            matrix,
            labels,
            "DBSCAN",
            {
                "k": np.nan,
                "best_initialization": np.nan,
                "eps": float(eps),
                "min_samples": int(min_samples),
                "kmeans_sse_inertia_method_specific": np.nan,
            },
        )

        # Cross-check the recomputed silhouette against the saved experiment score.
        stored = dbscan_params.loc[
            (dbscan_params["eps"].astype(float) == float(eps))
            & (dbscan_params["min_samples"].astype(int) == int(min_samples))
        ].iloc[0]["silhouette_score"]
        if pd.isna(stored) != pd.isna(summary["silhouette_score"]):
            raise ValueError(f"DBSCAN silhouette validity mismatch for eps={eps}, min_samples={min_samples}.")
        if pd.notna(stored) and not np.isclose(
            float(stored), summary["silhouette_score"], rtol=1e-6, atol=1e-6
        ):
            raise ValueError(f"DBSCAN silhouette mismatch for eps={eps}, min_samples={min_samples}.")

        rows.append(summary)
        for label, count in sizes.items():
            size_rows.append(
                {
                    "method": "DBSCAN",
                    "configuration": f"eps={float(eps):g}, min_samples={int(min_samples)}",
                    "cluster_label": int(label),
                    "cluster_size": count,
                    "is_noise": False,
                }
            )
        noise_count = int((labels == -1).sum())
        if noise_count:
            size_rows.append(
                {
                    "method": "DBSCAN",
                    "configuration": f"eps={float(eps):g}, min_samples={int(min_samples)}",
                    "cluster_label": -1,
                    "cluster_size": noise_count,
                    "is_noise": True,
                }
            )

    return pd.DataFrame(rows), pd.DataFrame(size_rows)


def configuration_label(row):
    if row["method"] == "K-Means":
        return f"K={int(row['k'])}"
    return f"e={row['eps']:g},m={int(row['min_samples'])}"


def create_plots(results):
    """Create comparison figures for balance, coverage/noise, and silhouette."""
    plot_data = results.copy()
    plot_data["display_label"] = plot_data.apply(configuration_label, axis=1)
    x_positions = np.arange(len(plot_data))
    colors = ["#4C78A8" if method == "K-Means" else "#F58518" for method in plot_data["method"]]

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.bar(x_positions, plot_data["cluster_size_normalized_entropy"], color=colors)
    ax.set_title("Cluster-Size Balance by Configuration")
    ax.set_xlabel("Configuration")
    ax.set_ylabel("Normalized cluster-size entropy (higher = more even)")
    ax.set_xticks(x_positions, plot_data["display_label"], rotation=55, ha="right")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.text(
        0.01,
        0.98,
        "DBSCAN balance is among non-noise clusters; noise is shown separately.",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(BALANCE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(15, 6))
    width = 0.38
    ax.bar(x_positions - width / 2, plot_data["coverage_percentage"], width, label="Clustered coverage (%)", color="#54A24B")
    ax.bar(x_positions + width / 2, plot_data["noise_percentage"], width, label="Noise (%)", color="#E45756")
    ax.set_title("Cluster Coverage and DBSCAN Noise by Configuration")
    ax.set_xlabel("Configuration")
    ax.set_ylabel("Percentage of all 835 records")
    ax.set_xticks(x_positions, plot_data["display_label"], rotation=55, ha="right")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(COVERAGE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 7))
    for method, marker, color in (
        ("K-Means", "o", "#4C78A8"),
        ("DBSCAN", "s", "#F58518"),
    ):
        subset = plot_data[plot_data["method"] == method]
        ax.scatter(
            subset["coverage_percentage"],
            subset["silhouette_score"],
            label=method,
            marker=marker,
            color=color,
            s=70,
        )
        for point_index, (_, row) in enumerate(subset.iterrows()):
            if method == "K-Means":
                # Separate the nearby K=3..6 points so each label stays readable.
                offsets = [(5, 6), (5, -15), (5, 16), (5, -28), (5, 28)]
                label_offset = offsets[point_index]
            else:
                label_offset = (5, 5)
            ax.annotate(
                row["display_label"],
                (row["coverage_percentage"], row["silhouette_score"]),
                xytext=label_offset,
                textcoords="offset points",
                fontsize=8,
            )
    ax.set_title("Silhouette and Coverage (Different Scored Populations)")
    ax.set_xlabel("Records included in clusters (%)")
    ax.set_ylabel("Silhouette score")
    ax.set_xlim(0, 105)
    ax.set_ylim(-1.05, 1.05)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.text(
        0.01,
        0.02,
        "K-Means silhouette uses all records; DBSCAN silhouette excludes noise.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(SILHOUETTE_PLOT_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    validate_files()
    raw_hash_before = sha256_file(RAW_PATH)
    feature_hash_before = sha256_file(FEATURES_PATH)

    feature_df = pd.read_csv(FEATURES_PATH)
    kmeans_runs = pd.read_csv(KMEANS_RUNS_PATH)
    kmeans_assignments = pd.read_csv(KMEANS_ASSIGNMENTS_PATH)
    dbscan_params = pd.read_csv(DBSCAN_PARAMS_PATH)
    dbscan_assignments = pd.read_csv(DBSCAN_ASSIGNMENTS_PATH)

    matrix = validate_matrix_and_assignments(
        feature_df, kmeans_assignments, dbscan_assignments
    )
    results, cluster_sizes = build_comparison(
        matrix,
        kmeans_runs,
        kmeans_assignments,
        dbscan_params,
        dbscan_assignments,
    )

    if sha256_file(RAW_PATH) != raw_hash_before:
        raise RuntimeError("Raw CSV changed during comparison.")
    if sha256_file(FEATURES_PATH) != feature_hash_before:
        raise RuntimeError("Processed feature matrix changed during comparison.")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(COMPARISON_PATH, index=False)
    cluster_sizes.to_csv(CLUSTER_SIZES_PATH, index=False)
    create_plots(results)

    display_rows = []
    for row in results.to_dict(orient="records"):
        score = row["silhouette_score"]
        config = (
            f"K={int(row['k'])}, best init={int(row['best_initialization'])}"
            if row["method"] == "K-Means"
            else f"eps={row['eps']:g}, min_samples={int(row['min_samples'])}"
        )
        display_rows.append(
            (
                row["method"],
                config,
                row["cluster_count_excluding_noise"],
                row["cluster_size_distribution"],
                f"{row['cluster_size_min_max_ratio']:.3f}",
                f"{row['cluster_size_normalized_entropy']:.3f}",
                f"{row['coverage_percentage']:.2f}%",
                f"{row['noise_percentage']:.2f}%",
                "undefined" if pd.isna(score) else f"{score:.6f}",
                f"{row['silhouette_records']} (n={row['silhouette_record_count']})",
            )
        )

    # Summarize observed parameter sensitivity without choosing an overall winner.
    db = results[results["method"] == "DBSCAN"]
    db_single_cluster = int((db["cluster_count_excluding_noise"] == 1).sum())
    db_valid_silhouette = int(db["silhouette_score"].notna().sum())
    kmeans_rows = results[results["method"] == "K-Means"]
    best_sil_row = kmeans_rows.loc[kmeans_rows["silhouette_score"].idxmax()]
    best_db_valid = db[db["silhouette_score"].notna()].sort_values(
        "silhouette_score", ascending=False
    )

    report = [
        "# K-Means and DBSCAN Comparative Evaluation\n\n",
        "> This report compares saved partitions on the same provisional standardized matrix. "
        "It does not select an overall winner or claim teacher approval.\n\n",
        "## Inputs and method\n\n",
        f"- **Shared feature matrix:** `data/processed/{FEATURES_PATH.name}` ({feature_df.shape[0]} rows x {feature_df.shape[1]} features).\n",
        "- K-Means configurations are the lowest-inertia saved initialization for each tested K; no K-Means run was repeated.\n",
        "- All eight saved DBSCAN parameter configurations and assignments were used; no DBSCAN run was repeated.\n",
        "- Each assignment group was validated to contain exactly one label for every shared input row position.\n",
        "- **Raw SHA-256 unchanged:** " + str(sha256_file(RAW_PATH) == raw_hash_before) + "\n",
        "- **Processed matrix SHA-256 unchanged:** " + str(sha256_file(FEATURES_PATH) == feature_hash_before) + "\n\n",
        "K-Means assigns every record to a cluster. DBSCAN may label records as noise (`-1`), so its clustered coverage can be below 100%. The cluster-size balance measures below describe formed clusters; DBSCAN noise is excluded from those calculations and reported separately.\n\n",
        "## Comparison criteria and definitions\n\n",
        "- **Cluster count and size distribution:** report each formed cluster's membership; DBSCAN noise is not counted as a cluster.\n",
        "- **Coverage and noise:** clustered coverage is the share assigned to a non-noise cluster. K-Means coverage is 100%; DBSCAN noise percentage is shown separately.\n",
        "- **Balance:** minimum-to-maximum cluster-size ratio ranges from 0 to 1, while normalized Shannon entropy ranges from 0 to 1 (higher means more even sizes). For DBSCAN these use non-noise clusters only. One-cluster entropy is defined as 0; its size ratio is 1 but does not imply a useful partition.\n",
        "- **Silhouette:** recomputed consistently from saved labels and Euclidean distance. K-Means includes all records; DBSCAN excludes noise and records the scored subset size. A DBSCAN score may describe only a selected subset, and differing cluster counts/coverage mean scores must not be ranked blindly.\n",
        "- **K-Means inertia/SSE:** deliberately omitted from cross-method comparison because DBSCAN has no centroid-based SSE objective. It is not a directly equivalent measure.\n\n",
        "## Saved configurations and computed summaries\n\n",
        markdown_table(
            ["Method", "Exact configuration", "Clusters", "Cluster sizes", "Min/max ratio", "Normalized entropy", "Coverage", "Noise", "Silhouette", "Silhouette population"],
            display_rows,
        ),
        "\n\n",
        "Full machine-readable tables are saved in `clustering_comparison_metrics.csv` and `clustering_comparison_cluster_sizes.csv`.\n\n",
        "## Observations from this grid\n\n",
        f"- K-Means best-SSE runs have silhouette values from {kmeans_rows['silhouette_score'].min():.4f} to {kmeans_rows['silhouette_score'].max():.4f}; the highest is at K={int(best_sil_row['k'])} ({best_sil_row['silhouette_score']:.4f}), with cluster sizes {best_sil_row['cluster_size_distribution']}. This describes the tested assignments and does not establish the preferred method or K.\n",
        f"- DBSCAN has {db_single_cluster} of {len(db)} configurations with one non-noise cluster and {db_valid_silhouette} configurations with a mathematically valid non-noise silhouette.\n",
        "- DBSCAN's cluster counts and noise levels change across the tested parameter grid, showing sensitivity to `eps` and `min_samples`. Some configurations produce small clusters; inspect their size distributions and coverage alongside silhouette.\n",
    ]
    if not best_db_valid.empty:
        best_db_row = best_db_valid.iloc[0]
        report.append(
            f"- Among DBSCAN settings with a valid silhouette, the largest value is {best_db_row['silhouette_score']:.4f} at eps={best_db_row['eps']:g}, min_samples={int(best_db_row['min_samples'])}; it excludes {int(best_db_row['noise_count'])} noise records ({best_db_row['noise_percentage']:.2f}%). This is a subset score, not a direct winner comparison.\n"
        )
    report.extend(
        [
            "\n## Limitations and interpretation\n\n",
            "- Silhouette uses different record populations: all 835 for K-Means and only non-noise records for DBSCAN. High DBSCAN silhouette can coexist with low coverage or tiny clusters.\n",
            "- The tested K-Means partitions use the best-SSE initialization per K, whereas DBSCAN rows are parameter settings; this is a comparison of those saved configurations, not an uncertainty-adjusted statistical test.\n",
            "- Cluster balance has different coverage context for DBSCAN because noise is excluded from its cluster sizes. The separate noise/coverage columns are essential.\n",
            "- The analysis uses provisional features, median imputation, duplicate removal, and standardization. Each choice affects distances and may change both methods' outputs; exact duplicate removal may affect DBSCAN density especially.\n",
            "- Method-specific settings and objectives differ. K-Means inertia is not compared to DBSCAN, and silhouette alone does not select a winner. Interpret cluster count, size, balance, coverage/noise, sensitivity, and silhouette limitations together.\n",
            "- Clusters are exploratory similarity groupings, not diagnoses, causal findings, or clinically meaningful risk categories. This is an educational data-mining project, not a medical diagnostic system.\n\n",
            "## Generated outputs\n\n",
            f"- Metrics table: `outputs/results/{COMPARISON_PATH.name}`\n",
            f"- Per-cluster size table: `outputs/results/{CLUSTER_SIZES_PATH.name}`\n",
            f"- Balance graph: `outputs/graphs/{BALANCE_PLOT_PATH.name}`\n",
            f"- Coverage/noise graph: `outputs/graphs/{COVERAGE_PLOT_PATH.name}`\n",
            f"- Silhouette-versus-coverage graph: `outputs/graphs/{SILHOUETTE_PLOT_PATH.name}`\n",
            f"- Detailed report: `outputs/results/{REPORT_PATH.name}`\n\n",
            "No overall winner is selected in this report. All preprocessing choices remain provisional, and no teacher approval is claimed.\n",
        ]
    )
    REPORT_PATH.write_text("".join(report), encoding="utf-8")

    print("Clustering comparison completed from saved assignments.")
    print(f"Configurations compared: {len(results)} (K-Means {len(kmeans_rows)}, DBSCAN {len(db)})")
    print(f"Metrics: {COMPARISON_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Report: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print("Graphs:", ", ".join(path.name for path in (BALANCE_PLOT_PATH, COVERAGE_PLOT_PATH, SILHOUETTE_PLOT_PATH)))
    print(f"Raw and processed hashes unchanged: {sha256_file(RAW_PATH) == raw_hash_before and sha256_file(FEATURES_PATH) == feature_hash_before}")


if __name__ == "__main__":
    main()
