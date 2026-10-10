# Provisional DBSCAN Experiment

> Exploratory syllabus-based experiment on the same provisional feature matrix used by K-Means. No teacher approval is claimed, and this report does not declare DBSCAN better than K-Means.

## Input and reproducibility

- **Input matrix:** `data/processed/PROVISIONAL_clustering_features.csv`
- **Input shape:** 835 records x 9 features
- **Features:** `Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives (years)`, `IUD (years)`, `STDs (number)`
- **Input validation:** missing=0; all values finite=True
- **Scikit-learn:** 1.8.0; DBSCAN uses `algorithm='auto'`, `metric='euclidean'`, `n_jobs=1`
- **Grid:** `eps` = 1.0, 1.5, 2.0, 2.5; `min_samples` = 5, 10
- **Random seed setting:** 42 is recorded for consistent project configuration, but DBSCAN has no random-state parameter. Input row order is unchanged and fixed.
- **Raw CSV SHA-256 unchanged:** True
- **Processed matrix SHA-256 unchanged:** True

DBSCAN forms density-connected clusters using the radius `eps` and minimum neighborhood count `min_samples`; it does not require a predefined cluster count. Label `-1` denotes noise. The tested parameter values follow the illustrative ranges in the study plan; they are not approved or guaranteed to suit this representation.

## Results for every parameter combination

Cluster sizes list only non-noise clusters. `silhouette_score` excludes noise points; the score is undefined when fewer than two non-noise clusters remain or the calculation is otherwise mathematically invalid.

| eps | min_samples | Clusters (no noise) | Noise count | Noise % | Cluster sizes (label:count) | Silhouette | Silhouette records | Limitation / invalid case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 3 | 267 | 31.98% | {"0": 554, "1": 9, "2": 5} | 0.465577 | non-noise records only | none beyond noise-excluded silhouette limitations |
| 1.5 | 5 | 6 | 136 | 16.29% | {"0": 658, "1": 8, "2": 14, "3": 9, "4": 5, "5": 5} | 0.096108 | non-noise records only | none beyond noise-excluded silhouette limitations |
| 2 | 5 | 1 | 81 | 9.70% | {"0": 754} | undefined | not calculated | one non-noise cluster; silhouette undefined |
| 2.5 | 5 | 1 | 44 | 5.27% | {"0": 791} | undefined | not calculated | one non-noise cluster; silhouette undefined |
| 1 | 10 | 1 | 311 | 37.25% | {"0": 524} | undefined | not calculated | one non-noise cluster; silhouette undefined |
| 1.5 | 10 | 2 | 189 | 22.63% | {"0": 633, "1": 13} | 0.452378 | non-noise records only | none beyond noise-excluded silhouette limitations |
| 2 | 10 | 1 | 90 | 10.78% | {"0": 745} | undefined | not calculated | one non-noise cluster; silhouette undefined |
| 2.5 | 10 | 1 | 48 | 5.75% | {"0": 787} | undefined | not calculated | one non-noise cluster; silhouette undefined |

## Metric and comparison limitations

- Silhouette is computed only on non-noise records. A high score can reflect a small subset if many records are noise; interpret it alongside noise count and percentage.
- A silhouette value is undefined for one cluster or all noise. Such configurations remain in the result table with the reason stated rather than being assigned a score.
- Parameter settings can yield different numbers and sizes of clusters, and silhouette is conditional on each resulting partition and its included records. Do not rank settings by silhouette alone.
- Results depend on the standardized feature space, Euclidean distance, and provisional median imputation and duplicate removal. Exact duplicate removal can alter DBSCAN neighborhood density.
- These results are internal geometric summaries. No outcome or diagnosis field was used as an input or evaluation label, and clusters are not diagnoses or medical risk categories.
- K-Means results are not compared here. Comparative analysis should wait until both result sets are reviewed using the shared feature representation and with the different metric/noise limitations made explicit.

## Output files

- Parameter results: `outputs/results/dbscan_parameter_results.csv`
- Assignments for every configuration: `outputs/results/dbscan_cluster_assignments.csv`
- Cluster-count plot: `outputs/graphs/dbscan_cluster_count_by_parameters.png`
- Noise-percentage plot: `outputs/graphs/dbscan_noise_percentage_by_parameters.png`
- Non-noise silhouette plot: `outputs/graphs/dbscan_silhouette_by_parameters.png`
- Detailed report: `outputs/results/dbscan_experiment_report.md`

Preprocessing choices remain provisional. This educational data-mining project is not a clinical diagnostic system.
