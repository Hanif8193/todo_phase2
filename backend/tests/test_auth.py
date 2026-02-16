"""
Tests for authentication routes: /auth/signup, /auth/signin, /auth/signout.
"""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestSignup:
    async def test_signup_success(self, client: AsyncClient):
        resp = await client.post("/auth/signup", json={
            "email": "new@example.com",
            "password": "securepass",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "token" in data
        assert data["user"]["email"] == "new@example.com"
        assert "password" not in data["user"]
        assert "password_hash" not in data["user"]

    async def test_signup_returns_jwt(self, client: AsyncClient):
        resp = await client.post("/auth/signup", json={
            "email": "jwt@example.com",
            "password": "securepass",
        })
        token = resp.json()["token"]
        # JWT has 3 dot-separated segments
        assert len(token.split(".")) == 3

    async def test_signup_duplicate_email(self, client: AsyncClient):
        payload = {"email": "dup@example.com", "password": "securepass"}
        await client.post("/auth/signup", json=payload)
        resp = await client.post("/auth/signup", json=payload)
        assert resp.status_code == 400
        assert "already registered" in resp.json()["detail"].lower()

    async def test_signup_password_too_short(self, client: AsyncClient):
        resp = await client.post("/auth/signup", json={
            "email": "short@example.com",
            "password": "abc",  # < 8 chars
        })
        assert resp.status_code == 422

    async def test_signup_email_too_short(self, client: AsyncClient):
        resp = await client.post("/auth/signup", json={
            "email": "a@",  # < 3 chars
            "password": "securepass",
        })
        assert resp.status_code == 422

    async def test_signup_missing_fields(self, client: AsyncClient):
        resp = await client.post("/auth/signup", json={"email": "only@example.com"})
        assert resp.status_code == 422


class TestSignin:
    async def test_signin_success(self, client: AsyncClient, registered_user):
        resp = await client.post("/auth/signin", json={
            "email": "test@example.com",
            "password": "password123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert data["user"]["email"] == "test@example.com"

    async def test_signin_wrong_password(self, client: AsyncClient, registered_user):
        resp = await client.post("/auth/signin", json={
            "email": "test@example.com",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401
        assert "invalid" in resp.json()["detail"].lower()

    async def test_signin_unknown_email(self, client: AsyncClient):
        resp = await client.post("/auth/signin", json={
            "email": "ghost@example.com",
            "password": "password123",
        })
        assert resp.status_code == 401

    async def test_signin_missing_password(self, client: AsyncClient):
        resp = await client.post("/auth/signin", json={"email": "test@example.com"})
        assert resp.status_code == 422


class TestSignout:
    async def test_signout_success(self, client: AsyncClient, auth_headers):
        resp = await client.post("/auth/signout", headers=auth_headers)
        assert resp.status_code == 200
        assert "signed out" in resp.json()["message"].lower()

    async def test_signout_without_token(self, client: AsyncClient):
        resp = await client.post("/auth/signout")
        assert resp.status_code == 403

    async def test_signout_invalid_token(self, client: AsyncClient):
        resp = await client.post(
            "/auth/signout",
            headers={"Authorization": "Bearer not.a.valid.token"},
        )
        assert resp.status_code == 401
