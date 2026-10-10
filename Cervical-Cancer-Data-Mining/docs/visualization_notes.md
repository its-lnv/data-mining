# Exploratory Visualization Notes

The figures in `outputs/graphs/` are descriptive views of the supplied 858-row CSV. The script reads `data/raw/risk_factors_cervical_cancer.csv` with `?` interpreted as missing in a temporary Pandas DataFrame. It does not change the CSV, impute values, remove duplicates, resample observations, select a final target or predictor set, or train a model. The 23 duplicate copies remain in every applicable plot.

## Generated plots

| Plot | What it shows | Missing-value treatment |
| --- | --- | --- |
| `missing_values_by_column.png` | Missing-value counts for each of the 36 columns. | Literal `?` tokens are counted as missing in memory. No rows are removed. |
| `screening_outcome_class_counts.png` | Counts for values 0 and 1 in `Biopsy`, `Hinselmann`, `Schiller`, and `Citology`. | Missing and non-0/1 values, if any, are omitted from the class bars and their counts are stated in the plot title. The inspected file has no missing values for these columns. |
| `age_distribution.png` | Histogram of recorded ages. | Missing ages are omitted from the histogram; the plot title states the omitted count. The inspection found no missing age values. |
| `sexual_partners_distribution.png` | Counts for recorded values of `Number of sexual partners`. | Missing values are omitted from the bars and the title states the omitted count (26 in this file). |
| `first_intercourse_age_distribution.png` | Counts by recorded `First sexual intercourse` age. | Missing values are omitted from the bars and the title states the omitted count (7 in this file). |
| `pregnancies_distribution.png` | Counts by recorded `Num of pregnancies` value. | Missing values are omitted from the bars and the title states the omitted count (56 in this file). |
| `smoking_status_counts.png` | Counts for the recorded `Smokes` codes 0 and 1, plus a separate Missing bar. | Missing values are displayed as their own category (13 in this file), not imputed. Codes are shown as recorded; the chart does not infer additional meaning. |

## Limitations

During final submission review, the original vertical missing-value chart was found to have overlapping long column labels. `src/data_visualization.py` now uses a sorted horizontal bar chart with value labels, and `missing_values_by_column.png` was regenerated. The plotted values and treatment are unchanged.

These plots summarize the current file only. Duplicate rows are retained because their handling is unresolved; they contribute to plotted counts. Histograms and category counts describe recorded values and do not explain why values are missing. Class-count figures are not model evaluation results. None of the plots establishes cause, medical risk, or a clinical conclusion, and they do not finalize a target or predictor set.
