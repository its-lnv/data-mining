"""Prepare a provisional, numeric clustering feature matrix.

The source CSV is read-only. Literal '?' values become missing values in memory
only. This script applies configurable provisional choices to a separate
feature-only copy; it does not run K-Means, DBSCAN, or any other mining method.
"""

import hashlib
import math
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "PROVISIONAL_clustering_features.csv"
AUDIT_PATH = PROJECT_ROOT / "outputs" / "results" / "clustering_preprocessing_audit.md"

# Change these settings explicitly to compare documented preprocessing choices.
CANDIDATE_FEATURES = [
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
MISSING_VALUE_POLICY = "median"  # Options: "median", "complete_case", "error"
DUPLICATE_POLICY = "drop_exact"  # Options: "drop_exact", "retain"
SCALING_METHOD = "standardize"  # Options: "standardize", "normalize_minmax", "none"
RANDOM_SEED = 42  # Recorded for reproducibility; preprocessing itself is deterministic.

# Never allow outcomes or direct diagnosis/diagnosis-history fields as inputs.
PROHIBITED_FEATURES = {
    "Biopsy",
    "Hinselmann",
    "Schiller",
    "Citology",
    "Dx:Cancer",
    "Dx:CIN",
    "Dx:HPV",
    "Dx",
    "STDs: Number of diagnosis",
    "STDs: Time since first diagnosis",
    "STDs: Time since last diagnosis",
}


def sha256_file(path):
    """Return a SHA-256 digest without loading the whole file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_table(headers, rows):
    """Create a simple Markdown table using only Python's standard library."""
    lines = ["| " + " | ".join(str(value) for value in headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def validate_configuration(data):
    """Fail clearly when configuration or requested columns are unsafe."""
    if not CANDIDATE_FEATURES:
        raise ValueError("CANDIDATE_FEATURES is empty; select at least one feature.")
    if len(CANDIDATE_FEATURES) != len(set(CANDIDATE_FEATURES)):
        raise ValueError("CANDIDATE_FEATURES contains duplicate column names.")

    prohibited_selected = sorted(set(CANDIDATE_FEATURES) & PROHIBITED_FEATURES)
    if prohibited_selected:
        raise ValueError(
            "Screening outcomes and diagnosis fields cannot be clustering inputs: "
            + ", ".join(prohibited_selected)
        )

    missing_columns = [name for name in CANDIDATE_FEATURES if name not in data.columns]
    if missing_columns:
        raise ValueError("Required candidate columns are missing: " + ", ".join(missing_columns))

    if MISSING_VALUE_POLICY not in {"median", "complete_case", "error"}:
        raise ValueError(f"Unsupported MISSING_VALUE_POLICY: {MISSING_VALUE_POLICY}")
    if DUPLICATE_POLICY not in {"drop_exact", "retain"}:
        raise ValueError(f"Unsupported DUPLICATE_POLICY: {DUPLICATE_POLICY}")
    if SCALING_METHOD not in {"standardize", "normalize_minmax", "none"}:
        raise ValueError(f"Unsupported SCALING_METHOD: {SCALING_METHOD}")


def ensure_numeric_features(data):
    """Convert candidate columns to numbers and reject unexpected text values."""
    numeric = pd.DataFrame(index=data.index)
    problems = []

    for column in CANDIDATE_FEATURES:
        source = data[column]
        converted = pd.to_numeric(source, errors="coerce")
        unexpected = source.notna() & converted.isna()
        if unexpected.any():
            examples = source.loc[unexpected].astype(str).unique()[:5].tolist()
            problems.append(f"{column}: {int(unexpected.sum())} unexpected value(s), e.g. {examples}")

        non_finite_mask = converted.notna() & ~converted.map(
            lambda value: math.isfinite(float(value))
        )
        if non_finite_mask.any():
            problems.append(f"{column}: {int(non_finite_mask.sum())} non-finite value(s)")
        numeric[column] = converted

    if problems:
        raise ValueError("Candidate feature validation failed:\n- " + "\n- ".join(problems))

    all_missing = [column for column in CANDIDATE_FEATURES if numeric[column].isna().all()]
    if all_missing:
        raise ValueError("All-missing candidate feature(s): " + ", ".join(all_missing))
    return numeric


def apply_missing_policy(features):
    """Handle missing entries according to the explicit configuration."""
    missing_before = features.isna().sum()

    if MISSING_VALUE_POLICY == "error":
        if int(missing_before.sum()):
            raise ValueError("Missing values found, but MISSING_VALUE_POLICY is 'error'.")
        return features.copy(), {}

    if MISSING_VALUE_POLICY == "complete_case":
        result = features.dropna(axis=0, how="any").copy()
        if result.empty:
            raise ValueError("Complete-case handling produced an empty feature matrix.")
        return result, {}

    # Median is resistant to extreme values and easy to explain for skewed or
    # count-like columns. It still inserts synthetic values and can affect
    # distances, so every used median is reported in the audit.
    result = features.copy()
    medians = {}
    for column in result.columns:
        median = result[column].median(skipna=True)
        if pd.isna(median):
            raise ValueError(f"Cannot calculate a median for all-missing feature: {column}")
        medians[column] = float(median)
        result[column] = result[column].fillna(median)
    return result, medians


def apply_scaling(features):
    """Scale numeric features using pandas only, with safe constant handling."""
    result = features.copy().astype(float)
    parameters = []

    if SCALING_METHOD == "none":
        parameters = [(column, "not scaled", "not scaled") for column in result.columns]
    elif SCALING_METHOD == "standardize":
        # Population standard deviation (ddof=0) is used consistently.
        for column in result.columns:
            mean = float(result[column].mean())
            std = float(result[column].std(ddof=0))
            if std == 0:
                result[column] = 0.0
                parameters.append((column, f"mean={mean:g}", "constant; mapped to 0"))
            else:
                result[column] = (result[column] - mean) / std
                parameters.append((column, f"mean={mean:.8g}", f"population std={std:.8g}"))
    else:  # normalize_minmax
        for column in result.columns:
            minimum = float(result[column].min())
            maximum = float(result[column].max())
            span = maximum - minimum
            if span == 0:
                result[column] = 0.0
                parameters.append((column, f"min={minimum:g}", "constant; mapped to 0"))
            else:
                result[column] = (result[column] - minimum) / span
                parameters.append((column, f"min={minimum:.8g}", f"max={maximum:.8g}"))

    return result, parameters


def main():
    if not RAW_DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )
    if PROCESSED_PATH.resolve() == RAW_DATA_PATH.resolve():
        raise RuntimeError("Processed output path must never point to the raw CSV.")

    raw_hash_before = sha256_file(RAW_DATA_PATH)
    raw = pd.read_csv(RAW_DATA_PATH, na_values=["?"])
    original_rows, original_columns = raw.shape
    validate_configuration(raw)

    # Validate and count missingness before any row filtering or imputation.
    numeric_all = ensure_numeric_features(raw)
    missing_before_rows = numeric_all.isna().sum()
    if numeric_all.empty:
        raise ValueError("Raw dataset has no rows; cannot create a feature matrix.")

    duplicate_mask = raw.duplicated(keep="first")
    duplicate_copies = int(duplicate_mask.sum())
    if DUPLICATE_POLICY == "drop_exact":
        keep_mask = ~duplicate_mask
        working = numeric_all.loc[keep_mask].copy()
    else:
        working = numeric_all.copy()
    rows_after_duplicate_policy = len(working)
    if working.empty:
        raise ValueError("Duplicate policy produced an empty feature matrix.")

    missing_after_duplicates = working.isna().sum()
    if any(working[column].isna().all() for column in working.columns):
        all_missing = [column for column in working if working[column].isna().all()]
        raise ValueError("All-missing feature(s) after duplicate handling: " + ", ".join(all_missing))

    imputed, medians = apply_missing_policy(working)
    if imputed.empty:
        raise ValueError("Missing-value policy produced an empty feature matrix.")
    if imputed.isna().any().any():
        raise ValueError("Missing values remain after applying the configured policy.")

    scaled, scaling_parameters = apply_scaling(imputed)
    if scaled.empty or scaled.shape[1] == 0:
        raise ValueError("Processed feature matrix is empty.")
    non_finite = scaled.apply(
        lambda series: ~series.map(lambda value: math.isfinite(float(value)))
    )
    if non_finite.any().any():
        locations = [
            f"{column}: {int(non_finite[column].sum())}"
            for column in non_finite.columns
            if non_finite[column].any()
        ]
        raise ValueError("Non-finite output value(s): " + ", ".join(locations))

    raw_hash_after = sha256_file(RAW_DATA_PATH)
    raw_unchanged = raw_hash_before == raw_hash_after
    if not raw_unchanged:
        raise RuntimeError("Raw CSV SHA-256 changed during preprocessing; investigate immediately.")

    missing_rows = []
    for column in CANDIDATE_FEATURES:
        missing_rows.append(
            (
                column,
                int(missing_before_rows[column]),
                int(missing_after_duplicates[column]),
                int(scaled[column].isna().sum()),
                str(numeric_all[column].dtype),
            )
        )

    imputation_rows = [
        (column, f"{value:g}") for column, value in medians.items()
    ] or [("Not applicable", "No median imputation configured")]
    scaling_rows = scaling_parameters
    warnings = [
        "These processing choices are provisional and have not received teacher approval.",
        "Exact duplicate rows may represent separate observations; removing them can change DBSCAN density and K-Means centroids.",
        "Median imputation inserts synthetic values and can change distances or make imputed records appear closer together.",
        "Diagnosis-time columns are excluded from the configured candidate list; no missing diagnosis-time value was interpreted as zero or confirmed absence.",
        "Standardization choices affect distance geometry and therefore both clustering methods; use this same matrix for a fair comparison.",
    ]

    report = [
        "# Provisional Clustering Preprocessing Audit\n\n",
        "> This is a derived feature matrix for a provisional clustering baseline, not teacher-approved preprocessing. "
        "The raw CSV was read-only; no clustering algorithm was run.\n\n",
        "## Input and output summary\n\n",
        f"- **Raw source:** `data/raw/{RAW_DATA_PATH.name}`\n",
        f"- **Original raw dimensions:** {original_rows} rows x {original_columns} columns\n",
        f"- **Exact duplicate copies detected:** {duplicate_copies} (full-row equality across the parsed raw table; first occurrence retained for counting)\n",
        f"- **Duplicate policy:** `{DUPLICATE_POLICY}`\n",
        f"- **Rows after duplicate policy:** {rows_after_duplicate_policy}\n",
        f"- **Processed matrix dimensions:** {scaled.shape[0]} rows x {scaled.shape[1]} features\n",
        f"- **Processed feature file:** `data/processed/{PROCESSED_PATH.name}`\n",
        f"- **Audit report:** `outputs/results/{AUDIT_PATH.name}`\n",
        f"- **Configured random seed:** {RANDOM_SEED} (no random operation was used in this preprocessing step)\n",
        f"- **Raw SHA-256 unchanged:** {raw_unchanged}\n\n",
        "## Configured provisional choices\n\n",
        f"- **Features:** {', '.join(f'`{column}`' for column in CANDIDATE_FEATURES)}\n",
        f"- **Missing-value policy:** `{MISSING_VALUE_POLICY}`. Median imputation is a simple, robust-to-extremes choice for these numeric/count-like features and retains rows; it still creates synthetic values and can change distances, so this is provisional.\n",
        f"- **Scaling:** `{SCALING_METHOD}`. Features use different units and ranges; without scaling, large-range measurements can dominate Euclidean distances used by K-Means and the `eps` neighborhood distances used by DBSCAN.\n",
        "- **Excluded inputs:** screening outcomes and direct diagnosis/diagnosis-history fields are prohibited by configuration.\n\n",
        "## Missingness by candidate feature\n\n",
        "Counts before handling refer to the original parsed rows. The middle column is after duplicate handling; final counts are after the configured missing-value policy.\n\n",
        markdown_table(
            ["Feature", "Missing before duplicate handling", "Missing after duplicate handling", "Missing after handling", "Inferred numeric dtype"],
            missing_rows,
        ),
        "\n\n",
        "## Imputation values\n\n",
        markdown_table(["Feature", "Median used"], imputation_rows),
        "\n\n",
        "## Scaling parameters\n\n",
        markdown_table(["Feature", "Center / minimum", "Scale / maximum"], scaling_rows),
        "\n\n",
        "## Validation results\n\n",
        "- All configured columns were present.\n",
        "- Candidate values parsed as numeric; unexpected non-numeric values were not found.\n",
        "- No candidate feature was entirely missing.\n",
        "- Processed output is non-empty and contains only finite numeric values.\n",
        "- The processed file contains only the configured feature columns; no target or diagnosis columns were added.\n\n",
        "## Warnings and unresolved decisions\n\n",
        "\n".join(f"- {warning}" for warning in warnings),
        "\n\n",
        "The feature list, median-imputation policy, exact-duplicate removal policy, and standardization method are configurable provisional defaults. Review them before interpreting or comparing clusters. In particular, whether exact duplicate rows are erroneous remains unresolved. This project is educational and is not intended for clinical diagnosis.\n",
    ]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # A unique, separate output path is used; the raw CSV is never a write target.
    scaled.to_csv(PROCESSED_PATH, index=False)
    AUDIT_PATH.write_text("".join(report), encoding="utf-8")

    print("Provisional clustering preprocessing completed.")
    print(f"Raw dimensions: {original_rows} rows x {original_columns} columns")
    print(f"Exact duplicate copies: {duplicate_copies}; rows after policy: {rows_after_duplicate_policy}")
    print(f"Processed matrix: {scaled.shape[0]} rows x {scaled.shape[1]} features")
    print(f"Processed output: {PROCESSED_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Audit report: {AUDIT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Raw SHA-256 unchanged: {raw_unchanged}")


if __name__ == "__main__":
    main()
