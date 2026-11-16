"""Pilot approval and feature flag endpoints; server-authenticated tenant boundaries."""
import os,secrets
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel,Field
from sqlalchemy import Column,String,select,update
from sqlalchemy.orm import Session
from .main import Base, app, get_db, identity, Audit, audit, now

router=APIRouter()
class Approval(Base):
    __tablename__="approvals"
    id=Column(String,primary_key=True)
    tenant_id=Column(String,nullable=False,index=True)
    customer_id=Column(String,nullable=False)
    subject=Column(String,nullable=False)
    status=Column(String,nullable=False,default="pending")
    approver=Column(String,nullable=True)
class RequestIn(BaseModel):
    subject:str=Field(min_length=5,max_length=250)
class DecideIn(BaseModel):
    decision:str=Field(pattern="^(approve|reject)$")
@router.get("/api/pilot/flags")
def flags(auth=Depends(identity)):
    return {"tenant":auth[0],"ai_enabled":os.getenv("PILOT_AI_ENABLED","false").lower()=="true","write_approvals_enabled":True}
@router.post("/api/pilot/approvals",status_code=201)
def request_approval(data:RequestIn,db:Session=Depends(get_db),auth=Depends(identity)):
    if auth[3]!="buyer": raise HTTPException(403,"Buyer request required")
    row=Approval(id="APR-"+secrets.token_hex(7),tenant_id=auth[0],customer_id=auth[2],subject=data.subject,status="pending")
    db.add(row);audit(db,auth,"approval_requested",row.id);db.commit()
    return {"id":row.id,"status":row.status}
@router.get("/api/pilot/approvals")
def approvals(db:Session=Depends(get_db),auth=Depends(identity)):
    query=select(Approval).where(Approval.tenant_id==auth[0])
    if auth[3]=="buyer": query=query.where(Approval.customer_id==auth[2])
    return [{"id":p.id,"subject":p.subject,"status":p.status,"customer_id":p.customer_id} for p in db.scalars(query).all()]
@router.post("/api/pilot/approvals/{approval_id}/decision")
def decide(approval_id:str,data:DecideIn,db:Session=Depends(get_db),auth=Depends(identity)):
    if auth[3]!="csr":raise HTTPException(403,"CSR approval required")
    new_status="approved" if data.decision=="approve" else "rejected"
    # Compare-and-set: concurrent CSR requests cannot both approve a pending request.
    result=db.execute(update(Approval).where(
        Approval.id==approval_id,
        Approval.tenant_id==auth[0],
        Approval.status=="pending",
    ).values(status=new_status,approver=auth[1]))
    if result.rowcount!=1:
        exists=db.scalar(select(Approval.id).where(Approval.id==approval_id,Approval.tenant_id==auth[0]))
        db.rollback()
        raise HTTPException(409 if exists else 404,"Already decided" if exists else "Not found")
    audit(db,auth,"approval_"+new_status,approval_id)
    db.commit()
    return {"id":approval_id,"status":new_status}
