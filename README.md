# Data Mining Workspace

College Data Mining coursework by Laxmi Narayan Verma. This workspace contains five practical exercises and a separate Cervical Cancer Data Mining project.

## Contents

- **Practicals/** — independent coursework examples for data creation, cleaning, preprocessing, association rules, and K-Means.
- **Cervical-Cancer-Data-Mining/** — an educational comparison of K-Means and DBSCAN using the UCI Cervical Cancer Risk Factors dataset. Its preparation choices are provisional; cluster labels are not medical diagnoses.

Each section has its own files and workflow. The project-specific guide has more complete technical documentation: [Cervical Cancer project README](Cervical-Cancer-Data-Mining/README.md).

## Download the workspace

The repository is hosted at [github.com/its-lnv/data-mining](https://github.com/its-lnv/data-mining).

### Option A: Download as a ZIP

1. Open the repository link.
2. Select **Code → Download ZIP**.
3. Extract the ZIP to a folder.
4. In VS Code, open the extracted **Data Mining** folder.

### Option B: Clone with Git

Install Git if needed, then run in PowerShell:

~~~powershell
git clone https://github.com/its-lnv/data-mining.git
cd data-mining
code .
~~~

If the GitHub repository name or default branch changes, use the current clone URL shown by GitHub’s **Code** menu.

## Workspace structure

~~~text
Data Mining/
├── .vscode/
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
│   └── Practical-5/
│       ├── kmeans_1d.py
│       └── kmeans_dataset.py
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
~~~

The subfolders contain additional documents, scripts, and generated files. The structure above highlights the main entry points and output locations.

## Tech stack

| Technology | Used for |
|---|---|
| Python (3.12 or newer for the Cervical project runner) | All practicals and project scripts |
| Python standard library, including random, os, pathlib, subprocess, and hashlib | Random values, file and path handling, workflow execution, and integrity checks |
| pandas | Reading, cleaning, processing, and reporting tabular data |
| NumPy | Numeric processing, K-Means calculations, and data validation |
| Matplotlib | Practical 5 MSE plot and project visualizations |
| scikit-learn | DBSCAN clustering and silhouette evaluation in the Cervical project |
| CSV | Input datasets, processed feature matrix, assignments, and result tables |
| Markdown, HTML, and PDF | Documentation and project report formats |
| VS Code and PowerShell | Suggested editor and Windows terminal |

The Cervical project’s exact pinned third-party package versions are in [requirements.txt](Cervical-Cancer-Data-Mining/requirements.txt). The practicals use the packages imported by their scripts; they do not have a separate dependency file. The project’s PDF export helper also needs Microsoft Edge or Google Chrome installed, but this browser is not needed for the data-mining workflow.

## Setup in VS Code on Windows

Open the workspace folder in VS Code. To prepare the environment for the Cervical project and to run practical scripts that use the same Python libraries, open the VS Code terminal (PowerShell) and run:

~~~powershell
cd .\Cervical-Cancer-Data-Mining
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
code .
~~~

The project requires Python 3.12 or newer. If the Python launcher does not recognize 3.13, use an installed Python 3.12+ version, for example **py -3.12 -m venv .venv**. In VS Code, choose **.venv\Scripts\python.exe** using **Python: Select Interpreter**.

If PowerShell blocks environment activation, invoke the environment’s Python directly:

~~~powershell
.\.venv\Scripts\python.exe run_project.py
~~~

The dependency installation above is for the Cervical project and covers the third-party libraries used by the practical scripts in this workspace as well.

## Dataset setup

The Cervical project expects the UCI CSV at:

**Cervical-Cancer-Data-Mining/data/raw/risk_factors_cervical_cancer.csv**

Get the Cervical Cancer (Risk Factors) dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors), then place the CSV at that path. Keep the original CSV in the raw folder. The workflow writes processed data separately under data/processed/.

The Practical folders include their own sample CSV files. Practical 1 may create or update its generated student CSV when run; read each script before changing its input files.

## How to run

### Run the full Cervical Cancer project

From the workspace root, after setup and dataset placement:

~~~powershell
python .\Cervical-Cancer-Data-Mining\run_project.py
~~~

Or, after changing to the project folder:

~~~powershell
cd .\Cervical-Cancer-Data-Mining
python run_project.py
~~~

The runner executes data-integrity verification, clustering preprocessing, K-Means, DBSCAN, and comparative evaluation in order. It stops if a step fails. Running it again regenerates the workflow’s processed matrix, audit, reports, tables, and graphs. For more detail and individual script commands, see the [project README](Cervical-Cancer-Data-Mining/README.md).

### Run an individual Practical

Run commands from the workspace root. Use the project virtual environment’s Python if it is active:

~~~powershell
python .\Practicals\Practical-1\student_dataset.py
python .\Practicals\Practical-2\data_cleaning.py
python .\Practicals\Practical-3\data_preprocessing.py
python .\Practicals\Practical-4\association_rules.py
~~~

Practical 5 has two scripts:

~~~powershell
python .\Practicals\Practical-5\kmeans_1d.py
python .\Practicals\Practical-5\kmeans_dataset.py
~~~

The first demonstrates one-dimensional K-Means. The second compares K values and plots MSE after each iteration. Some practicals write or display results; check the relevant script before rerunning if you need to preserve generated files.

## Where to find project files

- **Raw and processed data:** Cervical-Cancer-Data-Mining/data/
- **Plans, inspection notes, and reports:** Cervical-Cancer-Data-Mining/docs/
- **Generated plots:** Cervical-Cancer-Data-Mining/outputs/graphs/
- **Experiment tables, assignments, and audit reports:** Cervical-Cancer-Data-Mining/outputs/results/
- **Submission reports:** Cervical-Cancer-Data-Mining/outputs/submission/
- **Project implementation:** Cervical-Cancer-Data-Mining/src/
- **Project runner:** Cervical-Cancer-Data-Mining/run_project.py

## Notes and limitations

- The Cervical project is for educational Data Mining study, not clinical diagnosis, screening, or treatment.
- The selected clustering features, missing-value treatment, duplicate handling, and scaling are documented as provisional methodological choices. They are not represented as teacher-approved.
- K-Means and DBSCAN may produce different partitions; DBSCAN can mark records as noise. Internal cluster scores have limitations and do not establish medical meaning.
- Keep the raw dataset unchanged. The runner writes separate processed and result files.
- Generated results can depend on package versions and settings. The Cervical project README records the pinned dependencies and experiment configuration.
- No separate README currently exists inside Practicals/.
