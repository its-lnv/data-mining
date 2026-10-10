"""Create exploratory plots from the raw dataset without cleaning it.

The script treats '?' as missing in an in-memory Pandas DataFrame for plotting.
It does not alter the source CSV, remove duplicate rows, impute values, or
perform modeling or other data-mining algorithms.
"""

from pathlib import Path
import os
from tempfile import TemporaryDirectory

# Keep Matplotlib's small font cache in a temporary writable location instead
# of relying on permissions in a particular user's home directory.
_MPL_CONFIG_DIR = TemporaryDirectory(prefix="cervical_cancer_mpl_")
os.environ["MPLCONFIGDIR"] = _MPL_CONFIG_DIR.name

import matplotlib

# Use a non-interactive backend so this script also works from a terminal.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "risk_factors_cervical_cancer.csv"
GRAPH_DIR = PROJECT_ROOT / "outputs" / "graphs"

TARGET_COLUMNS = ["Biopsy", "Hinselmann", "Schiller", "Citology"]


def save_figure(fig, filename):
    """Save a figure as a readable PNG and close it to free memory."""
    output_path = GRAPH_DIR / filename
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output_path.relative_to(PROJECT_ROOT)}")


def plot_missing_values(data):
    """Plot missing counts horizontally so all column labels remain readable."""
    counts = data.isna().sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(13, 11))
    bars = ax.barh(counts.index, counts.values, color="#4C78A8")
    ax.bar_label(bars, padding=3, fontsize=8)
    ax.set_title("Missing Values by Column")
    ax.set_xlabel("Missing values (rows)")
    ax.set_ylabel("Dataset column")
    ax.tick_params(axis="y", labelsize=8)
    ax.set_xlim(0, max(1, int(counts.max()) * 1.12))
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    save_figure(fig, "missing_values_by_column.png")


def plot_screening_class_counts(data):
    """Show the observed 0 and 1 counts for each screening outcome."""
    available = [column for column in TARGET_COLUMNS if column in data.columns]
    if not available:
        print("Skipped outcome counts: none of the requested columns were found.")
        return

    x_positions = list(range(len(available)))
    width = 0.36
    zero_counts = []
    one_counts = []
    omitted_counts = []
    for column in available:
        counts = data[column].value_counts(dropna=True)
        zero_counts.append(int(counts.get(0, 0)))
        one_counts.append(int(counts.get(1, 0)))
        omitted = data[column].isna() | ~data[column].isin([0, 1])
        omitted_counts.append(int(omitted.sum()))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        [position - width / 2 for position in x_positions],
        zero_counts,
        width,
        label="0",
        color="#4C78A8",
    )
    ax.bar(
        [position + width / 2 for position in x_positions],
        one_counts,
        width,
        label="1",
        color="#F58518",
    )
    ax.set_xticks(x_positions, available)
    omission_note = ", ".join(
        f"{column}: {count}" for column, count in zip(available, omitted_counts)
    )
    ax.set_title(
        "Observed Class Counts for Screening Outcomes\n"
        f"Missing or non-0/1 values omitted: {omission_note}"
    )
    ax.set_xlabel("Outcome column (coded 0 / 1)")
    ax.set_ylabel("Records")
    ax.legend(title="Observed value")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    save_figure(fig, "screening_outcome_class_counts.png")


def plot_numeric_distribution(data, column, filename, title, xlabel, histogram=False):
    """Plot non-missing numeric values and report omissions on the chart."""
    if column not in data.columns:
        print(f"Skipped {column}: column not found.")
        return

    values = pd.to_numeric(data[column], errors="coerce")
    observed = values.dropna()
    missing_count = int(values.isna().sum())
    if observed.empty:
        print(f"Skipped {column}: no numeric non-missing values to plot.")
        return

    fig, ax = plt.subplots(figsize=(9, 5.5))
    if histogram:
        ax.hist(observed, bins="auto", color="#4C78A8", edgecolor="white")
        ax.set_ylabel("Records")
    else:
        counts = observed.value_counts().sort_index()
        ax.bar(counts.index.astype(str), counts.values, color="#4C78A8")
        ax.set_ylabel("Records")
        ax.tick_params(axis="x", labelrotation=45)

    ax.set_title(f"{title}\nMissing values omitted: {missing_count}")
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    save_figure(fig, filename)


def plot_smoking_status(data):
    """Plot the existing 0/1 smoking field and show missing entries."""
    column = "Smokes"
    if column not in data.columns:
        print("Skipped smoking status: 'Smokes' column not found.")
        return

    values = pd.to_numeric(data[column], errors="coerce")
    known_counts = values.value_counts(dropna=True)
    missing_count = int(values.isna().sum())
    labels = ["0", "1", "Missing"]
    counts = [
        int(known_counts.get(0, 0)),
        int(known_counts.get(1, 0)),
        missing_count,
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, counts, color=["#4C78A8", "#F58518", "#B9B9B9"])
    ax.set_title("Smokes Column Counts (0/1 Coding)")
    ax.set_xlabel("Recorded value")
    ax.set_ylabel("Records")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    save_figure(fig, "smoking_status_counts.png")


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}\n"
            "Place risk_factors_cervical_cancer.csv in data/raw/."
        )

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    # '?' becomes a missing value in this temporary DataFrame only. No cleaning
    # or saving is performed on the source data.
    data = pd.read_csv(CSV_PATH, na_values=["?"])
    print(f"Read {data.shape[0]} rows and {data.shape[1]} columns from the raw CSV.")
    print("Rows, including the 23 duplicate copies, are retained in these plots.")

    plot_missing_values(data)
    plot_screening_class_counts(data)
    plot_numeric_distribution(
        data,
        "Age",
        "age_distribution.png",
        "Age Distribution",
        "Age (years)",
        histogram=True,
    )
    plot_numeric_distribution(
        data,
        "Number of sexual partners",
        "sexual_partners_distribution.png",
        "Number of Sexual Partners",
        "Recorded number of sexual partners",
    )
    plot_numeric_distribution(
        data,
        "First sexual intercourse",
        "first_intercourse_age_distribution.png",
        "Age at First Sexual Intercourse",
        "Age (years)",
    )
    plot_numeric_distribution(
        data,
        "Num of pregnancies",
        "pregnancies_distribution.png",
        "Number of Pregnancies",
        "Recorded number of pregnancies",
    )
    plot_smoking_status(data)
    print(f"Exploratory plots saved under {GRAPH_DIR.relative_to(PROJECT_ROOT)}.")
    print("These plots are descriptive and do not establish causation or medical risk.")


if __name__ == "__main__":
    main()
