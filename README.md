# Assignment Submission API

A simple REST API for managing student test and lab assignment submissions, built with FastAPI and designed for DevOps best practices.

## Features

- ✅ Submit test and lab assignments
- ✅ Track submission status and grades
- ✅ **Observability**: Prometheus metrics, structured JSON logging, request tracing
- ✅ **Security**: SAST & DAST scans integrated
- ✅ **Containerized**: Docker & Docker Compose ready
- ✅ **CI/CD**: GitHub Actions pipeline
- ✅ **Kubernetes**: Ready for K8s deployment

## API Endpoints

### 1. Health Check
```bash
GET /health
```
Returns the health status of the API.

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-28T21:53:58.700792"
}
```

---

### 2. Submit Assignment
```bash
POST /assignments/submit
```
Submit a new assignment (test or lab).

**Request Body:**
```json
{
  "student_name": "Alice Johnson",
  "student_id": "S001",
  "assignment_type": "lab",
  "assignment_name": "Lab 1 - Docker Intro",
  "submission_url": "https://github.com/alice/lab1"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/assignments/submit \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Alice Johnson",
    "student_id": "S001",
    "assignment_type": "lab",
    "assignment_name": "Lab 1 - Docker Intro",
    "submission_url": "https://github.com/alice/lab1"
  }'
```

**Response:**
```json
{
  "id": "7d26d66b-f1c9-434a-97f7-80a3522279ef",
  "student_name": "Alice Johnson",
  "student_id": "S001",
  "assignment_type": "lab",
  "assignment_name": "Lab 1 - Docker Intro",
  "submission_url": "https://github.com/alice/lab1",
  "submitted_at": "2025-11-28T21:53:59.769735",
  "grade": null,
  "graded_at": null
}
```

---

### 3. List Assignments
```bash
GET /assignments
```
List all assignments with optional filters.

**Query Parameters:**
- `assignment_type` (optional): Filter by "test" or "lab"
- `student_id` (optional): Filter by student ID

**Examples:**
```bash
# List all assignments
curl http://localhost:8000/assignments

# Filter by type
curl http://localhost:8000/assignments?assignment_type=lab

# Filter by student
curl http://localhost:8000/assignments?student_id=S001
```

---

### 4. Get Assignment
```bash
GET /assignments/{id}
```
Get a specific assignment by ID.

**Example:**
```bash
curl http://localhost:8000/assignments/7d26d66b-f1c9-434a-97f7-80a3522279ef
```

---

### 5. Grade Assignment
```bash
PUT /assignments/{id}/grade
```
Grade an assignment (instructor only).

**Request Body:**
```json
{
  "grade": 95.0
}
```

**Example:**
```bash
curl -X PUT http://localhost:8000/assignments/{id}/grade \
  -H "Content-Type: application/json" \
  -d '{"grade": 95.0}'
```

---

### 6. Metrics (Observability)
```bash
GET /metrics
```
Prometheus-format metrics for monitoring.

**Example:**
```bash
curl http://localhost:8000/metrics
```

**Metrics Exposed:**
- `http_requests_total`: Total number of HTTP requests
- `http_request_duration_seconds`: Request duration histogram
- Python runtime metrics (GC, memory, etc.)

---

## Local Setup

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/devops-assignment-api.git
cd devops-assignment-api
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

5. **Test the API:**
```bash
# Run unit tests
pytest tests/ -v

# Test health endpoint
curl http://localhost:8000/health
```

The API will be available at `http://localhost:8000`

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Docker Usage

### Build Docker Image
```bash
docker build -t assignment-api:v1.0 .
```

### Run Container
```bash
docker run -d -p 8000:8000 --name assignment-api assignment-api:v1.0
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Kubernetes Deployment

### Prerequisites
- minikube or kind installed
- kubectl configured

### Deploy to Kubernetes

1. **Start minikube:**
```bash
minikube start
```

2. **Apply manifests:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

3. **Check deployment:**
```bash
kubectl get pods
kubectl get services
```

4. **Access the service:**
```bash
minikube service assignment-api-service --url
```

---

## Observability

### Structured Logging
Every request is logged in JSON format:
```json
{
  "timestamp": "2025-11-28T21:53:59.123456",
  "request_id": "abc-123-def-456",
  "method": "POST",
  "path": "/assignments/submit",
  "status_code": 200,
  "duration_ms": 15.23
}
```

### Request Tracing
Each request gets a unique `X-Request-ID` header for tracing through the system.

### Metrics
Prometheus metrics available at `/metrics` endpoint:
- Request counts by method, endpoint, and status
- Request duration histograms
- Python runtime metrics

---

## Security

### SAST (Static Application Security Testing)
- Tool: **Bandit**
- Scans source code for security vulnerabilities
- Runs automatically in CI/CD pipeline

### DAST (Dynamic Application Security Testing)
- Tool: **OWASP ZAP**
- Tests running application for vulnerabilities
- Integrated into CI/CD pipeline

---

## CI/CD Pipeline

The GitHub Actions pipeline automatically:
1. ✅ Runs linting and code quality checks
2. ✅ Executes unit tests
3. ✅ Performs SAST scan with Bandit
4. ✅ Builds Docker image
5. ✅ Pushes to Docker Hub
6. ✅ Runs DAST scan with OWASP ZAP
7. ✅ Deploys to Kubernetes (on main branch)

---

## Project Structure

```
DevOps_Project/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container build instructions
├── docker-compose.yml    # Multi-container setup
├── .github/
│   └── workflows/
│       └── cicd.yml      # CI/CD pipeline
├── k8s/
│   ├── deployment.yaml   # Kubernetes deployment
│   └── service.yaml      # Kubernetes service
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Unit tests
├── .gitignore
└── README.md
```

---

## Line Count

The entire backend service (`app.py`) is **~160 lines** including:
- 5 API endpoints
- Observability features (metrics, logging, tracing)
- Request/response models
- Error handling

---

## Development

### Running Tests
```bash
pytest tests/ -v --cov=app
```

### Code Quality
```bash
# Run Bandit security scan
bandit -r app.py

# Run linting
pylint app.py
```

---

## License

MIT License

---

## Author

Built as part of the DevOps Course Project
