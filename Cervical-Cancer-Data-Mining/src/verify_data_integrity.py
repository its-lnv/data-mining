"""Verify raw dataset structure and integrity without modifying the CSV.

Literal '?' markers are interpreted as missing in an in-memory DataFrame only.
The script reports facts and historical-count comparisons; it does not clean,
transform, or mine the data.
"""

import hashlib
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
REPORT_PATH = PROJECT_ROOT / "outputs" / "results" / "data_integrity_verification.md"

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

# Historical values recorded in dataset_inspection.md and the cleaning audit.
DOCUMENTED_ROWS = 858
DOCUMENTED_COLUMNS = 36
DOCUMENTED_DUPLICATE_COPIES = 23
DOCUMENTED_REPEATED_GROUPS = 20


def sha256_file(path):
    """Return a SHA-256 digest by reading the file in binary chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_table(headers, rows):
    """Build a Markdown table using only the standard library."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def main():
    if not RAW_DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )

    raw_hash_before = sha256_file(RAW_DATA_PATH)

    # Treat '?' as missing in this DataFrame only; the source text is untouched.
    data = pd.read_csv(RAW_DATA_PATH, na_values=["?"])
    row_count, column_count = data.shape

    present_candidates = [name for name in CANDIDATE_COLUMNS if name in data.columns]
    missing_candidates = [name for name in CANDIDATE_COLUMNS if name not in data.columns]

    feature_rows = []
    for column in CANDIDATE_COLUMNS:
        if column in data.columns:
            feature_rows.append(
                (column, str(data[column].dtype), int(data[column].isna().sum()))
            )
        else:
            feature_rows.append((column, "not present", "not available"))

    # Duplicate definition: values match across every column after the parser
    # represents '?' as NaN. pandas duplicated() counts extra copies, excluding
    # the first member of each identical-row group.
    duplicate_mask = data.duplicated(keep="first")
    duplicate_copies = int(duplicate_mask.sum())

    # A repeated-row group is one distinct full-row pattern that occurs 2+ times.
    # Grouping with dropna=False ensures matching missing positions are included.
    repeated_patterns = data.groupby(
        list(data.columns), dropna=False, sort=False
    ).size()
    repeated_group_sizes = repeated_patterns[repeated_patterns > 1]
    repeated_group_count = int(len(repeated_group_sizes))
    rows_in_repeated_groups = int(repeated_group_sizes.sum())

    shape_matches = (row_count, column_count) == (
        DOCUMENTED_ROWS,
        DOCUMENTED_COLUMNS,
    )
    duplicates_match = (
        duplicate_copies == DOCUMENTED_DUPLICATE_COPIES
        and repeated_group_count == DOCUMENTED_REPEATED_GROUPS
    )

    raw_hash_after = sha256_file(RAW_DATA_PATH)
    hash_unchanged = raw_hash_before == raw_hash_after

    discrepancy_lines = []
    if not shape_matches:
        discrepancy_lines.append(
            f"- Current shape is {row_count} rows x {column_count} columns; "
            f"documentation records {DOCUMENTED_ROWS} x {DOCUMENTED_COLUMNS}."
        )
    if duplicate_copies != DOCUMENTED_DUPLICATE_COPIES:
        discrepancy_lines.append(
            f"- Current extra-copy count is {duplicate_copies}; documentation records "
            f"{DOCUMENTED_DUPLICATE_COPIES}. Both use exact full-row matching with the "
            "first row in each group retained for counting."
        )
    if repeated_group_count != DOCUMENTED_REPEATED_GROUPS:
        discrepancy_lines.append(
            f"- Current repeated-pattern group count is {repeated_group_count}; "
            f"documentation records {DOCUMENTED_REPEATED_GROUPS}. A group here means "
            "one distinct full-row pattern occurring at least twice, including matching "
            "missing positions."
        )
    if missing_candidates:
        discrepancy_lines.append(
            "- Candidate columns absent from the CSV: "
            + ", ".join(f"`{name}`" for name in missing_candidates)
            + "."
        )

    report = [
        "# Data Integrity Verification\n\n",
        "> Read-only verification. Literal `?` markers were treated as missing in memory only. "
        "No rows or values were removed, filled, scaled, or otherwise transformed.\n\n",
        "## Verified dataset structure\n\n",
        f"- **Source:** `data/raw/{RAW_DATA_PATH.name}`\n",
        f"- **Rows:** {row_count}\n",
        f"- **Columns:** {column_count}\n",
        f"- **Expected candidate columns present:** {len(present_candidates)} of {len(CANDIDATE_COLUMNS)}\n",
        "- **Missing candidate columns:** "
        + (", ".join(f"`{name}`" for name in missing_candidates) if missing_candidates else "None")
        + "\n\n",
        "### Provisional clustering candidate features\n\n",
        "Missing counts use the full dataset row count. Dtypes are pandas-inferred after interpreting `?` as missing.\n\n",
        markdown_table(["Column", "Inferred pandas dtype", "Missing values"], feature_rows),
        "\n\n",
        "## Duplicate-row verification\n\n",
        "Definition: rows are exact duplicates when all column values match after parsing `?` as missing. "
        "The duplicate-copy count uses `duplicated(keep='first')`, so the first occurrence is not counted. "
        "A repeated-row group is one distinct full-row pattern with at least two occurrences; matching missing positions are grouped together.\n\n",
        f"- **Extra duplicate copies:** {duplicate_copies}\n",
        f"- **Repeated-row groups:** {repeated_group_count}\n",
        f"- **Rows participating in repeated groups:** {rows_in_repeated_groups}\n",
        f"- **Documented historical counts:** {DOCUMENTED_DUPLICATE_COPIES} extra copies across {DOCUMENTED_REPEATED_GROUPS} groups\n",
        "- **Duplicate comparison:** " + ("matches the documented counts.\n\n" if duplicates_match else "differs; see discrepancy notes below.\n\n"),
        "## Comparison with existing documentation\n\n",
        f"- **Shape comparison:** {'matches' if shape_matches else 'differs from'} the documented {DOCUMENTED_ROWS} rows and {DOCUMENTED_COLUMNS} columns.\n",
        "- **Duplicate comparison:** " + ("matches" if duplicates_match else "differs") + " the documented extra-copy and repeated-group counts.\n",
        "- **Discrepancies:**\n\n",
        "\n".join(discrepancy_lines) if discrepancy_lines else "None detected against the stated historical counts.",
        "\n\n",
        "## Integrity and unresolved decisions\n\n",
        f"- **Raw-file SHA-256 before/after this run:** {'unchanged' if hash_unchanged else 'DIFFERENT; investigate'}\n",
        "- No duplicate policy was applied; all original rows remain in the source file.\n",
        "- No imputation or interpretation of diagnosis-time missingness was applied.\n",
        "- The candidate list remains provisional; feature inclusion, missing-value handling, duplicate treatment, and scaling require later justification and teacher guidance.\n",
        "- Screening outcomes and diagnosis fields are not included in the candidate-feature check and remain excluded as clustering inputs under the current study plan.\n",
        "- No K-Means, DBSCAN, or other data-mining algorithm was run.\n",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("".join(report), encoding="utf-8")

    print(f"Verified {row_count} rows x {column_count} columns.")
    print(f"Candidate columns present: {len(present_candidates)} of {len(CANDIDATE_COLUMNS)}.")
    print(f"Exact duplicate copies: {duplicate_copies}; repeated-row groups: {repeated_group_count}.")
    print(f"Raw file SHA-256 unchanged during run: {hash_unchanged}.")
    print(f"Report written: {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
