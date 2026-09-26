# Data Mining Practicals

This repository contains Python programs and datasets for Data Mining practicals.

The practicals cover data cleaning, data preprocessing, dataset generation, association rule mining, K-Means clustering, and basic data analysis using Python.

---

## 📚 Practicals Covered

### Practical 1 – Student Dataset and Analysis

A dataset of 200 students is created using Python's random functions.

The dataset contains:

- Student ID
- Name
- Surname
- Marks of 5 subjects

Marks are randomly generated between **0 and 50**.

The program performs:

- Creation of a 200-student dataset
- Saving the dataset as a CSV file
- Calculation of subject-wise class averages
- Finding the overall class topper
- Finding subject-wise toppers
- Finding students who scored less than 15 in any subject

---

### Practical 2 – Data Cleaning

This practical demonstrates basic data cleaning techniques using a CSV dataset.

The dataset contains missing, inconsistent, and incorrect values.

The program handles:

- Missing values
- Inconsistent values
- Outliers
- Invalid marks
- Basic validation rules

#### Techniques Used

- Handling missing values using mean values
- Standardizing inconsistent categorical values
- Detecting and handling outliers
- Validating marks within a valid range

---

### Practical 3 – Data Pre-processing

This practical demonstrates common data preprocessing techniques.

The following techniques are implemented:

- Normalization
- Standardization
- Transformation
- Aggregation
- Discretization
- Binarization
- Sampling

#### Normalization

Converts values into a range between 0 and 1.

Formula:

```text
(x - minimum) / (maximum - minimum)
```

#### Standardization

Scales values using mean and standard deviation.

Formula:

```text
(x - mean) / standard deviation
```

#### Transformation

Changes the representation of data, such as converting income into thousands.

#### Aggregation

Combines values to calculate useful summaries such as average marks and total income.

#### Discretization

Converts continuous values into categories such as Young, Adult, and Senior.

#### Binarization

Converts values into 0 and 1.

Example:

```text
Marks >= 50 → 1 (Pass)
Marks < 50  → 0 (Fail)
```

#### Sampling

Selects a smaller random subset of records from the dataset.

---

### Practical 4 – Association Rule Mining

This practical works with a transactional dataset from an electronic store.

The transactions, itemsets, and association rules are predefined according to the practical question.

The program calculates:

- Support of given itemsets
- Support of association rules
- Confidence of association rules

The results are displayed in tabular format using Pandas.

#### Support

Support measures how frequently an itemset occurs in the complete transaction dataset.

Formula:

```text
Support(X) =
(Number of transactions containing X / Total number of transactions) × 100
```

#### Confidence

Confidence measures how frequently the consequent occurs when the antecedent occurs.

Formula:

```text
Confidence(A → B) =
Support(A ∪ B) / Support(A) × 100
```

Example association rule:

```text
Laptop → Mouse
```

No external CSV file is required for this practical because the transactions, itemsets, and rules are provided directly in the Python program.

---

### Practical 5 – K-Means Clustering

This practical demonstrates the K-Means clustering algorithm by implementing the algorithm using Python, NumPy, and Matplotlib.

#### Question 1 – One-Dimensional K-Means

The program:

- Generates 20 random one-dimensional points
- Asks the user to enter the value of K
- Selects initial centroids
- Assigns each point to the nearest centroid
- Calculates new centroids
- Repeats the process until convergence
- Displays the final clusters and centroids

#### Question 2 – K-Means with Different Parameters

The program applies K-Means clustering to a two-dimensional dataset and compares the results by varying the value of K.

The program:

- Runs K-Means for different K values
- Calculates MSE after every iteration
- Displays final centroids
- Displays the number of iterations
- Compares clustering results
- Plots a line graph showing MSE versus iteration

#### Mean Squared Error (MSE)

MSE is used to measure the clustering error.

```text
MSE =
Sum of squared distances from points to their centroids
/ Number of points
```

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
├── Practical-3/
│   ├── data_preprocessing.py
│   └── preprocessing_dataset.csv
│
├── Practical-4/
│   └── association_rules.py
│
├── Practical-5/
│   ├── kmeans_1d.py
│   └── kmeans_dataset.py
│
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- CSV

---

## 📦 Installation

Make sure Python is installed on your system.

Install the required libraries using:

```bash
pip install pandas numpy matplotlib
```

---

## ▶️ How to Run

Open the project folder in VS Code or any Python-supported IDE.

### Practical 1

```bash
cd Practical-1
python student_dataset.py
```

The program creates or updates:

```text
student_dataset_200.csv
```

---

### Practical 2

```bash
cd Practical-2
python data_cleaning.py
```

The program reads:

```text
data_cleaning_dataset.csv
```

and displays the cleaned dataset.

---

### Practical 3

```bash
cd Practical-3
python data_preprocessing.py
```

The program reads:

```text
preprocessing_dataset.csv
```

and performs the required preprocessing techniques.

---

### Practical 4

```bash
cd Practical-4
python association_rules.py
```

The program uses the transactions, itemsets, and association rules given in the practical question and displays support and confidence in tabular format.

No external CSV file is required.

---

### Practical 5

For one-dimensional K-Means:

```bash
cd Practical-5
python kmeans_1d.py
```

The program generates 20 random one-dimensional points and asks the user to enter the value of K.

For K-Means with different parameters and MSE graph:

```bash
python kmeans_dataset.py
```

The program applies K-Means for different K values, calculates MSE after each iteration, and displays the MSE graph.

---

## 📊 Practical 1 – Dataset Information

The student dataset contains **200 records**.

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

The preprocessing practical demonstrates how raw data can be transformed into a suitable form for analysis and data mining.

The techniques include normalization, standardization, transformation, aggregation, discretization, binarization, and sampling.

---

## 🔗 Practical 4 – Association Rule Mining

Association rule mining is used to identify relationships between items in transactional data.

The practical uses:

- Transactions
- Itemsets
- Association rules
- Support calculation
- Confidence calculation

Example:

```text
Laptop → Mouse
```

The results are displayed in a structured tabular format.

---

## 📈 Practical 5 – K-Means Clustering

K-Means is an unsupervised learning algorithm used to divide data points into a predefined number of clusters.

The basic steps are:

1. Select the value of K.
2. Select initial centroids.
3. Calculate the distance between each point and every centroid.
4. Assign each point to its nearest centroid.
5. Calculate new centroids.
6. Repeat until the centroids converge.

The second part of the practical also calculates MSE after every iteration and visualizes the change in MSE using Matplotlib.

---

## 🎯 Learning Outcomes

After completing these practicals, the following concepts can be understood:

- Creating datasets using Python
- Reading and writing CSV files
- Working with Pandas DataFrames
- Handling missing data
- Handling inconsistent data
- Identifying and handling outliers
- Applying validation rules
- Normalizing data
- Standardizing data
- Transforming data
- Aggregating data
- Discretizing continuous data
- Binarizing data
- Performing random sampling
- Calculating support and confidence
- Understanding association rules
- Implementing K-Means clustering
- Calculating clustering error using MSE
- Comparing clustering results
- Visualizing results using Matplotlib
- Performing basic data analysis

---

## 🎓 Academic Purpose

This repository is created for academic learning and practical implementation of Data Mining concepts using Python.

The programs are kept simple and focused on understanding the implementation of common Data Mining algorithms and data preprocessing techniques.

They are suitable for practical assignments, examination preparation, and viva practice.

---

## 👨‍💻 Author

**Laxmi Narayan Verma**

---

## ⭐ Conclusion

These practicals demonstrate how Python can be used to create, clean, preprocess, analyze, and cluster datasets.

The repository provides a basic foundation for understanding data preparation, association rule mining, clustering, and data analysis techniques used in Data Mining.
