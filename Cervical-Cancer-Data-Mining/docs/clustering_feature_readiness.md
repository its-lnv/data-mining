# Clustering Feature Readiness Analysis

> **Provisional analysis only.** It reads the raw CSV and reports observed feature properties. It does not clean, transform, scale, impute, remove duplicates, create a processed dataset, or run K-Means or DBSCAN.

## Dataset and scope

- **Source file:** `data/raw/risk_factors_cervical_cancer.csv`
- **Rows inspected:** 858
- **Candidate numeric columns present:** 9 of 9
- Literal `?` values are treated as missing in memory only.
- The candidate list follows `docs/clustering_study_plan.md`; it is not an approved final feature set.

## Candidate feature summary

Missing percentages use all dataset rows as the denominator. Unique-value counts exclude missing entries. The observed-type label is a simple data check: `continuous / multi-valued numeric` does not prove that a field is mathematically continuous; count and duration fields may be discrete.

| Candidate column | Missing count (%) | Unique observed values | Observed value type | Pandas dtype |
| --- | --- | --- | --- | --- |
| Age | 0 (0.00%) | 44 | continuous / multi-valued numeric | int64 |
| Number of sexual partners | 26 (3.03%) | 12 | continuous / multi-valued numeric | float64 |
| First sexual intercourse | 7 (0.82%) | 21 | continuous / multi-valued numeric | float64 |
| Num of pregnancies | 56 (6.53%) | 11 | continuous / multi-valued numeric | float64 |
| Smokes (years) | 13 (1.52%) | 30 | continuous / multi-valued numeric | float64 |
| Smokes (packs/year) | 13 (1.52%) | 62 | continuous / multi-valued numeric | float64 |
| Hormonal Contraceptives (years) | 108 (12.59%) | 40 | continuous / multi-valued numeric | float64 |
| IUD (years) | 117 (13.64%) | 26 | continuous / multi-valued numeric | float64 |
| STDs (number) | 105 (12.24%) | 5 | continuous / multi-valued numeric | float64 |

## Outcome and diagnosis exclusions

The following screening outcomes are explicitly excluded from clustering inputs: `Biopsy`, `Hinselmann`, `Schiller`, `Citology`.

The following direct diagnosis or diagnosis-history fields are also excluded from this candidate input review: `Dx:Cancer`, `Dx:CIN`, `Dx:HPV`, `Dx`, `STDs: Number of diagnosis`, `STDs: Time since first diagnosis`, `STDs: Time since last diagnosis`. These fields must not be used to form clusters.

Other 0/1-coded risk-factor indicators are numeric in storage but categorical in meaning; they are not part of this initial all-numeric candidate list.

## Distance-based suitability considerations

- `Age` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `Number of sexual partners` has 26 missing values (3.03%); distance calculations need a teacher-approved missing-data policy.
- `Number of sexual partners` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `First sexual intercourse` has 7 missing values (0.82%); distance calculations need a teacher-approved missing-data policy.
- `First sexual intercourse` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `Num of pregnancies` has 56 missing values (6.53%); distance calculations need a teacher-approved missing-data policy.
- `Num of pregnancies` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `Smokes (years)` has 13 missing values (1.52%); distance calculations need a teacher-approved missing-data policy.
- `Smokes (years)` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `Smokes (packs/year)` has 13 missing values (1.52%); distance calculations need a teacher-approved missing-data policy.
- `Smokes (packs/year)` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `Hormonal Contraceptives (years)` has 108 missing values (12.59%); distance calculations need a teacher-approved missing-data policy.
- `Hormonal Contraceptives (years)` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `IUD (years)` has 117 missing values (13.64%); distance calculations need a teacher-approved missing-data policy.
- `IUD (years)` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.
- `STDs (number)` has 105 missing values (12.24%); distance calculations need a teacher-approved missing-data policy.
- `STDs (number)` has multiple numeric values. Its measurement units and range may differ from other columns, so unscaled Euclidean distance could give it more influence; its values may also be count-like or duration-like rather than truly continuous.

- **Different units and ranges:** age, counts, and durations may contribute very differently to Euclidean distance. Scaling may be considered later, but no scaling was done here.
- **Missing values:** K-Means and DBSCAN need numeric distance comparisons; missing entries cannot be passed through as ordinary values. Do not fill them with zero or remove rows until a policy is approved.
- **Mixed data types:** binary indicators and multi-valued measurements do not automatically have comparable distances. Keep them separate unless a justified representation is approved.
- **Duplicates:** the existing audit records 23 exact duplicate copies. Repeated rows may affect K-Means centroids and DBSCAN density; this analysis retains them and does not choose a duplicate policy.
- **Related features:** related measures (for example, age and durations) may give overlapping information and may unintentionally weight similar concepts more than once. Review feature meaning before selecting the final columns.

## Decisions still provisional

- Final candidate columns and whether `STDs (number)` belongs in the input.
- Missing-value treatment and whether diagnosis-time fields remain excluded.
- Duplicate handling.
- Whether any binary-coded fields should be considered in a separate mixed-feature analysis.
- Scaling method, distance settings, and K-Means / DBSCAN parameter ranges.

No feature is claimed to prove cancer risk or cause disease. The clusters produced later in this project are exploratory groups based on the provisional selected recorded values, not medical risk categories. No teacher approval is claimed.
