# Data Integrity Verification

> Read-only verification. Literal `?` markers were treated as missing in memory only. No rows or values were removed, filled, scaled, or otherwise transformed.

## Verified dataset structure

- **Source:** `data/raw/risk_factors_cervical_cancer.csv`
- **Rows:** 858
- **Columns:** 36
- **Expected candidate columns present:** 9 of 9
- **Missing candidate columns:** None

### Provisional clustering candidate features

Missing counts use the full dataset row count. Dtypes are pandas-inferred after interpreting `?` as missing.

| Column | Inferred pandas dtype | Missing values |
| --- | --- | --- |
| Age | int64 | 0 |
| Number of sexual partners | float64 | 26 |
| First sexual intercourse | float64 | 7 |
| Num of pregnancies | float64 | 56 |
| Smokes (years) | float64 | 13 |
| Smokes (packs/year) | float64 | 13 |
| Hormonal Contraceptives (years) | float64 | 108 |
| IUD (years) | float64 | 117 |
| STDs (number) | float64 | 105 |

## Duplicate-row verification

Definition: rows are exact duplicates when all column values match after parsing `?` as missing. The duplicate-copy count uses `duplicated(keep='first')`, so the first occurrence is not counted. A repeated-row group is one distinct full-row pattern with at least two occurrences; matching missing positions are grouped together.

- **Extra duplicate copies:** 23
- **Repeated-row groups:** 20
- **Rows participating in repeated groups:** 43
- **Documented historical counts:** 23 extra copies across 20 groups
- **Duplicate comparison:** matches the documented counts.

## Comparison with existing documentation

- **Shape comparison:** matches the documented 858 rows and 36 columns.
- **Duplicate comparison:** matches the documented extra-copy and repeated-group counts.
- **Discrepancies:**

None detected against the stated historical counts.

## Integrity and unresolved decisions

- **Raw-file SHA-256 before/after this run:** unchanged
- No duplicate policy was applied; all original rows remain in the source file.
- No imputation or interpretation of diagnosis-time missingness was applied.
- The candidate list remains provisional; feature inclusion, missing-value handling, duplicate treatment, and scaling require later justification and teacher guidance.
- Screening outcomes and diagnosis fields are not included in the candidate-feature check and remain excluded as clustering inputs under the current study plan.
- No K-Means, DBSCAN, or other data-mining algorithm was run.
