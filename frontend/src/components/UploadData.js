import React, { useState } from "react";
import api from "../services/api";

function UploadData() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadFile = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a CSV file before uploading.");
      return;
    }

    setLoading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(`${response.data.message}. ${response.data.results.length} records processed.`);
    } catch (err) {
      setMessage(err.response?.data?.message || "Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2 className="mb-4">Upload Network Traffic CSV</h2>
      <div className="card p-4 shadow-sm">
        <form onSubmit={uploadFile}>
          <input className="form-control mb-3" type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
          <button className="btn btn-primary" disabled={loading}>
            {loading ? "Analyzing..." : "Upload and Analyze"}
          </button>
        </form>
        {message && <div className="alert alert-secondary mt-3 mb-0">{message}</div>}
      </div>
    </div>
  );
}

export default UploadData;
