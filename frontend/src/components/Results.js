import React, { useEffect, useState } from "react";
import api from "../services/api";

function Results() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      const response = await api.get("/results");
      setResults(response.data.results || []);
    };
    fetchResults();
  }, []);

  return (
    <div className="container">
      <h2 className="mb-4">Latest Prediction Results</h2>
      <div className="table-responsive">
        <table className="table table-striped table-bordered">
          <thead className="table-dark">
            <tr>
              <th>Connection ID</th>
              <th>Protocol</th>
              <th>Service</th>
              <th>Prediction Result</th>
            </tr>
          </thead>
          <tbody>
            {results.length > 0 ? (
              results.map((row) => (
                <tr key={row.connection_id}>
                  <td>{row.connection_id}</td>
                  <td>{row.protocol}</td>
                  <td>{row.service}</td>
                  <td>
                    <span className={`badge ${row.prediction === "Normal" ? "bg-success" : "bg-danger"}`}>
                      {row.prediction}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center">
                  No results yet. Upload a CSV file first.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Results;
