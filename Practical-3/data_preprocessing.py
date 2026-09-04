import pandas as pd
import numpy as np
import os

# Get CSV path from same folder as Python file
file_path = os.path.join(
    os.path.dirname(__file__),
    "preprocessing_dataset.csv"
)

# Read CSV
df = pd.read_csv(file_path)

print("\nORIGINAL DATASET")
print(df)


# -----------------------------------
# 1. NORMALIZATION
# -----------------------------------

# Formula:
# (x - min) / (max - min)

df["Marks_Normalized"] = (
    (df["Marks"] - df["Marks"].min()) /
    (df["Marks"].max() - df["Marks"].min())
)

print("\nNORMALIZED DATA")
print(df[["Marks", "Marks_Normalized"]])


# -----------------------------------
# 2. STANDARDIZATION
# -----------------------------------

# Formula:
# (x - mean) / standard deviation

df["Age_Standardized"] = (
    (df["Age"] - df["Age"].mean()) /
    df["Age"].std()
)

print("\nSTANDARDIZED DATA")
print(df[["Age", "Age_Standardized"]])


# -----------------------------------
# 3. TRANSFORMATION
# -----------------------------------

df["Income_Thousands"] = df["Income"] / 1000

print("\nTRANSFORMED DATA")
print(df[["Income", "Income_Thousands"]])


# -----------------------------------
# 4. AGGREGATION
# -----------------------------------

average_marks = df["Marks"].mean()
total_income = df["Income"].sum()

print("\nAGGREGATION")

print("Average Marks =", round(average_marks, 2))
print("Total Income =", total_income)


# -----------------------------------
# 5. DISCRETIZATION
# -----------------------------------

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 25, 35, 100],
    labels=["Young", "Adult", "Senior"]
)

print("\nDISCRETIZED AGE")

print(
    df[
        ["Age", "Age_Group"]
    ]
)


# -----------------------------------
# 6. BINARIZATION
# -----------------------------------

# Marks >= 50 = Pass (1)
# Marks < 50 = Fail (0)

df["Pass"] = (
    df["Marks"] >= 50
).astype(int)

print("\nBINARIZED MARKS")

print(
    df[
        ["Marks", "Pass"]
    ]
)


# -----------------------------------
# 7. SAMPLING
# -----------------------------------

sample = df.sample(
    n=3,
    random_state=1
)

print("\nRANDOM SAMPLE")

print(
    sample[
        ["Name", "Age", "Marks"]
    ]
)


print("\nDATA PRE-PROCESSING COMPLETED SUCCESSFULLY")