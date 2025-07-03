# Performance Dashboard

This project provides a small FastAPI backend and a React frontend for exploring membership metrics.

## Setup

### Backend

1. Install dependencies (requires internet access to download packages such as
   `pandas` and `simple_salesforce`):
   ```bash
   pip install -r api/requirements.txt
   ```
2. Start the API:
   ```bash
   uvicorn api.app:app --reload
   ```

The API will run on `http://localhost:8000` by default and exposes `/api/metrics`.

### Frontend

1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

The React application will be available at `http://localhost:5173` and proxies API requests to the backend.

### Building for Production

To build the frontend for production:

```bash
npm run build
```

### Environment Variables

Create a `.env` file in the project root to store any required environment
variables. For example, Salesforce credentials might be configured as:

```dotenv
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_TOKEN=your_security_token
```

The backend will read these variables when connecting to external services.

### Notes

The previous command line interface is no longer emphasized. Use the web UI instead to view metrics.
