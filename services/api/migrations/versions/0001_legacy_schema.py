"""Legacy synthetic wholesale schema.
Revision ID: 0001
Revises:
"""
from alembic import op
import sqlalchemy as sa
revision="0001"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("products",sa.Column("id",sa.String,primary_key=True),sa.Column("name",sa.String,nullable=False),sa.Column("uom",sa.String,nullable=False))
    op.create_table("contracts",sa.Column("tenant_id",sa.String,primary_key=True),sa.Column("customer_id",sa.String,primary_key=True),sa.Column("product_id",sa.String,sa.ForeignKey("products.id"),primary_key=True),sa.Column("unit_price",sa.Numeric(12,2),nullable=False))
    op.create_table("stock",sa.Column("tenant_id",sa.String,primary_key=True),sa.Column("product_id",sa.String,primary_key=True),sa.Column("available",sa.Integer,nullable=False))
    op.create_table("orders",sa.Column("id",sa.String,primary_key=True),sa.Column("tenant_id",sa.String,nullable=False,index=True),sa.Column("customer_id",sa.String,nullable=False),sa.Column("product_id",sa.String,nullable=False),sa.Column("quantity",sa.Integer,nullable=False),sa.Column("unit_price",sa.Numeric(12,2),nullable=False),sa.Column("status",sa.String,nullable=False),sa.Column("nonce_hash",sa.String),sa.Column("created_at",sa.String,nullable=False))
    op.create_table("invoices",sa.Column("id",sa.String,primary_key=True),sa.Column("tenant_id",sa.String,nullable=False,index=True),sa.Column("customer_id",sa.String,nullable=False),sa.Column("order_id",sa.String,nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("status",sa.String,nullable=False))
    op.create_table("fulfillment",sa.Column("id",sa.String,primary_key=True),sa.Column("tenant_id",sa.String,nullable=False),sa.Column("order_id",sa.String,nullable=False),sa.Column("event",sa.String,nullable=False),sa.Column("at",sa.String,nullable=False))
    op.create_table("tickets",sa.Column("id",sa.String,primary_key=True),sa.Column("tenant_id",sa.String,nullable=False),sa.Column("customer_id",sa.String,nullable=False),sa.Column("subject",sa.String,nullable=False),sa.Column("status",sa.String,nullable=False))
    op.create_table("idempotency",sa.Column("tenant_id",sa.String,primary_key=True),sa.Column("actor_id",sa.String,primary_key=True),sa.Column("idem_key",sa.String,primary_key=True),sa.Column("draft_id",sa.String,nullable=False),sa.Column("order_id",sa.String,nullable=False))
    op.create_table("audit",sa.Column("id",sa.String,primary_key=True),sa.Column("tenant_id",sa.String,nullable=False),sa.Column("actor",sa.String,nullable=False),sa.Column("action",sa.String,nullable=False),sa.Column("resource",sa.String,nullable=False),sa.Column("timestamp",sa.String,nullable=False))
def downgrade():
    for name in ["audit","idempotency","tickets","fulfillment","invoices","orders","stock","contracts","products"]:op.drop_table(name)
