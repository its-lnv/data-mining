"""Summarize whether proposed numeric columns are ready for clustering.

This script reads the raw CSV and writes a Markdown readiness report. It does
not impute, remove, scale, transform, or save any dataset rows, and it does not
run K-Means or DBSCAN.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
REPORT_PATH = PROJECT_ROOT / "docs" / "clustering_feature_readiness.md"

# These are candidate numeric measurements from the provisional clustering
# plan. They are not a final feature set and need teacher guidance.
CANDIDATE_COLUMNS = [
    "Age",
    "Number of sexual partners",
    "First sexual intercourse",
    "Num of pregnancies",
    "Smokes (years)",
    "Smokes (packs/year)",
    "Hormonal Contraceptives (years)",
    "IUD (years)",
    "STDs (number)",
]

# Outcomes and direct diagnosis fields are never considered candidate inputs.
EXCLUDED_OUTCOME_COLUMNS = [
    "Biopsy",
    "Hinselmann",
    "Schiller",
    "Citology",
]
EXCLUDED_DIAGNOSIS_COLUMNS = [
    "Dx:Cancer",
    "Dx:CIN",
    "Dx:HPV",
    "Dx",
    "STDs: Number of diagnosis",
    "STDs: Time since first diagnosis",
    "STDs: Time since last diagnosis",
]


def markdown_table(headers, rows):
    """Create a simple Markdown table without extra dependencies."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def describe_values(series):
    """Classify observed values by their shape, not by medical meaning."""
    observed = series.dropna()
    unique_count = int(observed.nunique())

    if unique_count == 0:
        return unique_count, "no observed values"
    if unique_count == 1:
        return unique_count, "constant"
    if unique_count == 2:
        unique_values = set(observed.unique().tolist())
        if unique_values == {0, 1} or unique_values == {0.0, 1.0}:
            return unique_count, "binary (0/1)"
        return unique_count, "binary (two observed values)"
    return unique_count, "continuous / multi-valued numeric"


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Raw dataset not found: {CSV_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )

    # Interpret '?' as missing in this in-memory DataFrame only.
    data = pd.read_csv(CSV_PATH, na_values=["?"])
    total_rows = len(data)
    rows_for_report = []
    suitability_notes = []

    for column in CANDIDATE_COLUMNS:
        if column not in data.columns:
            rows_for_report.append((column, "not present", "not present", "not present", "not assessed"))
            suitability_notes.append(f"- `{column}` is not present in this CSV; it cannot be assessed.")
            continue

        values = pd.to_numeric(data[column], errors="coerce")
        missing_count = int(values.isna().sum())
        missing_percent = (missing_count / total_rows * 100) if total_rows else 0.0
        unique_count, value_type = describe_values(values)
        rows_for_report.append(
            (
                column,
                f"{missing_count} ({missing_percent:.2f}%)",
                unique_count,
                value_type,
                str(data[column].dtype),
            )
        )

        if missing_count:
            suitability_notes.append(
                f"- `{column}` has {missing_count} missing values ({missing_percent:.2f}%); "
                "distance calculations need a teacher-approved missing-data policy."
            )
        if value_type == "continuous / multi-valued numeric":
            suitability_notes.append(
                f"- `{column}` has multiple numeric values. Its measurement units and range "
                "may differ from other columns, so unscaled Euclidean distance could give it "
                "more influence; its values may also be count-like or duration-like rather "
                "than truly continuous."
            )
        elif value_type.startswith("binary"):
            suitability_notes.append(
                f"- `{column}` has only two observed values. Confirm its coding and intended "
                "distance contribution before combining it with continuous measurements."
            )
        elif value_type == "constant":
            suitability_notes.append(
                f"- `{column}` is constant among observed rows and would not distinguish "
                "observations in a distance calculation."
            )

    excluded_outcomes = [column for column in EXCLUDED_OUTCOME_COLUMNS if column in data.columns]
    excluded_diagnoses = [column for column in EXCLUDED_DIAGNOSIS_COLUMNS if column in data.columns]
    candidate_present = [column for column in CANDIDATE_COLUMNS if column in data.columns]

    report = [
        "# Clustering Feature Readiness Analysis\n\n",
        "> **Provisional analysis only.** It reads the raw CSV and reports observed feature properties. It does not clean, transform, scale, impute, remove duplicates, create a processed dataset, or run K-Means or DBSCAN.\n\n",
        "## Dataset and scope\n\n",
        f"- **Source file:** `data/raw/{CSV_PATH.name}`\n",
        f"- **Rows inspected:** {total_rows}\n",
        f"- **Candidate numeric columns present:** {len(candidate_present)} of {len(CANDIDATE_COLUMNS)}\n",
        "- Literal `?` values are treated as missing in memory only.\n",
        "- The candidate list follows `docs/clustering_study_plan.md`; it is not an approved final feature set.\n\n",
        "## Candidate feature summary\n\n",
        "Missing percentages use all dataset rows as the denominator. Unique-value counts exclude missing entries. The observed-type label is a simple data check: `continuous / multi-valued numeric` does not prove that a field is mathematically continuous; count and duration fields may be discrete.\n\n",
        markdown_table(
            ["Candidate column", "Missing count (%)", "Unique observed values", "Observed value type", "Pandas dtype"],
            rows_for_report,
        ),
        "\n\n",
        "## Outcome and diagnosis exclusions\n\n",
        "The following screening outcomes are explicitly excluded from clustering inputs: "
        + (", ".join(f"`{column}`" for column in excluded_outcomes) or "none found")
        + ".\n\n",
        "The following direct diagnosis or diagnosis-history fields are also excluded from this candidate input review: "
        + (", ".join(f"`{column}`" for column in excluded_diagnoses) or "none found")
        + ". These fields must not be used to form clusters.\n\n",
        "Other 0/1-coded risk-factor indicators are numeric in storage but categorical in meaning; they are not part of this initial all-numeric candidate list.\n\n",
        "## Distance-based suitability considerations\n\n",
        "\n".join(suitability_notes) if suitability_notes else "No candidate columns were available for assessment.",
        "\n\n",
        "- **Different units and ranges:** age, counts, and durations may contribute very differently to Euclidean distance. Scaling may be considered later, but no scaling was done here.\n",
        "- **Missing values:** K-Means and DBSCAN need numeric distance comparisons; missing entries cannot be passed through as ordinary values. Do not fill them with zero or remove rows until a policy is approved.\n",
        "- **Mixed data types:** binary indicators and multi-valued measurements do not automatically have comparable distances. Keep them separate unless a justified representation is approved.\n",
        "- **Duplicates:** the existing audit records 23 exact duplicate copies. Repeated rows may affect K-Means centroids and DBSCAN density; this analysis retains them and does not choose a duplicate policy.\n",
        "- **Related features:** related measures (for example, age and durations) may give overlapping information and may unintentionally weight similar concepts more than once. Review feature meaning before selecting the final columns.\n\n",
        "## Decisions still provisional\n\n",
        "- Final candidate columns and whether `STDs (number)` belongs in the input.\n",
        "- Missing-value treatment and whether diagnosis-time fields remain excluded.\n",
        "- Duplicate handling.\n",
        "- Whether any binary-coded fields should be considered in a separate mixed-feature analysis.\n",
        "- Scaling method, distance settings, and K-Means / DBSCAN parameter ranges.\n\n",
        "No feature is claimed to prove cancer risk or cause disease. Any later clusters will be exploratory groups based on the selected recorded values, not medical risk categories. No teacher approval is claimed.\n",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("".join(report), encoding="utf-8")
    print(f"Inspected {total_rows} rows and {len(data.columns)} columns.")
    print(f"Candidate columns present: {len(candidate_present)} of {len(CANDIDATE_COLUMNS)}.")
    print(f"Readiness report: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print("No dataset transformation or clustering was performed.")


if __name__ == "__main__":
    main()
