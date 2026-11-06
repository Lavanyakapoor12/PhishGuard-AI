import pandas as pd

# Load our downloaded dataset
data = pd.read_csv("dataset/phiusiil_raw.csv")

print("\nDATASET INFORMATION")
print("-------------------")

# Total rows and columns
print("Dataset shape:", data.shape)

# Display all column names
print("\nColumn names:")
print(data.columns.tolist())

# Check target label distribution
print("\nLabel distribution:")
print(data["label"].value_counts())

# Check missing values
print("\nMissing values:")
print(data.isnull().sum().sum())

# Check duplicate rows
print("\nDuplicate rows:")
print(data.duplicated().sum())

print("\nDATASET COLUMN DETAILS")
print("----------------------")

for column in data.columns:
    print(column)