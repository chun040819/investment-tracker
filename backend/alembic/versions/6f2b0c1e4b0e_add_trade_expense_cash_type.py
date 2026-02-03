"""add trade expense cash type

Revision ID: 6f2b0c1e4b0e
Revises: 4c8e2f3f6c9c
Create Date: 2026-02-03 09:30:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "6f2b0c1e4b0e"
down_revision = "4c8e2f3f6c9c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE cash_txn_type_enum ADD VALUE IF NOT EXISTS 'TRADE_EXPENSE'")
    elif bind.dialect.name == "sqlite":
        old_enum = sa.Enum(
            "DEPOSIT",
            "WITHDRAW",
            "DIVIDEND_CASH",
            "DIVIDEND_STOCK",
            "REWARD",
            "INTEREST",
            "FEE_REBATE",
            "TAX_REFUND",
            "OTHER",
            name="cash_txn_type_enum",
        )
        new_enum = sa.Enum(
            "DEPOSIT",
            "WITHDRAW",
            "DIVIDEND_CASH",
            "DIVIDEND_STOCK",
            "REWARD",
            "INTEREST",
            "FEE_REBATE",
            "TAX_REFUND",
            "TRADE_EXPENSE",
            "OTHER",
            name="cash_txn_type_enum",
        )
        with op.batch_alter_table("cash_transactions") as batch_op:
            batch_op.alter_column("type", existing_type=old_enum, type_=new_enum)


def downgrade() -> None:
    # Enum value removal is not supported in PostgreSQL without recreating the type.
    # No-op for downgrade to avoid destructive migrations.
    pass
