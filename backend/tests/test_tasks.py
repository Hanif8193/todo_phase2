"""
Tests for task CRUD routes and ownership enforcement.

Routes under test:
  GET    /api/{user_id}/tasks
  POST   /api/{user_id}/tasks
  GET    /api/{user_id}/tasks/{id}
  PUT    /api/{user_id}/tasks/{id}
  DELETE /api/{user_id}/tasks/{id}
  PATCH  /api/{user_id}/tasks/{id}/complete
"""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _create_task(client, user_id, auth_headers, title="Test task", description=None):
    payload = {"title": title}
    if description:
        payload["description"] = description
    resp = await client.post(f"/api/{user_id}/tasks", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


# ---------------------------------------------------------------------------
# GET /api/{user_id}/tasks
# ---------------------------------------------------------------------------

class TestGetTasks:
    async def test_empty_list(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.get(f"/api/{user_id}/tasks", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_created_tasks(self, client: AsyncClient, auth_headers, user_id):
        await _create_task(client, user_id, auth_headers, "Task A")
        await _create_task(client, user_id, auth_headers, "Task B")
        resp = await client.get(f"/api/{user_id}/tasks", headers=auth_headers)
        assert resp.status_code == 200
        titles = [t["title"] for t in resp.json()]
        assert "Task A" in titles
        assert "Task B" in titles

    async def test_requires_auth(self, client: AsyncClient, user_id):
        resp = await client.get(f"/api/{user_id}/tasks")
        assert resp.status_code == 403

    async def test_cannot_access_other_users_tasks(
        self, client: AsyncClient, auth_headers, user_id
    ):
        other_id = user_id + 999
        resp = await client.get(f"/api/{other_id}/tasks", headers=auth_headers)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# POST /api/{user_id}/tasks
# ---------------------------------------------------------------------------

class TestCreateTask:
    async def test_create_with_title_only(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.post(
            f"/api/{user_id}/tasks",
            json={"title": "Buy groceries"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Buy groceries"
        assert data["description"] is None
        assert data["is_completed"] is False
        assert data["user_id"] == user_id

    async def test_create_with_description(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.post(
            f"/api/{user_id}/tasks",
            json={"title": "Read book", "description": "Finish chapter 5"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["description"] == "Finish chapter 5"

    async def test_create_requires_title(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.post(
            f"/api/{user_id}/tasks",
            json={"description": "No title here"},
            headers=auth_headers,
        )
        assert resp.status_code == 422

    async def test_create_empty_title_rejected(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.post(
            f"/api/{user_id}/tasks",
            json={"title": ""},
            headers=auth_headers,
        )
        assert resp.status_code == 422

    async def test_create_requires_auth(self, client: AsyncClient, user_id):
        resp = await client.post(f"/api/{user_id}/tasks", json={"title": "Task"})
        assert resp.status_code == 403

    async def test_cannot_create_for_other_user(
        self, client: AsyncClient, auth_headers, user_id
    ):
        other_id = user_id + 999
        resp = await client.post(
            f"/api/{other_id}/tasks",
            json={"title": "Sneaky task"},
            headers=auth_headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# GET /api/{user_id}/tasks/{id}
# ---------------------------------------------------------------------------

class TestGetTask:
    async def test_get_existing_task(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers, "Specific task")
        resp = await client.get(
            f"/api/{user_id}/tasks/{task['id']}", headers=auth_headers
        )
        assert resp.status_code == 200
        assert resp.json()["id"] == task["id"]

    async def test_get_nonexistent_task(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.get(f"/api/{user_id}/tasks/99999", headers=auth_headers)
        assert resp.status_code == 404

    async def test_get_requires_auth(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.get(f"/api/{user_id}/tasks/{task['id']}")
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# PUT /api/{user_id}/tasks/{id}
# ---------------------------------------------------------------------------

class TestUpdateTask:
    async def test_update_title(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers, "Old title")
        resp = await client.put(
            f"/api/{user_id}/tasks/{task['id']}",
            json={"title": "New title"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "New title"

    async def test_update_description(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.put(
            f"/api/{user_id}/tasks/{task['id']}",
            json={"description": "Updated desc"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["description"] == "Updated desc"

    async def test_update_nonexistent_task(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.put(
            f"/api/{user_id}/tasks/99999",
            json={"title": "Ghost"},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    async def test_update_requires_auth(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.put(
            f"/api/{user_id}/tasks/{task['id']}",
            json={"title": "Sneaky"},
        )
        assert resp.status_code == 403

    async def test_cannot_update_other_users_task(
        self, client: AsyncClient, auth_headers, user_id
    ):
        task = await _create_task(client, user_id, auth_headers)
        other_id = user_id + 999
        resp = await client.put(
            f"/api/{other_id}/tasks/{task['id']}",
            json={"title": "Hijack"},
            headers=auth_headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /api/{user_id}/tasks/{id}
# ---------------------------------------------------------------------------

class TestDeleteTask:
    async def test_delete_task(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.delete(
            f"/api/{user_id}/tasks/{task['id']}", headers=auth_headers
        )
        assert resp.status_code == 204

        # Confirm it's gone
        get_resp = await client.get(
            f"/api/{user_id}/tasks/{task['id']}", headers=auth_headers
        )
        assert get_resp.status_code == 404

    async def test_delete_nonexistent_task(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.delete(f"/api/{user_id}/tasks/99999", headers=auth_headers)
        assert resp.status_code == 404

    async def test_delete_requires_auth(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.delete(f"/api/{user_id}/tasks/{task['id']}")
        assert resp.status_code == 403

    async def test_cannot_delete_other_users_task(
        self, client: AsyncClient, auth_headers, user_id
    ):
        task = await _create_task(client, user_id, auth_headers)
        other_id = user_id + 999
        resp = await client.delete(
            f"/api/{other_id}/tasks/{task['id']}", headers=auth_headers
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# PATCH /api/{user_id}/tasks/{id}/complete
# ---------------------------------------------------------------------------

class TestToggleCompletion:
    async def test_mark_complete(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        assert task["is_completed"] is False

        resp = await client.patch(
            f"/api/{user_id}/tasks/{task['id']}/complete",
            json={"is_completed": True},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["is_completed"] is True

    async def test_mark_incomplete(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        # Complete first
        await client.patch(
            f"/api/{user_id}/tasks/{task['id']}/complete",
            json={"is_completed": True},
            headers=auth_headers,
        )
        # Then undo
        resp = await client.patch(
            f"/api/{user_id}/tasks/{task['id']}/complete",
            json={"is_completed": False},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["is_completed"] is False

    async def test_toggle_nonexistent_task(self, client: AsyncClient, auth_headers, user_id):
        resp = await client.patch(
            f"/api/{user_id}/tasks/99999/complete",
            json={"is_completed": True},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    async def test_toggle_requires_auth(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.patch(
            f"/api/{user_id}/tasks/{task['id']}/complete",
            json={"is_completed": True},
        )
        assert resp.status_code == 403

    async def test_toggle_missing_field(self, client: AsyncClient, auth_headers, user_id):
        task = await _create_task(client, user_id, auth_headers)
        resp = await client.patch(
            f"/api/{user_id}/tasks/{task['id']}/complete",
            json={},
            headers=auth_headers,
        )
        assert resp.status_code == 422
