import random
import pandas as pd
import os

# Same random data every time
random.seed(42)

# Names
names = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Kabir",
    "Rohan", "Rahul", "Aman", "Karan", "Neha",
    "Priya", "Riya", "Ananya", "Ishita", "Sneha",
    "Pooja", "Nisha", "Simran", "Vikash", "Yash"
]

# Surnames
surnames = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar",
    "Mehta", "Patel", "Agarwal", "Mishra", "Jain"
]

# Create 200 students
data = []

for i in range(1, 201):

    name = random.choice(names)
    surname = random.choice(surnames)

    marks = [
        random.randint(0, 50),
        random.randint(0, 50),
        random.randint(0, 50),
        random.randint(0, 50),
        random.randint(0, 50)
    ]

    data.append([i, name, surname] + marks)


# Create DataFrame
df = pd.DataFrame(data, columns=[
    "ID",
    "Name",
    "Surname",
    "Subject1",
    "Subject2",
    "Subject3",
    "Subject4",
    "Subject5"
])

# Save CSV in the same folder as this Python file
file_path = os.path.join(
    os.path.dirname(__file__),
    "student_dataset_200.csv"
)

df.to_csv(file_path, index=False)


# Display first 10 records
print("\nDATASET - FIRST 10 RECORDS")
print(df.head(10))


# -----------------------------------
# A. Average of all subjects
# -----------------------------------

subjects = [
    "Subject1",
    "Subject2",
    "Subject3",
    "Subject4",
    "Subject5"
]

print("\nAVERAGE MARKS OF WHOLE CLASS")

for subject in subjects:
    average = df[subject].mean()
    print(subject, "=", round(average, 2))


# -----------------------------------
# B. Overall Topper
# -----------------------------------

df["Total"] = df[subjects].sum(axis=1)

topper = df.loc[df["Total"].idxmax()]

print("\nOVERALL TOPPER")

print("ID       :", topper["ID"])
print("Name     :", topper["Name"], topper["Surname"])
print("Subject1 :", topper["Subject1"])
print("Subject2 :", topper["Subject2"])
print("Subject3 :", topper["Subject3"])
print("Subject4 :", topper["Subject4"])
print("Subject5 :", topper["Subject5"])
print("Total    :", topper["Total"])


# -----------------------------------
# C. Subject-wise Topper
# -----------------------------------

print("\nSUBJECT-WISE TOPPERS")

for subject in subjects:

    topper = df.loc[df[subject].idxmax()]

    print(
        subject,
        "->",
        topper["Name"],
        topper["Surname"],
        "| Marks =", topper[subject]
    )


# -----------------------------------
# D. Students scoring less than 15
# -----------------------------------

low_students = df[
    (df[subjects] < 15).any(axis=1)
]

print("\nSTUDENTS WHO SCORED LESS THAN 15 IN ANY SUBJECT")

print(
    low_students[
        ["ID", "Name", "Surname"] + subjects
    ].to_string(index=False)
)

print("\nTotal students =", len(low_students))

print("\nCSV file saved at:")
print(file_path)