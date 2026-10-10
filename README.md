# Data Mining Workspace

This workspace contains two separate parts of the college Data Mining work:

- **Practicals** — five syllabus practicals covering dataset creation and analysis, cleaning, preprocessing, association rules, and K-Means.
- **Cervical-Cancer-Data-Mining** — a separate project comparing K-Means and DBSCAN on the UCI Cervical Cancer Risk Factors dataset.

The projects have separate data, scripts, outputs, and run instructions. This workspace README is an index; use the Cervical project guide for its detailed environment setup and results.

## Workspace structure

~~~text
Data Mining/
├── .vscode/
│       ├── settings.json
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
│   │   │   └── risk_factors_cervical_cancer.csv
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

The project folders contain additional files; see their guides for full details:

- [Cervical Cancer project guide](Cervical-Cancer-Data-Mining/README.md)
- Practical scripts and sample datasets are listed above. There is currently no separate README inside Practicals/.

## Practicals

Each practical is self-contained. Open a terminal at the workspace root and run the relevant command:

| Practical | Topics | Run command |
|---|---|---|
| 1 | Student dataset creation and analysis | **python .\Practicals\Practical-1\student_dataset.py** |
| 2 | Data cleaning | **python .\Practicals\Practical-2\data_cleaning.py** |
| 3 | Data preprocessing | **python .\Practicals\Practical-3\data_preprocessing.py** |
| 4 | Association-rule calculations | **python .\Practicals\Practical-4\association_rules.py** |
| 5 | K-Means examples and iteration MSE plot | See the two commands below |

For Practical 5:

~~~powershell
python .\Practicals\Practical-5\kmeans_1d.py
python .\Practicals\Practical-5\kmeans_dataset.py
~~~

The first script runs the one-dimensional example; the second compares K values and plots MSE by iteration. See the script prompts and output while running.

## Cervical Cancer Data Mining project

This is an educational, syllabus-aligned clustering study. Its runner performs integrity verification, provisional preprocessing, K-Means, DBSCAN, and comparative evaluation in order.

From the workspace root, run:

~~~powershell
python .\Cervical-Cancer-Data-Mining\run_project.py
~~~

For Python version, virtual environment setup, dependencies, individual script commands, and detailed results, follow the [project README](Cervical-Cancer-Data-Mining/README.md). The raw dataset must be present at Cervical-Cancer-Data-Mining/data/raw/risk_factors_cervical_cancer.csv.

The project’s feature selection and preprocessing choices are provisional. Its cluster assignments are exploratory and are not medical diagnoses or clinical risk categories.

## Open in VS Code

To open the whole workspace in VS Code from this directory:

~~~powershell
code .
~~~

To open only the Cervical Cancer project:

~~~powershell
code .\Cervical-Cancer-Data-Mining
~~~
