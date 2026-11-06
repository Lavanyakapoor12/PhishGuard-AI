import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

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

print("Training Random Forest model...")

# Create the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

# Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")

# Make predictions
y_pred = model.predict(X_test)

# Check model performance
accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL PERFORMANCE")
print("-----------------")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Phishing", "Legitimate"]
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save the trained model
joblib.dump(model, "ml/phishguard_model.pkl")

# Save the feature names in the correct order
joblib.dump(X.columns.tolist(), "ml/feature_names.pkl")

print("\nModel saved successfully!")
print("File: ml/phishguard_model.pkl")