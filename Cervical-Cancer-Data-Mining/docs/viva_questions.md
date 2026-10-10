# Viva Questions and Suggested Answers

These answers describe the current provisional implementation. The feature list and preprocessing choices are not teacher-approved, and the clusters have no clinical interpretation.

## Dataset and preparation

1. **What is the dataset source?**  
   It is the Cervical Cancer (Risk Factors) dataset, dataset 383, from the UCI Machine Learning Repository. The project reads the supplied CSV from `data/raw/`.

2. **How large is the raw dataset?**  
   The inspection and integrity reports record 858 rows and 36 columns.

3. **What does `?` mean in the scripts?**  
   The scripts parse literal question marks as missing values in memory. The raw file is not edited.

4. **How many duplicate rows were found?**  
   There are 23 extra exact duplicate copies under full-row equality after parsing `?` as missing, grouped into 20 repeated-row groups.

5. **Were the duplicates proven to be accidental?**  
   No. The CSV does not establish whether identical rows are erroneous or represent separate observations. The first baseline excludes exact copies from its modeling copy as a provisional setting.

6. **What features were used for clustering?**  
   Age; number of sexual partners; first sexual intercourse; number of pregnancies; smoking years; smoking packs per year; hormonal contraceptive years; IUD years; and STD count.

7. **Were Biopsy or other screening outcomes used as clustering inputs?**  
   No. `Biopsy`, `Hinselmann`, `Schiller`, `Citology`, and direct diagnosis fields were excluded from the cluster input matrix.

8. **How were missing candidate values handled?**  
   The baseline filled each selected feature’s missing values with its median after exact duplicate removal. It is configurable and provisional; it may affect distances.

9. **Were the diagnosis-time missing values replaced by zero?**  
   No. Those columns are excluded from the candidate set, and their missing values were not interpreted as zero or confirmed absence of diagnosis.

10. **Why standardize features?**  
    Euclidean distances can be dominated by columns with larger numeric ranges. Standardization centers each selected feature and scales it by its population standard deviation. It changes geometry and does not make different feature meanings equivalent.

11. **What is the processed matrix shape?**  
    835 rows by 9 features, saved separately as `data/processed/PROVISIONAL_clustering_features.csv`.

## K-Means

12. **What does K-Means do?**  
    It assigns each point to its nearest centroid, recomputes each non-empty centroid as the mean of its assigned points, and repeats until its stopping condition or iteration limit.

13. **What is a centroid?**  
    It is the coordinate-wise mean of the records assigned to a cluster in the current feature space.

14. **What K values were tested?**  
    K=2, 3, 4, 5, and 6.

15. **How was K-Means initialized?**  
    Each run selected K distinct input rows as starting centroids. There were 10 starts per K, using NumPy seed 42; the lowest final-SSE run for each K is reported.

16. **What is SSE or inertia?**  
    It is the sum, over all records, of squared Euclidean distances from each record to its assigned centroid.

17. **What is the project’s MSE?**  
    Per-record MSE is total SSE divided by N=835 records. It is not divided by the number of feature cells.

18. **Why does inertia usually decrease as K increases?**  
    More centroids allow a partition to split groups and cannot worsen the globally optimal minimum SSE. In practice, finite initializations can converge to local solutions, so observed results also depend on the optimization procedure.

19. **What were the K-Means stopping settings?**  
    Maximum 300 iterations; stop when labels are unchanged or the maximum centroid shift is at most 0.0001.

20. **What was the highest saved K-Means silhouette?**  
    0.506262 at K=2, where the cluster sizes were 49 and 786. The uneven size distribution is relevant; the score alone does not decide K.

## DBSCAN and evaluation

21. **What does DBSCAN’s `eps` parameter mean?**  
    It is the radius used to define a point’s neighborhood under the selected distance, here Euclidean distance in the standardized feature space.

22. **What does `min_samples` mean?**  
    It is the minimum neighborhood count for a core point; scikit-learn counts the point itself in that neighborhood.

23. **What are core and border points?**  
    A core point has at least `min_samples` records in its `eps` neighborhood, including itself. A border point does not meet that count itself but lies in a core point’s neighborhood and can be assigned to that cluster.

24. **What is a noise point?**  
    It is not density-reachable from a core point under the current parameters and is labelled `-1` by the saved DBSCAN implementation.

25. **Does DBSCAN need a predefined cluster count?**  
    No. The number of clusters emerges from density connectivity and the selected `eps` and `min_samples` values.

26. **What DBSCAN grid was tested?**  
    `eps` = 1.0, 1.5, 2.0, 2.5 and `min_samples` = 5, 10, giving eight settings.

27. **What was the DBSCAN noise range?**  
    5.27% to 37.25% across the tested settings. Five settings formed one non-noise cluster.

28. **Why are some DBSCAN silhouettes undefined?**  
    The silhouette requires at least two clusters in the scored rows. A one-cluster non-noise result does not satisfy that condition, so the report records it as undefined.

29. **Why are DBSCAN and K-Means silhouette scores not directly equivalent here?**  
    K-Means silhouette includes all 835 records. DBSCAN silhouette excludes noise, so it may score a smaller subset; its coverage and cluster count can also differ by parameter setting.

30. **What does silhouette measure?**  
    It compares a record’s average distance to its own cluster with its average distance to the nearest other cluster. It is an internal geometric measure, not clinical or external validation.

31. **Why include cluster balance and coverage?**  
    A single large cluster and tiny clusters can produce a score that hides imbalance. Coverage and noise show how many records DBSCAN actually assigns to formed clusters, while balance summarizes cluster sizes.

32. **Which method is the winner?**  
    The project does not name an overall winner. Metrics, cluster sizes, coverage, noise, parameter sensitivity, and provisional data choices prevent a defensible single-score ranking.

33. **What is the main limitation?**  
    The results depend on provisional feature selection, median imputation, exact-duplicate removal, standardization, distance, and tested parameter ranges. These have not received teacher approval.

34. **Can the cluster labels be used as disease diagnoses?**  
    No. They are arbitrary exploratory group IDs from an educational data-mining exercise, not medical diagnoses or validated risk categories.

## Reproducibility

35. **How can the workflow be rerun?**  
    Run `python run_project.py` from the project root, or invoke its absolute path. The runner records package versions and settings in `outputs/results/workflow_run_manifest.md`.
