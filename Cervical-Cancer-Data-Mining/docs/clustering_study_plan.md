# Provisional Clustering Study Plan

> **Status:** This plan records the provisional study design used before implementation. K-Means and DBSCAN have since been run; see `outputs/results/kmeans_experiment_report.md`, `outputs/results/dbscan_experiment_report.md`, and `outputs/results/clustering_comparison_report.md` for actual settings and measured results. Feature selection, missing-value handling, duplicate treatment, scaling, and parameter ranges remain provisional; teacher approval is not claimed. The raw CSV remains unchanged.

## 1. Study objective

This plan proposed comparing K-Means and DBSCAN as syllabus-based methods for exploratory grouping of selected numeric measurements. The provisional experiment has since been run; its observed cluster quality, coverage, parameter sensitivity, and limitations are documented in the experiment and comparative reports. The project direction and data representation remain unapproved.

The goal is methodological comparison only. A cluster is a group formed from the selected numeric measurements; it must not be described as a medical diagnosis, actual risk category, or clinically meaningful patient type. This clustering study does not use a target variable.

## 2. Syllabus-level distinction

### K-Means

K-Means partitions observations into a chosen number, `k`, of clusters. It assigns each observation to the nearest cluster centroid, recalculates each centroid as the mean of its assigned observations, and repeats these steps until assignment changes stop or an iteration limit is reached. It minimizes within-cluster squared distances. The method requires `k` in advance, assigns every included observation to a cluster, and can be affected by feature scale, extreme values, and its starting centroids. It is most interpretable when groups are reasonably compact around their means.

### DBSCAN

DBSCAN forms groups from dense neighborhoods. `eps` sets the neighborhood radius and `min_samples` sets the minimum number of nearby observations needed for a core point. Connected dense regions form clusters; observations in sparse regions may be labelled noise. DBSCAN does **not** require a predefined number of clusters and can identify noise points. Its results depend on the scale of the input, `eps`, `min_samples`, and whether the data have a useful density structure.

Both methods use distances in the proposed comparison, so they must receive the same selected rows, numeric features, feature scaling, and distance measure. The experiment will compare only these two syllabus algorithms.

## 3. Candidate numerical input features

The inspection report identifies the following numeric-valued risk-factor/count/duration columns as possible candidates. Their inclusion is not final:

| Candidate column | Missing entries in inspection | Provisional note |
| --- | ---: | --- |
| `Age` | 0 | Numeric age measurement. |
| `Number of sexual partners` | 26 | Count-valued measurement. |
| `First sexual intercourse` | 7 | Age-valued measurement. |
| `Num of pregnancies` | 56 | Count-valued measurement. |
| `Smokes (years)` | 13 | Duration-valued measurement. |
| `Smokes (packs/year)` | 13 | Numeric exposure measurement. |
| `Hormonal Contraceptives (years)` | 108 | Duration-valued measurement. |
| `IUD (years)` | 117 | Duration-valued measurement. |
| `STDs (number)` | 105 | Count-valued measurement; include only if its meaning and role are approved. |

A cautious first feature set could use the first eight columns above and leave `STDs (number)` for a separate approved comparison because of its substantial missingness and medical-history meaning. Even this candidate set is provisional and needs review for appropriate meaning, redundancy, and missingness.

The following are **not clustering input features**: `Biopsy`, `Hinselmann`, `Schiller`, `Citology`, `Dx:Cancer`, `Dx:CIN`, `Dx:HPV`, and `Dx`. Do not use outcome or diagnosis labels to form clusters. `STDs: Number of diagnosis` is also deferred unless its role is explicitly clarified; the two diagnosis-time columns are unsuitable for an initial feature set because each has 787 missing entries and their missingness treatment remains unresolved.

The 0/1-coded smoking, contraceptive, STD, and other indicator columns are numerically stored but categorical in meaning. They are not part of the initial all-numeric candidate set. Mixing them with continuous values may give them unintended distance weight; adding them would require a separate, documented feature-design decision.

## 4. Data issues to resolve before clustering

### Missing values

The inspection report records literal `?` values, including 26 missing entries in number of partners, 56 in pregnancies, 105 in many STD fields, 108 in hormonal-contraceptive fields, and 117 in IUD fields. Each diagnosis-time column has 787 missing entries. Distance calculations need complete numeric vectors, but the reason for a missing entry cannot be inferred from the marker alone.

At the time this plan was written, it proposed no imputation or row removal. The subsequent provisional baseline used the choices documented in `outputs/results/clustering_preprocessing_audit.md`: median imputation for the nine selected fields and removal of exact duplicate copies from the modeling copy. Those choices have not been teacher-approved. Unknown diagnosis-time values were not changed to zero. Both algorithms used the same resulting rows, and the audit reports the retained count.

### Feature scaling

The candidate columns use different units and ranges (for example, age, duration, and counts). Without scaling, larger-range columns can dominate Euclidean distances and thereby affect both algorithms. A later experiment may standardize or normalize the selected numeric columns, but the precise method and feature list are pending. If scaling is approved, use one common transformed feature matrix for K-Means and DBSCAN, document the procedure, and retain the raw file unchanged.

### Mixed feature types

Numeric codes do not all have numeric meaning. A 0/1 indicator is categorical, whereas age, durations, and counts have numeric distances. The proposed baseline therefore limits input to numeric-valued age/count/duration fields. If binary indicators are later included, document why their distance contribution is appropriate and compare them as a separately defined feature set rather than silently mixing types.

### Duplicate records

The inspection and cleaning audit found 23 exact duplicate copies, grouped across 20 repeated-value groups. No copies have been removed. Repeated records can influence K-Means centroids and can make local areas appear denser to DBSCAN, which may change its core/noise classifications. Whether those rows represent accidental copies or distinct records is unresolved.

Keep the same duplicate policy and same rows for both algorithms. Do not remove or collapse duplicates before teacher guidance. If a later sensitivity comparison with an approved duplicate policy is performed, label it separately and document the number of rows affected.

## 5. Provisional fair-comparison design

1. **Confirm scope:** Keep all screening outcomes and diagnosis labels out of the clustering input. Confirm the candidate numeric feature list and educational purpose with the teacher.
2. **Set one data representation:** Apply the same approved missing-value policy, selected rows, feature list, scaling, and Euclidean distance to both methods. Record the final shape and any omitted rows.
3. **Vary K-Means settings:** Provisionally compare `k = 2, 3, 4, 5, 6`. Run each setting from several documented initializations/seeds so a result is not selected from one fortunate start. Record stopping settings and cluster sizes.
4. **Plot K-Means MSE by iteration:** For selected `k` settings, record the mean squared distance of observations to their assigned centroids after every K-Means iteration. Plot iteration number on the x-axis and MSE on the y-axis, with a separate labelled curve for each selected `k` (and/or initialization, if shown). Report the feature scale and formula. This fulfills the project-sheet requirement to plot K-Means MSE after each iteration. Do not use the curve alone to declare the best method: MSE generally tends to fall when more clusters are allowed, and DBSCAN has no centroid-based MSE counterpart.
5. **Vary DBSCAN settings:** Provisionally vary both `eps` and `min_samples`. For example, after an approved scaling choice, test a small, documented set of `min_samples` values such as 5 and 10 and several `eps` radii selected after inspecting distances in the scaled feature space. Illustrative `eps` candidates such as 1.0, 1.5, 2.0, and 2.5 are only starting assumptions; replace or refine them if the chosen feature space makes them inappropriate. Do not pick one setting after seeing a preferred cluster story without documenting the selection rule.
6. **Use common internal measures:** Calculate the silhouette coefficient when a result has at least two valid clusters and enough assigned observations. For K-Means, calculate it on all assigned observations. For DBSCAN, exclude points labelled noise from the silhouette calculation and report the number and fraction excluded alongside the score. This makes clear that the two silhouette values cover different observations when DBSCAN finds noise; they are not perfectly like-for-like.
7. **Report method-specific information:** For K-Means, report `k`, initialization, convergence/iteration count, cluster sizes, and final MSE. For DBSCAN, report `eps`, `min_samples`, number of clusters excluding noise, cluster sizes, noise count/fraction, and the silhouette score where defined. Do not calculate a centroid MSE for DBSCAN.
8. **Compare suitability:** Discuss internal cluster separation, cluster compactness, coverage, noise points, sensitivity to parameter changes/initialization, and how clearly the results can be explained. If a metric is undefined or a setting yields one cluster or all noise, state that rather than forcing a score. A best-suited method may remain inconclusive if the results are unstable or poor under both methods.

The metric review will use only the selected numeric feature matrix. It will not compare clusters to Biopsy or other outcome/diagnosis columns, and it will not use those columns to attach medical meaning to clusters.

## 6. Planned tables and figures for the later experiment

- A parameter table for each algorithm, including the chosen settings and resulting cluster counts/sizes.
- K-Means MSE-versus-iteration curves for selected `k` settings.
- A comparison table with silhouette score (where defined), assigned-observation coverage, cluster count, and DBSCAN noise fraction.
- Optional cluster-size plots for describing the geometry of the resulting partitions, without clinical labels.

No figures or tables in this section have been generated; they are a plan only.

## 7. Provisional assumptions and decisions still open

- Whether the teacher wants clustering as a separate study alongside the previously planned classification proposal, or as the primary data mining objective.
- Which numeric risk-factor/count/duration columns are appropriate, including whether to include `STDs (number)`.
- How to handle missingness and whether diagnosis-time columns should be excluded from clustering.
- Whether to retain all 23 duplicate copies or apply a teacher-approved alternative.
- Whether standardization or normalization is expected and which scaling procedure to use.
- The candidate `k`, `eps`, and `min_samples` ranges, initialization count, stopping criteria, and comparison measures.
- Whether silhouette plus cluster coverage/noise and the required K-Means MSE plots meet the teacher's expected comparison criteria.

These assumptions are explicitly provisional. No teacher approval is claimed.

## 8. Project and syllabus alignment

- **Syllabus algorithms:** K-Means and DBSCAN only. No classification, association-rule, or out-of-syllabus method is included in this study plan.
- **Preprocessing link:** Use the existing [preprocessing plan](preprocessing_plan.md) and [provisional cleaning audit](../data/processed/PROVISIONAL_data_cleaning_audit.md); both state that missing-value and duplicate handling remain unresolved.
- **Dataset facts:** Use the existing [inspection report](dataset_inspection.md) for 858 rows, 36 columns, missing counts, data types, and 23 duplicate copies.
- **Visualization link:** Treat existing [visualization notes](visualization_notes.md) as descriptive only; outcome-count plots from that phase must not be reused as cluster labels.
- **Report link:** The [final project report](final_project_report.md) now describes the actual provisional experiment settings and findings. Teacher confirmation is still pending; revise the scope and decisions if later guidance changes the project direction.
- **Educational limit:** Clustering describes similarity in selected recorded features. It does not establish causation, clinical diagnoses, or medical risk categories.

This project is educational and is not intended for clinical diagnosis.
