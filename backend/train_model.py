import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "nsl_kdd.csv"
MODEL_PATH = Path(__file__).resolve().parent / "intrusion_model.pkl"
METRICS_PATH = Path(__file__).resolve().parent / "model_metrics.json"

FEATURE_COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "src_bytes",
    "dst_bytes",
    "count",
    "srv_count",
    "logged_in",
    "wrong_fragment",
]

ATTACK_MAP = {
    "normal": "Normal",
    "neptune": "DoS attack",
    "smurf": "DoS attack",
    "back": "DoS attack",
    "teardrop": "DoS attack",
    "pod": "DoS attack",
    "land": "DoS attack",
    "ipsweep": "Probe attack",
    "nmap": "Probe attack",
    "portsweep": "Probe attack",
    "satan": "Probe attack",
    "ftp_write": "R2L attack",
    "guess_passwd": "R2L attack",
    "imap": "R2L attack",
    "multihop": "R2L attack",
    "phf": "R2L attack",
    "spy": "R2L attack",
    "warezclient": "R2L attack",
    "warezmaster": "R2L attack",
    "buffer_overflow": "U2R attack",
    "loadmodule": "U2R attack",
    "perl": "U2R attack",
    "rootkit": "U2R attack",
}


def map_attack_label(raw_label: str) -> str:
    key = str(raw_label).strip().replace(".", "").lower()
    return ATTACK_MAP.get(key, "Probe attack")


def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. Place NSL-KDD formatted CSV in dataset/nsl_kdd.csv"
        )

    df = pd.read_csv(DATASET_PATH)
    required = set(FEATURE_COLUMNS + ["label"])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")

    df["target"] = df["label"].apply(map_attack_label)
    return df


def build_preprocessor() -> ColumnTransformer:
    numeric_features = [
        "duration",
        "src_bytes",
        "dst_bytes",
        "count",
        "srv_count",
        "logged_in",
        "wrong_fragment",
    ]
    categorical_features = ["protocol_type", "service"]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def train() -> None:
    df = load_dataset()
    x = df[FEATURE_COLUMNS]
    y = df["target"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor()
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
    }

    metrics = {}
    best_name = None
    best_acc = -1.0
    best_pipeline = None

    for model_name, model in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )
        pipeline.fit(x_train, y_train)
        preds = pipeline.predict(x_test)
        acc = accuracy_score(y_test, preds)
        report = classification_report(y_test, preds, output_dict=True, zero_division=0)

        metrics[model_name] = {
            "accuracy": round(float(acc), 4),
            "weighted_precision": round(float(report["weighted avg"]["precision"]), 4),
            "weighted_recall": round(float(report["weighted avg"]["recall"]), 4),
        }

        if acc > best_acc:
            best_acc = acc
            best_name = model_name
            best_pipeline = pipeline

    if best_pipeline is None:
        raise RuntimeError("Training failed to produce a model.")

    joblib.dump(best_pipeline, MODEL_PATH)

    payload = {
        "best_model": best_name,
        "best_accuracy": round(float(best_acc), 4),
        "model_scores": metrics,
        "feature_columns": FEATURE_COLUMNS,
        "class_names": ["Normal", "DoS attack", "Probe attack", "R2L attack", "U2R attack"],
    }
    METRICS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Saved best model ({best_name}) to {MODEL_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")


if __name__ == "__main__":
    train()
