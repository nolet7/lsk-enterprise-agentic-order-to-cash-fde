"""Pilot approvals. Revision ID 0002."""
from alembic import op
import sqlalchemy as sa
revision="0002"
down_revision="0001"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("approvals",sa.Column("id",sa.String,primary_key=True),sa.Column("tenant_id",sa.String,nullable=False,index=True),sa.Column("customer_id",sa.String,nullable=False),sa.Column("subject",sa.String,nullable=False),sa.Column("status",sa.String,nullable=False),sa.Column("approver",sa.String))
def downgrade():op.drop_table("approvals")
