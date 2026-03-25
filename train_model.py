import sys
import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


FEATURE_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]
TARGET_COLUMN = "target"
DATASET_PATH = "dataset.csv"


def preprocess(dataset_path=DATASET_PATH):
    """Load and preprocess the heart disease dataset.

    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    # Load dataset
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' not found. "
              "Please place the Kaggle Heart Disease CSV at the project root.")
        sys.exit(1)

    df = pd.read_csv(dataset_path)

    # Drop rows with missing values
    df = df.dropna()

    # Separate features and target
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/test split (80/20, fixed seed for reproducibility)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, scaler


MODEL_DIR = "model"


def train_and_save(X_train, X_test, y_train, y_test, scaler, model_dir=MODEL_DIR):
    """Train a RandomForestClassifier, evaluate it, and save model + scaler.

    Args:
        X_train, X_test, y_train, y_test: split dataset arrays
        scaler: fitted StandardScaler from preprocessing
        model_dir: directory to save model.pkl and scaler.pkl

    Returns:
        model: the trained RandomForestClassifier
        accuracy: float accuracy on the test set
    """
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    # Save
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    return model, accuracy


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler = preprocess()
    print(f"Preprocessing complete. "
          f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    train_and_save(X_train, X_test, y_train, y_test, scaler)
