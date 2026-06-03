"""
Tests for event endpoints.
"""

import pytest
from datetime import date, datetime, timedelta
from app.models.event import Event, EventType, EventStatus


class TestEventCreation:
    """Event creation endpoint tests."""

    def test_create_event_success(self, client, headers_with_token):
        """Test successful event creation."""
        event_data = {
            "title": "Summer Wedding",
            "description": "A beautiful beach wedding",
            "event_type": "WEDDING",
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=31)),
            "location": "Maldives",
            "estimated_guests": 150,
            "budget": 50000.00,
            "currency": "USD",
            "thumbnail_url": "https://example.com/wedding.jpg",
        }

        response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == event_data["title"]
        assert data["description"] == event_data["description"]
        assert data["event_type"] == event_data["event_type"]
        assert data["status"] == "PLANNING"
        assert data["location"] == event_data["location"]
        assert data["estimated_guests"] == event_data["estimated_guests"]
        assert float(data["budget"]) == event_data["budget"]
        assert data["currency"] == event_data["currency"]
        assert "id" in data
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_event_without_auth(self, client):
        """Test event creation without authentication."""
        event_data = {
            "title": "Birthday Party",
            "event_type": "BIRTHDAY",
            "start_date": str(date.today() + timedelta(days=7)),
            "end_date": str(date.today() + timedelta(days=7)),
        }

        response = client.post(
            "/api/v1/events",
            json=event_data,
        )

        assert response.status_code == 401

    def test_create_event_invalid_dates(self, client, headers_with_token):
        """Test event creation with end_date before start_date."""
        event_data = {
            "title": "Invalid Event",
            "event_type": "CORPORATE_EVENT",
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=20)),  # Before start_date
        }

        response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )

        assert response.status_code == 422

    def test_create_event_missing_required_fields(self, client, headers_with_token):
        """Test event creation with missing required fields."""
        event_data = {
            "title": "Incomplete Event",
            # Missing event_type, start_date, end_date
        }

        response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )

        assert response.status_code == 422

    def test_create_event_invalid_event_type(self, client, headers_with_token):
        """Test event creation with invalid event type."""
        event_data = {
            "title": "Invalid Type Event",
            "event_type": "INVALID_TYPE",
            "start_date": str(date.today() + timedelta(days=7)),
            "end_date": str(date.today() + timedelta(days=7)),
        }

        response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )

        assert response.status_code == 422

    def test_create_event_minimal_data(self, client, headers_with_token):
        """Test event creation with minimal required data."""
        event_data = {
            "title": "Minimal Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
        }

        response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Event"
        assert data["status"] == "PLANNING"
        assert data["description"] is None
        assert data["location"] is None


class TestEventFetching:
    """Event fetching endpoint tests."""

    def test_get_user_events_empty(self, client, headers_with_token):
        """Test fetching events when user has none."""
        response = client.get(
            "/api/v1/events",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
        assert data["skip"] == 0
        assert data["limit"] == 10

    def test_get_user_events_success(self, client, headers_with_token):
        """Test fetching user's events."""
        # Create multiple events
        for i in range(3):
            event_data = {
                "title": f"Event {i + 1}",
                "event_type": "WEDDING" if i % 2 == 0 else "BIRTHDAY",
                "start_date": str(date.today() + timedelta(days=i + 1)),
                "end_date": str(date.today() + timedelta(days=i + 2)),
            }
            client.post(
                "/api/v1/events",
                json=event_data,
                headers=headers_with_token,
            )

        response = client.get(
            "/api/v1/events",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3
        # Events should be ordered by creation date (newest first)
        assert data["items"][0]["title"] == "Event 3"
        assert data["items"][1]["title"] == "Event 2"
        assert data["items"][2]["title"] == "Event 1"

    def test_get_user_events_pagination(self, client, headers_with_token):
        """Test event pagination."""
        # Create 15 events
        for i in range(15):
            event_data = {
                "title": f"Event {i + 1}",
                "event_type": "OTHER",
                "start_date": str(date.today() + timedelta(days=1)),
                "end_date": str(date.today() + timedelta(days=2)),
            }
            client.post(
                "/api/v1/events",
                json=event_data,
                headers=headers_with_token,
            )

        # Get first page (limit 10)
        response = client.get(
            "/api/v1/events?skip=0&limit=10",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert data["skip"] == 0
        assert data["limit"] == 10
        assert len(data["items"]) == 10

        # Get second page (limit 10, skip 10)
        response = client.get(
            "/api/v1/events?skip=10&limit=10",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert data["skip"] == 10
        assert len(data["items"]) == 5

    def test_get_user_events_search_by_title(self, client, headers_with_token):
        """Test event search by title."""
        # Create events with different titles
        events_to_create = [
            {"title": "Summer Wedding", "event_type": "WEDDING"},
            {"title": "Birthday Bash", "event_type": "BIRTHDAY"},
            {"title": "Summer Conference", "event_type": "CONFERENCE"},
        ]

        for event_data in events_to_create:
            event_data["start_date"] = str(date.today() + timedelta(days=1))
            event_data["end_date"] = str(date.today() + timedelta(days=2))
            client.post(
                "/api/v1/events",
                json=event_data,
                headers=headers_with_token,
            )

        # Search for "Summer"
        response = client.get(
            "/api/v1/events?search=Summer",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2
        titles = [item["title"] for item in data["items"]]
        assert "Summer Wedding" in titles
        assert "Summer Conference" in titles

    def test_get_user_events_filter_by_type(self, client, headers_with_token):
        """Test event filtering by type."""
        # Create events of different types
        for event_type in ["WEDDING", "WEDDING", "BIRTHDAY", "CONFERENCE"]:
            event_data = {
                "title": f"{event_type} Event",
                "event_type": event_type,
                "start_date": str(date.today() + timedelta(days=1)),
                "end_date": str(date.today() + timedelta(days=2)),
            }
            client.post(
                "/api/v1/events",
                json=event_data,
                headers=headers_with_token,
            )

        # Filter by WEDDING
        response = client.get(
            "/api/v1/events?event_type=WEDDING",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2
        assert all(item["event_type"] == "WEDDING" for item in data["items"])

    def test_get_user_events_filter_by_status(self, client, headers_with_token):
        """Test event filtering by status."""
        # Create an event
        event_data = {
            "title": "Status Test Event",
            "event_type": "OTHER",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=2)),
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = create_response.json()["id"]

        # Update event status to ACTIVE
        update_data = {"status": "ACTIVE"}
        client.patch(
            f"/api/v1/events/{event_id}",
            json=update_data,
            headers=headers_with_token,
        )

        # Filter by PLANNING status
        response = client.get(
            "/api/v1/events?status=PLANNING",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

        # Filter by ACTIVE status
        response = client.get(
            "/api/v1/events?status=ACTIVE",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    def test_get_user_events_without_auth(self, client):
        """Test fetching events without authentication."""
        response = client.get("/api/v1/events")

        assert response.status_code == 401

    def test_get_user_does_not_see_other_users_events(self, client, headers_with_token, mock_user_token):
        """Test that users can only see their own events."""
        from app.core.security import create_access_token

        # Create event as first user
        event_data = {
            "title": "Private Event",
            "event_type": "WEDDING",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=2)),
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )

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

        # Try to fetch events as the other user
        response = client.get(
            "/api/v1/events",
            headers=other_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0  # Other user shouldn't see the first user's events


class TestEventDetails:
    """Event detail endpoint tests."""

    def test_get_event_by_id_success(self, client, headers_with_token):
        """Test fetching a specific event."""
        # Create an event
        event_data = {
            "title": "Test Event",
            "event_type": "CONFERENCE",
            "start_date": str(date.today() + timedelta(days=10)),
            "end_date": str(date.today() + timedelta(days=12)),
            "location": "Convention Center",
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = create_response.json()["id"]

        # Fetch the event
        response = client.get(
            f"/api/v1/events/{event_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == event_id
        assert data["title"] == "Test Event"
        assert data["location"] == "Convention Center"

    def test_get_event_not_found(self, client, headers_with_token):
        """Test fetching non-existent event."""
        response = client.get(
            "/api/v1/events/invalid-uuid-12345",
            headers=headers_with_token,
        )

        assert response.status_code == 404

    def test_get_event_unauthorized(self, client, headers_with_token, mock_user_token):
        """Test unauthorized event access."""
        from app.core.security import create_access_token

        # Create event as first user
        event_data = {
            "title": "Secret Event",
            "event_type": "WEDDING",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=2)),
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = create_response.json()["id"]

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

        # Try to access event as other user
        response = client.get(
            f"/api/v1/events/{event_id}",
            headers=other_headers,
        )

        assert response.status_code == 403


class TestEventUpdate:
    """Event update endpoint tests."""

    def test_update_event_success(self, client, headers_with_token):
        """Test successful event update."""
        # Create an event
        event_data = {
            "title": "Original Title",
            "event_type": "BIRTHDAY",
            "start_date": str(date.today() + timedelta(days=7)),
            "end_date": str(date.today() + timedelta(days=7)),
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = create_response.json()["id"]

        # Update the event
        update_data = {
            "title": "Updated Title",
            "status": "ACTIVE",
            "budget": 5000.00,
        }
        response = client.patch(
            f"/api/v1/events/{event_id}",
            json=update_data,
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "ACTIVE"
        assert float(data["budget"]) == 5000.00

    def test_update_event_not_found(self, client, headers_with_token):
        """Test updating non-existent event."""
        response = client.patch(
            "/api/v1/events/invalid-uuid-12345",
            json={"title": "Updated Title"},
            headers=headers_with_token,
        )

        assert response.status_code == 404

    def test_delete_event_success(self, client, headers_with_token):
        """Test successful event deletion."""
        # Create an event
        event_data = {
            "title": "Event to Delete",
            "event_type": "OTHER",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=2)),
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = create_response.json()["id"]

        # Delete the event
        response = client.delete(
            f"/api/v1/events/{event_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 204

        # Verify event is deleted (soft delete, should not be accessible)
        response = client.get(
            f"/api/v1/events/{event_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 404


class TestEventDashboard:
    """Event dashboard endpoint tests."""

    def test_get_event_dashboard_success(self, client, headers_with_token):
        """Test fetching event dashboard."""
        # Create an event
        event_data = {
            "title": "Dashboard Test Event",
            "event_type": "WEDDING",
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=31)),
            "budget": 50000.00,
            "estimated_guests": 200,
        }
        create_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = create_response.json()["id"]

        # Get dashboard
        response = client.get(
            f"/api/v1/events/{event_id}/dashboard",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()

        # Check event data
        assert data["event"]["id"] == event_id
        assert data["event"]["title"] == "Dashboard Test Event"

        # Check stats
        assert data["tasks_total"] == 0
        assert data["tasks_completed"] == 0
        assert data["tasks_completion_percentage"] == 0
        assert float(data["budget_total"]) == 50000.00
        assert float(data["budget_spent"]) == 0
        assert float(data["budget_remaining"]) == 50000.00
        assert data["budget_percentage_used"] == 0
        assert data["vendors_saved"] == 0
        assert data["guests_count"] == 0
        assert data["days_remaining"] == 30
        assert data["progress_percentage"] == 0

    def test_get_event_dashboard_not_found(self, client, headers_with_token):
        """Test dashboard for non-existent event."""
        response = client.get(
            "/api/v1/events/invalid-uuid-12345/dashboard",
            headers=headers_with_token,
        )

        assert response.status_code == 404
