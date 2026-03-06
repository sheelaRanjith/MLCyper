import React, { useEffect, useState } from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";
import api from "../services/api";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

function Dashboard() {
  const [summary, setSummary] = useState({
    total_requests: 0,
    attacks_detected: 0,
    normal_traffic: 0,
    distribution: {},
  });
  const [metrics, setMetrics] = useState({ model_scores: {}, best_accuracy: 0, best_model: "-" });

  useEffect(() => {
    const fetchData = async () => {
      const response = await api.get("/dashboard");
      setSummary(response.data.summary);
      setMetrics(response.data.model_metrics);
    };
    fetchData();
  }, []);

  const pieData = {
    labels: Object.keys(summary.distribution || {}),
    datasets: [
      {
        data: Object.values(summary.distribution || {}),
        backgroundColor: ["#198754", "#dc3545", "#ffc107", "#0dcaf0", "#6f42c1"],
      },
    ],
  };

  const barData = {
    labels: ["Normal", "Attacks"],
    datasets: [
      {
        label: "Traffic Count",
        data: [summary.normal_traffic, summary.attacks_detected],
        backgroundColor: ["#198754", "#dc3545"],
      },
    ],
  };

  const accuracyData = {
    labels: Object.keys(metrics.model_scores || {}),
    datasets: [
      {
        label: "Accuracy",
        data: Object.values(metrics.model_scores || {}).map((item) => item.accuracy * 100),
        backgroundColor: "#0d6efd",
      },
    ],
  };

  return (
    <div className="container">
      <h2 className="mb-4">System Dashboard</h2>
      <div className="row g-3 mb-4">
        <StatCard title="Total Requests Analyzed" value={summary.total_requests} color="primary" />
        <StatCard title="Attacks Detected" value={summary.attacks_detected} color="danger" />
        <StatCard title="Normal Traffic" value={summary.normal_traffic} color="success" />
      </div>

      <div className="alert alert-info">
        <strong>Best Model:</strong> {metrics.best_model} | <strong>Accuracy:</strong> {(metrics.best_accuracy * 100).toFixed(2)}%
      </div>

      <div className="row g-4">
        <div className="col-md-6">
          <div className="card p-3 shadow-sm">
            <h5>Attack Distribution</h5>
            <Pie data={pieData} />
          </div>
        </div>
        <div className="col-md-6">
          <div className="card p-3 shadow-sm">
            <h5>Normal vs Attack</h5>
            <Bar data={barData} />
          </div>
        </div>
        <div className="col-12">
          <div className="card p-3 shadow-sm">
            <h5>Model Accuracy Comparison</h5>
            <Bar data={accuracyData} />
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, color }) {
  return (
    <div className="col-md-4">
      <div className={`card text-bg-${color} shadow-sm`}>
        <div className="card-body">
          <h6>{title}</h6>
          <h3>{value}</h3>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
