"""Safety invariants verified independently of model behavior."""
import pytest
from fastapi.testclient import TestClient
from app.main import app,identity
def test_demo_auth_fails_closed_outside_local(monkeypatch):
    monkeypatch.setenv("APP_ENV","production")
    monkeypatch.setenv("AUTH_MODE","demo")
    with pytest.raises(Exception) as err:
        with TestClient(app):
            pass
    assert "AUTH_MODE=oidc" in str(err.value)
def test_readiness_checks_database():
    with TestClient(app) as client:
        result=client.get("/ready")
        assert result.status_code==200
def test_demo_identity_directly_rejected_when_production(monkeypatch):
    monkeypatch.setenv("APP_ENV","production")
    monkeypatch.setenv("AUTH_MODE","demo")
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as err:
        identity("Bearer demo-buyer-a")
    assert err.value.status_code==503
