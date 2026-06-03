"""
Tests for vendor endpoints: search, save, unsave, compare, CRUD.
"""

import pytest
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_event(client, headers, *, budget=50000.0, location="Mumbai", event_type="WEDDING"):
    resp = client.post(
        "/api/v1/events",
        json={
            "title": "Test Event",
            "event_type": event_type,
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=31)),
            "budget": budget,
            "location": location,
        },
        headers=headers,
    )
    assert resp.status_code == 201, resp.json()
    return resp.json()["id"]


def make_vendor(client, headers, **overrides):
    payload = {
        "business_name": "Grand Feast Caterers",
        "category": "CATERING",
        "location": "Mumbai, Maharashtra",
        "city": "Mumbai",
        "starting_price": 10000.0,
        "currency": "INR",
        "verified": False,
    }
    payload.update(overrides)
    resp = client.post("/api/v1/vendors", json=payload, headers=headers)
    assert resp.status_code == 201, resp.json()
    return resp.json()["id"]


# ---------------------------------------------------------------------------
# Vendor CRUD
# ---------------------------------------------------------------------------

class TestVendorCRUD:
    """Vendor create / get / update tests."""

    def test_create_vendor_success(self, client, headers_with_token):
        vendor_id = make_vendor(client, headers_with_token, business_name="Elite Venues")
        assert vendor_id

    def test_create_vendor_missing_required_fields(self, client, headers_with_token):
        resp = client.post(
            "/api/v1/vendors",
            json={"business_name": "Incomplete"},
            headers=headers_with_token,
        )
        assert resp.status_code == 422

    def test_create_vendor_requires_auth(self, client):
        resp = client.post(
            "/api/v1/vendors",
            json={"business_name": "X", "category": "VENUE", "location": "Delhi"},
        )
        assert resp.status_code == 401

    def test_get_vendor_public(self, client, headers_with_token):
        vendor_id = make_vendor(client, headers_with_token)
        resp = client.get(f"/api/v1/vendors/{vendor_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == vendor_id
        assert data["business_name"] == "Grand Feast Caterers"
        assert data["category"] == "CATERING"

    def test_get_vendor_not_found(self, client):
        resp = client.get("/api/v1/vendors/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    def test_update_vendor_owner(self, client, headers_with_token):
        vendor_id = make_vendor(client, headers_with_token)
        resp = client.patch(
            f"/api/v1/vendors/{vendor_id}",
            json={"business_name": "Grand Feast Pro", "starting_price": 12000.0},
            headers=headers_with_token,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["business_name"] == "Grand Feast Pro"
        assert float(data["starting_price"]) == 12000.0

    def test_update_vendor_non_owner_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        vendor_id = make_vendor(client, headers_with_token)

        other_token = create_access_token({"sub": "other-user", "email": "other@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.patch(
            f"/api/v1/vendors/{vendor_id}",
            json={"business_name": "Hijacked"},
            headers=other_headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Vendor Services
# ---------------------------------------------------------------------------

class TestVendorServices:
    """Add and list vendor services."""

    def test_add_service_owner(self, client, headers_with_token):
        vendor_id = make_vendor(client, headers_with_token)
        resp = client.post(
            f"/api/v1/vendors/{vendor_id}/services",
            json={"name": "Buffet Package", "price": 800.0, "unit": "per person"},
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Buffet Package"
        assert data["vendor_id"] == vendor_id

    def test_list_services_public(self, client, headers_with_token):
        vendor_id = make_vendor(client, headers_with_token)
        client.post(
            f"/api/v1/vendors/{vendor_id}/services",
            json={"name": "Veg Buffet", "price": 700.0, "unit": "per person"},
            headers=headers_with_token,
        )
        client.post(
            f"/api/v1/vendors/{vendor_id}/services",
            json={"name": "Non-Veg Buffet", "price": 900.0, "unit": "per person"},
            headers=headers_with_token,
        )
        resp = client.get(f"/api/v1/vendors/{vendor_id}/services")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_add_service_non_owner_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        vendor_id = make_vendor(client, headers_with_token)

        other_token = create_access_token({"sub": "intruder", "email": "i@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.post(
            f"/api/v1/vendors/{vendor_id}/services",
            json={"name": "Fake Service"},
            headers=other_headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Vendor Search
# ---------------------------------------------------------------------------

class TestVendorSearch:
    """Search and filter vendors."""

    def _seed_vendors(self, client, headers):
        """Create a variety of vendors and return their IDs."""
        ids = []
        specs = [
            {"business_name": "Star Caterers",    "category": "CATERING",     "city": "Mumbai", "starting_price": 8000,  "rating_hint": 4.8},
            {"business_name": "Palace Venue",     "category": "VENUE",        "city": "Delhi",  "starting_price": 50000, "rating_hint": 4.2},
            {"business_name": "Snap Memories",    "category": "PHOTOGRAPHY",  "city": "Mumbai", "starting_price": 15000, "rating_hint": 4.5},
            {"business_name": "Cheap Eats",       "category": "CATERING",     "city": "Pune",   "starting_price": 3000,  "rating_hint": 3.8},
            {"business_name": "Verified Flowers", "category": "FLORIST",      "city": "Mumbai", "starting_price": 5000,  "rating_hint": 4.0},
        ]
        for s in specs:
            vid = make_vendor(client, headers,
                              business_name=s["business_name"],
                              category=s["category"],
                              location=f"{s['city']}, India",
                              city=s["city"],
                              starting_price=s["starting_price"])
            ids.append(vid)
        return ids

    def test_search_returns_all_no_filters(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get("/api/v1/vendors/search?limit=50")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 5
        # Each card should have match_score and match_reason
        for item in data["items"]:
            assert "match_score" in item
            assert "match_reason" in item

    def test_search_filter_by_category(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get("/api/v1/vendors/search?category=CATERING&limit=50")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 2
        for item in data["items"]:
            assert item["category"] == "CATERING"

    def test_search_filter_by_location(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get("/api/v1/vendors/search?location=Mumbai&limit=50")
        assert resp.status_code == 200
        data = resp.json()
        # Star Caterers, Snap Memories, Verified Flowers are in Mumbai
        assert data["total"] >= 3
        for item in data["items"]:
            assert "mumbai" in item["location"].lower() or "Mumbai" in (item["city"] or "")

    def test_search_filter_min_price(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get("/api/v1/vendors/search?min_price=10000&limit=50")
        assert resp.status_code == 200
        data = resp.json()
        for item in data["items"]:
            if item["starting_price"] is not None:
                assert float(item["starting_price"]) >= 10000

    def test_search_filter_max_price(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get("/api/v1/vendors/search?max_price=10000&limit=50")
        assert resp.status_code == 200
        data = resp.json()
        for item in data["items"]:
            if item["starting_price"] is not None:
                assert float(item["starting_price"]) <= 10000

    def test_search_results_sorted_by_match_score_descending(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get(
            "/api/v1/vendors/search?location=Mumbai&event_type=WEDDING&event_budget=100000&limit=50"
        )
        assert resp.status_code == 200
        scores = [item["match_score"] for item in resp.json()["items"]]
        assert scores == sorted(scores, reverse=True), "Items should be sorted by match_score desc"

    def test_search_pagination(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        page1 = client.get("/api/v1/vendors/search?skip=0&limit=2").json()
        page2 = client.get("/api/v1/vendors/search?skip=2&limit=2").json()
        assert len(page1["items"]) == 2
        ids_p1 = {item["id"] for item in page1["items"]}
        ids_p2 = {item["id"] for item in page2["items"]}
        assert ids_p1.isdisjoint(ids_p2), "Pages must not overlap"

    def test_search_no_auth_required(self, client, headers_with_token):
        self._seed_vendors(client, headers_with_token)
        resp = client.get("/api/v1/vendors/search")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Save / unsave vendor
# ---------------------------------------------------------------------------

class TestSaveVendor:
    """Tests for saving and unsaving vendors to events."""

    def test_save_vendor_success(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vendor_id = make_vendor(client, headers_with_token)

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/save",
            json={"vendor_id": vendor_id, "notes": "Top pick for catering"},
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["vendor_id"] == vendor_id
        assert data["event_id"] == event_id
        assert data["notes"] == "Top pick for catering"
        assert "vendor" in data
        assert data["vendor"]["id"] == vendor_id

    def test_save_vendor_requires_auth(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vendor_id = make_vendor(client, headers_with_token)

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/save",
            json={"vendor_id": vendor_id},
        )
        assert resp.status_code == 401

    def test_save_vendor_duplicate_returns_409(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vendor_id = make_vendor(client, headers_with_token)

        client.post(
            f"/api/v1/events/{event_id}/vendors/save",
            json={"vendor_id": vendor_id},
            headers=headers_with_token,
        )
        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/save",
            json={"vendor_id": vendor_id},
            headers=headers_with_token,
        )
        assert resp.status_code == 409

    def test_save_vendor_wrong_event_owner_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        event_id = make_event(client, headers_with_token)
        vendor_id = make_vendor(client, headers_with_token)

        other_token = create_access_token({"sub": "other-user", "email": "other@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/save",
            json={"vendor_id": vendor_id},
            headers=other_headers,
        )
        assert resp.status_code == 403

    def test_list_saved_vendors(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        v1 = make_vendor(client, headers_with_token, business_name="Vendor A", category="CATERING")
        v2 = make_vendor(client, headers_with_token, business_name="Vendor B", category="VENUE")

        for vid in [v1, v2]:
            client.post(
                f"/api/v1/events/{event_id}/vendors/save",
                json={"vendor_id": vid},
                headers=headers_with_token,
            )

        resp = client.get(
            f"/api/v1/events/{event_id}/vendors/saved",
            headers=headers_with_token,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        saved_vendor_ids = {item["vendor_id"] for item in data["items"]}
        assert v1 in saved_vendor_ids
        assert v2 in saved_vendor_ids

    def test_list_saved_vendors_empty(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.get(
            f"/api/v1/events/{event_id}/vendors/saved",
            headers=headers_with_token,
        )
        assert resp.status_code == 200
        assert resp.json()["total"] == 0

    def test_unsave_vendor_success(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vendor_id = make_vendor(client, headers_with_token)

        client.post(
            f"/api/v1/events/{event_id}/vendors/save",
            json={"vendor_id": vendor_id},
            headers=headers_with_token,
        )

        resp = client.delete(
            f"/api/v1/events/{event_id}/vendors/{vendor_id}/unsave",
            headers=headers_with_token,
        )
        assert resp.status_code == 204

        # Confirm removed
        saved = client.get(
            f"/api/v1/events/{event_id}/vendors/saved",
            headers=headers_with_token,
        ).json()
        assert saved["total"] == 0

    def test_unsave_vendor_not_saved_returns_404(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vendor_id = make_vendor(client, headers_with_token)

        resp = client.delete(
            f"/api/v1/events/{event_id}/vendors/{vendor_id}/unsave",
            headers=headers_with_token,
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Compare vendors
# ---------------------------------------------------------------------------

class TestCompareVendors:
    """Tests for vendor comparison endpoint."""

    def test_compare_two_vendors(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token, budget=100000, location="Mumbai")
        v1 = make_vendor(client, headers_with_token, business_name="Top Caterer",
                         category="CATERING", city="Mumbai", starting_price=20000)
        v2 = make_vendor(client, headers_with_token, business_name="Budget Caterer",
                         category="CATERING", city="Delhi", starting_price=8000)

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": [v1, v2]},
            headers=headers_with_token,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["vendors"]) == 2
        # Both vendors present by id
        ids_returned = {v["id"] for v in data["vendors"]}
        assert v1 in ids_returned
        assert v2 in ids_returned
        # Recommended vendor is set
        assert data["recommended_vendor_id"] is not None
        assert data["recommendation_reason"] != ""

    def test_compare_four_vendors(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vids = [
            make_vendor(client, headers_with_token, business_name=f"Vendor {i}",
                        category="CATERING", city="Mumbai", starting_price=5000 * i)
            for i in range(1, 5)
        ]

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": vids},
            headers=headers_with_token,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["vendors"]) == 4

    def test_compare_requires_minimum_two_vendors(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        v1 = make_vendor(client, headers_with_token)

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": [v1]},
            headers=headers_with_token,
        )
        assert resp.status_code == 422

    def test_compare_max_four_vendors(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vids = [
            make_vendor(client, headers_with_token, business_name=f"V{i}", category="CATERING")
            for i in range(5)
        ]
        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": vids},
            headers=headers_with_token,
        )
        assert resp.status_code == 422

    def test_compare_requires_auth(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        v1 = make_vendor(client, headers_with_token)
        v2 = make_vendor(client, headers_with_token, business_name="Vendor 2", category="VENUE")

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": [v1, v2]},
        )
        assert resp.status_code == 401

    def test_compare_wrong_event_owner_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        event_id = make_event(client, headers_with_token)
        v1 = make_vendor(client, headers_with_token)
        v2 = make_vendor(client, headers_with_token, business_name="V2", category="VENUE")

        other_token = create_access_token({"sub": "other-user", "email": "o@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": [v1, v2]},
            headers=other_headers,
        )
        assert resp.status_code == 403

    def test_compare_higher_budget_fit_scores_higher(self, client, headers_with_token):
        """Vendor whose price fits within budget should outscore one that doesn't."""
        event_id = make_event(client, headers_with_token, budget=20000, location="Mumbai")
        affordable = make_vendor(
            client, headers_with_token,
            business_name="Affordable", category="CATERING",
            city="Mumbai", starting_price=8000,
        )
        expensive = make_vendor(
            client, headers_with_token,
            business_name="Expensive", category="CATERING",
            city="Delhi", starting_price=50000,
        )

        resp = client.post(
            f"/api/v1/events/{event_id}/vendors/compare",
            json={"vendor_ids": [affordable, expensive]},
            headers=headers_with_token,
        )
        assert resp.status_code == 200
        vendors_by_id = {v["id"]: v for v in resp.json()["vendors"]}
        assert vendors_by_id[affordable]["match_score"] > vendors_by_id[expensive]["match_score"]
