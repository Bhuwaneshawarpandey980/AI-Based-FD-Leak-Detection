import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib


# ============================================================
# AI-BASED FILE DESCRIPTOR LEAK DETECTION
# MODEL TRAINING
# ============================================================

print("=" * 70)
print("AI-BASED FILE DESCRIPTOR LEAK DETECTION")
print("MODEL TRAINING")
print("=" * 70)


# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

DATASET = "training_dataset.csv"

df = pd.read_csv(DATASET)

print("\nDataset loaded successfully.")
print("Total samples:", len(df))

print("\nClass distribution:")
print(df["label"].value_counts())


# ------------------------------------------------------------
# 2. SELECT FEATURES
# ------------------------------------------------------------

features = [
    "fd_count",
    "fd_delta",
    "fd_growth_rate",
    "file_count",
    "socket_count",
    "pipe_count",
    "device_count",
    "unknown_count",
    "fd_limit",
    "fd_utilization"
]

X = df[features]
y = df["label"]


# ------------------------------------------------------------
# 3. SPLIT DATA
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ------------------------------------------------------------
# 4. CREATE RANDOM FOREST MODEL
# ------------------------------------------------------------

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("Model training completed.")


# ------------------------------------------------------------
# 5. PREDICTION
# ------------------------------------------------------------

y_pred = model.predict(X_test)


# ------------------------------------------------------------
# 6. MODEL ACCURACY
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(f"\nAccuracy: {accuracy * 100:.2f}%")


# ------------------------------------------------------------
# 7. CLASSIFICATION REPORT
# ------------------------------------------------------------

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["NORMAL", "LEAK"]
))


# ------------------------------------------------------------
# 8. CONFUSION MATRIX
# ------------------------------------------------------------

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ------------------------------------------------------------
# 9. FEATURE IMPORTANCE
# ------------------------------------------------------------

print("\nFeature Importance:")

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance.to_string(index=False))


# ------------------------------------------------------------
# 10. SAVE TRAINED MODEL
# ------------------------------------------------------------

MODEL_FILE = "fd_leak_model.pkl"

joblib.dump(model, MODEL_FILE)

print("\n" + "=" * 70)
print(f"Trained model saved as: {MODEL_FILE}")
print("=" * 70)

print("\nAI model training completed successfully.")