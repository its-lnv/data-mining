"""Check whether syllabus-relevant preprocessing is ready to run.

No preprocessing transformation is safe to apply yet: duplicate treatment,
missing-value policy, diagnosis-time treatment, target/predictors, and the
evaluation split remain unresolved. This script audits those prerequisites
and stops without writing a dataset until a documented approved configuration
is supplied.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"

# Leave these unset until the teacher has decided and the decision is recorded.
# This script intentionally has no default imputation, row-removal, scaling,
# discretization, or class-resampling behavior.
APPROVED_CONFIGURATION = {
    "duplicate_policy": None,
    "missing_value_policy": None,
    "diagnosis_time_policy": None,
    "target_column": None,
    "predictor_columns": None,
    "evaluation_split_policy": None,
    "class_resampling": False,
}


def main():
    if not RAW_DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )

    # Read the supplied file for a readiness check only. Interpreting '?' as
    # missing in this temporary DataFrame does not change the CSV on disk.
    data = pd.read_csv(RAW_DATA_PATH, na_values=["?"])
    duplicate_count = int(data.duplicated().sum())
    pending = [
        key for key, value in APPROVED_CONFIGURATION.items()
        if value is None
    ]

    print("Preprocessing readiness check")
    print(f"Dataset: {RAW_DATA_PATH}")
    print(f"Shape: {data.shape[0]} rows x {data.shape[1]} columns")
    print(f"Exact duplicate rows still present: {duplicate_count}")
    print("No transformations have been applied.")

    if pending:
        print("\nSTOP: no provisional processed dataset was written.")
        print("Record teacher-approved choices in APPROVED_CONFIGURATION before implementation.")
        print("Pending decisions:")
        for decision in pending:
            print(f"- {decision}")
        print("\nStandardization/normalization must be fitted only on training data after the evaluation split is approved.")
        print("Discretization is only appropriate if the separate syllabus-based Apriori analysis is approved.")
        print("Class resampling remains disabled unless explicitly approved.")
        return 2

    # Reaching this branch still does not silently perform arbitrary cleaning.
    # The approved, documented policies must be implemented explicitly in a
    # later revision after they are reviewed against the chosen task.
    print("STOP: approved choices are recorded, but transformation implementation must be reviewed before running.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
