# Data Mining Workspace

College Data Mining coursework by Laxmi Narayan Verma. This workspace
contains six practical exercises and a separate Cervical Cancer Data
Mining project.

## Contents

-   **Practicals/** --- six independent coursework exercises covering
    dataset creation, data cleaning, preprocessing, association rules,
    K-Means clustering, and DBSCAN density-based clustering.
-   **Cervical-Cancer-Data-Mining/** --- an educational comparison of
    K-Means and DBSCAN using the UCI Cervical Cancer Risk Factors
    dataset. Its preparation choices are provisional; cluster labels are
    not medical diagnoses.

Each Practical has its own script and input data where required. The
Cervical Cancer project has a separate workflow and a more complete
technical guide: [Cervical Cancer project
README](Cervical-Cancer-Data-Mining/README.md).

## Download the workspace

The repository is hosted at
[github.com/its-lnv/data-mining](https://github.com/its-lnv/data-mining).

### Option A: Download as a ZIP

1.  Open the repository link.
2.  Select **Code → Download ZIP**.
3.  Extract the ZIP to a folder.
4.  In VS Code, open the extracted **Data Mining** folder.

### Option B: Clone with Git

Install Git if needed, then run in PowerShell:

``` powershell
git clone https://github.com/its-lnv/data-mining.git
cd data-mining
code .
```

If the GitHub repository name or default branch changes, use the current
clone URL shown by GitHub's **Code** menu.

## Workspace structure

``` text
Data Mining/
├── .gitignore
├── Practicals/
│   ├── Practical-1/
│   │   ├── student_dataset.py
│   │   └── student_dataset_200.csv
│   ├── Practical-2/
│   │   ├── data_cleaning.py
│   │   └── data_cleaning_dataset.csv
│   ├── Practical-3/
│   │   ├── data_preprocessing.py
│   │   └── preprocessing_dataset.csv
│   ├── Practical-4/
│   │   └── association_rules.py
│   ├── Practical-5/
│   │   ├── kmeans_1d.py
│   │   └── kmeans_dataset.py
│   └── Practical-6/
│       ├── dbscan_iris_practical.py
│       └── iris.csv
├── Cervical-Cancer-Data-Mining/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── docs/
│   ├── outputs/
│   │   ├── graphs/
│   │   ├── results/
│   │   └── submission/
│   ├── src/
│   ├── requirements.txt
│   ├── run_project.py
│   └── README.md
└── README.md
```

The subfolders contain additional documents, scripts, and generated
files. This tree highlights the main entry points and input/output
locations.

## Tech stack

  -----------------------------------------------------------------------
  Technology                          Used for
  ----------------------------------- -----------------------------------
  Python (3.12 or newer for the       All practicals and project scripts
  Cervical project runner)            

  Python standard library, including  Random values, file and path
  `random`, `os`, `pathlib`,          handling, workflow execution, and
  `subprocess`, and `hashlib`         integrity checks

  pandas                              Reading, cleaning, processing, and
                                      reporting tabular data

  NumPy                               Numeric processing, K-Means
                                      calculations, and data validation

  Matplotlib                          Practical 5 MSE plot, Practical 6
                                      parameter-comparison plot, and
                                      project visualizations

  scikit-learn                        DBSCAN clustering and silhouette
                                      evaluation in Practical 6 and the
                                      Cervical project

  CSV                                 Input datasets, processed feature
                                      matrix, assignments, and result
                                      tables

  Markdown, HTML, and PDF             Documentation and project report
                                      formats

  VS Code and PowerShell              Suggested editor and Windows
                                      terminal
  -----------------------------------------------------------------------

The Cervical project's exact pinned third-party package versions are in
[requirements.txt](Cervical-Cancer-Data-Mining/requirements.txt). The
practicals use the packages imported by their scripts; they do not have
a separate dependency file. The project's PDF export helper also needs
Microsoft Edge or Google Chrome installed, but this browser is not
needed for the data-mining workflow.

## Setup in VS Code on Windows

Open the workspace folder in VS Code. To prepare the environment for the
Cervical project and the practicals that use the same Python libraries,
open the VS Code terminal (PowerShell) and run:

``` powershell
cd .\Cervical-Cancer-Data-Mining
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
code ..
```

The Cervical project requires Python 3.12 or newer. If the Python
launcher does not recognize 3.13, use an installed Python 3.12+ version,
for example `py -3.12 -m venv .venv`. In VS Code, choose
`.venv\Scripts\python.exe` using **Python: Select Interpreter**.

If PowerShell blocks environment activation, invoke the environment's
Python directly:

``` powershell
.\.venv\Scripts\python.exe run_project.py
```

The dependency installation above is for the Cervical project and
includes pandas, NumPy, Matplotlib, and scikit-learn, which are also
used by the practicals where applicable.

## Practicals

Run Practical scripts from the workspace root unless a command below
says otherwise. Use the activated virtual environment's Python.

### Practical 1 --- Dataset creation

**Files:** `Practicals/Practical-1/student_dataset.py` and
`student_dataset_200.csv`

Creates or updates the student dataset used in the exercise. Read the
script before rerunning it if you need to preserve an existing generated
CSV.

``` powershell
python .\Practicals\Practical-1\student_dataset.py
```

### Practical 2 --- Data cleaning

**Files:** `Practicals/Practical-2/data_cleaning.py` and
`data_cleaning_dataset.csv`

Demonstrates data-cleaning operations on the supplied sample dataset.

``` powershell
python .\Practicals\Practical-2\data_cleaning.py
```

### Practical 3 --- Data preprocessing

**Files:** `Practicals/Practical-3/data_preprocessing.py` and
`preprocessing_dataset.csv`

Demonstrates data-preprocessing operations on the supplied sample
dataset.

``` powershell
python .\Practicals\Practical-3\data_preprocessing.py
```

### Practical 4 --- Association rules

**File:** `Practicals/Practical-4/association_rules.py`

Demonstrates association-rule mining as implemented in the practical
script.

``` powershell
python .\Practicals\Practical-4\association_rules.py
```

### Practical 5 --- K-Means clustering

**Files:** `Practicals/Practical-5/kmeans_1d.py` and `kmeans_dataset.py`

-   `kmeans_1d.py` demonstrates one-dimensional K-Means.
-   `kmeans_dataset.py` compares K values and plots MSE after each
    iteration.

``` powershell
python .\Practicals\Practical-5\kmeans_1d.py
python .\Practicals\Practical-5\kmeans_dataset.py
```

### Practical 6 --- Density-based clustering using DBSCAN

**Files:** `Practicals/Practical-6/dbscan_iris_practical.py` and
`iris.csv`

This practical applies **DBSCAN (Density-Based Spatial Clustering of
Applications with Noise)** to the supplied Iris dataset. It standardizes
four numerical flower measurements and tests different combinations of:

-   `eps`: maximum neighbourhood distance.
-   `min_samples`: minimum number of samples required to form a dense
    region.

For each parameter combination, the script records the number of
clusters, noise points, noise percentage, and silhouette score where the
score is defined. Noise points (label `-1`) are excluded from the
silhouette calculation. The script saves a results table and a graph
comparing the number of clusters across parameter settings.

**Run from the workspace root:**

``` powershell
python .\Practicals\Practical-6\dbscan_iris_practical.py
```

The script expects `iris.csv` in the same directory as the Python file.
It creates these output files in the current working directory:

-   `dbscan_results.csv` --- results for the tested `eps` and
    `min_samples` combinations.
-   `dbscan_cluster_comparison.png` --- graph showing how the number of
    clusters changes with the parameters.

To keep the generated files inside Practical 6, run it from that folder
instead:

``` powershell
cd .\Practicals\Practical-6
python dbscan_iris_practical.py
```

The Iris CSV includes a `species` reference column, but the DBSCAN
script does **not** use it as a clustering feature. Only the four
numeric measurements are used. A silhouette score is not available when
fewer than two non-noise clusters are found. A higher silhouette score
alone is not enough to select the best DBSCAN setting; also inspect
cluster count and noise.

## Run the Cervical Cancer project

### Dataset setup

The Cervical project expects the UCI CSV at:

`Cervical-Cancer-Data-Mining/data/raw/risk_factors_cervical_cancer.csv`

Get the Cervical Cancer (Risk Factors) dataset from the [UCI Machine
Learning
Repository](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors),
then place the CSV at that path. Keep the original CSV in the raw
folder. The workflow writes processed data separately under
`data/processed/`.

### Run the full workflow

From the workspace root:

``` powershell
python .\Cervical-Cancer-Data-Mining\run_project.py
```

Or, after changing to the project folder:

``` powershell
cd .\Cervical-Cancer-Data-Mining
python run_project.py
```

The runner executes data-integrity verification, clustering
preprocessing, K-Means, DBSCAN, and comparative evaluation in order. It
stops if a step fails. Running it again regenerates the workflow's
processed matrix, audit, reports, tables, and graphs. For more detail
and individual script commands, see the [project
README](Cervical-Cancer-Data-Mining/README.md).

## Where to find project files

-   **Practical source code and sample datasets:** `Practicals/`
-   **Raw and processed Cervical project data:**
    `Cervical-Cancer-Data-Mining/data/`
-   **Plans, inspection notes, and reports:**
    `Cervical-Cancer-Data-Mining/docs/`
-   **Generated project plots:**
    `Cervical-Cancer-Data-Mining/outputs/graphs/`
-   **Experiment tables, assignments, and audit reports:**
    `Cervical-Cancer-Data-Mining/outputs/results/`
-   **Submission reports:**
    `Cervical-Cancer-Data-Mining/outputs/submission/`
-   **Project implementation:** `Cervical-Cancer-Data-Mining/src/`
-   **Project runner:** `Cervical-Cancer-Data-Mining/run_project.py`

Practical 6 writes its result CSV and PNG graph to the current working
directory. Run it from `Practicals/Practical-6/` to keep those outputs
there.

## Notes and limitations

-   The Cervical project is for educational Data Mining study, not
    clinical diagnosis, screening, or treatment.
-   The selected clustering features, missing-value treatment, duplicate
    handling, and scaling in the Cervical project are documented as
    provisional methodological choices. They are not represented as
    teacher-approved.
-   K-Means and DBSCAN may produce different partitions; DBSCAN can mark
    records as noise. Internal cluster scores have limitations and do
    not establish medical meaning.
-   Keep the Cervical raw dataset unchanged. Its runner writes separate
    processed and result files.
-   Practical 6 uses the four numeric Iris measurements for clustering;
    the species label is retained only as reference and is not supplied
    to DBSCAN.
-   Generated results can depend on package versions and settings. The
    Cervical project README records the pinned dependencies and
    experiment configuration.
-   No separate README currently exists inside `Practicals/`.
