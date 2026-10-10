# Clustering Study Implementation Checklist

> **Current status:** The provisional clustering baseline and comparison have been implemented and run. This checklist records completed work and remaining decisions. No teacher approval is claimed; the earlier Biopsy classification proposal remains documented separately as an alternative.

## Completed and verified

- [x] Raw UCI CSV is present at `data/raw/risk_factors_cervical_cancer.csv`; integrity verification records 858 rows, 36 columns, 9 of 9 candidate columns present, and 23 extra exact duplicate copies across 20 repeated-row groups.
- [x] Inspection, feature readiness, preprocessing options, clustering study, and evaluation planning documents are available under `docs/`.
- [x] Exploratory visualization script and seven data-description figures exist; `docs/visualization_notes.md` explains their scope and limitations.
- [x] Provisional preprocessing script and audit create a separate 835 × 9 matrix using the nine documented candidate features, median imputation, exact-duplicate removal, and standardization. These choices remain configurable and provisional.
- [x] K-Means was run for K=2–6 with 10 initializations per K, seed 42, maximum 300 iterations, centroid-shift tolerance 0.0001, and saved per-iteration SSE/MSE.
- [x] DBSCAN was run on the same feature matrix for `eps` = 1.0, 1.5, 2.0, 2.5 and `min_samples` = 5, 10; parameter-level assignments, cluster sizes, noise, and valid silhouette results were saved.
- [x] Comparative evaluation reused saved assignments for five K-Means and eight DBSCAN configurations. It reports cluster sizes, balance, coverage/noise, and silhouette population limitations without selecting an overall winner.
- [x] Root `run_project.py` runs integrity verification, preprocessing, K-Means, DBSCAN, and comparison in dependency order.
- [x] `docs/final_project_report.md`, its submission PDF, viva questions, demo sequence, submission checklist, and presentation outline have been prepared. Personal details and any teacher-specific requirements remain blank/pending.

## Current implementation files and outputs

| Purpose | Current file(s) |
|---|---|
| Integrity check | `src/verify_data_integrity.py`; `outputs/results/data_integrity_verification.md` |
| Provisional preprocessing | `src/clustering_preprocessing.py`; `data/processed/PROVISIONAL_clustering_features.csv`; `outputs/results/clustering_preprocessing_audit.md` |
| K-Means | `src/kmeans_experiment.py`; iteration metrics, run summary, assignments, report, and three figures under `outputs/` |
| DBSCAN | `src/dbscan_experiment.py`; parameter results, assignments, report, and three figures under `outputs/` |
| Comparison | `src/compare_clustering.py`; comparison tables, report, and three figures under `outputs/` |
| One-command workflow | `run_project.py` |

## Preprocessing and study choices still provisional

- [ ] Confirm that K-Means versus DBSCAN is the final teacher-required project direction; no scope approval is recorded.
- [ ] Confirm whether the nine numeric candidate features are suitable, especially distance treatment for count-like and zero-heavy fields. Screening outcomes and direct diagnosis/outcome fields remain excluded from cluster inputs.
- [ ] Confirm whether median imputation is acceptable. It inserts synthetic values and can change distances; diagnosis-time missing values were not imputed or interpreted as zero because those columns are excluded from this candidate set.
- [ ] Investigate whether the 23 exact duplicate copies are erroneous before treating their removal as final. The current modeling copy drops them; the raw data remain intact. Duplicate frequency can affect DBSCAN density and K-Means centroids.
- [ ] Confirm standardization and Euclidean distance for both methods. They define the geometry of the provisional feature space and DBSCAN `eps` interpretation.
- [ ] Confirm tested parameter ranges: K-Means K=2–6; DBSCAN `eps`=1.0–2.5 and `min_samples`=5 or 10. The saved results correspond to these values only.
- [ ] Confirm that silhouette, cluster counts/sizes, balance, coverage/noise, parameter sensitivity, and the required K-Means MSE-per-iteration plot meet the project evaluation rubric.
- [ ] Obtain the teacher’s preferred criteria for discussing a suitable method; current evidence does not identify a universal winner.

## Submission checks

- [ ] Add student, institution, course/semester, instructor, and submission date only when the student supplies the details.
- [ ] Review the final report and figures against the actual saved experiment artifacts.
- [ ] Run the documented workflow in the intended submission environment.
- [ ] Check any teacher-specific format, binding, presentation, and rubric requirements.

This project is educational. Clusters are exploratory groupings and are not diagnoses or validated clinical categories.
