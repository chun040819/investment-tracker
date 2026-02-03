"""add tax lots

Revision ID: ab31c1f5d6e2
Revises: 9a7b4e3c2d11
Create Date: 2026-02-03 11:25:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "ab31c1f5d6e2"
down_revision = "9a7b4e3c2d11"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tax_lots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("lot_date", sa.Date(), nullable=False),
        sa.Column("original_shares", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("remaining_shares", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("cost_per_share", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("total_cost", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("asset_currency", sa.String(length=10), nullable=True),
        sa.Column("settlement_currency", sa.String(length=10), nullable=True),
        sa.Column("fx_rate", sa.Numeric(precision=18, scale=6), nullable=True),
        sa.Column("source", sa.String(length=20), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("portfolio_id", "asset_id", "source", "source_id", name="uq_tax_lot_source"),
    )
    op.create_index(
        "ix_tax_lot_portfolio_asset_date", "tax_lots", ["portfolio_id", "asset_id", "lot_date"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_tax_lot_portfolio_asset_date", table_name="tax_lots")
    op.drop_table("tax_lots")
