# Cloud Marketplace Cost Comparator

A modern web application that compares compute pricing across AWS, Azure, and GCP cloud providers. Built with FastAPI, React, and Docker.

## Features

- Real-time price comparison for compute instances
- Support for on-demand, spot, and reserved instance pricing
- Interactive charts and visualizations using Recharts
- Modern UI with Material-UI and dark mode support
- Responsive design for all screen sizes
- Redis caching for improved performance
- Dockerized deployment for easy setup

## Prerequisites

- Docker and Docker Compose
- Cloud provider credentials:
  - AWS: Access Key ID and Secret Access Key
  - GCP: Project ID and API Key
  - Azure: No credentials required for retail pricing API

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cloud-marketplace-cost-comparator.git
   cd cloud-marketplace-cost-comparator
   ```

2. Create a `.env` file in the root directory with your cloud credentials:
   ```env
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   GCP_PROJECT_ID=your_gcp_project_id
   GCP_API_KEY=your_gcp_api_key
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost
   - Backend API docs: http://localhost:8000/docs

## Architecture

### Backend (FastAPI)

- FastAPI for high-performance async API
- Modular design with separate providers for each cloud
- Redis caching for improved response times
- Pydantic models for data validation

### Frontend (React)

- React with TypeScript for type safety
- Material-UI for consistent design
- Recharts for interactive visualizations
- Dark mode support
- Responsive layout

### Infrastructure

- Docker containers for all services
- Redis for caching
- Nginx for serving frontend and proxying API requests
- Docker Compose for orchestration

## API Endpoints

- `GET /api/v1/compute/prices`: Get compute prices across providers
- `GET /api/v1/regions`: List available regions
- `GET /api/v1/instance-types`: List available instance types

## Development

### Backend Development

1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Development

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Material-UI](https://mui.com/)
- [Recharts](https://recharts.org/)
- Cloud Provider Documentation:
  - [AWS Pricing API](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html)
  - [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices)
  - [GCP Cloud Billing API](https://cloud.google.com/billing/docs/reference/rest) 