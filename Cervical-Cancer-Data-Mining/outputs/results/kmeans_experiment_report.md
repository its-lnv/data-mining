# Provisional K-Means Experiment

> Exploratory syllabus-based experiment on a provisional processed matrix. No teacher approval is claimed. This is not a medical diagnostic system.

## Configuration and input

- **Input matrix:** `data/processed/PROVISIONAL_clustering_features.csv`
- **Input dimensions:** 835 rows x 9 features
- **Features:** `Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives (years)`, `IUD (years)`, `STDs (number)`
- **Candidate K values:** 2, 3, 4, 5, 6
- **Random seed:** 42
- **Initializations per K:** 10; the run with lowest final SSE is reported as best for that K
- **Maximum iterations:** 300
- **Convergence:** stop when labels are unchanged between iterations or maximum centroid shift is at most 0.0001; otherwise stop at the iteration limit
- **Initialization:** choose K distinct input rows as initial centroids using NumPy's seeded generator.
- **Iteration procedure:** assign each record to its nearest centroid by squared Euclidean distance, recompute each non-empty centroid as the arithmetic mean of its assigned records, then record that iteration's SSE and MSE.
- **Empty cluster handling:** retain the previous centroid for an empty cluster and report its zero size; the effective non-empty cluster count is included in the results.
- **Input validation:** missing, non-numeric, empty, or non-finite inputs cause a clear error before results are written.
- **Input SHA-256 unchanged:** True

## Metric definitions

For each record, squared error is the sum of squared Euclidean coordinate differences from its assigned centroid. **Inertia/SSE** is the sum of those squared errors over all records. The plotted **MSE per record** is `SSE / N`, where N is the number of input records; it is the mean squared Euclidean distance per record, not SSE divided by the number of feature cells. Thus, MSE is a scaled version of SSE for this fixed N, while total inertia grows with the number of records.

The silhouette coefficient is also reported for the best-SSE run per K. It summarizes within-cluster versus nearest-other-cluster Euclidean distances, with values closer to 1 generally indicating better separation, near 0 indicating overlap, and negative values indicating some records are closer on average to another cluster. Singleton clusters receive 0.

## Best run per K

| K | Best init | Inertia / SSE | MSE per record | Silhouette | Iterations | Non-empty clusters | Cluster sizes by label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 6454.52904309 | 7.72997490 | 0.50626153 | 16 | 2 | 49;786 |
| 3 | 2 | 5565.73958319 | 6.66555639 | 0.23194543 | 11 | 3 | 300;495;40 |
| 4 | 4 | 4947.96081994 | 5.92570158 | 0.25851382 | 11 | 4 | 474;48;28;285 |
| 5 | 8 | 4386.01749140 | 5.25271556 | 0.25837455 | 18 | 5 | 453;33;274;28;47 |
| 6 | 8 | 3969.92178819 | 4.75439735 | 0.26015180 | 24 | 6 | 47;430;90;32;28;208 |

## Output files

- Iteration history for every initialization: `outputs/results/kmeans_iteration_metrics.csv`
- Run summary for every initialization: `outputs/results/kmeans_run_summary.csv`
- Assignments from the selected best-SSE run for each K: `outputs/results/kmeans_cluster_assignments.csv`
- Per-iteration MSE plot: `outputs/graphs/kmeans_mse_by_iteration.png`
- Inertia-by-K plot: `outputs/graphs/kmeans_inertia_by_k.png`
- Silhouette-by-K plot: `outputs/graphs/kmeans_silhouette_by_k.png`

## Interpretation limits and warnings

- Inertia cannot be compared naively across different K values: it generally cannot increase when K increases, and a larger K often lowers SSE.
- Silhouette is an internal geometric measure; it depends on the selected standardized features and Euclidean distance and does not validate medical meaning.
- The selected run per K is the lowest-inertia initialization, so its score is an optimization selection, not independent evidence of cluster quality.
- The input was already produced using provisional median imputation, exact-duplicate removal, and standardization. Those choices can affect cluster geometry; duplicate removal may especially alter density for the later DBSCAN comparison.
- No DBSCAN run or cross-method comparison was performed. Cluster labels are arbitrary grouping identifiers, not diagnoses or risk classes.
