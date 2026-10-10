from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
REPORT_PATH = PROJECT_ROOT / "docs" / "dataset_inspection.md"
TARGET_COLUMNS = ["Hinselmann", "Schiller", "Citology", "Biopsy"]
PREVIEW_ROWS = 8


def markdown_table(headers, rows):
    """Render a small Markdown table without optional dependencies."""
    def clean(value):
        return str(value).replace("|", r"\|").replace("\n", " ")

    lines = ["| " + " | ".join(clean(item) for item in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend(
        "| " + " | ".join(clean(item) for item in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )

    # Count literal question marks separately, then parse them as missing values
    # so pandas can infer numeric data types where possible.
    raw = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    df = pd.read_csv(CSV_PATH, na_values=["?"])

    rows, columns = df.shape
    missing_rows = []
    for column in df.columns:
        question_marks = int(raw[column].eq("?").sum())
        pandas_missing = int(df[column].isna().sum())
        missing_rows.append((column, pandas_missing, question_marks))

    dtype_rows = [(column, str(dtype)) for column, dtype in df.dtypes.items()]
    numeric_dtype_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = [
        column
        for column in numeric_dtype_columns
        if set(df[column].dropna().unique()).issubset({0, 1})
    ]
    numerical_columns = [
        column for column in numeric_dtype_columns if column not in categorical_columns
    ]

    duplicate_count = int(df.duplicated().sum())
    target_sections = []
    missing_targets = [column for column in TARGET_COLUMNS if column not in df.columns]
    for column in TARGET_COLUMNS:
        if column not in df.columns:
            continue
        counts = df[column].value_counts(dropna=False, sort=False)
        target_sections.append(f"### {column}\n\n")
        target_sections.append(
            markdown_table(
                ["Value", "Count"],
                [("(missing)" if pd.isna(value) else value, count)
                 for value, count in counts.items()],
            )
        )
        target_sections.append("\n\n")

    preview = df.head(PREVIEW_ROWS).to_string(index=False)
    report = [
        "# Dataset Inspection Report\n",
        "\n",
        "## Dataset\n\n",
        f"- **File:** `data/raw/{CSV_PATH.name}`\n",
        f"- **Rows:** {rows}\n",
        f"- **Columns:** {columns}\n",
        f"- **Duplicate rows:** {duplicate_count}\n",
        "\n",
        "## Column names\n\n",
        ", ".join(f"`{column}`" for column in df.columns),
        "\n\n",
        "## Data types\n\n",
        markdown_table(["Column", "Pandas dtype"], dtype_rows),
        "\n\n",
        "## Missing values\n\n",
        "`Missing values` counts values treated as missing by pandas after interpreting literal `?` as missing. `Question marks` counts literal `?` tokens in the source CSV.\n\n",
        markdown_table(["Column", "Missing values", "Question marks"], missing_rows),
        "\n\n",
        "## Target column value counts\n\n",
    ]
    if target_sections:
        report.extend(target_sections)
        report.append("\n\n")
    if missing_targets:
        report.append(
            "Target columns not found in the CSV: "
            + ", ".join(f"`{column}`" for column in missing_targets)
            + ".\n\n"
        )

    report.extend([
        "## Numerical columns (non-binary numeric values)\n\n",
        ", ".join(f"`{column}`" for column in numerical_columns) or "None",
        "\n\n",
        "## Categorical columns (binary-coded 0/1)\n\n",
        ", ".join(f"`{column}`" for column in categorical_columns) or "None",
        "\n\n",
        "All columns have numeric pandas dtypes after interpreting `?` as missing. The categorical list above flags numeric columns whose observed non-missing values are only 0 and 1; review their meaning before analysis.\n\n",
        f"## Preview (first {min(PREVIEW_ROWS, rows)} rows)\n\n",
        "```text\n",
        preview,
        "\n```\n\n",
        "## Initial preprocessing considerations\n\n",
        "- Resolve the missing entries recorded above, including literal `?` values, using a method agreed with the teacher.\n",
        "- Review duplicate rows and decide whether they represent repeated observations before handling them.\n",
        "- Confirm the target column and predictor feature set with the teacher after reviewing the dataset and project requirements.\n",
        "- Many outcome and risk-factor indicators are 0/1 coded; review their categorical meaning. The four requested target columns are imbalanced, so account for their class distributions when selecting evaluation measures.\n",
        "- `STDs: Time since first diagnosis` and `STDs: Time since last diagnosis` each have 787 missing entries; assess whether those values are structurally missing.\n",
        "- Check feature scales and categorical encodings during preprocessing; this report does not alter or preprocess the source data.\n",
    ])

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("".join(report), encoding="utf-8")
    print(f"Dataset: {CSV_PATH}")
    print(f"Shape: {rows} rows x {columns} columns")
    print(f"Duplicate rows: {duplicate_count}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()


