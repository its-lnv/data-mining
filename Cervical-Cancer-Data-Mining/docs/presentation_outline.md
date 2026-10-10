# Presentation Outline (9 Slides)

## Slide 1 — Title and project scope

- Editable student, course, institution, teacher, and date fields
- Title: Comparative Clustering of Cervical Cancer Risk-Factor Records
- State that scope and preprocessing choices remain provisional
- Visual: simple two-method comparison motif; no clinical imagery needed

## Slide 2 — Dataset and data quality

- UCI source, 858 rows, 36 columns
- 23 exact duplicate copies and `?` missing markers
- 787 missing entries in each of the two diagnosis-time columns
- Visual: missing-values-by-column figure

## Slide 3 — Provisional feature matrix

- List the nine candidate inputs
- Explain exclusion of screening outcomes and diagnosis fields
- Show median imputation, exact duplicate removal, and standardization as provisional
- Show 835 × 9 output dimensions
- Visual: preparation flow diagram: raw CSV → selected columns → provisional processing → shared matrix

## Slide 4 — K-Means method and settings

- Centroid assignment and update, K selection, multiple starts
- K=2–6; 10 starts; seed 42; stopping rule
- Define SSE/inertia and MSE=SSE/835
- Visual: simple Lloyd iteration diagram or MSE-by-iteration plot

## Slide 5 — K-Means results

- Concise table: K, silhouette, cluster sizes, MSE
- Highest saved silhouette at K=2; emphasize uneven 49/786 sizes
- Explain SSE generally declines as K rises, so it does not alone select K
- Visual: inertia-by-K and silhouette-by-K figures

## Slide 6 — DBSCAN method and parameter grid

- Explain `eps`, `min_samples`, core/border/noise, no predefined K
- Grid: eps 1.0/1.5/2.0/2.5 and min_samples 5/10
- Visual: density neighborhood schematic (conceptual) plus parameter grid

## Slide 7 — DBSCAN findings

- One to six clusters, 5.27%–37.25% noise
- Five of eight settings produce one cluster and undefined silhouette
- Explain silhouette is computed only for non-noise records
- Visual: cluster-count, noise, and valid silhouette plots

## Slide 8 — Comparative evaluation and limitations

- Compare cluster sizes, balance, coverage/noise, and silhouette population
- K-Means covers all rows; DBSCAN may mark noise
- Do not compare SSE as if DBSCAN had the same objective
- Visual: comparative balance and coverage/noise graphs

## Slide 9 — Conclusion and discussion

- Describe results as parameter-dependent exploratory groupings
- No universal winner or clinical interpretation
- List provisional assumptions and pending teacher confirmation
- Visual: summary checklist or workflow output paths
