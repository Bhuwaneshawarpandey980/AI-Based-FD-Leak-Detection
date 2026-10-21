import pandas as pd
import joblib
import sys


# ============================================================
# AI-BASED FILE DESCRIPTOR LEAK DETECTION
# PREDICTION MODULE
# ============================================================

MODEL_FILE = "fd_leak_model.pkl"


FEATURES = [
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


def predict_from_dataset(csv_file):

    print("=" * 70)
    print("AI-BASED FILE DESCRIPTOR LEAK DETECTION")
    print("PREDICTION")
    print("=" * 70)

    # Load trained model
    model = joblib.load(MODEL_FILE)

    print("\nTrained model loaded successfully.")
    print("Input dataset:", csv_file)

    # Load dataset
    df = pd.read_csv(csv_file)

    # Check required columns
    missing = [feature for feature in FEATURES if feature not in df.columns]

    if missing:
        print("\nERROR: Missing features:")
        print(missing)
        return

    # Select features
    X = df[FEATURES]

    # Make predictions
    predictions = model.predict(X)

    # Prediction probabilities
    probabilities = model.predict_proba(X)

    print("\n" + "-" * 70)
    print("PREDICTION RESULTS")
    print("-" * 70)

    for i in range(len(df)):

        prediction = predictions[i]

        if prediction == 1:
            status = "LEAK DETECTED"
            confidence = probabilities[i][1] * 100
        else:
            status = "NORMAL"
            confidence = probabilities[i][0] * 100

        print(
            f"Sample {i + 1:03d} | "
            f"FDs={df.iloc[i]['fd_count']} | "
            f"Files={df.iloc[i]['file_count']} | "
            f"Sockets={df.iloc[i]['socket_count']} | "
            f"Prediction={status} | "
            f"Confidence={confidence:.2f}%"
        )

    # Summary
    normal_count = sum(predictions == 0)
    leak_count = sum(predictions == 1)

    print("\n" + "=" * 70)
    print("PREDICTION SUMMARY")
    print("=" * 70)

    print("Total samples :", len(predictions))
    print("Normal        :", normal_count)
    print("Leak detected :", leak_count)

    if leak_count > 0:
        print("\nWARNING: File descriptor leak behaviour detected.")
    else:
        print("\nSystem behaviour appears NORMAL.")

    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Usage:")
        print("python3 predict_leak.py <dataset.csv>")

        print("\nExample:")
        print("python3 predict_leak.py leak_dataset.csv")

        sys.exit(1)

    csv_file = sys.argv[1]

    predict_from_dataset(csv_file)