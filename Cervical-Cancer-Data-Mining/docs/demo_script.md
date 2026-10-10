# Project Demonstration Script (6–7 minutes)

## Before the demonstration

- Open the `Cervical-Cancer-Data-Mining` folder in VS Code.
- Confirm `data/raw/risk_factors_cervical_cancer.csv` exists.
- Select the project’s Python interpreter with pandas, NumPy, Matplotlib, and scikit-learn installed.
- Keep the PowerShell terminal at the project root.
- If you do not want to regenerate result files during the live talk, open the saved reports and graphs instead of running the workflow live.

## Sequence and timing

### 0:00–0:45 — Introduce project and scope

Open `README.md` and `docs/final_project_report.md`. Explain that the study compares syllabus methods K-Means and DBSCAN as exploratory clustering. State that the feature and preprocessing choices are provisional and that this is not a diagnostic tool.

### 0:45–1:30 — Dataset and data quality

Open `docs/dataset_inspection.md` or `outputs/results/data_integrity_verification.md`. Point out 858 rows, 36 columns, 23 duplicate copies, `?` missing markers, and the 787 missing values in each diagnosis-time field. Explain that diagnosis-time columns and all screening outcomes are not clustering inputs.

### 1:30–2:15 — Preprocessing

Open `outputs/results/clustering_preprocessing_audit.md`. Show the nine candidate columns and the provisional choices: median imputation, remove exact duplicate copies from the modeling copy, standardize. Explain the separate 835 × 9 output and that the original CSV remains unchanged.

### 2:15–3:15 — K-Means

Open `outputs/graphs/kmeans_mse_by_iteration.png`, then `kmeans_inertia_by_k.png` and `kmeans_silhouette_by_k.png`. Explain K, centroids, SSE/inertia, and MSE=SSE/835. Mention ten initializations per K with seed 42. The highest saved silhouette is 0.506262 at K=2, with sizes 49 and 786; point out that the uneven split matters.

### 3:15–4:15 — DBSCAN

Open `outputs/graphs/dbscan_cluster_count_by_parameters.png` and `dbscan_noise_percentage_by_parameters.png`, then `dbscan_silhouette_by_parameters.png`. Explain `eps`, `min_samples`, core/border/noise concepts, and that DBSCAN does not ask for a K in advance. State that noise spans 5.27%–37.25%; five settings produce one non-noise cluster, making silhouette undefined.

### 4:15–5:30 — Compare and interpret

Open `outputs/results/clustering_comparison_report.md` and the balance and coverage/noise plots. Explain that K-Means assigns all records, while DBSCAN can leave noise. DBSCAN silhouettes exclude noise and represent subsets; do not compare scores as though the populations match. K-Means SSE has no directly equivalent DBSCAN objective. Do not announce a winner.

### 5:30–6:30 — Reproducibility and close

Show `run_project.py` and `outputs/results/workflow_run_manifest.md`. The exact command from the project root is:

```powershell
python run_project.py
```

State that it regenerates processed data and outputs. Close with limitations: provisional preprocessing, feature semantics, duplicate interpretation, parameter grid, internal metrics, and no clinical interpretation. If asked about approval, state that teacher confirmation has not been received.

## Optional live run

Only when regeneration is acceptable, run `python run_project.py` in the terminal. It reruns all five workflow stages and overwrites their derived outputs at the documented paths using the configured settings. Do not edit the raw CSV or use the generated clusters for clinical decisions.
