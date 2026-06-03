"""
Tests for task endpoints.
"""

import pytest
from datetime import date, datetime, timedelta
from app.models.task import Task, TaskStatus, TaskPriority


class TestTaskCreation:
    """Task creation endpoint tests."""

    def setup_method(self):
        """Create a test event before each test."""
        pass

    def test_create_task_success(self, client, headers_with_token):
        """Test successful task creation."""
        # First create an event
        event_data = {
            "title": "Wedding Event",
            "event_type": "WEDDING",
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=31)),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create a task for the event
        task_data = {
            "title": "Send Invitations",
            "description": "Send out wedding invitations to all guests",
            "priority": "HIGH",
            "category": "Communications",
            "due_date": str(date.today() + timedelta(days=20)),
            "assigned_to": "user-123",
        }

        response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json=task_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["priority"] == task_data["priority"]
        assert data["category"] == task_data["category"]
        assert data["status"] == "PENDING"
        assert data["event_id"] == event_id
        assert "id" in data
        assert "created_at" in data

    def test_create_task_minimal_data(self, client, headers_with_token):
        """Test task creation with minimal required data."""
        # Create an event
        event_data = {
            "title": "Event",
            "event_type": "BIRTHDAY",
            "start_date": str(date.today() + timedelta(days=7)),
            "end_date": str(date.today() + timedelta(days=7)),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create task with minimal data
        task_data = {
            "title": "Buy decorations",
        }

        response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json=task_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy decorations"
        assert data["status"] == "PENDING"
        assert data["priority"] == "MEDIUM"

    def test_create_task_unauthorized(self, client, headers_with_token):
        """Test task creation without authentication."""
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_data = {"title": "Task"}

        response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json=task_data,
        )

        assert response.status_code == 401

    def test_create_task_invalid_event(self, client, headers_with_token):
        """Test task creation for non-existent event."""
        task_data = {"title": "Task"}

        response = client.post(
            "/api/v1/events/00000000-0000-0000-0000-000000000000/tasks",
            json=task_data,
            headers=headers_with_token,
        )

        assert response.status_code == 404


class TestTaskFetching:
    """Task fetching and listing endpoint tests."""

    def test_list_tasks_empty(self, client, headers_with_token):
        """Test listing tasks when event has none."""
        # Create an event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        response = client.get(
            f"/api/v1/events/{event_id}/tasks",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_list_tasks_success(self, client, headers_with_token):
        """Test successful task listing."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create multiple tasks
        for i in range(3):
            task_data = {"title": f"Task {i + 1}"}
            client.post(
                f"/api/v1/events/{event_id}/tasks",
                json=task_data,
                headers=headers_with_token,
            )

        response = client.get(
            f"/api/v1/events/{event_id}/tasks",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

    def test_list_tasks_filter_by_status(self, client, headers_with_token):
        """Test filtering tasks by status."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create tasks
        task1_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task 1"},
            headers=headers_with_token,
        )
        task1_id = task1_response.json()["id"]

        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task 2"},
            headers=headers_with_token,
        )

        # Update first task to IN_PROGRESS
        client.patch(
            f"/api/v1/tasks/{task1_id}/status",
            json={"status": "IN_PROGRESS"},
            headers=headers_with_token,
        )

        # Filter by PENDING
        response = client.get(
            f"/api/v1/events/{event_id}/tasks?status=PENDING",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Task 2"

    def test_list_tasks_filter_by_priority(self, client, headers_with_token):
        """Test filtering tasks by priority."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create tasks with different priorities
        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Urgent Task", "priority": "URGENT"},
            headers=headers_with_token,
        )
        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Low Task", "priority": "LOW"},
            headers=headers_with_token,
        )

        # Filter by URGENT
        response = client.get(
            f"/api/v1/events/{event_id}/tasks?priority=URGENT",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Urgent Task"

    def test_list_tasks_filter_by_category(self, client, headers_with_token):
        """Test filtering tasks by category."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create tasks with categories
        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Food Task", "category": "Catering"},
            headers=headers_with_token,
        )
        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Venue Task", "category": "Venue"},
            headers=headers_with_token,
        )

        # Filter by Catering
        response = client.get(
            f"/api/v1/events/{event_id}/tasks?category=Catering",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["category"] == "Catering"

    def test_list_tasks_search(self, client, headers_with_token):
        """Test searching tasks."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create tasks
        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Buy flowers", "description": "Get wedding flowers"},
            headers=headers_with_token,
        )
        client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Book venue", "description": "Reserve venue"},
            headers=headers_with_token,
        )

        # Search for "flowers"
        response = client.get(
            f"/api/v1/events/{event_id}/tasks?search=flowers",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert "flowers" in data["items"][0]["title"].lower()

    def test_list_tasks_kanban_board(self, client, headers_with_token):
        """Test Kanban board grouping by status."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create tasks
        task1_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task 1"},
            headers=headers_with_token,
        )
        task1_id = task1_response.json()["id"]

        task2_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task 2"},
            headers=headers_with_token,
        )
        task2_id = task2_response.json()["id"]

        # Update statuses
        client.patch(
            f"/api/v1/tasks/{task1_id}/status",
            json={"status": "IN_PROGRESS"},
            headers=headers_with_token,
        )
        client.patch(
            f"/api/v1/tasks/{task2_id}/status",
            json={"status": "COMPLETED"},
            headers=headers_with_token,
        )

        # Get Kanban board
        response = client.get(
            f"/api/v1/events/{event_id}/tasks?group_by_status=true",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["pending"]) == 0
        assert len(data["in_progress"]) == 1
        assert len(data["completed"]) == 1


class TestTaskUpdate:
    """Task update endpoint tests."""

    def test_update_task_success(self, client, headers_with_token):
        """Test successful task update."""
        # Create event and task
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Original Title"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        # Update task
        update_data = {
            "title": "Updated Title",
            "priority": "HIGH",
            "description": "Updated description",
        }
        response = client.patch(
            f"/api/v1/tasks/{task_id}",
            json=update_data,
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["priority"] == "HIGH"
        assert data["description"] == "Updated description"

    def test_update_task_status(self, client, headers_with_token):
        """Test updating only task status."""
        # Create event and task
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        # Update status
        response = client.patch(
            f"/api/v1/tasks/{task_id}/status",
            json={"status": "IN_PROGRESS"},
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "IN_PROGRESS"

    def test_delete_task_success(self, client, headers_with_token):
        """Test successful task deletion."""
        # Create event and task
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task to Delete"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 204

        # Verify task is deleted
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 404


class TestSubtasks:
    """Subtask endpoint tests."""

    def test_create_subtask_success(self, client, headers_with_token):
        """Test successful subtask creation."""
        # Create event and task
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Main Task"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        # Create subtask
        subtask_data = {
            "title": "Subtask 1",
            "description": "First subtask",
        }
        response = client.post(
            f"/api/v1/tasks/{task_id}/subtasks",
            json=subtask_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Subtask 1"
        assert data["description"] == "First subtask"
        assert data["status"] == "PENDING"
        assert data["task_id"] == task_id

    def test_create_multiple_subtasks(self, client, headers_with_token):
        """Test creating multiple subtasks for a task."""
        # Create event and task
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Main Task"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        # Create multiple subtasks
        for i in range(3):
            client.post(
                f"/api/v1/tasks/{task_id}/subtasks",
                json={"title": f"Subtask {i + 1}"},
                headers=headers_with_token,
            )

        # Fetch task to see subtasks
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["subtasks"]) == 3

    def test_update_subtask_success(self, client, headers_with_token):
        """Test successful subtask update."""
        # Create event, task, and subtask
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Main Task"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        subtask_response = client.post(
            f"/api/v1/tasks/{task_id}/subtasks",
            json={"title": "Original Subtask"},
            headers=headers_with_token,
        )
        subtask_id = subtask_response.json()["id"]

        # Update subtask
        update_data = {
            "title": "Updated Subtask",
            "status": "COMPLETED",
        }
        response = client.patch(
            f"/api/v1/subtasks/{subtask_id}",
            json=update_data,
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Subtask"
        assert data["status"] == "COMPLETED"

    def test_user_cannot_access_other_users_tasks(self, client, headers_with_token):
        """Test that users can only access their own tasks."""
        from app.core.security import create_access_token

        # Create event and task as first user
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        task_response = client.post(
            f"/api/v1/events/{event_id}/tasks",
            json={"title": "Task"},
            headers=headers_with_token,
        )
        task_id = task_response.json()["id"]

        # Create a different user's token
        other_token = create_access_token(
            data={
                "sub": "other-user-id",
                "email": "other@example.com",
            }
        )
        other_headers = {
            "Authorization": f"Bearer {other_token}",
            "Content-Type": "application/json",
        }

        # Try to access task as other user
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers=other_headers,
        )

        assert response.status_code == 403
