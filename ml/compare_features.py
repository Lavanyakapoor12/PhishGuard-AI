import pandas as pd
from feature_extractor import extract_features

# Load original dataset
data = pd.read_csv("dataset/phiusiil_raw.csv")

# Take one URL from the dataset
sample = data.iloc[0]

url = sample["URL"]

# Extract features using our function
extracted = extract_features(url)

print("SAMPLE URL:")
print(url)

print("\nFEATURE COMPARISON")
print("------------------")

for feature, calculated_value in extracted.items():

    dataset_value = sample[feature]

    print(f"\n{feature}")
    print("Dataset value   :", dataset_value)
    print("Calculated value:", calculated_value)