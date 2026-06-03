"""
Tests for budget endpoints.
"""

import pytest
from datetime import date, datetime, timedelta


class TestBudgetItemCreation:
    """Budget item creation endpoint tests."""

    def test_create_budget_item_success(self, client, headers_with_token):
        """Test successful budget item creation."""
        # Create an event
        event_data = {
            "title": "Wedding",
            "event_type": "WEDDING",
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=31)),
            "budget": 50000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create a budget item
        budget_data = {
            "category": "Catering",
            "planned_amount": 15000.00,
            "actual_amount": 13500.00,
            "notes": "Food and beverages for reception",
        }

        response = client.post(
            f"/api/v1/events/{event_id}/budget",
            json=budget_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["category"] == "Catering"
        assert float(data["planned_amount"]) == 15000.00
        assert float(data["actual_amount"]) == 13500.00
        assert data["notes"] == "Food and beverages for reception"
        assert "id" in data
        assert data["event_id"] == event_id

    def test_create_budget_item_minimal_data(self, client, headers_with_token):
        """Test budget item creation with minimal data."""
        # Create an event
        event_data = {
            "title": "Party",
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

        # Create budget item with minimal data
        budget_data = {
            "category": "Decorations",
            "planned_amount": 500.00,
        }

        response = client.post(
            f"/api/v1/events/{event_id}/budget",
            json=budget_data,
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["category"] == "Decorations"
        assert float(data["planned_amount"]) == 500.00
        assert float(data["actual_amount"]) == 0.0

    def test_create_budget_item_unauthorized(self, client, headers_with_token):
        """Test budget item creation without authentication."""
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

        budget_data = {
            "category": "Test",
            "planned_amount": 100.00,
        }

        response = client.post(
            f"/api/v1/events/{event_id}/budget",
            json=budget_data,
        )

        assert response.status_code == 401

    def test_create_budget_item_invalid_event(self, client, headers_with_token):
        """Test budget item creation for non-existent event."""
        budget_data = {
            "category": "Test",
            "planned_amount": 100.00,
        }

        response = client.post(
            "/api/v1/events/00000000-0000-0000-0000-000000000000/budget",
            json=budget_data,
            headers=headers_with_token,
        )

        assert response.status_code == 404


class TestBudgetItemListing:
    """Budget item listing and filtering tests."""

    def test_list_budget_items_empty(self, client, headers_with_token):
        """Test listing budget items when event has none."""
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
            f"/api/v1/events/{event_id}/budget",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_list_budget_items_success(self, client, headers_with_token):
        """Test successful budget item listing."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 10000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create multiple budget items
        categories = ["Venue", "Catering", "Decorations"]
        for category in categories:
            budget_data = {
                "category": category,
                "planned_amount": 3000.00,
            }
            client.post(
                f"/api/v1/events/{event_id}/budget",
                json=budget_data,
                headers=headers_with_token,
            )

        response = client.get(
            f"/api/v1/events/{event_id}/budget",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

    def test_list_budget_items_filter_by_category(self, client, headers_with_token):
        """Test filtering budget items by category."""
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

        # Create items with different categories
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Venue", "planned_amount": 5000.00},
            headers=headers_with_token,
        )
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Catering", "planned_amount": 3000.00},
            headers=headers_with_token,
        )

        # Filter by Venue
        response = client.get(
            f"/api/v1/events/{event_id}/budget?category=Venue",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["category"] == "Venue"

    def test_list_budget_items_pagination(self, client, headers_with_token):
        """Test budget items pagination."""
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

        # Create 15 budget items
        for i in range(15):
            budget_data = {
                "category": f"Category {i + 1}",
                "planned_amount": 1000.00,
            }
            client.post(
                f"/api/v1/events/{event_id}/budget",
                json=budget_data,
                headers=headers_with_token,
            )

        # Get first page
        response = client.get(
            f"/api/v1/events/{event_id}/budget?skip=0&limit=10",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["items"]) == 10

        # Get second page
        response = client.get(
            f"/api/v1/events/{event_id}/budget?skip=10&limit=10",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["items"]) == 5


class TestBudgetItemUpdate:
    """Budget item update endpoint tests."""

    def test_update_budget_item_success(self, client, headers_with_token):
        """Test successful budget item update."""
        # Create event and budget item
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

        budget_response = client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Original", "planned_amount": 1000.00},
            headers=headers_with_token,
        )
        item_id = budget_response.json()["id"]

        # Update budget item
        update_data = {
            "category": "Updated",
            "actual_amount": 950.00,
            "notes": "Updated notes",
        }
        response = client.patch(
            f"/api/v1/budget/{item_id}",
            json=update_data,
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "Updated"
        assert float(data["actual_amount"]) == 950.00
        assert data["notes"] == "Updated notes"

    def test_delete_budget_item_success(self, client, headers_with_token):
        """Test successful budget item deletion."""
        # Create event and budget item
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

        budget_response = client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "To Delete", "planned_amount": 500.00},
            headers=headers_with_token,
        )
        item_id = budget_response.json()["id"]

        # Delete budget item
        response = client.delete(
            f"/api/v1/budget/{item_id}",
            headers=headers_with_token,
        )

        assert response.status_code == 204

        # Verify it's deleted (should not appear in list)
        response = client.get(
            f"/api/v1/events/{event_id}/budget",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0


class TestBudgetSummary:
    """Budget summary endpoint tests."""

    def test_get_budget_summary_empty(self, client, headers_with_token):
        """Test budget summary with no items."""
        # Create event with budget
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 10000.00,
            "currency": "USD",
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        response = client.get(
            f"/api/v1/events/{event_id}/budget/summary",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert float(data["total_budget"]) == 10000.00
        assert float(data["total_planned"]) == 0.0
        assert float(data["total_actual"]) == 0.0
        assert float(data["remaining_budget"]) == 10000.00
        assert data["budget_percentage_used"] == 0
        assert data["budget_health_status"] == "GOOD"
        assert data["currency"] == "USD"

    def test_get_budget_summary_good_status(self, client, headers_with_token):
        """Test budget summary with GOOD status (< 80% used)."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 10000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create budget items (50% of budget)
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Venue", "planned_amount": 3000.00, "actual_amount": 5000.00},
            headers=headers_with_token,
        )

        response = client.get(
            f"/api/v1/events/{event_id}/budget/summary",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert float(data["total_actual"]) == 5000.00
        assert data["budget_percentage_used"] == 50
        assert data["budget_health_status"] == "GOOD"

    def test_get_budget_summary_warning_status(self, client, headers_with_token):
        """Test budget summary with WARNING status (80-100% used)."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 10000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create budget items (90% of budget)
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Venue", "planned_amount": 5000.00, "actual_amount": 9000.00},
            headers=headers_with_token,
        )

        response = client.get(
            f"/api/v1/events/{event_id}/budget/summary",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert float(data["total_actual"]) == 9000.00
        assert data["budget_percentage_used"] == 90
        assert data["budget_health_status"] == "WARNING"

    def test_get_budget_summary_over_budget_status(self, client, headers_with_token):
        """Test budget summary with OVER_BUDGET status."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 10000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create budget items (110% of budget)
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Venue", "planned_amount": 5000.00, "actual_amount": 11000.00},
            headers=headers_with_token,
        )

        response = client.get(
            f"/api/v1/events/{event_id}/budget/summary",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        assert float(data["total_actual"]) == 11000.00
        assert data["budget_percentage_used"] == 110
        assert data["budget_health_status"] == "OVER_BUDGET"

    def test_get_budget_summary_over_budget_categories(self, client, headers_with_token):
        """Test budget summary identifies over-budget categories."""
        # Create event
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 20000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

        # Create budget items
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Catering", "planned_amount": 5000.00, "actual_amount": 6000.00},
            headers=headers_with_token,
        )
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Venue", "planned_amount": 8000.00, "actual_amount": 7000.00},
            headers=headers_with_token,
        )

        response = client.get(
            f"/api/v1/events/{event_id}/budget/summary",
            headers=headers_with_token,
        )

        assert response.status_code == 200
        data = response.json()
        # Should have one over-budget category (Catering)
        assert len(data["over_budget_categories"]) == 1
        assert data["over_budget_categories"][0]["category"] == "Catering"
        assert float(data["over_budget_categories"][0]["overage"]) == 1000.00

    def test_budget_summary_unauthorized(self, client, headers_with_token):
        """Test that users can't access other users' budget summaries."""
        from app.core.security import create_access_token

        # Create event as first user
        event_data = {
            "title": "Event",
            "event_type": "OTHER",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "budget": 5000.00,
        }
        event_response = client.post(
            "/api/v1/events",
            json=event_data,
            headers=headers_with_token,
        )
        event_id = event_response.json()["id"]

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

        # Try to access budget as other user
        response = client.get(
            f"/api/v1/events/{event_id}/budget/summary",
            headers=other_headers,
        )

        assert response.status_code == 403
