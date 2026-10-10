# Preprocessing Options for Provisional Clustering Features

> **Status: options for discussion only.** This document compares possible preprocessing choices for the nine provisional numeric candidates in `docs/clustering_feature_readiness.md`. It does not select a final feature set or method, change the raw CSV, or create processed data. The options predate the provisional baseline; its actual settings are recorded in `outputs/results/clustering_preprocessing_audit.md`. Those choices remain open to revision and are not teacher-approved.

## 1. Dataset observations

The readiness report describes 858 rows. Literal `?` values were treated as missing in memory for that analysis only. The nine proposed candidates are all multi-valued numeric fields; none was constant or binary in its observed values. Some are counts or durations, so the label “multi-valued numeric” does not mean that each variable is truly continuous.

| Candidate column | Missing values | Missing percentage | Observed unique values | Observed type |
| --- | ---: | ---: | ---: | --- |
| `Age` | 0 | 0.00% | 44 | Multi-valued numeric |
| `Number of sexual partners` | 26 | 3.03% | 12 | Multi-valued numeric |
| `First sexual intercourse` | 7 | 0.82% | 21 | Multi-valued numeric |
| `Num of pregnancies` | 56 | 6.53% | 11 | Multi-valued numeric |
| `Smokes (years)` | 13 | 1.52% | 30 | Multi-valued numeric |
| `Smokes (packs/year)` | 13 | 1.52% | 62 | Multi-valued numeric |
| `Hormonal Contraceptives (years)` | 108 | 12.59% | 40 | Multi-valued numeric |
| `IUD (years)` | 117 | 13.64% | 26 | Multi-valued numeric |
| `STDs (number)` | 105 | 12.24% | 5 | Multi-valued numeric |

The current proposal treats these as candidates, not approved clustering inputs. The readiness report excludes `Biopsy`, `Hinselmann`, `Schiller`, `Citology`, `Dx:Cancer`, `Dx:CIN`, `Dx:HPV`, `Dx`, and diagnosis-history fields from clustering inputs. No outcomes or diagnoses should be used to form the clusters.

## 2. Missing-value options

Distance calculations require values that can be compared in the same feature space. A `?` is an unknown or unrecorded value, not an observed zero. The following are options for later discussion; none has been applied.

| Option | Possible advantage | Risk or limitation | Provisional status |
| --- | --- | --- | --- |
| Complete-case rows for the selected feature set | Avoids inventing replacement values and keeps observed measurements intact. | Removing a row missing any selected field can reduce the data substantially or change which records remain. The retained row count and missingness pattern must be measured for the final feature set. | Candidate for comparison after teacher guidance; not selected. |
| Exclude a high-missingness feature from the initial feature set | Avoids filling many unknown values and may simplify the distance representation. | Removes that measurement from the study and may discard useful information. The feature choice must be justified and reported. | Consider for the diagnosis-time fields; decision pending. |
| Fill numeric values with a column mean | Simple numeric replacement and keeps the row count. | Can be influenced by extreme values and may pull missing records toward the center of a feature, changing distances and cluster membership. It can also create artificial values for integer counts. | Only if specifically approved and compared with another defensible option. |
| Fill numeric values with a column median | Less influenced by extreme values than the mean and simple to explain for skewed/count-like data. | Still creates an artificial value and can make records with missing data appear closer together. A median is not automatically a meaningful value for every duration or count. | Only if specifically approved; not selected. |
| Fill with zero or a mode | May look convenient for some coded fields. | Zero can mean a real observed value and is not equivalent to missing; mode filling repeats a common observed value and can create artificial density. Neither should be used without a field-specific rationale. | Do not apply by default. |
| Pairwise distance using whatever fields happen to be present | Could retain rows with partial values in some kinds of exploratory calculations. | Different record pairs would be compared using different subsets of features, making distances inconsistent. It is not the proposed common complete feature matrix for this K-Means/DBSCAN comparison. | Not proposed for the primary comparison. |

`Age` has no recorded missing values, so it needs no missing-value treatment in the inspected file. The remaining percentages range from 0.82% to 13.64%; the actual impact of complete-case removal depends on the combined pattern across whichever columns are finally approved.

### Diagnosis-time columns require separate care

`STDs: Time since first diagnosis` and `STDs: Time since last diagnosis` each have 787 missing values (about 91.72% of 858 rows). They are not among the nine provisional candidates. The preprocessing plan notes that all rows with missing times have `STDs: Number of diagnosis = 0`, but there are also missing-time rows with positive or unknown STD status; the data alone do not establish the reason for each missing value. The project notes also cite privacy or lack of information as possible explanations for nonresponse.

Do not convert the missing diagnosis times to zero or otherwise treat missing as “no diagnosis.” For the initial clustering comparison, exclusion from the input is a cautious proposal already recorded in the clustering study plan, not a final decision. Adding them would require clarification of their meaning and an approved missing-data policy. `STDs: Number of diagnosis` is also deferred because its diagnosis-count meaning has not been approved as a clustering feature.

## 3. Duplicate-record options and effects

The cleaning audit found 23 exact duplicate copies across 20 repeated-value groups. No duplicate handling has been approved or applied. Identical records can have real algorithmic effects:

- **K-Means:** repeated points receive repeated weight in centroid calculations. This can move a centroid and affect nearby assignments.
- **DBSCAN:** repeated points increase local point density. A location may meet `min_samples` because of repeated records, changing whether points form a dense region or are treated as noise.

Possible later policies are to retain all copies, remove only copies confirmed accidental, or run a separately documented sensitivity comparison if the teacher approves. A duplicate count alone cannot establish whether two records represent the same person or separate people with identical recorded values. Use the same approved row set for both algorithms, and document any change in row count. No rows are removed in this options review.

## 4. Normalization and standardization

K-Means and DBSCAN use distances. The candidate fields mix years, counts, age, and exposure units. Without scaling, a field with a wider numeric range can contribute more to Euclidean distance simply because its values have larger magnitudes. That can dominate both K-Means assignments and DBSCAN neighborhoods.

| Scaling option | Conceptual operation | Potential benefit | Limitation |
| --- | --- | --- | --- |
| Min-max normalization | Rescales observed values to a fixed interval, commonly 0 to 1. | Puts features on a shared bounded range and preserves the order of values. | Extreme values determine the endpoints and can compress most observations into a narrow interval. |
| Standardization | Subtracts the feature mean and divides by its standard deviation, producing values centered around zero with unit standard deviation. | Makes differences relative to each feature's spread and avoids using original units directly. | Does not bound values; unusual values can affect the mean and standard deviation. |

Neither option is automatically best. The final choice should be documented, used consistently for both algorithms, and considered alongside the feature distributions. Scaling does not resolve missing values, mixed feature meanings, redundant fields, or duplicate records. No scaling has been performed, and the choice remains provisional.

## 5. Binary/categorical and multi-valued numeric columns

The nine candidate columns above are multi-valued numeric, though several measure counts or durations. Their increments and units need interpretation; an integer count is not necessarily a continuous measurement. The readiness report separately identifies binary 0/1 risk-factor indicators as categorical in meaning even though they are stored numerically.

For the initial comparison, keeping the candidate representation numeric and leaving binary indicators out is one coherent option. If a binary field is added later, its 0/1 distance contribution should be considered explicitly: a one-unit change in a binary field may become as influential as one standardized unit in a numeric field. Do not silently combine indicators and numeric measurements or treat category codes as continuous quantities. Any separate feature design that includes categorical fields needs a clear, syllabus-appropriate explanation and the same representation for K-Means and DBSCAN.

Feature overlap also needs review. For example, durations and their corresponding use/status indicators may encode related information; age, age at first intercourse, and duration fields may also overlap conceptually. Including redundant measurements can give the related concept extra weight in distance calculations. This is a reason to review features, not a finding that any particular column must be removed.

## 6. Provisional options for a later comparison

A fair K-Means versus DBSCAN experiment could compare two or more approved preprocessing scenarios, such as:

1. One fixed numeric candidate set with a teacher-approved complete-case row policy.
2. The same fixed candidate set with a teacher-approved simple imputation policy, if imputation is chosen.
3. A separately labelled feature-set comparison that omits `STDs (number)` if the teacher decides its missingness or meaning makes it unsuitable.

For every scenario, both algorithms should receive the same columns, rows, missing-value treatment, and selected normalization or standardization. Report the input shape and feature definitions. Do not use `Biopsy`, other screening outcomes, or diagnosis fields as clustering inputs or as labels for interpreting cluster quality. Any comparison values and conclusions belong in the experiment report only after the methods are actually run.

## 7. Decisions awaiting teacher guidance

- Final numeric clustering feature set, including whether to use `STDs (number)`.
- Whether to omit diagnosis-time fields from the study or consider them later under a justified treatment.
- Missing-value policy for each selected feature: complete-case rows, approved imputation, or feature exclusion.
- Whether the 23 duplicate copies should be retained, removed after verification, or assessed in an approved sensitivity scenario.
- Whether to use min-max normalization or standardization, and how to document the chosen feature scale.
- Whether any binary/categorical columns should be included in a separately justified representation.
- Whether the proposed K-Means/DBSCAN comparison and its parameter and cluster-quality measures meet the teacher's project-sheet requirements.

No teacher approval is claimed. This document is a comparison of options, not a decision or implementation.
