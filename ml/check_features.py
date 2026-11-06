import pandas as pd

# Load selected dataset
data = pd.read_csv("dataset/selected_features.csv")

print("FEATURE DATASET CHECK")
print("---------------------")

# Check dataset size
print("Dataset shape:", data.shape)

# Check missing values
print("\nMissing values:")
print(data.isnull().sum().sum())

# Check duplicate rows
print("\nDuplicate rows:")
print(data.duplicated().sum())

# Check target labels
print("\nLabel distribution:")
print(data["label"].value_counts())

# Check data types
print("\nColumn data types:")
print(data.dtypes)  