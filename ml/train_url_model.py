import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load original dataset
data = pd.read_csv("dataset/phiusiil_raw.csv")

# Keep URL and label columns
data = data[["URL", "label"]].dropna()

# Convert URLs into strings
X = data["URL"].astype(str)
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create the machine learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 5),
            min_df=2,
            max_features=300000,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])

print("Training URL-based AI model...")

# Train model
model.fit(X_train, y_train)

print("\nTraining completed!")

# Predict test URLs
y_pred = model.predict(X_test)

# Evaluate model
print("\nMODEL PERFORMANCE")
print("-----------------")

print(
    "Accuracy:",
    round(accuracy_score(y_test, y_pred) * 100, 2),
    "%"
)

print("\nClassification Report:")

print(classification_report(
    y_test,
    y_pred,
    labels=[0, 1],
    target_names=["Phishing", "Legitimate"]
))

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

# Save model
joblib.dump(model, "ml/phishguard_url_model.pkl")

print("\nURL-based model saved successfully!")