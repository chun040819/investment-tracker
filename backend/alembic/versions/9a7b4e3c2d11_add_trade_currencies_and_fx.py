"""add trade currencies and fx rate

Revision ID: 9a7b4e3c2d11
Revises: 8d2e8c1a9f5a
Create Date: 2026-02-03 10:55:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "9a7b4e3c2d11"
down_revision = "8d2e8c1a9f5a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("trades", sa.Column("asset_currency", sa.String(length=10), nullable=True))
    op.add_column("trades", sa.Column("settlement_currency", sa.String(length=10), nullable=True))
    op.add_column("trades", sa.Column("fx_rate", sa.Numeric(precision=18, scale=6), nullable=True))

    op.execute("UPDATE trades SET asset_currency = currency WHERE asset_currency IS NULL AND currency IS NOT NULL")
    op.execute(
        "UPDATE trades SET settlement_currency = currency WHERE settlement_currency IS NULL AND currency IS NOT NULL"
    )
    op.execute("UPDATE trades SET fx_rate = 1 WHERE fx_rate IS NULL AND currency IS NOT NULL")


def downgrade() -> None:
    op.drop_column("trades", "fx_rate")
    op.drop_column("trades", "settlement_currency")
    op.drop_column("trades", "asset_currency")
