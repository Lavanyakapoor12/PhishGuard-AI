from feature_extractor import extract_features

# Sample URL for testing
url = "https://www.google.com"

# Extract URL features
features = extract_features(url)

# Display the results
print("URL:", url)

print("\nEXTRACTED FEATURES")
print("------------------")

for feature, value in features.items():
    print(feature, ":", value)

print("\nTotal features:", len(features))