from fastapi.testclient import TestClient
from app.main import app
def test_contracts_and_denial():
    with TestClient(app) as client:
        a={"Authorization":"Bearer demo-buyer-a"}
        b={"Authorization":"Bearer demo-buyer-b"}
        assert client.get("/api/catalog").status_code==401
        assert client.get("/api/orders",headers=a).status_code==200
        assert client.get("/api/invoices",headers=b).json()[0]["id"]=="INV-b-100"
        assert client.get("/api/orders/ORD-b-100",headers=a).status_code==404
        assert client.post("/api/orders/drafts",headers=a,json={"product_id":"SUG-25","quantity":999999}).status_code==422
        assert client.post("/api/orders/drafts",headers=a,json={"product_id":"SUG-25","quantity":9999}).status_code==409
        assert client.post("/api/orders/drafts",headers=a,json={"product_id":"BOGUS","quantity":2}).status_code==404
        assert client.post("/api/tickets",headers=a,json={"subject":"Shipment carrier delayed"}).status_code==201
        assert client.get("/api/tickets",headers=b).json()==[]
        assert client.get("/api/audit",headers=a).status_code==403
