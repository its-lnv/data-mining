# Dataset Inspection Report

## Dataset

- **File:** `data/raw/risk_factors_cervical_cancer.csv`
- **Rows:** 858
- **Columns:** 36
- **Duplicate rows:** 23

## Column names

`Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives`, `Hormonal Contraceptives (years)`, `IUD`, `IUD (years)`, `STDs`, `STDs (number)`, `STDs:condylomatosis`, `STDs:cervical condylomatosis`, `STDs:vaginal condylomatosis`, `STDs:vulvo-perineal condylomatosis`, `STDs:syphilis`, `STDs:pelvic inflammatory disease`, `STDs:genital herpes`, `STDs:molluscum contagiosum`, `STDs:AIDS`, `STDs:HIV`, `STDs:Hepatitis B`, `STDs:HPV`, `STDs: Number of diagnosis`, `STDs: Time since first diagnosis`, `STDs: Time since last diagnosis`, `Dx:Cancer`, `Dx:CIN`, `Dx:HPV`, `Dx`, `Hinselmann`, `Schiller`, `Citology`, `Biopsy`

## Data types

| Column | Pandas dtype |
| --- | --- |
| Age | int64 |
| Number of sexual partners | float64 |
| First sexual intercourse | float64 |
| Num of pregnancies | float64 |
| Smokes | float64 |
| Smokes (years) | float64 |
| Smokes (packs/year) | float64 |
| Hormonal Contraceptives | float64 |
| Hormonal Contraceptives (years) | float64 |
| IUD | float64 |
| IUD (years) | float64 |
| STDs | float64 |
| STDs (number) | float64 |
| STDs:condylomatosis | float64 |
| STDs:cervical condylomatosis | float64 |
| STDs:vaginal condylomatosis | float64 |
| STDs:vulvo-perineal condylomatosis | float64 |
| STDs:syphilis | float64 |
| STDs:pelvic inflammatory disease | float64 |
| STDs:genital herpes | float64 |
| STDs:molluscum contagiosum | float64 |
| STDs:AIDS | float64 |
| STDs:HIV | float64 |
| STDs:Hepatitis B | float64 |
| STDs:HPV | float64 |
| STDs: Number of diagnosis | int64 |
| STDs: Time since first diagnosis | float64 |
| STDs: Time since last diagnosis | float64 |
| Dx:Cancer | int64 |
| Dx:CIN | int64 |
| Dx:HPV | int64 |
| Dx | int64 |
| Hinselmann | int64 |
| Schiller | int64 |
| Citology | int64 |
| Biopsy | int64 |

## Missing values

`Missing values` counts values treated as missing by pandas after interpreting literal `?` as missing. `Question marks` counts literal `?` tokens in the source CSV.

| Column | Missing values | Question marks |
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

## Target column value counts

### Hinselmann

| Value | Count |
| --- | --- |
| 0 | 823 |
| 1 | 35 |

### Schiller

| Value | Count |
| --- | --- |
| 0 | 784 |
| 1 | 74 |

### Citology

| Value | Count |
| --- | --- |
| 0 | 814 |
| 1 | 44 |

### Biopsy

| Value | Count |
| --- | --- |
| 0 | 803 |
| 1 | 55 |



## Numerical columns (non-binary numeric values)

`Age`, `Number of sexual partners`, `First sexual intercourse`, `Num of pregnancies`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives (years)`, `IUD (years)`, `STDs (number)`, `STDs: Number of diagnosis`, `STDs: Time since first diagnosis`, `STDs: Time since last diagnosis`

## Categorical columns (binary-coded 0/1)

`Smokes`, `Hormonal Contraceptives`, `IUD`, `STDs`, `STDs:condylomatosis`, `STDs:cervical condylomatosis`, `STDs:vaginal condylomatosis`, `STDs:vulvo-perineal condylomatosis`, `STDs:syphilis`, `STDs:pelvic inflammatory disease`, `STDs:genital herpes`, `STDs:molluscum contagiosum`, `STDs:AIDS`, `STDs:HIV`, `STDs:Hepatitis B`, `STDs:HPV`, `Dx:Cancer`, `Dx:CIN`, `Dx:HPV`, `Dx`, `Hinselmann`, `Schiller`, `Citology`, `Biopsy`

All columns have numeric pandas dtypes after interpreting `?` as missing. The categorical list above flags numeric columns whose observed non-missing values are only 0 and 1; review their meaning before analysis.

## Preview (first 8 rows)

```text
 Age  Number of sexual partners  First sexual intercourse  Num of pregnancies  Smokes  Smokes (years)  Smokes (packs/year)  Hormonal Contraceptives  Hormonal Contraceptives (years)  IUD  IUD (years)  STDs  STDs (number)  STDs:condylomatosis  STDs:cervical condylomatosis  STDs:vaginal condylomatosis  STDs:vulvo-perineal condylomatosis  STDs:syphilis  STDs:pelvic inflammatory disease  STDs:genital herpes  STDs:molluscum contagiosum  STDs:AIDS  STDs:HIV  STDs:Hepatitis B  STDs:HPV  STDs: Number of diagnosis  STDs: Time since first diagnosis  STDs: Time since last diagnosis  Dx:Cancer  Dx:CIN  Dx:HPV  Dx  Hinselmann  Schiller  Citology  Biopsy
  18                        4.0                      15.0                 1.0     0.0             0.0                  0.0                      0.0                              0.0  0.0          0.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           0         0         0       0
  15                        1.0                      14.0                 1.0     0.0             0.0                  0.0                      0.0                              0.0  0.0          0.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           0         0         0       0
  34                        1.0                       NaN                 1.0     0.0             0.0                  0.0                      0.0                              0.0  0.0          0.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           0         0         0       0
  52                        5.0                      16.0                 4.0     1.0            37.0                 37.0                      1.0                              3.0  0.0          0.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          1       0       1   0           0         0         0       0
  46                        3.0                      21.0                 4.0     0.0             0.0                  0.0                      1.0                             15.0  0.0          0.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           0         0         0       0
  42                        3.0                      23.0                 2.0     0.0             0.0                  0.0                      0.0                              0.0  0.0          0.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           0         0         0       0
  51                        3.0                      17.0                 6.0     1.0            34.0                  3.4                      0.0                              0.0  1.0          7.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           1         1         0       1
  26                        1.0                      26.0                 3.0     0.0             0.0                  0.0                      1.0                              2.0  1.0          7.0   0.0            0.0                  0.0                           0.0                          0.0                                 0.0            0.0                               0.0                  0.0                         0.0        0.0       0.0               0.0       0.0                          0                               NaN                              NaN          0       0       0   0           0         0         0       0
```

## Initial preprocessing considerations

- Resolve the missing entries recorded above, including literal `?` values, using a method agreed with the teacher.
- Review duplicate rows and decide whether they represent repeated observations before handling them.
- Confirm the target column and predictor feature set with the teacher after reviewing the dataset and project requirements.
- Many outcome and risk-factor indicators are 0/1 coded; review their categorical meaning. The four requested target columns are imbalanced, so account for their class distributions when selecting evaluation measures.
- `STDs: Time since first diagnosis` and `STDs: Time since last diagnosis` each have 787 missing entries; assess whether those values are structurally missing.
- Check feature scales and categorical encodings during preprocessing; this report does not alter or preprocess the source data.
