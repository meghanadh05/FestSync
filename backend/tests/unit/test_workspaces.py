"""
Tests for workspace foundation endpoints.
"""


class TestWorkspaces:
    def test_create_workspace_success(self, client, headers_with_token):
        response = client.post(
            "/api/v1/workspaces",
            json={
                "name": "Tech Summit Team",
                "organization": "FestSync Labs",
                "country": "India",
                "currency": "INR",
                "timezone": "Asia/Kolkata",
            },
            headers=headers_with_token,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tech Summit Team"
        assert data["role"] == "OWNER"
        assert data["currency"] == "INR"

    def test_list_workspaces_only_current_user(self, client, headers_with_token):
        client.post(
            "/api/v1/workspaces",
            json={"name": "Current User Workspace"},
            headers=headers_with_token,
        )

        response = client.get("/api/v1/workspaces", headers=headers_with_token)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Current User Workspace"

    def test_get_workspace_requires_membership(self, client, headers_with_token):
        created = client.post(
            "/api/v1/workspaces",
            json={"name": "Private Workspace"},
            headers=headers_with_token,
        ).json()

        from app.core.security import create_access_token

        other_token = create_access_token({"sub": "other-user", "email": "other@example.com"})
        response = client.get(
            f"/api/v1/workspaces/{created['id']}",
            headers={"Authorization": f"Bearer {other_token}"},
        )

        assert response.status_code == 403
