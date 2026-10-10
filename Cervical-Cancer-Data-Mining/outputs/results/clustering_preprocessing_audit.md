# Provisional Clustering Preprocessing Audit

> This is a derived feature matrix for a provisional clustering baseline, not teacher-approved preprocessing. The raw CSV was read-only; no clustering algorithm was run.

## Input and output summary

- **Raw source:** `data/raw/risk_factors_cervical_cancer.csv`
- **Original raw dimensions:** 858 rows x 36 columns
- **Exact duplicate copies detected:** 23 (full-row equality across the parsed raw table; first occurrence retained for counting)
- **Duplicate policy:** `drop_exact`
- **Rows after duplicate policy:** 835
- **Processed matrix dimensions:** 835 rows x 9 features
- **Processed feature file:** `data/processed/PROVISIONAL_clustering_features.csv`
- **Audit report:** `outputs/results/clustering_preprocessing_audit.md`
- **Configured random seed:** 42 (no random operation was used in this preprocessing step)
- **Raw SHA-256 unchanged:** True

## Configured provisional choices

- **Features:** `Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives (years)`, `IUD (years)`, `STDs (number)`
- **Missing-value policy:** `median`. Median imputation is a simple, robust-to-extremes choice for these numeric/count-like features and retains rows; it still creates synthetic values and can change distances, so this is provisional.
- **Scaling:** `standardize`. Features use different units and ranges; without scaling, large-range measurements can dominate Euclidean distances used by K-Means and the `eps` neighborhood distances used by DBSCAN.
- **Excluded inputs:** screening outcomes and direct diagnosis/diagnosis-history fields are prohibited by configuration.

## Missingness by candidate feature

Counts before handling refer to the original parsed rows. The middle column is after duplicate handling; final counts are after the configured missing-value policy.

| Feature | Missing before duplicate handling | Missing after duplicate handling | Missing after handling | Inferred numeric dtype |
| --- | --- | --- | --- | --- |
| Age | 0 | 0 | 0 | int64 |
| Number of sexual partners | 26 | 25 | 0 | float64 |
| First sexual intercourse | 7 | 7 | 0 | float64 |
| Num of pregnancies | 56 | 56 | 0 | float64 |
| Smokes (years) | 13 | 13 | 0 | float64 |
| Smokes (packs/year) | 13 | 13 | 0 | float64 |
| Hormonal Contraceptives (years) | 108 | 103 | 0 | float64 |
| IUD (years) | 117 | 112 | 0 | float64 |
| STDs (number) | 105 | 100 | 0 | float64 |

## Imputation values

| Feature | Median used |
| --- | --- |
| Age | 26 |
| Number of sexual partners | 2 |
| First sexual intercourse | 17 |
| Num of pregnancies | 2 |
| Smokes (years) | 0 |
| Smokes (packs/year) | 0 |
| Hormonal Contraceptives (years) | 0.5 |
| IUD (years) | 0 |
| STDs (number) | 0 |

## Scaling parameters

| Feature | Center / minimum | Scale / maximum |
| --- | --- | --- |
| Age | mean=27.023952 | population std=8.4779051 |
| Number of sexual partners | mean=2.5353293 | population std=1.653053 |
| First sexual intercourse | mean=17.020359 | population std=2.8034739 |
| Num of pregnancies | mean=2.2838323 | population std=1.4073084 |
| Smokes (years) | mean=1.2343289 | population std=4.108801 |
| Smokes (packs/year) | mean=0.45857082 | population std=2.2380214 |
| Hormonal Contraceptives (years) | mean=2.0805202 | population std=3.5992068 |
| IUD (years) | mean=0.4568503 | population std=1.8364397 |
| STDs (number) | mean=0.15928144 | population std=0.53591443 |

## Validation results

- All configured columns were present.
- Candidate values parsed as numeric; unexpected non-numeric values were not found.
- No candidate feature was entirely missing.
- Processed output is non-empty and contains only finite numeric values.
- The processed file contains only the configured feature columns; no target or diagnosis columns were added.

## Warnings and unresolved decisions

- These processing choices are provisional and have not received teacher approval.
- Exact duplicate rows may represent separate observations; removing them can change DBSCAN density and K-Means centroids.
- Median imputation inserts synthetic values and can change distances or make imputed records appear closer together.
- Diagnosis-time columns are excluded from the configured candidate list; no missing diagnosis-time value was interpreted as zero or confirmed absence.
- Standardization choices affect distance geometry and therefore both clustering methods; use this same matrix for a fair comparison.

The feature list, median-imputation policy, exact-duplicate removal policy, and standardization method are configurable provisional defaults. Review them before interpreting or comparing clusters. In particular, whether exact duplicate rows are erroneous remains unresolved. This project is educational and is not intended for clinical diagnosis.
