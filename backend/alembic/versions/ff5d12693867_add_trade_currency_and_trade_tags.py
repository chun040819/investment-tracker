"""add trade currency and trade tags

Revision ID: ff5d12693867
Revises: 321bd3024a7a
Create Date: 2026-02-02 18:25:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "ff5d12693867"
down_revision = "321bd3024a7a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("trades", sa.Column("currency", sa.String(length=10), nullable=True))
    op.create_table(
        "trade_tags",
        sa.Column("trade_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trade_id"], ["trades.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("trade_id", "tag_id"),
    )


def downgrade() -> None:
    op.drop_table("trade_tags")
    op.drop_column("trades", "currency")
