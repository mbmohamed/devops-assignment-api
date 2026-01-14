"""
Student Assignment Submission API
A simple REST API for managing test and lab assignment submissions
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime
import time
import logging
import json
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import uuid

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

app = FastAPI(title="Assignment Submission API", version="1.0.0")

# In-memory database (for simplicity)
assignments_db = {}

# Models
class AssignmentSubmission(BaseModel):
    student_name: str
    student_id: str
    assignment_type: str  # Intentional mistake: removed Literal["test", "lab"]
    assignment_name: str
    submission_url: str
    submitted_at: Optional[str] = None

class AssignmentSubmission(BaseModel):
    student_name: str
    student_id: str
    assignment_type: Literal["test", "lab"]  # Fixed: restored validation
    assignment_name: str
    submission_url: str
    submitted_at: Optional[str] = None

class GradeSubmission(BaseModel):
    grade: float  # 0-100

# Middleware for logging and metrics
@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Structured logging (Fixed)
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": round(duration * 1000, 2)
    }
    logger.info(json.dumps(log_data))
    
    # Update metrics
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_DURATION.observe(duration)
    
    # Add request ID to response header
    response.headers["X-Request-ID"] = request_id
    return response

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Assignment Submission API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/assignments/submit", response_model=AssignmentResponse)
def submit_assignment(submission: AssignmentSubmission):
    """Submit a new assignment (test or lab)"""
    assignment_id = str(uuid.uuid4())
    submitted_at = datetime.utcnow().isoformat()
    
    assignment_data = {
        "id": assignment_id,
        **submission.dict(),
        "submitted_at": submitted_at,
        "grade": None,
        "graded_at": None
    }
    
    assignments_db[assignment_id] = assignment_data
    return assignment_data

@app.get("/assignments", response_model=List[AssignmentResponse])
def list_assignments(
    assignment_type: Optional[Literal["test", "lab"]] = None,
    student_id: Optional[str] = None
):
    """List all assignments with optional filters"""
    results = list(assignments_db.values())
    
    # Filter by type
    if assignment_type:
        results = [a for a in results if a["assignment_type"] == assignment_type]
    
    # Filter by student
    if student_id:
        results = [a for a in results if a["student_id"] == student_id]
    
    return results

@app.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(assignment_id: str):
    """Get a specific assignment submission"""
    if assignment_id not in assignments_db:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignments_db[assignment_id]

@app.put("/assignments/{assignment_id}/grade", response_model=AssignmentResponse)
def grade_assignment(assignment_id: str, grade_data: GradeSubmission):
    """Grade an assignment (instructor only)"""
    if assignment_id not in assignments_db:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if not 0 <= grade_data.grade <= 100:
        raise HTTPException(status_code=400, detail="Grade must be between 0 and 100")
    
    assignments_db[assignment_id]["grade"] = grade_data.grade
    assignments_db[assignment_id]["graded_at"] = datetime.utcnow().isoformat()
    
    return assignments_db[assignment_id]

@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: str):
    """Delete an assignment (intentional mistake: no error handling)"""
    if assignment_id not in assignments_db:
        raise HTTPException(status_code=404, detail="Assignment not found")
    del assignments_db[assignment_id]
    return {"message": "Assignment deleted"}