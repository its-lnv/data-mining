# PROVISIONAL Data Cleaning Audit

> Audit only: this is not a cleaned dataset. The source CSV was read but not modified.

## Dataset summary

- **Source:** `data/raw/risk_factors_cervical_cancer.csv`
- **Rows:** 858
- **Columns:** 36
- **Exact duplicate rows beyond the first copy:** 23
- **Groups containing repeated rows:** 20
- **Duplicate handling:** pending teacher decision; no rows removed.
- **Missing-value handling:** literal `?` is treated as missing in this in-memory audit only; no values were imputed.

## Missing-value counts

`Missing after parsing` includes `?` as missing. `Literal ?` counts those source tokens directly.

| Column | Missing after parsing | Literal ? |
| --- | --- | --- |
| Age | 0 | 0 |
| Number of sexual partners | 26 | 26 |
| First sexual intercourse | 7 | 7 |
| Num of pregnancies | 56 | 56 |
| Smokes | 13 | 13 |
| Smokes (years) | 13 | 13 |
| Smokes (packs/year) | 13 | 13 |
| Hormonal Contraceptives | 108 | 108 |
| Hormonal Contraceptives (years) | 108 | 108 |
| IUD | 117 | 117 |
| IUD (years) | 117 | 117 |
| STDs | 105 | 105 |
| STDs (number) | 105 | 105 |
| STDs:condylomatosis | 105 | 105 |
| STDs:cervical condylomatosis | 105 | 105 |
| STDs:vaginal condylomatosis | 105 | 105 |
| STDs:vulvo-perineal condylomatosis | 105 | 105 |
| STDs:syphilis | 105 | 105 |
| STDs:pelvic inflammatory disease | 105 | 105 |
| STDs:genital herpes | 105 | 105 |
| STDs:molluscum contagiosum | 105 | 105 |
| STDs:AIDS | 105 | 105 |
| STDs:HIV | 105 | 105 |
| STDs:Hepatitis B | 105 | 105 |
| STDs:HPV | 105 | 105 |
| STDs: Number of diagnosis | 0 | 0 |
| STDs: Time since first diagnosis | 787 | 787 |
| STDs: Time since last diagnosis | 787 | 787 |
| Dx:Cancer | 0 | 0 |
| Dx:CIN | 0 | 0 |
| Dx:HPV | 0 | 0 |
| Dx | 0 | 0 |
| Hinselmann | 0 | 0 |
| Schiller | 0 | 0 |
| Citology | 0 | 0 |
| Biopsy | 0 | 0 |

## Duplicate row locations

The following CSV line numbers are extra copies after each group's first row. They are listed for review only; the audit does not decide whether these observations are erroneous.

68, 236, 257, 358, 397, 408, 421, 433, 437, 442, 444, 455, 456, 468, 488, 527, 532, 538, 577, 582, 640, 717, 787

## Pending decisions

- Confirm whether exact duplicate rows are accidental copies before removing or grouping them.
- Approve missing-value handling; this audit does not impute values.
- Decide how to handle the two diagnosis-time columns with 787 missing entries each.
- Confirm the target and predictor columns before creating a modeling-ready dataset.
- Do not resample the Biopsy classes unless explicitly approved.
