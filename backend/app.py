import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "intrusion_model.pkl"
METRICS_PATH = BASE_DIR / "model_metrics.json"
LOG_FILE = BASE_DIR / "detection_logs.json"

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

ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

model = None
model_metrics = {
    "best_model": "Not trained",
    "best_accuracy": 0,
    "model_scores": {},
    "class_names": ["Normal", "DoS attack", "Probe attack", "R2L attack", "U2R attack"],
}
last_results = []



def load_logs():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return []


def save_logs(logs):
    LOG_FILE.write_text(json.dumps(logs, indent=2), encoding="utf-8")


def initialize():
    global model, model_metrics
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    if METRICS_PATH.exists():
        model_metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))


initialize()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        return jsonify({"message": "Login successful", "token": "demo-admin-token"})
    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/upload", methods=["POST"])
def upload_file():
    global last_results

    if model is None:
        return jsonify({"message": "Model file not found. Run train_model.py first."}), 500

    if "file" not in request.files:
        return jsonify({"message": "CSV file is required"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "Please choose a CSV file"}), 400

    try:
        df = pd.read_csv(file)
    except Exception as exc:
        return jsonify({"message": f"Unable to parse CSV: {exc}"}), 400

    missing_columns = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing_columns:
        return (
            jsonify({"message": f"Missing required columns: {', '.join(missing_columns)}"}),
            400,
        )

    if "connection_id" not in df.columns:
        df["connection_id"] = [f"CONN-{i+1:05d}" for i in range(len(df))]

    predictions = model.predict(df[FEATURE_COLUMNS])

    uploaded_results = []
    timestamp = datetime.utcnow().isoformat() + "Z"
    for idx, pred in enumerate(predictions):
        row = {
            "connection_id": str(df.iloc[idx]["connection_id"]),
            "protocol": str(df.iloc[idx]["protocol_type"]),
            "service": str(df.iloc[idx]["service"]),
            "prediction": str(pred),
            "timestamp": timestamp,
        }
        uploaded_results.append(row)

    logs = load_logs()
    logs.extend(uploaded_results)
    save_logs(logs)

    last_results = uploaded_results

    return jsonify(
        {
            "message": "File analyzed successfully",
            "results": uploaded_results,
            "summary": get_summary(logs),
            "model_metrics": model_metrics,
        }
    )


@app.route("/results", methods=["GET"])
def get_results():
    return jsonify({"results": last_results, "model_metrics": model_metrics})


@app.route("/logs", methods=["GET"])
def get_logs():
    logs = load_logs()
    return jsonify({"logs": logs, "summary": get_summary(logs), "model_metrics": model_metrics})


@app.route("/dashboard", methods=["GET"])
def dashboard():
    logs = load_logs()
    return jsonify({"summary": get_summary(logs), "model_metrics": model_metrics})


def get_summary(logs):
    total = len(logs)
    normal = sum(1 for row in logs if row["prediction"] == "Normal")
    attacks = total - normal
    distribution = {
        "Normal": 0,
        "DoS attack": 0,
        "Probe attack": 0,
        "R2L attack": 0,
        "U2R attack": 0,
    }
    for row in logs:
        if row["prediction"] in distribution:
            distribution[row["prediction"]] += 1

    return {
        "total_requests": total,
        "attacks_detected": attacks,
        "normal_traffic": normal,
        "distribution": distribution,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
