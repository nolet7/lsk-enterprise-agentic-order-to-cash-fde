"""Synthetic wholesale commerce: deterministic legacy system of record API (POC).
POC demo tokens are NOT production authentication; pilot replaces with signed OIDC JWT.
"""
import hashlib
import os
import secrets
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, Integer, Numeric, ForeignKey, UniqueConstraint, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./lsk-demo.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
API_CALLS = Counter("lsk_api_requests_total", "Requests by operation", ["operation"])
DEMO_TOKENS = {
    "demo-buyer-a": ("tenant-a", "buyer-a", "customer-a", "buyer"),
    "demo-buyer-b": ("tenant-b", "buyer-b", "customer-b", "buyer"),
    "demo-csr-a": ("tenant-a", "csr-a", None, "csr"),
}
class Product(Base):
    __tablename__="products"
    id=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    uom=Column(String,nullable=False)
class Contract(Base):
    __tablename__="contracts"
    tenant_id=Column(String,primary_key=True)
    customer_id=Column(String,primary_key=True)
    product_id=Column(String,ForeignKey("products.id"),primary_key=True)
    unit_price=Column(Numeric(12,2),nullable=False)
class Stock(Base):
    __tablename__="stock"
    tenant_id=Column(String,primary_key=True)
    product_id=Column(String,primary_key=True)
    available=Column(Integer,nullable=False)
class Order(Base):
    __tablename__="orders"
    id=Column(String,primary_key=True)
    tenant_id=Column(String,nullable=False,index=True)
    customer_id=Column(String,nullable=False)
    product_id=Column(String,nullable=False)
    quantity=Column(Integer,nullable=False)
    unit_price=Column(Numeric(12,2),nullable=False)
    status=Column(String,nullable=False)
    nonce_hash=Column(String,nullable=True)
    created_at=Column(String,nullable=False)
class Invoice(Base):
    __tablename__="invoices"
    id=Column(String,primary_key=True)
    tenant_id=Column(String,nullable=False,index=True)
    customer_id=Column(String,nullable=False)
    order_id=Column(String,nullable=False)
    amount=Column(Numeric(12,2),nullable=False)
    status=Column(String,nullable=False)
class Fulfillment(Base):
    __tablename__="fulfillment"
    id=Column(String,primary_key=True)
    tenant_id=Column(String,nullable=False)
    order_id=Column(String,nullable=False)
    event=Column(String,nullable=False)
    at=Column(String,nullable=False)
class Ticket(Base):
    __tablename__="tickets"
    id=Column(String,primary_key=True)
    tenant_id=Column(String,nullable=False)
    customer_id=Column(String,nullable=False)
    subject=Column(String,nullable=False)
    status=Column(String,nullable=False,default="open")
class Idempotency(Base):
    __tablename__="idempotency"
    tenant_id=Column(String,primary_key=True)
    actor_id=Column(String,primary_key=True)
    idem_key=Column(String,primary_key=True)
    draft_id=Column(String,nullable=False)
    order_id=Column(String,nullable=False)
class Audit(Base):
    __tablename__="audit"
    id=Column(String,primary_key=True)
    tenant_id=Column(String,nullable=False)
    actor=Column(String,nullable=False)
    action=Column(String,nullable=False)
    resource=Column(String,nullable=False)
    timestamp=Column(String,nullable=False)
def now():
    return datetime.now(timezone.utc).isoformat()
def seed(db):
    if db.get(Product,"SUG-25"): return
    for p in [Product(id="SUG-25",name="Fine Granulated Cane Sugar 25kg",uom="bag"),Product(id="MOL-10",name="Food Grade Molasses 10L",uom="jug"),Product(id="SYR-20",name="Liquid Sugar Syrup 20L",uom="pail")]: db.add(p)
    for tenant,customer,scale in [("tenant-a","customer-a",1),("tenant-b","customer-b",2)]:
        for sku,price,qty in [("SUG-25",Decimal("38.50"),480),("MOL-10",Decimal("24.25"),130),("SYR-20",Decimal("42.75"),95)]:
            db.add(Contract(tenant_id=tenant,customer_id=customer,product_id=sku,unit_price=price*scale))
            db.add(Stock(tenant_id=tenant,product_id=sku,available=qty))
        db.add(Order(id="ORD-"+tenant[-1]+"-100",tenant_id=tenant,customer_id=customer,product_id="SUG-25",quantity=10,unit_price=Decimal("38.50")*scale,status="shipped",created_at=now()))
        db.add(Invoice(id="INV-"+tenant[-1]+"-100",tenant_id=tenant,customer_id=customer,order_id="ORD-"+tenant[-1]+"-100",amount=Decimal("385.00")*scale,status="open"))
        db.add(Fulfillment(id="EV-"+tenant[-1]+"-100",tenant_id=tenant,order_id="ORD-"+tenant[-1]+"-100",event="Carrier picked up shipment",at=now()))
    db.commit()
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    with SessionLocal() as db: seed(db)
    yield
app=FastAPI(title="LSK Order-to-Cash Legacy API",version="0.1.0",lifespan=lifespan)
def get_db():
    with SessionLocal() as db: yield db
def identity(authorization: str | None=Header(None)):
    token=(authorization or "").removeprefix("Bearer ").strip()
    if os.getenv("AUTH_MODE","demo") != "demo":
        raise HTTPException(503,"OIDC mode requires configured verified JWT middleware")
    if token not in DEMO_TOKENS: raise HTTPException(401,"Invalid demo credential")
    return DEMO_TOKENS[token]
def scoped_customer(auth, customer=None):
    tenant,actor,bound,role=auth
    if role=="buyer" and customer and customer!=bound: raise HTTPException(403,"Customer access denied")
    return bound if role=="buyer" else customer
def audit(db,auth,action,resource):
    db.add(Audit(id=secrets.token_hex(12),tenant_id=auth[0],actor=auth[1],action=action,resource=resource,timestamp=now()))
def price_for(db,auth,sku,customer=None):
    customer=scoped_customer(auth,customer)
    row=db.get(Contract,(auth[0],customer,sku))
    if not row: raise HTTPException(404,"No contracted price; contact CSR")
    return row
class DraftIn(BaseModel):
    product_id:str
    quantity:int=Field(ge=1,le=10000)
class ConfirmIn(BaseModel):
    confirmation_nonce:str=Field(min_length=16)
    idempotency_key:str=Field(min_length=12,max_length=128)
class TicketIn(BaseModel):
    subject:str=Field(min_length=4,max_length=250)
@app.get("/health")
def health(): return {"status":"ok","synthetic":True}
@app.get("/metrics")
def metrics(): return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
@app.get("/api/catalog")
def catalog(db:Session=Depends(get_db),auth=Depends(identity)):
    API_CALLS.labels("catalog").inc()
    products=db.scalars(select(Product)).all()
    return [{"sku":p.id,"name":p.name,"uom":p.uom,"unit_price":str(price_for(db,auth,p.id).unit_price),"available":db.get(Stock,(auth[0],p.id)).available} for p in products]
@app.get("/api/orders")
def orders(db:Session=Depends(get_db),auth=Depends(identity)):
    customer=scoped_customer(auth)
    q=select(Order).where(Order.tenant_id==auth[0])
    if customer:q=q.where(Order.customer_id==customer)
    return [{"id":o.id,"sku":o.product_id,"quantity":o.quantity,"unit_price":str(o.unit_price),"status":o.status} for o in db.scalars(q).all()]
@app.get("/api/orders/{order_id}")
def order_detail(order_id:str,db:Session=Depends(get_db),auth=Depends(identity)):
    row=db.get(Order,order_id)
    if not row or row.tenant_id!=auth[0]: raise HTTPException(404,"Order not found")
    scoped_customer(auth,row.customer_id)
    events=db.scalars(select(Fulfillment).where(Fulfillment.tenant_id==auth[0],Fulfillment.order_id==order_id)).all()
    return {"id":row.id,"status":row.status,"product_id":row.product_id,"quantity":row.quantity,"unit_price":str(row.unit_price),"events":[{"event":e.event,"at":e.at} for e in events]}
@app.get("/api/invoices")
def invoices(db:Session=Depends(get_db),auth=Depends(identity)):
    q=select(Invoice).where(Invoice.tenant_id==auth[0])
    if auth[2]:q=q.where(Invoice.customer_id==auth[2])
    return [{"id":i.id,"order_id":i.order_id,"amount":str(i.amount),"status":i.status} for i in db.scalars(q).all()]
@app.get("/api/tickets")
def tickets(db:Session=Depends(get_db),auth=Depends(identity)):
    q=select(Ticket).where(Ticket.tenant_id==auth[0])
    if auth[2]:q=q.where(Ticket.customer_id==auth[2])
    return [{"id":t.id,"subject":t.subject,"status":t.status} for t in db.scalars(q).all()]
@app.post("/api/tickets",status_code=201)
def create_ticket(data:TicketIn,db:Session=Depends(get_db),auth=Depends(identity)):
    if not auth[2]: raise HTTPException(403,"Select a customer for CSR requests")
    t=Ticket(id="TCK-"+secrets.token_hex(5),tenant_id=auth[0],customer_id=auth[2],subject=data.subject,status="open")
    db.add(t);audit(db,auth,"ticket_created",t.id);db.commit()
    return {"id":t.id,"status":"open"}
@app.post("/api/orders/drafts",status_code=201)
def create_draft(data:DraftIn,db:Session=Depends(get_db),auth=Depends(identity)):
    if auth[3]!="buyer": raise HTTPException(403,"Buyer only")
    contract=price_for(db,auth,data.product_id)
    stock=db.get(Stock,(auth[0],data.product_id))
    if not stock or stock.available<data.quantity: raise HTTPException(409,"Insufficient stock; not reserved")
    nonce=secrets.token_urlsafe(24)
    draft=Order(id="DRF-"+secrets.token_hex(7),tenant_id=auth[0],customer_id=auth[2],product_id=data.product_id,quantity=data.quantity,unit_price=contract.unit_price,status="draft",nonce_hash=hashlib.sha256(nonce.encode()).hexdigest(),created_at=now())
    db.add(draft);audit(db,auth,"draft_created",draft.id);db.commit()
    return {"draft_id":draft.id,"sku":draft.product_id,"quantity":draft.quantity,"unit_price":str(draft.unit_price),"total":str(draft.unit_price*draft.quantity),"confirmation_nonce":nonce,"notice":"Review and confirm explicitly; inventory is not reserved."}
@app.post("/api/orders/drafts/{draft_id}/confirm")
def confirm(draft_id:str,data:ConfirmIn,db:Session=Depends(get_db),auth=Depends(identity)):
    if auth[3]!="buyer": raise HTTPException(403,"Buyer only")
    prev=db.get(Idempotency,(auth[0],auth[1],data.idempotency_key))
    if prev:
        if prev.draft_id!=draft_id: raise HTTPException(409,"Idempotency key reused for different draft")
        return {"order_id":prev.order_id,"status":"confirmed","replayed":True}
    draft=db.get(Order,draft_id)
    if not draft or draft.tenant_id!=auth[0] or draft.customer_id!=auth[2]: raise HTTPException(404,"Draft not found")
    if draft.status!="draft": raise HTTPException(409,"Draft already processed")
    if not secrets.compare_digest(draft.nonce_hash or "",hashlib.sha256(data.confirmation_nonce.encode()).hexdigest()): raise HTTPException(403,"Explicit confirmation nonce invalid")
    contract=price_for(db,auth,draft.product_id)
    if contract.unit_price!=draft.unit_price: raise HTTPException(409,"Contract price changed; recreate draft")
    stock=db.get(Stock,(auth[0],draft.product_id))
    # SQL row lock on PostgreSQL and stock decrement in the same transaction.
    stock=db.execute(select(Stock).where(Stock.tenant_id==auth[0],Stock.product_id==draft.product_id).with_for_update()).scalar_one()
    if stock.available<draft.quantity: raise HTTPException(409,"Stock changed; recreate draft")
    stock.available-=draft.quantity
    draft.status="confirmed"
    draft.nonce_hash=None
    db.add(Idempotency(tenant_id=auth[0],actor_id=auth[1],idem_key=data.idempotency_key,draft_id=draft_id,order_id=draft.id))
    audit(db,auth,"order_confirmed",draft.id)
    db.commit()
    return {"order_id":draft.id,"status":"confirmed","replayed":False}
@app.get("/api/audit")
def audit_log(db:Session=Depends(get_db),auth=Depends(identity)):
    if auth[3]!="csr": raise HTTPException(403,"CSR only")
    q=select(Audit).where(Audit.tenant_id==auth[0]).order_by(Audit.timestamp.desc()).limit(100)
    return [{"actor":x.actor,"action":x.action,"resource":x.resource,"at":x.timestamp} for x in db.scalars(q).all()]
@app.get("/",response_class=HTMLResponse)
def root():
    return '<h1>LSK synthetic Order-to-Cash</h1><p>Portal: port 18473; API: <a href="/docs">OpenAPI</a></p>'
