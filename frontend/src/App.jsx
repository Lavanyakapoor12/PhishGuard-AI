
import { useState, useEffect } from "react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

import "./App.css";

// Backend API URL.
const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";


function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Scan history.
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");

  // Search and filter.
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("All");

  // Dashboard statistics.
  const [stats, setStats] = useState({
    total_scans: 0,
    phishing_detected: 0,
    legitimate_urls: 0,
    phishing_rate: 0,
  });

  const [statsLoading, setStatsLoading] = useState(false);
  const [statsError, setStatsError] = useState("");

  // Clear history loading state.
  const [clearLoading, setClearLoading] = useState(false);


  // Fetch scan history.
  async function fetchHistory() {
    setHistoryLoading(true);
    setHistoryError("");

    try {
      const response = await fetch(`${API_URL}/history`);

      if (!response.ok) {
        throw new Error("Unable to fetch scan history.");
      }

      const data = await response.json();

      setHistory(data);

    } catch (err) {
      setHistoryError(
        err.message === "Failed to fetch"
          ? "Cannot connect to the backend."
          : err.message
      );
    } finally {
      setHistoryLoading(false);
    }
  }


  // Fetch dashboard statistics.
  async function fetchStats() {
    setStatsLoading(true);
    setStatsError("");

    try {
      const response = await fetch(`${API_URL}/stats`);

      if (!response.ok) {
        throw new Error("Unable to fetch dashboard statistics.");
      }

      const data = await response.json();

      setStats(data);

    } catch (err) {
      setStatsError(
        err.message === "Failed to fetch"
          ? "Cannot connect to the backend."
          : err.message
      );
    } finally {
      setStatsLoading(false);
    }
  }


  // Refresh dashboard.
  async function refreshDashboard() {
    await Promise.all([
      fetchHistory(),
      fetchStats()
    ]);
  }


  // Load dashboard when application starts.
  useEffect(() => {
    refreshDashboard();
  }, []);


  // Scan URL.
  async function handleScan() {
    if (!url.trim()) {
      setError("Please enter a URL to scan.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          url: url.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail?.[0]?.msg || "Unable to scan this URL."
        );
      }

      setResult(data);

      await refreshDashboard();

    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to the backend. Please check that the server is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }


  // Clear all scan history (admin only).
  async function handleClearHistory() {

    const adminPassword = window.prompt(
      "Enter admin password to clear scan history:"
    );

    // Stop if the user cancels.
    if (adminPassword === null) {
      return;
    }

    if (!adminPassword.trim()) {
      alert("Admin password cannot be empty.");
      return;
    }

    // Ask for final confirmation.
    const confirmed = window.confirm(
      "Are you sure you want to permanently delete ALL scan history?"
    );

    if (!confirmed) {
      return;
    }

    setClearLoading(true);

    try {
      const response = await fetch(`${API_URL}/history`, {
        method: "DELETE",

        headers: {
          "X-Admin-Key": adminPassword,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to clear scan history."
        );
      }

      alert(
        `${data.deleted_count} scan records deleted successfully!`
      );

      // Clear old prediction result and filters.
      setResult(null);
      setSearchTerm("");
      setFilterType("All");

      // Refresh statistics and history.
      await refreshDashboard();

    } catch (err) {
      alert(err.message);
    } finally {
      setClearLoading(false);
    }
  }


  const isPhishing = result?.prediction === "Phishing";


  // Pie chart data.
  const chartData = [
    {
      name: "Phishing",
      value: stats.phishing_detected,
    },
    {
      name: "Legitimate",
      value: stats.legitimate_urls,
    },
  ];

  const chartColors = ["#f04452", "#20c997"];


  // Bar chart data.
  const barChartData = [
    {
      name: "Phishing",
      scans: stats.phishing_detected,
      fill: "#f04452",
    },
    {
      name: "Legitimate",
      scans: stats.legitimate_urls,
      fill: "#20c997",
    },
  ];


  // Search and filter scan history.
  const filteredHistory = history.filter((scan) => {

    const matchesSearch = scan.url
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    const matchesFilter =
      filterType === "All" ||
      scan.prediction === filterType;

    return matchesSearch && matchesFilter;
  });


  return (
    <div className="app">

      {/* Navigation */}
      <nav className="navbar">

        <div className="brand">
          <div className="brand-icon">🛡️</div>

          <span>
            PhishGuard <strong>AI</strong>
          </span>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          AI Engine Ready
        </div>

      </nav>


      <main className="main-content">

        {/* Hero Section */}
        <section className="hero">

          <div className="eyebrow">
            <span>✦</span> AI-POWERED CYBERSECURITY
          </div>

          <h1>
            Stay One Step Ahead of
            <span> Phishing Attacks.</span>
          </h1>

          <p>
            Protect yourself from malicious websites.
            Scan any URL with our machine learning-powered
            phishing detection system.
          </p>

        </section>


        {/* URL Scanner */}
        <section className="scanner-card">

          <div className="scanner-heading">

            <div>
              <h2>Website Security Scanner</h2>
              <p>Enter a URL below to analyse its security.</p>
            </div>

            <div className="scanner-icon">⌕</div>

          </div>


          <label htmlFor="url-input">WEBSITE URL</label>


          <div className="input-wrapper">

            <span className="input-icon">🔗</span>

            <input
              id="url-input"
              type="url"
              placeholder="https://example.com"
              value={url}

              onChange={(e) => {
                setUrl(e.target.value);
                setError("");
                setResult(null);
              }}

              onKeyDown={(e) => {
                if (e.key === "Enter" && !loading) {
                  handleScan();
                }
              }}
            />


            <button
              className="scan-button"
              onClick={handleScan}
              disabled={loading}
            >
              {loading ? "Scanning..." : "Scan URL →"}
            </button>

          </div>


          <div className="scanner-hint">
            <span>ⓘ</span>
            We analyse the URL text only. We do not open the website.
          </div>


          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}


          {loading && (
            <div className="loading-message">
              <span className="loader"></span>
              Analysing URL with PhishGuard AI...
            </div>
          )}


          {/* Prediction Result */}
          {result && (

            <div
              className={`result-card ${
                isPhishing ? "danger" : "safe"
              }`}
            >

              <div className="result-top">

                <div>
                  <div className="result-label">SCAN RESULT</div>

                  <h3>
                    {isPhishing
                      ? "⚠️ Phishing Detected"
                      : "✓ Classified as Legitimate"}
                  </h3>
                </div>

                <span className="result-badge">
                  {result.prediction.toUpperCase()}
                </span>

              </div>


              <div className="result-url">
                <span>Scanned URL</span>
                <p>{result.url}</p>
              </div>


              <div className="probability-section">

                <div className="probability-heading">
                  <span>Estimated phishing probability</span>

                  <strong>
                    {result.phishing_probability}%
                  </strong>
                </div>


                <div className="progress-track">

                  <div
                    className="progress-fill"
                    style={{
                      width: `${result.phishing_probability}%`,
                    }}
                  ></div>

                </div>

              </div>


              <p className="result-disclaimer">
                This is an AI model estimate, not a guarantee of website
                safety. Avoid entering sensitive information on suspicious
                websites.
              </p>

            </div>

          )}

        </section>


        {/* Security Overview */}
        <section className="analytics-section">

          <div className="analytics-heading">

            <div>
              <h2>Security Overview</h2>
              <p>Scanning statistics from your database.</p>
            </div>


            <button
              className="history-refresh"
              onClick={refreshDashboard}
              disabled={historyLoading || statsLoading}
            >
              {historyLoading || statsLoading
                ? "Loading..."
                : "↻ Refresh Dashboard"}
            </button>

          </div>


          {statsError && (
            <div className="error-message">
              ⚠️ {statsError}
            </div>
          )}


          {/* Analytics Cards */}
          <div className="analytics-grid">

            <div className="analytics-card">
              <div className="analytics-icon purple">⌕</div>
              <p>Total Scans</p>
              <h3>{statsLoading ? "..." : stats.total_scans}</h3>
            </div>


            <div className="analytics-card">
              <div className="analytics-icon red">⚠</div>
              <p>Phishing Detected</p>
              <h3>
                {statsLoading ? "..." : stats.phishing_detected}
              </h3>
            </div>


            <div className="analytics-card">
              <div className="analytics-icon green">✓</div>
              <p>Legitimate URLs</p>
              <h3>
                {statsLoading ? "..." : stats.legitimate_urls}
              </h3>
            </div>


            <div className="analytics-card">
              <div className="analytics-icon blue">◈</div>
              <p>Phishing Rate</p>
              <h3>
                {statsLoading
                  ? "..."
                  : `${stats.phishing_rate}%`}
              </h3>
            </div>

          </div>


          {/* Pie Chart */}
          <div className="chart-card">

            <div className="chart-heading">
              <h2>URL Security Distribution</h2>
              <p>Phishing vs Legitimate URLs</p>
            </div>


            {statsLoading ? (

              <p className="chart-message">
                Loading chart...
              </p>

            ) : stats.total_scans === 0 ? (

              <p className="chart-message">
                No scan data available. Scan your first URL to see the chart.
              </p>

            ) : (

              <>

                <div className="chart-container">

                  <ResponsiveContainer width="100%" height={300}>

                    <PieChart>

                      <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={65}
                        outerRadius={105}
                        paddingAngle={4}
                        dataKey="value"
                        nameKey="name"
                      >

                        {chartData.map((entry, index) => (
                          <Cell
                            key={entry.name}
                            fill={chartColors[index]}
                          />
                        ))}

                      </Pie>


                      <Tooltip
                        formatter={(value, name) => [
                          `${value} URLs`,
                          name,
                        ]}
                      />

                      <Legend verticalAlign="bottom" />

                    </PieChart>

                  </ResponsiveContainer>

                </div>


                <div className="chart-percentages">

                  <p>
                    <span className="percentage-dot phishing-dot"></span>
                    Phishing:{" "}
                    {(
                      (stats.phishing_detected / stats.total_scans) * 100
                    ).toFixed(1)}%
                  </p>


                  <p>
                    <span className="percentage-dot legitimate-dot"></span>
                    Legitimate:{" "}
                    {(
                      (stats.legitimate_urls / stats.total_scans) * 100
                    ).toFixed(1)}%
                  </p>

                </div>

              </>

            )}

          </div>


          {/* Bar Chart */}
          <div className="chart-card">

            <div className="chart-heading">
              <h2>Scan Activity Comparison</h2>
              <p>Number of phishing and legitimate URLs detected.</p>
            </div>


            {statsLoading ? (

              <p className="chart-message">
                Loading chart...
              </p>

            ) : stats.total_scans === 0 ? (

              <p className="chart-message">
                No scan data available. Scan your first URL to see the chart.
              </p>

            ) : (

              <div className="chart-container">

                <ResponsiveContainer width="100%" height={300}>

                  <BarChart
                    data={barChartData}
                    margin={{
                      top: 20,
                      right: 20,
                      left: 0,
                      bottom: 10,
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="#374151"
                    />

                    <XAxis dataKey="name" stroke="#9ca3af" />

                    <YAxis
                      allowDecimals={false}
                      stroke="#9ca3af"
                    />

                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#1f2937",
                        border: "1px solid #374151",
                        borderRadius: "8px",
                        color: "#ffffff",
                      }}
                    />


                    <Bar
                      dataKey="scans"
                      name="Number of scans"
                      radius={[8, 8, 0, 0]}
                    >

                      {barChartData.map((entry) => (
                        <Cell
                          key={entry.name}
                          fill={entry.fill}
                        />
                      ))}

                    </Bar>

                  </BarChart>

                </ResponsiveContainer>

              </div>

            )}

          </div>

        </section>


        {/* Scan History */}
        <section className="history-section">

          <div className="history-heading">

            <div>
              <h2>Recent Scan History</h2>
              <p>Your previously scanned URLs and their results.</p>
            </div>


            {/* Refresh and Clear History Buttons */}
            <div className="history-actions">

              <button
                className="history-refresh"
                onClick={fetchHistory}
                disabled={historyLoading || clearLoading}
              >
                {historyLoading ? "Loading..." : "↻ Refresh"}
              </button>


              <button
                className="clear-history-button"
                onClick={handleClearHistory}
                disabled={historyLoading || clearLoading}
              >
                {clearLoading
                  ? "Clearing..."
                  : "🗑 Clear History"}
              </button>

            </div>

          </div>


          {historyError && (
            <div className="error-message">
              ⚠️ {historyError}
            </div>
          )}


          {/* Search and Filter */}
          <div className="history-controls">

            <div className="search-box">

              <span>🔍</span>

              <input
                type="text"
                placeholder="Search scanned URLs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />

            </div>


            <select
              className="filter-select"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >

              <option value="All">All Scans</option>
              <option value="Phishing">Phishing Only</option>
              <option value="Legitimate">Legitimate Only</option>

            </select>

          </div>


          <div className="history-result-count">
            Showing {filteredHistory.length} of {history.length} scans
          </div>


          {historyLoading && history.length === 0 && (
            <p className="history-message">
              Loading scan history...
            </p>
          )}


          {!historyLoading && filteredHistory.length === 0 && (

            <p className="history-message">
              {history.length === 0
                ? "No scans available yet. Scan your first URL!"
                : "No matching scans found. Try another search or filter."}
            </p>

          )}


          {filteredHistory.length > 0 && (

            <div className="history-table-wrapper">

              <table className="history-table">

                <thead>

                  <tr>
                    <th>ID</th>
                    <th>Scanned URL</th>
                    <th>Prediction</th>
                    <th>Phishing Probability</th>
                    <th>Scan Time</th>
                  </tr>

                </thead>


                <tbody>

                  {filteredHistory.map((scan) => (

                    <tr key={scan.id}>

                      <td>#{scan.id}</td>

                      <td className="history-url">
                        {scan.url}
                      </td>


                      <td>

                        <span
                          className={`history-badge ${
                            scan.prediction === "Phishing"
                              ? "history-danger"
                              : "history-safe"
                          }`}
                        >
                          {scan.prediction}
                        </span>

                      </td>


                      <td>
                        {scan.phishing_probability}%
                      </td>


                      <td>
                        {new Date(scan.created_at).toLocaleString()}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* Features */}
        <section className="features">

          <div className="feature-card">
            <div className="feature-icon purple">✦</div>

            <h3>AI-Powered Detection</h3>

            <p>
              Machine learning analyses URL patterns to identify
              possible phishing links.
            </p>
          </div>


          <div className="feature-card">
            <div className="feature-icon green">⌁</div>

            <h3>Fast URL Analysis</h3>

            <p>
              Submit a URL and receive a prediction from our trained AI model.
            </p>
          </div>


          <div className="feature-card">
            <div className="feature-icon blue">◈</div>

            <h3>Security Awareness</h3>

            <p>
              Get a clear warning when a URL is classified as potentially malicious.
            </p>
          </div>

        </section>


        {/* Footer */}
        <footer>

          <div>🛡️ PhishGuard AI</div>

          <p>Built for a safer digital world.</p>

        </footer>

      </main>

    </div>
  );
}

export default App;
