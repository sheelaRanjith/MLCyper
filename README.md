# Machine Learning Based Cyber Intrusion Detection System for Secure Digital Governance

This project is a beginner-friendly full stack IDS (Intrusion Detection System) using **Flask + React + Scikit-learn**.

## 1) Project Structure

```text
cyber_intrusion_detection_project/
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── intrusion_model.pkl            # generated after training
│   ├── model_metrics.json             # generated after training
│   ├── detection_logs.json            # generated after uploads
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── services/
│       │   └── api.js
│       └── components/
│           ├── Login.js
│           ├── Dashboard.js
│           ├── UploadData.js
│           ├── Results.js
│           └── Logs.js
└── dataset/
    └── nsl_kdd.csv
```

## 2) Features Implemented

- Admin Login (`/login` API) with default credentials: `admin / admin123`
- Dashboard summary cards:
  - Total requests analyzed
  - Number of attacks detected
  - Normal traffic count
- CSV upload and backend analysis (`/upload` API)
- Intrusion classification into:
  - Normal
  - DoS attack
  - Probe attack
  - R2L attack
  - U2R attack
- Results table (`/results` API)
- Persistent logs/history (`/logs` API)
- Chart.js visualizations:
  - Attack distribution pie chart
  - Normal vs Attack bar chart
  - Model accuracy comparison bar chart

## 3) Backend Setup (Flask + ML)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Train model

```bash
python train_model.py
```

This will generate:
- `backend/intrusion_model.pkl`
- `backend/model_metrics.json`

### Run backend API

```bash
python app.py
```

Backend runs on: `http://127.0.0.1:5000`

## 4) Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on: `http://127.0.0.1:3000`

## 5) API Endpoints

- `POST /login`
  - Request JSON: `{ "username": "admin", "password": "admin123" }`
- `POST /upload`
  - Form-data with CSV file field name: `file`
- `GET /results`
  - Returns latest upload prediction results
- `GET /logs`
  - Returns all detection history logs

## 6) Example Dataset Format

CSV must include these columns:

```csv
duration,protocol_type,service,src_bytes,dst_bytes,count,srv_count,logged_in,wrong_fragment,label
0,tcp,http,181,5450,2,2,1,0,normal
0,tcp,private,0,0,121,19,0,0,neptune
3,tcp,telnet,0,52,4,2,0,0,buffer_overflow
```

For prediction upload, `label` is optional. If `connection_id` is missing, backend auto-generates IDs.

## 7) Example Prediction Output

```json
{
  "results": [
    {
      "connection_id": "CONN-00001",
      "protocol": "tcp",
      "service": "http",
      "prediction": "Normal",
      "timestamp": "2026-01-01T10:00:00Z"
    },
    {
      "connection_id": "CONN-00002",
      "protocol": "tcp",
      "service": "private",
      "prediction": "DoS attack",
      "timestamp": "2026-01-01T10:00:00Z"
    }
  ]
}
```

## 8) Beginner-Friendly Workflow (Step-by-Step)

1. Clone/open this project.
2. Put your full NSL-KDD dataset at `dataset/nsl_kdd.csv` (sample already included).
3. Setup backend virtual environment and install packages.
4. Run `python train_model.py` to train 4 algorithms and save best model.
5. Start backend with `python app.py`.
6. Setup frontend and run `npm start`.
7. Open browser at `http://127.0.0.1:3000`.
8. Login with admin credentials.
9. Upload CSV network traffic data.
10. View predictions in **Results**, logs in **Logs**, and charts on **Dashboard**.

## 9) ML Algorithms Compared

- Logistic Regression
- Decision Tree
- Random Forest
- KNN

The script selects the best model by test accuracy and stores it as `intrusion_model.pkl`.

## 10) Important Notes

- This project is intentionally simple for final-year demonstration.
- For production use, add secure JWT auth, role-based access, database storage, and model versioning.
