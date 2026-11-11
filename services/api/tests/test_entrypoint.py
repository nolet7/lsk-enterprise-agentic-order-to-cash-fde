"""Exercise assembled ASGI application, not merely legacy module imports."""
import os
from fastapi.testclient import TestClient
from app.entrypoint import app
def test_startup_composition_and_agent_fail_closed():
    assert os.getenv("AUTH_MODE","demo")=="demo"
    with TestClient(app) as client:
        assert client.get("/health").status_code==200
        response=client.post("/api/chat",headers={"Authorization":"Bearer demo-buyer-a"},json={"message":"What is the status of my order?"})
        assert response.status_code==503
        assert client.post("/api/chat",headers={"Authorization":"Bearer invalid"},json={"message":"Show me prices"}).status_code==401
