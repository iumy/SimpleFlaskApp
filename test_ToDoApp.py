"""Unit tests for the SimpleFlaskApp To-Do Flask application.

These tests exercise the basic web endpoints and in-memory task storage.
The module provides fixtures to create a Flask test client and to ensure
`tasks` is reset between tests.
"""

import pytest
import sys
from ToDoApp import app, tasks

sys.path.insert(0, ".")


@pytest.fixture
def client():
    """Create a test client for the Flask app.

    Uses Flask's `test_client()` context manager and yields a client
    instance to tests. The inner client variable is named `test_client`
    to avoid shadowing the fixture name (prevents W0621 warnings).
    """
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
    # Clean up tasks after each test
    tasks.clear()


@pytest.fixture(autouse=True)
def reset_tasks():
    """Automatically reset tasks before each test"""
    tasks.clear()
    yield
    tasks.clear()


def test_home_page_loads(client):
    """Test that the home page loads successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"To-Do List" in response.data


def test_add_task(client):
    """Test adding a new task"""
    response = client.post("/add", data={"task": "Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Task" in response.data
    assert len(tasks) == 1
    assert tasks[0] == "Test Task"


def test_add_multiple_tasks(client):
    """Test adding multiple tasks"""
    client.post("/add", data={"task": "First Task"}, follow_redirects=True)
    client.post("/add", data={"task": "Second Task"}, follow_redirects=True)
    client.post("/add", data={"task": "Third Task"}, follow_redirects=True)

    assert len(tasks) == 3
    assert tasks[0] == "First Task"
    assert tasks[1] == "Second Task"
    assert tasks[2] == "Third Task"


def test_add_empty_task(client):
    """Test that empty tasks are not added"""
    client.post("/add", data={"task": ""}, follow_redirects=True)
    assert len(tasks) == 0


def test_delete_task(client):
    """Test deleting a task"""
    # Add a task first
    client.post("/add", data={"task": "Task to Delete"}, follow_redirects=True)
    assert len(tasks) == 1

    # Delete the task
    response = client.post("/delete/0", follow_redirects=True)
    assert response.status_code == 200
    assert len(tasks) == 0
    assert b"Task to Delete" not in response.data


def test_delete_middle_task(client):
    """Test deleting a task from the middle of the list"""
    client.post("/add", data={"task": "First"}, follow_redirects=True)
    client.post("/add", data={"task": "Second"}, follow_redirects=True)
    client.post("/add", data={"task": "Third"}, follow_redirects=True)

    # Delete the middle task
    client.post("/delete/1", follow_redirects=True)

    assert len(tasks) == 2
    assert tasks[0] == "First"
    assert tasks[1] == "Third"


def test_delete_invalid_task_id(client):
    """Test deleting with an invalid task ID"""
    client.post("/add", data={"task": "Test Task"}, follow_redirects=True)

    # Try to delete a non-existent task
    response = client.post("/delete/99", follow_redirects=True)
    assert response.status_code == 200
    assert len(tasks) == 1  # Task should still be there


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["tasks_count"] == 0


def test_health_endpoint_with_tasks(client):
    """Test health endpoint returns correct task count"""
    client.post("/add", data={"task": "Task 1"}, follow_redirects=True)
    client.post("/add", data={"task": "Task 2"}, follow_redirects=True)

    response = client.get("/health")
    json_data = response.get_json()
    assert json_data["tasks_count"] == 2


def test_empty_task_list_message(client):
    """Test that empty list shows appropriate message"""
    response = client.get("/")
    assert b"No tasks yet" in response.data


def test_task_persistence_across_requests(client):
    """Test that tasks persist across multiple requests"""
    client.post("/add", data={"task": "Persistent Task"}, follow_redirects=True)

    # Make another request
    response = client.get("/")
    assert b"Persistent Task" in response.data
    assert len(tasks) == 1
