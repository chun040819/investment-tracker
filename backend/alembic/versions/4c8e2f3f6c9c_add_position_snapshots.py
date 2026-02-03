"""add position snapshots

Revision ID: 4c8e2f3f6c9c
Revises: ff5d12693867
Create Date: 2026-02-02 22:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "4c8e2f3f6c9c"
down_revision = "ff5d12693867"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "position_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("shares", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("cost_basis", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("realized_pnl", sa.Numeric(precision=18, scale=6), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("portfolio_id", "asset_id", "snapshot_date", name="uq_snapshot_portfolio_asset_date"),
    )
    op.create_index(
        "ix_snapshot_portfolio_date", "position_snapshots", ["portfolio_id", "snapshot_date"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_snapshot_portfolio_date", table_name="position_snapshots")
    op.drop_table("position_snapshots")
