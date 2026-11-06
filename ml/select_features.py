import pandas as pd

# Load the original dataset
data = pd.read_csv("dataset/phiusiil_raw.csv")

# Select only URL-based features
selected_features = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS"
]

# Keep selected features and the target label
clean_data = data[selected_features + ["label"]]

# Save the selected dataset
clean_data.to_csv("dataset/selected_features.csv", index=False)

print("Feature selection completed!")
print("New dataset shape:", clean_data.shape)
print("\nSelected features:")
print(clean_data.columns.tolist())

print("\nFirst 5 rows:")
print(clean_data.head())