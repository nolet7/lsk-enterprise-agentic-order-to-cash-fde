"""Regression guard for the proof-of-concept AI read-only tool boundary."""
from app.agent import registry
from app.main import DEMO_TOKENS, SessionLocal

def test_agent_registers_only_read_tools():
    with SessionLocal() as db:
        names={tool.name for tool in registry(db,DEMO_TOKENS["demo-buyer-a"])}
    assert names == {
        "lookup_catalog", "lookup_orders", "lookup_order",
        "lookup_invoices", "lookup_support", "search_policy"
    }
    assert not any(word in name for name in names for word in (
        "confirm", "create", "refund", "update", "delete", "execute_sql"
    ))
