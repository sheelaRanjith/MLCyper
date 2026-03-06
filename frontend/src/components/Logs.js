import React, { useEffect, useState } from "react";
import api from "../services/api";

function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const response = await api.get("/logs");
      setLogs(response.data.logs || []);
    };
    fetchLogs();
  }, []);

  return (
    <div className="container">
      <h2 className="mb-4">Intrusion Detection Logs</h2>
      <div className="table-responsive">
        <table className="table table-hover table-bordered">
          <thead className="table-secondary">
            <tr>
              <th>Timestamp</th>
              <th>Connection ID</th>
              <th>Protocol</th>
              <th>Service</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            {logs.length > 0 ? (
              logs.map((row, index) => (
                <tr key={`${row.connection_id}-${index}`}>
                  <td>{row.timestamp}</td>
                  <td>{row.connection_id}</td>
                  <td>{row.protocol}</td>
                  <td>{row.service}</td>
                  <td>{row.prediction}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center">No logs available yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Logs;
