"""
Unit tests for Assignment Submission API
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_submit_assignment():
    """Test assignment submission"""
    assignment = {
        "student_name": "John Doe",
        "student_id": "S12345",
        "assignment_type": "lab",
        "assignment_name": "Lab 1 - Docker Basics",
        "submission_url": "https://github.com/johndoe/lab1"
    }
    response = client.post("/assignments/submit", json=assignment)
    assert response.status_code == 200
    data = response.json()
    assert data["student_name"] == "John Doe"
    assert "id" in data
    assert "submitted_at" in data
    return data["id"]

def test_list_assignments():
    """Test listing assignments"""
    # First submit an assignment
    test_submit_assignment()
    
    # Then list all
    response = client.get("/assignments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_grade_assignment():
    """Test grading an assignment"""
    # First submit
    assignment_id = test_submit_assignment()
    
    # Then grade
    grade_data = {"grade": 95.0}
    response = client.put(f"/assignments/{assignment_id}/grade", json=grade_data)
    assert response.status_code == 200
    assert response.json()["grade"] == 95.0
    assert "graded_at" in response.json()

def test_get_nonexistent_assignment():
    """Test getting an assignment that doesn't exist"""
    response = client.get("/assignments/nonexistent-id")
    assert response.status_code == 404
