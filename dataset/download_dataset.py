
# Import the function used to download UCI datasets
from ucimlrepo import fetch_ucirepo

# Import pandas to handle our dataset
import pandas as pd

# Download the PhiUSIIL dataset
print("Downloading PhiUSIIL dataset...")

dataset = fetch_ucirepo(id=967)

# Get input features
features = dataset.data.features

# Get target labels
targets = dataset.data.targets

# Combine features and labels into one table
data = pd.concat([features, targets], axis=1)

# Save the original dataset as a CSV file
data.to_csv("dataset/phiusiil_raw.csv", index=False)

# Display basic information
print("Dataset downloaded successfully!")

print("Dataset shape:", data.shape)

print("Available columns:")
print(data.columns.tolist())

print("First 5 rows:")
print(data.head())
