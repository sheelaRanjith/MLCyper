import React, { useState } from "react";
import { BrowserRouter, Navigate, Route, Routes, Link } from "react-router-dom";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import UploadData from "./components/UploadData";
import Results from "./components/Results";
import Logs from "./components/Logs";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <BrowserRouter>
      {!token ? (
        <Routes>
          <Route path="*" element={<Login setToken={setToken} />} />
        </Routes>
      ) : (
        <div className="container-fluid">
          <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4 px-3 rounded-bottom">
            <span className="navbar-brand">Cyber IDS</span>
            <div className="navbar-nav gap-2">
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/upload" className="nav-link">Upload Data</Link>
              <Link to="/results" className="nav-link">Results</Link>
              <Link to="/logs" className="nav-link">Logs</Link>
            </div>
            <button onClick={handleLogout} className="btn btn-outline-light ms-auto">
              Logout
            </button>
          </nav>

          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/upload" element={<UploadData />} />
            <Route path="/results" element={<Results />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="*" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      )}
    </BrowserRouter>
  );
}

export default App;
