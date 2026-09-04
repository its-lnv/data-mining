# Data Mining Practicals

This repository contains Python programs and datasets for Data Mining practicals.

The practicals cover data cleaning, data preprocessing, random dataset generation, and basic data analysis using Python.

---

## 📚 Practicals Covered

### Practical 1 – Student Dataset and Analysis

A dataset of 200 students is created using Python's random functions.

The dataset contains:

- Student ID
- Name
- Surname
- Marks of 5 subjects

Marks are randomly generated between 0 and 50.

The program performs:

- Creation of a 200-student dataset
- Saving the dataset as a CSV file
- Calculation of subject-wise class averages
- Finding the overall class topper
- Finding subject-wise toppers
- Finding students who scored less than 15 in any subject

### Practical 2 – Data Cleaning

This practical demonstrates basic data cleaning techniques using a CSV dataset.

The dataset contains missing, inconsistent, and incorrect values.

The program handles:

- Missing values
- Inconsistent values
- Outliers
- Invalid marks
- Basic validation rules

### Practical 3 – Data Pre-processing

This practical demonstrates common data preprocessing techniques:

- Normalization
- Standardization
- Transformation
- Aggregation
- Discretization
- Binarization
- Sampling

---

## 🗂️ Project Structure

```text
Data Mining/
│
├── Practical-1/
│   ├── student_dataset.py
│   └── student_dataset_200.csv
│
├── Practical-2/
│   ├── data_cleaning.py
│   └── data_cleaning_dataset.csv
│
└── Practical-3/
    ├── data_preprocessing.py
    └── preprocessing_dataset.csv
```

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- CSV

---

## 📦 Installation

Make sure Python is installed on your system.

Install the required libraries:

```bash
pip install pandas numpy
```

---

## ▶️ How to Run

Open the project in VS Code or any Python-supported IDE.

### Practical 1

```bash
cd Practical-1
python student_dataset.py
```

The program generates/updates `student_dataset_200.csv`.

### Practical 2

```bash
cd Practical-2
python data_cleaning.py
```

The program reads `data_cleaning_dataset.csv` and displays the cleaned dataset.

### Practical 3

```bash
cd Practical-3
python data_preprocessing.py
```

The program reads `preprocessing_dataset.csv` and performs the preprocessing techniques.

---

## 📊 Practical 1 – Dataset

The student dataset contains 200 records.

| Column | Description |
|---|---|
| ID | Unique student ID |
| Name | Student first name |
| Surname | Student surname |
| Subject1 | Marks in Subject 1 |
| Subject2 | Marks in Subject 2 |
| Subject3 | Marks in Subject 3 |
| Subject4 | Marks in Subject 4 |
| Subject5 | Marks in Subject 5 |

Marks are generated randomly in the range **0–50**.

---

## 🧹 Practical 2 – Data Cleaning

The data cleaning dataset contains examples of common data quality problems.

### Missing Values

Missing Age and Marks values are handled using the mean.

### Inconsistent Values

Values such as `Male`, `male`, and `MALE` are converted into a common format.

### Outliers

An invalid age value outside the expected range is treated as an outlier and replaced.

### Validation

Marks are validated to ensure that they fall between 0 and 100.

---

## ⚙️ Practical 3 – Data Pre-processing

### Normalization

Converts values into a range between 0 and 1.

Formula:

```text
(x - minimum) / (maximum - minimum)
```

### Standardization

Scales values using mean and standard deviation.

Formula:

```text
(x - mean) / standard deviation
```

### Transformation

Changes the representation of data, such as converting income into thousands.

### Aggregation

Combines values to calculate useful summaries such as average marks and total income.

### Discretization

Converts continuous values into categories such as Young, Adult, and Senior.

### Binarization

Converts values into 0 and 1. For example:

```text
Marks >= 50 → 1 (Pass)
Marks < 50  → 0 (Fail)
```

### Sampling

Selects a smaller random subset of records from the dataset.

---

## 🎯 Learning Outcomes

These practicals provide hands-on understanding of:

- Creating datasets using Python
- Reading and writing CSV files
- Working with Pandas DataFrames
- Handling missing data
- Handling inconsistent data
- Handling outliers
- Applying validation rules
- Normalizing data
- Standardizing data
- Transforming data
- Aggregating data
- Discretizing data
- Binarizing data
- Sampling data
- Performing basic data analysis

---

## 🎓 Academic Purpose

This repository is created for academic learning and practical implementation of basic Data Mining concepts using Python.

The programs are kept simple so that the concepts can be easily understood and explained during practical examinations and viva.

---

## 👨‍💻 Author

**Data Mining Practical Work**

---

## ⭐ Conclusion

These practicals demonstrate how Python can be used to create, clean, preprocess, and analyze datasets.

They provide a basic foundation for understanding data preparation and analysis techniques used in Data Mining.
