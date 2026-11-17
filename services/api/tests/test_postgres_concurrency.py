"""True PostgreSQL row-lock/idempotency regression. Skipped for SQLite CI."""
import os
import secrets
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
import pytest
from app.main import SessionLocal, Stock, DraftIn, ConfirmIn, create_draft, confirm

@pytest.mark.skipif(not os.environ.get("DATABASE_URL","").startswith("postgresql"),reason="Requires PostgreSQL row locks")
def test_concurrent_confirmation_prevents_double_decrement():
    auth=("tenant-a","buyer-a","customer-a","buyer")
    with SessionLocal() as db:
        before=db.get(Stock,("tenant-a","MOL-10")).available
        draft=create_draft(DraftIn(product_id="MOL-10",quantity=1),db=db,auth=auth)
        draft_id=draft["draft_id"]
        nonce=draft["confirmation_nonce"]
    def attempt(key):
        with SessionLocal() as session:
            try:
                answer=confirm(draft_id,ConfirmIn(confirmation_nonce=nonce,idempotency_key=key),db=session,auth=auth)
                return answer["status"]
            except HTTPException as exc:
                return str(exc.status_code)
    with ThreadPoolExecutor(max_workers=2) as pool:
        attempts=list(pool.map(attempt,["parallel-A-"+secrets.token_hex(8),"parallel-B-"+secrets.token_hex(8)]))
    assert sorted(attempts)==["409","confirmed"],attempts
    with SessionLocal() as db:
        after=db.get(Stock,("tenant-a","MOL-10")).available
    assert before-after==1,{"before":before,"after":after}
