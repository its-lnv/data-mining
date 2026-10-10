import pandas as pd
import numpy as np
import os

# Get CSV path from the same folder as Python file
file_path = os.path.join(
    os.path.dirname(__file__),
    "data_cleaning_dataset.csv"
)

# Read CSV
df = pd.read_csv(file_path)

print("\nORIGINAL DATASET")
print(df)


# -----------------------------------
# 1. HANDLE MISSING VALUES
# -----------------------------------

df["Age"] = df["Age"].fillna(df["Age"].mean())

df["Marks"] = df["Marks"].fillna(df["Marks"].mean())


# -----------------------------------
# 2. HANDLE INCONSISTENT VALUES
# -----------------------------------

df["Gender"] = df["Gender"].str.capitalize()


# -----------------------------------
# 3. HANDLE OUTLIERS
# -----------------------------------

# Age should be between 18 and 60
df.loc[
    (df["Age"] < 18) | (df["Age"] > 60),
    "Age"
] = np.nan

# Replace outlier with mean
df["Age"] = df["Age"].fillna(df["Age"].mean())


# -----------------------------------
# 4. VALIDATION
# -----------------------------------

# Marks should be between 0 and 100
df = df[
    (df["Marks"] >= 0) &
    (df["Marks"] <= 100)
]


# -----------------------------------
# FINAL CLEANED DATA
# -----------------------------------

print("\nCLEANED DATASET")
print(df)


print("\nDATA CLEANING COMPLETED SUCCESSFULLY")