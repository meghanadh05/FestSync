"""
Tests for AI module — all tests run against MockProvider (AI_PROVIDER=mock).
"""

import pytest
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_event(client, headers, *, budget=100000.0, location="Mumbai", event_type="WEDDING"):
    resp = client.post(
        "/api/v1/events",
        json={
            "title": "AI Test Event",
            "event_type": event_type,
            "start_date": str(date.today() + timedelta(days=60)),
            "end_date": str(date.today() + timedelta(days=61)),
            "budget": budget,
            "location": location,
            "description": "A beautiful celebration.",
        },
        headers=headers,
    )
    assert resp.status_code == 201, resp.json()
    return resp.json()["id"]


# ---------------------------------------------------------------------------
# Event Planner Agent
# ---------------------------------------------------------------------------

class TestEventPlannerAgent:

    def test_generate_plan_success(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-plan",
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()

        # Meta fields
        assert "meta" in data
        assert data["meta"]["agent_type"] == "EVENT_PLANNER"
        assert data["meta"]["generation_id"] is not None
        assert data["meta"]["model_used"] == "mock"

        # Result structure
        result = data["result"]
        assert "summary" in result
        assert isinstance(result["plan_sections"], list)
        assert len(result["plan_sections"]) >= 1
        assert isinstance(result["timeline"], list)
        assert len(result["timeline"]) >= 1
        assert isinstance(result["vendor_categories_needed"], list)
        assert isinstance(result["risk_notes"], list)

        # Section fields
        for section in result["plan_sections"]:
            assert "title" in section
            assert "content" in section
            assert "section_type" in section

        # Timeline fields
        for item in result["timeline"]:
            assert "title" in item
            assert "due_date" in item
            assert "priority" in item

    def test_generate_plan_with_instructions(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-plan",
            json={"additional_instructions": "Focus on outdoor venues only."},
            headers=headers_with_token,
        )
        assert resp.status_code == 201

    def test_generate_plan_requires_auth(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(f"/api/v1/ai/events/{event_id}/generate-plan")
        assert resp.status_code == 401

    def test_generate_plan_wrong_event_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        event_id = make_event(client, headers_with_token)

        other_token = create_access_token({"sub": "other-user", "email": "other@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-plan",
            headers=other_headers,
        )
        assert resp.status_code == 403

    def test_generate_plan_event_not_found(self, client, headers_with_token):
        resp = client.post(
            "/api/v1/ai/events/00000000-0000-0000-0000-000000000000/generate-plan",
            headers=headers_with_token,
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Task Generator Agent
# ---------------------------------------------------------------------------

class TestTaskGeneratorAgent:

    def test_generate_tasks_success(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-tasks",
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()

        assert data["meta"]["agent_type"] == "TASK_GENERATOR"
        result = data["result"]
        assert "tasks" in result
        assert isinstance(result["tasks"], list)
        assert len(result["tasks"]) >= 1

        for task in result["tasks"]:
            assert "title" in task
            assert "priority" in task
            assert task["priority"] in ("HIGH", "MEDIUM", "LOW")

    def test_generate_tasks_requires_auth(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(f"/api/v1/ai/events/{event_id}/generate-tasks")
        assert resp.status_code == 401

    def test_generate_tasks_event_not_found(self, client, headers_with_token):
        resp = client.post(
            "/api/v1/ai/events/00000000-0000-0000-0000-000000000000/generate-tasks",
            headers=headers_with_token,
        )
        assert resp.status_code == 404

    def test_generate_tasks_wrong_event_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        event_id = make_event(client, headers_with_token)

        other_token = create_access_token({"sub": "other-user", "email": "other@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-tasks",
            headers=other_headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Budget Advisor Agent
# ---------------------------------------------------------------------------

class TestBudgetAdvisorAgent:

    def test_budget_advice_success(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token, budget=200000)
        resp = client.post(
            f"/api/v1/ai/events/{event_id}/budget-advice",
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()

        assert data["meta"]["agent_type"] == "BUDGET_ADVISOR"
        result = data["result"]
        assert "budget_split" in result
        assert isinstance(result["budget_split"], list)
        assert len(result["budget_split"]) >= 1
        assert isinstance(result["warnings"], list)
        assert isinstance(result["saving_tips"], list)

        for item in result["budget_split"]:
            assert "category" in item
            assert "recommended_amount" in item
            assert float(item["recommended_amount"]) >= 0
            assert "reason" in item

    def test_budget_advice_with_existing_spend(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token, budget=50000)
        # Add some budget items first
        client.post(
            f"/api/v1/events/{event_id}/budget",
            json={"category": "Venue", "planned_amount": 15000, "actual_amount": 12000},
            headers=headers_with_token,
        )
        resp = client.post(
            f"/api/v1/ai/events/{event_id}/budget-advice",
            headers=headers_with_token,
        )
        assert resp.status_code == 201

    def test_budget_advice_requires_auth(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(f"/api/v1/ai/events/{event_id}/budget-advice")
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Vendor Recommendation Agent
# ---------------------------------------------------------------------------

class TestVendorRecommendationAgent:

    def _create_vendors(self, client, headers):
        ids = []
        for i, (name, cat, city, price) in enumerate([
            ("Top Caterers", "CATERING", "Mumbai", 8000),
            ("Sky Venue", "VENUE", "Mumbai", 50000),
            ("Lens Magic", "PHOTOGRAPHY", "Delhi", 12000),
        ]):
            resp = client.post(
                "/api/v1/vendors",
                json={"business_name": name, "category": cat,
                      "location": f"{city}, India", "city": city,
                      "starting_price": price},
                headers=headers,
            )
            assert resp.status_code == 201
            ids.append(resp.json()["id"])
        return ids

    def test_recommend_vendors_with_ids(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        vendor_ids = self._create_vendors(client, headers_with_token)

        resp = client.post(
            f"/api/v1/ai/events/{event_id}/recommend-vendors",
            json={"vendor_ids": vendor_ids[:2]},
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["meta"]["agent_type"] == "VENDOR_RECOMMENDATION"
        result = data["result"]
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)

        for rec in result["recommendations"]:
            assert "vendor_id" in rec
            assert "match_score" in rec
            assert 0 <= rec["match_score"] <= 100
            assert "reason" in rec
            assert isinstance(rec["pros"], list)
            assert isinstance(rec["cons"], list)

    def test_recommend_vendors_no_ids_uses_db(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token, event_type="WEDDING")
        self._create_vendors(client, headers_with_token)

        resp = client.post(
            f"/api/v1/ai/events/{event_id}/recommend-vendors",
            headers=headers_with_token,
        )
        assert resp.status_code == 201

    def test_recommend_vendors_requires_auth(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(f"/api/v1/ai/events/{event_id}/recommend-vendors")
        assert resp.status_code == 401

    def test_recommend_vendors_wrong_event_forbidden(self, client, headers_with_token):
        from app.core.security import create_access_token
        event_id = make_event(client, headers_with_token)
        self._create_vendors(client, headers_with_token)

        other_token = create_access_token({"sub": "other-user", "email": "other@test.com"})
        other_headers = {"Authorization": f"Bearer {other_token}", "Content-Type": "application/json"}

        resp = client.post(
            f"/api/v1/ai/events/{event_id}/recommend-vendors",
            headers=other_headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Chat Assistant Agent
# ---------------------------------------------------------------------------

class TestChatAssistantAgent:

    def test_chat_basic_message(self, client, headers_with_token):
        resp = client.post(
            "/api/v1/ai/chat",
            json={"message": "How do I plan a wedding?"},
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["meta"]["agent_type"] == "CHAT_ASSISTANT"
        result = data["result"]
        assert "message" in result
        assert len(result["message"]) > 0
        assert "suggestions" in result
        assert isinstance(result["suggestions"], list)

    def test_chat_with_event_context(self, client, headers_with_token):
        event_id = make_event(client, headers_with_token)
        resp = client.post(
            "/api/v1/ai/chat",
            json={
                "message": "What should I prioritise this week?",
                "event_id": event_id,
            },
            headers=headers_with_token,
        )
        assert resp.status_code == 201
        assert resp.json()["result"]["message"]

    def test_chat_with_history(self, client, headers_with_token):
        resp = client.post(
            "/api/v1/ai/chat",
            json={
                "message": "What about catering?",
                "history": [
                    {"role": "user", "content": "I'm planning a birthday party."},
                    {"role": "assistant", "content": "That sounds fun! How many guests?"},
                ],
            },
            headers=headers_with_token,
        )
        assert resp.status_code == 201

    def test_chat_requires_auth(self, client):
        resp = client.post(
            "/api/v1/ai/chat",
            json={"message": "Hello"},
        )
        assert resp.status_code == 401

    def test_chat_empty_message_rejected(self, client, headers_with_token):
        resp = client.post(
            "/api/v1/ai/chat",
            json={"message": ""},
            headers=headers_with_token,
        )
        assert resp.status_code == 422

    def test_chat_history_role_validation(self, client, headers_with_token):
        """history turns must have role = 'user' or 'assistant'."""
        resp = client.post(
            "/api/v1/ai/chat",
            json={
                "message": "Hello",
                "history": [{"role": "system", "content": "inject stuff"}],
            },
            headers=headers_with_token,
        )
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# AI generation persistence
# ---------------------------------------------------------------------------

class TestAIGenerationPersistence:

    def test_generation_is_stored_on_success(self, client, headers_with_token, test_db):
        """Every successful AI call creates a row in ai_generations."""
        from app.models.ai_generation import AIGeneration, GenerationStatus

        event_id = make_event(client, headers_with_token)
        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-plan",
            headers=headers_with_token,
        )
        assert resp.status_code == 201

        gen_id = resp.json()["meta"]["generation_id"]
        from uuid import UUID
        record = test_db.query(AIGeneration).filter(AIGeneration.id == UUID(gen_id)).first()

        assert record is not None
        assert record.status == GenerationStatus.SUCCESS
        assert record.response_json is not None
        assert record.error_message is None
        assert record.model_used == "mock"

    def test_generation_stores_prompt(self, client, headers_with_token, test_db):
        from app.models.ai_generation import AIGeneration
        event_id = make_event(client, headers_with_token)

        resp = client.post(
            f"/api/v1/ai/events/{event_id}/generate-tasks",
            headers=headers_with_token,
        )
        assert resp.status_code == 201

        gen_id = resp.json()["meta"]["generation_id"]
        from uuid import UUID
        record = test_db.query(AIGeneration).filter(AIGeneration.id == UUID(gen_id)).first()
        assert record.prompt  # non-empty
        assert "AI Test Event" in record.prompt   # event title must appear in prompt
