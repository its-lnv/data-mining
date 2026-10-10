# Comparative Study of K-Means and DBSCAN on the UCI Cervical Cancer Risk Factors Dataset

> **Submission copy:** The polished submission version, with title-page fields, figure captions, full parameter tables, and execution appendix, is `final_project_report.md`. This file is retained as the working report draft.

> **Report status:** Completed from the project’s recorded inspection, preprocessing audit, saved experiment outputs, and comparative evaluation. The feature set and preprocessing choices remain provisional and have not been presented as teacher-approved. This educational analysis is not a medical diagnostic tool.

## 1. Abstract

This project performs an exploratory, syllabus-based comparison of K-Means and DBSCAN using the UCI Cervical Cancer Risk Factors dataset. The source file contains 858 rows and 36 columns. For the provisional clustering baseline, nine numeric candidate features were selected, 23 exact duplicate copies were excluded, missing feature values were filled with feature medians, and all nine features were standardized. The resulting feature matrix contains 835 rows and nine columns. K-Means was evaluated for K values 2 through 6 with ten seeded initializations per K. DBSCAN was evaluated for four `eps` values and two `min_samples` values. Results include cluster sizes, internal silhouette scores, K-Means iteration histories, and DBSCAN noise counts. These are geometric summaries of one provisional representation; they do not establish medical meaning or identify diagnoses.

## 2. Problem Statement

The project asks how two syllabus-listed clustering methods, K-Means and DBSCAN, partition records in one common standardized feature space, and how their partitions vary with method settings. K-Means requires a chosen cluster count and assigns every record to a cluster. DBSCAN uses a density radius and a minimum-neighbor count, can form clusters of different shapes, and can mark points as noise. The study compares internal partition summaries and coverage while accounting for these different behaviors. It does not use screening outcomes as clustering inputs or claim that any cluster represents a medical category.

## 3. Aim and Objectives

**Aim:** Compare K-Means and DBSCAN on a shared provisional feature matrix using the project’s syllabus-level clustering methods and internal evaluation measures.

**Objectives:**

- Preserve and inspect the supplied source CSV and document its structure and data-quality observations.
- Prepare a separate, configurable feature matrix for the provisional clustering experiments.
- Measure K-Means results for K=2, 3, 4, 5, and 6, including SSE/inertia and MSE at each iteration.
- Measure DBSCAN results over a documented grid of `eps` and `min_samples` values, including noise.
- Compare cluster counts, cluster-size distributions, balance, coverage, and silhouette with the metric limitations stated explicitly.
- Document assumptions and avoid medical or causal interpretations.

## 4. Dataset Collection, Source, and Description

The supplied dataset is **Cervical Cancer (Risk Factors)** from the [UCI Machine Learning Repository, dataset 383](https://archive.ics.uci.edu/dataset/383/cervical%2Bcancer%2Brisk%2Bfactors). The project file is `data/raw/risk_factors_cervical_cancer.csv`; the raw file is retained as the source copy. The project does not record a separate survey or data-collection procedure performed by the student.

The inspection report records **858 rows and 36 columns**. Columns cover age, habits, contraceptive use, STD-related history, diagnosis-related fields, and the screening outcomes `Hinselmann`, `Schiller`, `Citology`, and `Biopsy`. The literal `?` is parsed as missing in memory by the inspection and preprocessing code; it is not replaced in the raw file. Initial inspection recorded 23 exact duplicate copies and substantial missingness in some fields, including 787 missing entries in each of the two STD diagnosis-time fields. The `Biopsy` outcome has 803 zero and 55 one records in the inspection, but outcomes were excluded from clustering inputs.

The provisional nine-feature clustering input is: `Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives (years)`, `IUD (years)`, and `STDs (number)`. Pandas inferred numeric data for these columns after interpreting `?` as missing. The values have different units and distributions; several are count-like or zero-heavy. Numeric storage does not by itself establish that every feature is continuous or equally meaningful for distance calculations.

## 5. Data Preparation and Provisional Assumptions

`src/clustering_preprocessing.py` reads the raw CSV and writes a separate feature-only matrix. The recorded settings and measured row counts are:

- **Feature selection:** the nine candidates listed above; screening outcomes and direct diagnosis fields are excluded. This selection is provisional.
- **Missing values:** median imputation per feature. The audit reports the median used for each column and missing counts before and after handling. This keeps rows but inserts synthetic values and may change distances.
- **Duplicate rows:** exact duplicate copies are removed, retaining the first occurrence; the parsed full-row equality check detected 23 extra copies. The resulting matrix has 835 rows. Whether those copies are erroneous or separate observations is unresolved; removal can affect both centroid positions and DBSCAN neighborhood density.
- **Scaling:** standardization using each feature’s mean and population standard deviation (`ddof=0`). This prevents larger numeric ranges from dominating Euclidean distance solely because of their units. Standardization itself changes geometry and is provisional.
- **Diagnosis-time missingness:** diagnosis-time columns are not candidate clustering inputs. Their missing values were not interpreted as zero or as confirmed absence of diagnosis.
- **Validation:** the preprocessing audit reports all nine columns present, no all-missing selected feature, no unexpected non-numeric candidate values, and a non-empty finite numeric result.

These are the choices that produced the experiments, not approved or uniquely correct policies. The feature list, median imputation, duplicate removal, and standardization need review before their results are treated as final. The source CSV was read-only; integrity reports and experiment scripts compare hashes to detect changes.

## 6. K-Means Methodology and Results

The project implements K-Means using NumPy. For each K in **2, 3, 4, 5, 6**, it performs **10 initializations** with random seed **42**, selecting the run with the lowest final SSE for that K. Initial centroids are selected from distinct input rows. Each iteration assigns every row to its nearest centroid by squared Euclidean distance and recomputes non-empty centroids as arithmetic means. The iteration limit is 300; the saved experiment describes stopping when labels are unchanged or maximum centroid shift is at most 0.0001. Empty clusters retain their previous centroid and are reported.

For a given iteration, the squared error of a record is the sum of squared coordinate differences from its assigned centroid. **SSE/inertia** is the sum of these errors over all N records. The required plotted **MSE per record** is `SSE / N`, where N=835. It is not divided by the number of feature cells. For this fixed dataset, MSE is SSE scaled by 1/835. Neither quantity should be used to select among different K values alone: adding clusters generally reduces or preserves SSE.

| K | Best initialization | SSE / inertia | MSE per record | Silhouette | Iterations | Cluster sizes |
|---:|---:|---:|---:|---:|---:|---|
| 2 | 2 | 6454.5290 | 7.72997 | 0.506262 | 16 | 49, 786 |
| 3 | 2 | 5565.7396 | 6.66556 | 0.231945 | 11 | 300, 495, 40 |
| 4 | 4 | 4947.9608 | 5.92570 | 0.258514 | 11 | 474, 48, 28, 285 |
| 5 | 8 | 4386.0175 | 5.25272 | 0.258375 | 18 | 453, 33, 274, 28, 47 |
| 6 | 8 | 3969.9218 | 4.75440 | 0.260152 | 24 | 47, 430, 90, 32, 28, 208 |

The MSE-by-iteration figure plots per-record MSE, and the iteration CSV records the run histories. K-Means silhouette is computed over all 835 assigned records. Among these tested best-SSE runs, K=2 has the highest recorded silhouette, but its cluster sizes are markedly uneven. This observation does not by itself establish the best K or a meaningful grouping.

## 7. DBSCAN Methodology and Results

DBSCAN groups points connected through neighborhoods defined by `eps` and `min_samples`; it does **not** require a predefined number of clusters. Labels of `-1` indicate noise and are not counted as a cluster. The project used Euclidean distance with scikit-learn and evaluated `eps` values **1.0, 1.5, 2.0, 2.5** with `min_samples` **5, 10**. The input row order was fixed. Seed 42 is recorded as project configuration, but DBSCAN itself has no random-state parameter.

The table reports saved counts and the silhouette outcomes. DBSCAN silhouette is calculated only among non-noise records; it can describe a subset of the 835 records and must be read with noise percentage and cluster sizes. It is undefined where only one non-noise cluster remains.

| eps | min_samples | Clusters | Noise (count; %) | Non-noise cluster sizes | Silhouette (non-noise only) |
|---:|---:|---:|---:|---|---:|
| 1.0 | 5 | 3 | 267; 31.98% | 554, 9, 5 | 0.465577 |
| 1.5 | 5 | 6 | 136; 16.29% | 658, 8, 14, 9, 5, 5 | 0.096108 |
| 2.0 | 5 | 1 | 81; 9.70% | 754 | undefined: one cluster |
| 2.5 | 5 | 1 | 44; 5.27% | 791 | undefined: one cluster |
| 1.0 | 10 | 1 | 311; 37.25% | 524 | undefined: one cluster |
| 1.5 | 10 | 2 | 189; 22.63% | 633, 13 | 0.452378 |
| 2.0 | 10 | 1 | 90; 10.78% | 745 | undefined: one cluster |
| 2.5 | 10 | 1 | 48; 5.75% | 787 | undefined: one cluster |

Five of the eight tested settings yielded one non-noise cluster, so their silhouette scores are undefined. The largest valid silhouette in this grid was 0.465577 at `eps=1.0, min_samples=5`, calculated for 568 non-noise records; 267 records were excluded as noise. A relatively high score on that subset does not imply a better overall partition. The results show sensitivity to the chosen density parameters.

## 8. Comparative Evaluation

The comparative script reuses saved labels and results; it does not rerun either algorithm. It validates that each assignment group contains one label for each row position in the common 835-row matrix. It reports exact parameters, cluster count and sizes, coverage, noise, minimum-to-maximum cluster-size ratio, normalized Shannon entropy, and silhouette. K-Means coverage is 100% because every row is assigned. DBSCAN coverage is its non-noise share; noise is shown separately. DBSCAN balance measures are calculated over non-noise clusters only.

K-Means best-SSE runs have silhouette values from **0.231945 to 0.506262**. DBSCAN has three settings with valid non-noise silhouettes and five single-cluster cases. Silhouette is not directly comparable across all configurations because K-Means scores include all records while DBSCAN scores exclude noise and can represent varying subsets. Cluster count and sizes, balance, coverage/noise, and sensitivity to parameter settings therefore accompany silhouette. K-Means SSE/inertia is not compared with DBSCAN: DBSCAN has no centroid-based SSE objective, so these are not equivalent cross-method scores. The project does not declare an overall winner.

## 9. Visualizations and Generated Results

The exploratory plots in `outputs/graphs/` show missing-value counts, screening outcome counts, age, sexual-partner count, first-intercourse age, pregnancy count, and recorded smoking-status counts. They are descriptive plots of the raw data and do not imply causality or clinical risk.

Clustering plots show K-Means inertia by K, K-Means per-iteration MSE, K-Means silhouette by K, DBSCAN cluster counts and noise percentage by parameter setting, DBSCAN non-noise silhouette, and the cross-method balance, coverage/noise, and silhouette-versus-coverage summaries. Machine-readable outputs include K-Means iteration histories, run summaries and assignments; DBSCAN parameter results and assignments; and comparative configuration and cluster-size tables. The detailed experiment records are in `outputs/results/kmeans_experiment_report.md`, `dbscan_experiment_report.md`, `clustering_comparison_report.md`, and `clustering_preprocessing_audit.md`.

## 10. Limitations and Ethical Considerations

- Every clustering result depends on the selected features, the median-imputed values, the removed duplicate copies, standardization, Euclidean distance, and algorithm parameters. Those choices are provisional and have not received teacher approval.
- Median imputation can distort distances, particularly for skewed and zero-heavy data. Exact duplicate removal can change density estimates; the data alone do not establish whether repeated rows are errors.
- Numeric codes do not guarantee that the selected attributes are suitable continuous distance dimensions. Standardization equalizes scale but does not make mixed or discrete features semantically equivalent.
- K-Means favors centroid-based partitions and assigns all points; DBSCAN depends on density thresholds and may mark many records as noise. Neither method’s behavior alone establishes the “true” number or structure of groups.
- Silhouette is an internal geometric measure, not external validation. DBSCAN scores omit noise and are conditional on the included subset; single-cluster cases have no defined silhouette. The comparison is not a statistical significance test.
- Cluster IDs are arbitrary and are not labels for diagnoses, severity, or medical risk. The study makes no causal inference and is not intended for clinical decisions.
- The dataset contains sensitive health-related information. Report aggregate results and avoid unnecessary disclosure of individual-level records.

## 11. Conclusion

The implemented experiments demonstrate how the two syllabus methods behave on the same provisional 835 × 9 standardized representation. K-Means assigned all records across the five tested K values, with cluster sizes often uneven and per-record MSE decreasing as K increased. DBSCAN produced between one and six clusters in the tested grid, with noise from 5.27% to 37.25%; most settings produced one non-noise cluster. The internal scores and coverage describe different partitions and, for DBSCAN, sometimes different subsets. The saved evidence supports describing parameter sensitivity and partition structure, but it does not support naming a universally better algorithm, a medically meaningful group, or an approved final preprocessing policy. Teacher guidance and further justification are still needed before treating the provisional choices as final.

## 12. References

1. UCI Machine Learning Repository. [Cervical Cancer (Risk Factors), dataset 383](https://archive.ics.uci.edu/dataset/383/cervical%2Bcancer%2Brisk%2Bfactors). Dataset citation listed by UCI: Fernandes, K., Cardoso, J. S., & Fernandes, J. (2017). *Cervical Cancer (Risk Factors)* [Dataset]. DOI: [10.24432/C5Z310](https://doi.org/10.24432/C5Z310).
2. Fernandes, K., Cardoso, J. S., & Fernandes, J. (2017). *Transfer Learning with Partial Observability Applied to Cervical Cancer Screening*. Paper listed on the UCI dataset page.
3. Project [Dataset Inspection Report](dataset_inspection.md), [Clustering Study Plan](clustering_study_plan.md), and [Clustering Evaluation Plan](clustering_evaluation_plan.md).
4. Project [Provisional Clustering Preprocessing Audit](../outputs/results/clustering_preprocessing_audit.md), [K-Means Experiment Report](../outputs/results/kmeans_experiment_report.md), [DBSCAN Experiment Report](../outputs/results/dbscan_experiment_report.md), and [Comparative Evaluation Report](../outputs/results/clustering_comparison_report.md). These are the primary records for computed values reported here.
5. Project scripts: `src/clustering_preprocessing.py`, `src/kmeans_experiment.py`, `src/dbscan_experiment.py`, and `src/compare_clustering.py`.
