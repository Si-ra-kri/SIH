import React, { useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, ImageOverlay } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';

// A simple chart component
const SimpleBarChart = ({ data }) => (
  <div className="chart">
    {data.map((item, index) => (
      <div className="bar-container" key={index}>
        <div className="bar-label">{item.label}</div>
        <div className="bar" style={{ width: `${item.value}%`, backgroundColor: item.color }}>
          {item.value.toFixed(1)}%
        </div>
      </div>
    ))}
  </div>
);

// The GeoJSON data is hardcoded to prevent file errors
const claimPolygonData = {
  "type": "FeatureCollection", "features": [ { "type": "Feature", "properties": {}, "geometry": { "type": "Polygon", "coordinates": [ [ [79.0, 23.0], [79.1, 23.0], [79.1, 23.1], [79.0, 23.1], [79.0, 23.0] ] ] } } ]
};


function App() {
  const [ocrData, setOcrData] = useState(null);
  const [dashboardStats, setDashboardStats] = useState({
    claimsProcessed: 0,
    anomaliesFlagged: 0,
    forestPercent: 0,
  });

  const imageBounds = [[23.0, 79.0], [23.1, 79.1]];
  const mapCenter = [23.05, 79.05];

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/process_claim/', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      // THIS IS THE NEW, IMPORTANT PART
      // Check if the backend sent an error message
      if (data.error) {
        alert(`Backend Error: ${data.error}`); // Show the specific error from Python
        console.error("Backend Error:", data.error);
        return; // Stop here to prevent the crash
      }

      setOcrData(data);

      setDashboardStats({
        claimsProcessed: 1,
        anomaliesFlagged: data.analysis.flagged_as_anomaly ? 1 : 0,
        forestPercent: data.analysis.forest_cover_percent,
      });

    } catch (error) {
      // This catches network errors
      console.error("Error uploading file:", error);
      alert("Network error processing file. See console for details.");
    }
  };

  const forestData = [
      { label: 'Forest', value: dashboardStats.forestPercent, color: '#2E7D32' },
      { label: 'Non-Forest', value: 100 - dashboardStats.forestPercent, color: '#E8F5E9' },
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered FRA Claim Monitoring</h1>
      </header>
      <main className="container">
        <div className="left-panel">
          <h2>1. Upload Claim Document</h2>
          <input type="file" onChange={handleFileUpload} accept="image/png, image/jpeg" />

          {ocrData && !ocrData.error && ( // Only show if ocrData exists AND there is no error
            <div className="ocr-output">
              <h3>Extracted Details</h3>
              <p><strong>Name:</strong> {ocrData.name}</p>
              <p><strong>Village:</strong> {ocrData.village}</p>
              <p><strong>Area:</strong> {ocrData.area}</p>
              <p><strong>Anomaly?:</strong> {ocrData.analysis?.flagged_as_anomaly ? 'Yes 🚩' : 'No ✅'}</p>
            </div>
          )}

          <div className="dashboard">
            <h2>Dashboard</h2>
            <div className="stat-box">
              <div className="stat-value">{dashboardStats.claimsProcessed}</div>
              <div className="stat-label">Claims Processed</div>
            </div>
             <div className="stat-box">
              <div className="stat-value">{dashboardStats.anomaliesFlagged}</div>
              <div className="stat-label">Anomalies Flagged</div>
            </div>
            <h3>Land Cover Analysis</h3>
            <SimpleBarChart data={forestData} />
          </div>
        </div>
        <div className="right-panel">
          <MapContainer center={mapCenter} zoom={13} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <GeoJSON data={claimPolygonData} style={() => ({ color: 'blue', weight: 3 })} />

            {ocrData && ocrData.analysis && ( // Only show overlay if analysis data exists
              <ImageOverlay
                url={ocrData.analysis.change_map_url}
                bounds={imageBounds}
                opacity={0.7}
              />
            )}
          </MapContainer>
        </div>
      </main>
    </div>
  );
}

export default App;