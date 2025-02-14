import React from 'react';
import '../styles/Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard">
      <h1>Cloud Cost Comparison Dashboard</h1>
      <div className="cost-cards">
        <div className="cost-card aws">
          <h2>AWS</h2>
          <p>Loading costs...</p>
        </div>
        <div className="cost-card azure">
          <h2>Azure</h2>
          <p>Loading costs...</p>
        </div>
        <div className="cost-card gcp">
          <h2>GCP</h2>
          <p>Loading costs...</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 