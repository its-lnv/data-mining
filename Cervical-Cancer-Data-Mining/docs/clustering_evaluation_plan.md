# Provisional Clustering Evaluation Plan

> **Status:** This was the evaluation plan before implementation. Experiments have since been run; actual outcomes are in `outputs/results/kmeans_experiment_report.md`, `outputs/results/dbscan_experiment_report.md`, and `outputs/results/clustering_comparison_report.md`. Evaluation and preprocessing choices remain provisional; teacher approval is not claimed.

## 1. Purpose and scope

This plan describes how the syllabus methods K-Means and DBSCAN could be compared for exploratory grouping of the dataset's selected numeric measurements. The comparison is methodological: clusters describe similarity under a chosen feature representation. They must not be treated as medical diagnoses or as validated medical risk categories.

The dataset inspection records 858 rows, 36 columns, and 23 duplicate rows. The feature-readiness document lists nine provisional numeric candidates: `Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives (years)`, `IUD (years)`, and `STDs (number)`. This is not an approved final feature set. Screening outcomes and diagnosis fields are excluded from clustering inputs.

## 2. Syllabus requirements

- Compare only the syllabus-listed K-Means and DBSCAN methods for this study.
- Plot K-Means mean squared error (MSE) after each iteration for selected parameter settings.
- Describe and compare the experimental settings and results after experiments have actually been run.

The MSE plot is a K-Means-specific view of its iterative centroid fitting. DBSCAN has no centroid-based MSE equivalent, so MSE will not be presented as a direct score for comparing both algorithms.

## 3. Proposed method-specific evaluation

### K-Means

K-Means requires a chosen number of clusters, `k`. The existing study plan suggests provisionally examining `k = 2, 3, 4, 5, 6`. For each setting, the later experiment should record its initialization/seed, stopping condition, number of iterations, cluster sizes, and final within-cluster squared-distance measure. Multiple documented initializations should be used for each `k` because starting centroids can affect the result.

For selected `k` values, record MSE after every iteration and plot iteration number on the horizontal axis and MSE on the vertical axis. Label each curve with its `k` and, where multiple starts are shown, its run/initialization. State the MSE definition and the feature scale used. The plot can show the optimization progression for that run; it does not by itself establish a globally best `k` or show that K-Means is superior to DBSCAN. MSE commonly decreases as `k` increases, so compare it alongside cluster sizes and other evidence rather than choosing the largest `k` solely for a lower value.

### DBSCAN

DBSCAN uses `eps` (neighborhood radius) and `min_samples` (minimum neighborhood population for a core point). It discovers the number of clusters from density connectivity and can label observations in sparse regions as noise; a predefined cluster count is not required.

Vary both `eps` and `min_samples` in a documented grid. The study plan gives `min_samples` values such as 5 and 10 and `eps` values such as 1.0, 1.5, 2.0, and 2.5 as illustrative starting points only. Those `eps` values may be inappropriate until the feature set, scaling, and distance space are settled; replace or refine them with a stated rationale after those decisions are confirmed. For every setting, record the number of clusters excluding noise, size of each cluster, noise count, noise fraction of the input rows, and any internal measure that is defined.

## 4. Internal cluster-quality measures and limits

### Silhouette coefficient

The silhouette coefficient summarizes how close an observation is to its own cluster compared with other clusters. It ranges from -1 to 1; a higher value generally indicates better separation under the selected distance representation. Report the average score only when there are at least two valid clusters and the calculation is defined. If a setting yields one cluster, all noise, or otherwise invalid cluster sizes, report the score as undefined and explain why rather than forcing a value.

For K-Means, calculate silhouette on all observations assigned to clusters. For DBSCAN, the proposed plan calculates it on non-noise observations and reports the number and fraction of excluded noise observations beside the score. Because DBSCAN's score omits noise while K-Means assigns every included observation, the scores do not summarize identical coverage and are not perfectly like-for-like. A DBSCAN setting must not appear better merely because difficult observations were excluded; discuss its coverage and noise rate with the score.

### Method-specific summaries

- **K-Means:** report per-iteration MSE curves, final MSE, cluster sizes, initialization/seed, and iteration/stopping information.
- **DBSCAN:** report `eps`, `min_samples`, cluster count and sizes, noise count/fraction, and silhouette only where defined.
- **Both:** report the input row and feature counts and use the same approved distance representation. These summaries describe the produced partition; they are not medical validation.

Do not compare K-Means MSE numerically with a DBSCAN score: they measure different things, and DBSCAN has no centroid objective. Silhouette, cluster coverage, cluster-size balance, and sensitivity can inform a cautious suitability discussion, but no single measure proves one method is universally best.

## 5. Fair comparison across settings

Before running experiments, fix and document a common data representation for both algorithms: the same approved feature columns, rows, missing-value treatment, duplicate policy, scaling method, and distance measure. Record the input shape and preprocessing decisions for every scenario. If a distinct approved feature or preprocessing scenario is explored, label it separately and compare K-Means and DBSCAN within that same scenario.

Use a declared parameter grid rather than selecting settings after seeing a preferred result. Keep K-Means initialization and stopping rules documented and use multiple starts; evaluate DBSCAN across the declared `eps`/`min_samples` combinations. Present a result row per setting, including failed/degenerate cases, undefined metrics, cluster sizes, and noise. Discuss sensitivity to K-Means starts and to DBSCAN parameter changes. Do not omit settings just because they produce one cluster or mostly noise.

The comparison should consider internal separation, cluster sizes, coverage/noise, and parameter sensitivity together. If metrics disagree or results are unstable, report the comparison as inconclusive rather than asserting a winner. No external labels, including `Biopsy`, `Hinselmann`, `Schiller`, `Citology`, or diagnosis fields, should be used as clustering inputs or to score or interpret clusters.

## 6. Medical and interpretation limits

These are unsupervised groupings based on selected recorded values and choices such as scaling and distance. They do not establish causation, clinical significance, diagnosis, or actual medical risk groups. Cluster identifiers are arbitrary labels for groups, not disease labels. The project is educational and is not intended for clinical diagnosis.

## 7. Decisions still provisional

The following decisions remain unresolved even though a provisional baseline has been run:

- Whether this clustering comparison is part of the final project objective.
- Which candidate features to use, including whether `STDs (number)` is appropriate; outcomes and direct diagnosis fields remain excluded from cluster inputs.
- How to handle missing values, particularly the diagnosis-time columns with 787 missing entries each; no cause for that missingness is assumed.
- Whether to retain or otherwise handle the 23 duplicate rows; the audit does not establish why they repeat.
- Whether to normalize or standardize, and which distance representation to use.
- The final `k`, `eps`, and `min_samples` ranges, initialization count, and stopping rules.
- Whether silhouette plus cluster coverage/noise and the required K-Means MSE plots satisfy the expected evaluation criteria.
- What criteria the teacher expects when identifying a best-suited method.

This plan records the proposed evaluation framework used to shape the experiments. The current provisional dataset and measured results are recorded in the preprocessing audit and experiment reports. The plan does not represent teacher approval; its metric and parameter choices may be revised if guidance changes.

## 8. Project references

- [Clustering study plan](clustering_study_plan.md)
- [Clustering feature readiness](clustering_feature_readiness.md)
- [Preprocessing plan](preprocessing_plan.md)
- [Preprocessing options](preprocessing_options.md)
- [Dataset inspection](dataset_inspection.md)
