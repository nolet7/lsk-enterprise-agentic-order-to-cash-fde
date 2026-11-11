import os
os.environ["DATABASE_URL"]="sqlite:///./test-lsk.db"
from fastapi.testclient import TestClient
from app.main import app
def test_legacy_flow():
    with TestClient(app) as c:
        h={"Authorization":"Bearer demo-buyer-a"}
        other={"Authorization":"Bearer demo-buyer-b"}
        assert c.get("/health").status_code==200
        rows=c.get("/api/catalog",headers=h).json()
        assert rows[0]["unit_price"]=="38.50"
        assert c.get("/api/catalog",headers=other).json()[0]["unit_price"]=="77.00"
        assert c.get("/api/orders/ORD-b-100",headers=h).status_code==404
        assert c.get("/api/orders/ORD-a-100",headers=other).status_code==404
        assert c.get("/api/invoices",headers=h).json()[0]["id"]=="INV-a-100"
        assert c.post("/api/orders/drafts",headers={"Authorization":"Bearer demo-csr-a"},json={"product_id":"SUG-25","quantity":1}).status_code==403
        draft=c.post("/api/orders/drafts",headers=h,json={"product_id":"SUG-25","quantity":2})
        assert draft.status_code==201
        d=draft.json()
        endpoint="/api/orders/drafts/"+d["draft_id"]+"/confirm"
        assert c.post(endpoint,headers=other,json={"confirmation_nonce":d["confirmation_nonce"],"idempotency_key":"duplicate-key-123"}).status_code==404
        assert c.post(endpoint,headers=h,json={"confirmation_nonce":"wrong-nonce-value","idempotency_key":"duplicate-key-123"}).status_code==403
        ok=c.post(endpoint,headers=h,json={"confirmation_nonce":d["confirmation_nonce"],"idempotency_key":"duplicate-key-123"})
        assert ok.status_code==200
        assert c.post(endpoint,headers=h,json={"confirmation_nonce":d["confirmation_nonce"],"idempotency_key":"duplicate-key-123"}).json()["replayed"] is True
        assert c.get("/api/audit",headers=h).status_code==403
