# K-Means and DBSCAN Comparative Evaluation

> This report compares saved partitions on the same provisional standardized matrix. It does not select an overall winner or claim teacher approval.

## Inputs and method

- **Shared feature matrix:** `data/processed/PROVISIONAL_clustering_features.csv` (835 rows x 9 features).
- K-Means configurations are the lowest-inertia saved initialization for each tested K; no K-Means run was repeated.
- All eight saved DBSCAN parameter configurations and assignments were used; no DBSCAN run was repeated.
- Each assignment group was validated to contain exactly one label for every shared input row position.
- **Raw SHA-256 unchanged:** True
- **Processed matrix SHA-256 unchanged:** True

K-Means assigns every record to a cluster. DBSCAN may label records as noise (`-1`), so its clustered coverage can be below 100%. The cluster-size balance measures below describe formed clusters; DBSCAN noise is excluded from those calculations and reported separately.

## Comparison criteria and definitions

- **Cluster count and size distribution:** report each formed cluster's membership; DBSCAN noise is not counted as a cluster.
- **Coverage and noise:** clustered coverage is the share assigned to a non-noise cluster. K-Means coverage is 100%; DBSCAN noise percentage is shown separately.
- **Balance:** minimum-to-maximum cluster-size ratio ranges from 0 to 1, while normalized Shannon entropy ranges from 0 to 1 (higher means more even sizes). For DBSCAN these use non-noise clusters only. One-cluster entropy is defined as 0; its size ratio is 1 but does not imply a useful partition.
- **Silhouette:** recomputed consistently from saved labels and Euclidean distance. K-Means includes all records; DBSCAN excludes noise and records the scored subset size. A DBSCAN score may describe only a selected subset, and differing cluster counts/coverage mean scores must not be ranked blindly.
- **K-Means inertia/SSE:** deliberately omitted from cross-method comparison because DBSCAN has no centroid-based SSE objective. It is not a directly equivalent measure.

## Saved configurations and computed summaries

| Method | Exact configuration | Clusters | Cluster sizes | Min/max ratio | Normalized entropy | Coverage | Noise | Silhouette | Silhouette population |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K-Means | K=2, best init=2 | 2 | {"0": 49, "1": 786} | 0.062 | 0.322 | 100.00% | 0.00% | 0.506262 | all rows (n=835) |
| K-Means | K=3, best init=2 | 3 | {"0": 300, "1": 495, "2": 40} | 0.081 | 0.749 | 100.00% | 0.00% | 0.231945 | all rows (n=835) |
| K-Means | K=4, best init=4 | 4 | {"0": 474, "1": 48, "2": 28, "3": 285} | 0.059 | 0.697 | 100.00% | 0.00% | 0.258514 | all rows (n=835) |
| K-Means | K=5, best init=8 | 5 | {"0": 453, "1": 33, "2": 274, "3": 28, "4": 47} | 0.062 | 0.684 | 100.00% | 0.00% | 0.258375 | all rows (n=835) |
| K-Means | K=6, best init=8 | 6 | {"0": 47, "1": 430, "2": 90, "3": 32, "4": 28, "5": 208} | 0.065 | 0.742 | 100.00% | 0.00% | 0.260152 | all rows (n=835) |
| DBSCAN | eps=1, min_samples=5 | 3 | {"0": 554, "1": 9, "2": 5} | 0.009 | 0.120 | 68.02% | 31.98% | 0.465577 | non-noise rows only (n=568) |
| DBSCAN | eps=1, min_samples=10 | 1 | {"0": 524} | 1.000 | 0.000 | 62.75% | 37.25% | undefined | non-noise rows only (n=524) |
| DBSCAN | eps=1.5, min_samples=5 | 6 | {"0": 658, "1": 8, "2": 14, "3": 9, "4": 5, "5": 5} | 0.008 | 0.175 | 83.71% | 16.29% | 0.096108 | non-noise rows only (n=699) |
| DBSCAN | eps=1.5, min_samples=10 | 2 | {"0": 633, "1": 13} | 0.021 | 0.142 | 77.37% | 22.63% | 0.452378 | non-noise rows only (n=646) |
| DBSCAN | eps=2, min_samples=5 | 1 | {"0": 754} | 1.000 | 0.000 | 90.30% | 9.70% | undefined | non-noise rows only (n=754) |
| DBSCAN | eps=2, min_samples=10 | 1 | {"0": 745} | 1.000 | 0.000 | 89.22% | 10.78% | undefined | non-noise rows only (n=745) |
| DBSCAN | eps=2.5, min_samples=5 | 1 | {"0": 791} | 1.000 | 0.000 | 94.73% | 5.27% | undefined | non-noise rows only (n=791) |
| DBSCAN | eps=2.5, min_samples=10 | 1 | {"0": 787} | 1.000 | 0.000 | 94.25% | 5.75% | undefined | non-noise rows only (n=787) |

Full machine-readable tables are saved in `clustering_comparison_metrics.csv` and `clustering_comparison_cluster_sizes.csv`.

## Observations from this grid

- K-Means best-SSE runs have silhouette values from 0.2319 to 0.5063; the highest is at K=2 (0.5063), with cluster sizes {"0": 49, "1": 786}. This describes the tested assignments and does not establish the preferred method or K.
- DBSCAN has 5 of 8 configurations with one non-noise cluster and 3 configurations with a mathematically valid non-noise silhouette.
- DBSCAN's cluster counts and noise levels change across the tested parameter grid, showing sensitivity to `eps` and `min_samples`. Some configurations produce small clusters; inspect their size distributions and coverage alongside silhouette.
- Among DBSCAN settings with a valid silhouette, the largest value is 0.4656 at eps=1, min_samples=5; it excludes 267 noise records (31.98%). This is a subset score, not a direct winner comparison.

## Limitations and interpretation

- Silhouette uses different record populations: all 835 for K-Means and only non-noise records for DBSCAN. High DBSCAN silhouette can coexist with low coverage or tiny clusters.
- The tested K-Means partitions use the best-SSE initialization per K, whereas DBSCAN rows are parameter settings; this is a comparison of those saved configurations, not an uncertainty-adjusted statistical test.
- Cluster balance has different coverage context for DBSCAN because noise is excluded from its cluster sizes. The separate noise/coverage columns are essential.
- The analysis uses provisional features, median imputation, duplicate removal, and standardization. Each choice affects distances and may change both methods' outputs; exact duplicate removal may affect DBSCAN density especially.
- Method-specific settings and objectives differ. K-Means inertia is not compared to DBSCAN, and silhouette alone does not select a winner. Interpret cluster count, size, balance, coverage/noise, sensitivity, and silhouette limitations together.
- Clusters are exploratory similarity groupings, not diagnoses, causal findings, or clinically meaningful risk categories. This is an educational data-mining project, not a medical diagnostic system.

## Generated outputs

- Metrics table: `outputs/results/clustering_comparison_metrics.csv`
- Per-cluster size table: `outputs/results/clustering_comparison_cluster_sizes.csv`
- Balance graph: `outputs/graphs/clustering_balance_comparison.png`
- Coverage/noise graph: `outputs/graphs/clustering_coverage_and_noise.png`
- Silhouette-versus-coverage graph: `outputs/graphs/clustering_silhouette_vs_coverage.png`
- Detailed report: `outputs/results/clustering_comparison_report.md`

No overall winner is selected in this report. All preprocessing choices remain provisional, and no teacher approval is claimed.
