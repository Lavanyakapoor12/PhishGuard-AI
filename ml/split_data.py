import pandas as pd
from sklearn.model_selection import train_test_split

# Load selected dataset
data = pd.read_csv("dataset/selected_features.csv")

# Separate input features and target label
X = data.drop("label", axis=1)
y = data["label"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Display dataset sizes
print("DATASET SPLIT COMPLETED!")
print("------------------------")

print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)

print("\nTraining labels:")
print(y_train.value_counts())

print("\nTesting labels:")
print(y_test.value_counts())