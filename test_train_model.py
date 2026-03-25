import sys
import os
import pytest
import numpy as np
import pandas as pd

# Ensure workspace root is on path
sys.path.insert(0, os.path.dirname(__file__))

from train_model import preprocess, train_and_save, FEATURE_COLUMNS, TARGET_COLUMN


SAMPLE_CSV = "test_dataset_tmp.csv"


def make_sample_csv(path, rows=50, with_nan=False):
    """Create a minimal valid CSV for testing."""
    rng = np.random.default_rng(0)
    data = {col: rng.integers(0, 5, size=rows).astype(float) for col in FEATURE_COLUMNS}
    data[TARGET_COLUMN] = rng.integers(0, 2, size=rows)
    df = pd.DataFrame(data)
    if with_nan:
        df.iloc[0, 0] = float("nan")
        df.iloc[5, 3] = float("nan")
    df.to_csv(path, index=False)


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(SAMPLE_CSV):
        os.remove(SAMPLE_CSV)


def test_csv_loads():
    """DataFrame is non-empty when a valid CSV is present."""
    make_sample_csv(SAMPLE_CSV)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    assert len(X_train) + len(X_test) > 0


def test_missing_file_exits():
    """sys.exit(1) is called when the CSV file is not found."""
    with pytest.raises(SystemExit) as exc_info:
        preprocess("nonexistent_file.csv")
    assert exc_info.value.code == 1


def test_nan_rows_dropped():
    """Rows with NaN values are removed before splitting."""
    make_sample_csv(SAMPLE_CSV, rows=50, with_nan=True)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    total = len(X_train) + len(X_test)
    # 2 NaN rows should have been dropped from 50
    assert total == 48


def test_split_ratio():
    """Train set is approximately 80% and test set approximately 20%."""
    make_sample_csv(SAMPLE_CSV, rows=100)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    total = len(X_train) + len(X_test)
    assert total == 100
    assert len(X_train) == 80
    assert len(X_test) == 20


def test_feature_count():
    """Scaled output has exactly 13 feature columns."""
    make_sample_csv(SAMPLE_CSV)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    assert X_train.shape[1] == 13
    assert X_test.shape[1] == 13


# ── Task 2.4 tests ────────────────────────────────────────────────────────────

MODEL_DIR_TMP = "test_model_tmp"


@pytest.fixture(autouse=False)
def cleanup_model_dir():
    yield
    import shutil
    if os.path.exists(MODEL_DIR_TMP):
        shutil.rmtree(MODEL_DIR_TMP)


def test_model_directory_created(cleanup_model_dir):
    """train_and_save creates the model directory if it does not exist."""
    make_sample_csv(SAMPLE_CSV, rows=50)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    train_and_save(X_train, X_test, y_train, y_test, scaler, model_dir=MODEL_DIR_TMP)
    assert os.path.isdir(MODEL_DIR_TMP)


def test_model_files_saved(cleanup_model_dir):
    """model.pkl and scaler.pkl are written to the model directory."""
    make_sample_csv(SAMPLE_CSV, rows=50)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    train_and_save(X_train, X_test, y_train, y_test, scaler, model_dir=MODEL_DIR_TMP)
    assert os.path.isfile(os.path.join(MODEL_DIR_TMP, "model.pkl"))
    assert os.path.isfile(os.path.join(MODEL_DIR_TMP, "scaler.pkl"))


def test_accuracy_is_valid_float(cleanup_model_dir):
    """Returned accuracy is a float in [0.0, 1.0]."""
    make_sample_csv(SAMPLE_CSV, rows=100)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    _, accuracy = train_and_save(X_train, X_test, y_train, y_test, scaler, model_dir=MODEL_DIR_TMP)
    assert isinstance(accuracy, float)
    assert 0.0 <= accuracy <= 1.0


def test_saved_model_loads_and_predicts(cleanup_model_dir):
    """Saved model.pkl can be loaded and produces predictions of shape (n,)."""
    import pickle
    make_sample_csv(SAMPLE_CSV, rows=100)
    X_train, X_test, y_train, y_test, scaler = preprocess(SAMPLE_CSV)
    train_and_save(X_train, X_test, y_train, y_test, scaler, model_dir=MODEL_DIR_TMP)
    with open(os.path.join(MODEL_DIR_TMP, "model.pkl"), "rb") as f:
        loaded_model = pickle.load(f)
    preds = loaded_model.predict(X_test)
    assert preds.shape == (len(X_test),)
