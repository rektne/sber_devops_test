import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_ip_only():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "ip" in data
        assert data["ip"] == "127.0.0.1"


@pytest.mark.asyncio
async def test_save_hostname_and_lookup():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/", params={"hostname": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["hostname"] == "test"
        assert data["status"] == "saved"
        assert data["ip"] == "127.0.0.1"

        response = await client.get("/lookup/test")
        assert response.status_code == 200
        assert response.json()["ip"] == "127.0.0.1"


@pytest.mark.asyncio
async def test_lookup_missing():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/lookup/ghost")
        assert response.status_code == 404
