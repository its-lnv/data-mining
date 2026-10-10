"""Safely audit the raw cervical-cancer dataset without changing it.

This first cleaning step only reads the original CSV, treats literal '?' as
missing in memory for counting, and writes a clearly labelled audit report.
It does not remove duplicates, fill missing values, or save a cleaned dataset.
"""

from collections import Counter
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
AUDIT_PATH = PROJECT_ROOT / "data" / "processed" / "PROVISIONAL_data_cleaning_audit.md"


def make_markdown_table(headers, rows):
    """Build a Markdown table using only Python's standard library."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main():
    if not RAW_DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )

    # Keep one raw text copy to count literal '?' tokens exactly. The second
    # in-memory copy lets pandas treat '?' as missing for safe auditing only.
    raw_text = pd.read_csv(RAW_DATA_PATH, dtype=str, keep_default_na=False)
    audited = pd.read_csv(RAW_DATA_PATH, na_values=["?"])

    missing_rows = []
    for column in audited.columns:
        question_marks = int(raw_text[column].eq("?").sum())
        missing_count = int(audited[column].isna().sum())
        missing_rows.append((column, missing_count, question_marks))

    # duplicated(keep="first") counts only extra copies, matching the count
    # reported in the initial inspection. No rows are removed here.
    duplicate_mask = audited.duplicated(keep="first")
    duplicate_count = int(duplicate_mask.sum())
    duplicate_lines = [str(index + 2) for index in audited.index[duplicate_mask]]

    # Count repeated-row groups without printing any patient feature values.
    group_sizes = Counter(
        audited.groupby(list(audited.columns), dropna=False, sort=False).size().tolist()
    )
    duplicate_groups = sum(
        group_count for size, group_count in group_sizes.items() if size > 1
    )

    report = [
        "# PROVISIONAL Data Cleaning Audit\n\n",
        "> Audit only: this is not a cleaned dataset. The source CSV was read but not modified.\n\n",
        "## Dataset summary\n\n",
        f"- **Source:** `data/raw/{RAW_DATA_PATH.name}`\n",
        f"- **Rows:** {audited.shape[0]}\n",
        f"- **Columns:** {audited.shape[1]}\n",
        f"- **Exact duplicate rows beyond the first copy:** {duplicate_count}\n",
        f"- **Groups containing repeated rows:** {duplicate_groups}\n",
        "- **Duplicate handling:** pending teacher decision; no rows removed.\n",
        "- **Missing-value handling:** literal `?` is treated as missing in this in-memory audit only; no values were imputed.\n\n",
        "## Missing-value counts\n\n",
        "`Missing after parsing` includes `?` as missing. `Literal ?` counts those source tokens directly.\n\n",
        make_markdown_table(
            ["Column", "Missing after parsing", "Literal ?"], missing_rows
        ),
        "\n\n",
        "## Duplicate row locations\n\n",
        "The following CSV line numbers are extra copies after each group's first row. They are listed for review only; the audit does not decide whether these observations are erroneous.\n\n",
        ", ".join(duplicate_lines) if duplicate_lines else "None",
        "\n\n",
        "## Pending decisions\n\n",
        "- Confirm whether exact duplicate rows are accidental copies before removing or grouping them.\n",
        "- Approve missing-value handling; this audit does not impute values.\n",
        "- Decide how to handle the two diagnosis-time columns with 787 missing entries each.\n",
        "- Confirm the target and predictor columns before creating a modeling-ready dataset.\n",
        "- Do not resample the Biopsy classes unless explicitly approved.\n",
    ]

    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text("".join(report), encoding="utf-8")
    print("Safe audit completed.")
    print(f"Rows: {audited.shape[0]} | Columns: {audited.shape[1]}")
    print(f"Duplicate copies flagged: {duplicate_count} (none removed)")
    print(f"Audit report: {AUDIT_PATH}")
    print("No cleaned dataset was written; the raw CSV was not changed.")


if __name__ == "__main__":
    main()
