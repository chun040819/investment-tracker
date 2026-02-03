"""add drip and processed_at to corporate actions

Revision ID: 8d2e8c1a9f5a
Revises: 6f2b0c1e4b0e
Create Date: 2026-02-03 10:20:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "8d2e8c1a9f5a"
down_revision = "6f2b0c1e4b0e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE corporate_action_type_enum ADD VALUE IF NOT EXISTS 'MERGE'")
        op.execute("ALTER TYPE corporate_action_type_enum ADD VALUE IF NOT EXISTS 'DRIP'")
    elif bind.dialect.name == "sqlite":
        old_enum = sa.Enum("SPLIT", "REVERSE_SPLIT", name="corporate_action_type_enum")
        new_enum = sa.Enum("SPLIT", "REVERSE_SPLIT", "MERGE", "DRIP", name="corporate_action_type_enum")
        with op.batch_alter_table("corporate_actions") as batch_op:
            batch_op.alter_column("type", existing_type=old_enum, type_=new_enum)

    op.add_column("corporate_actions", sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("corporate_actions", "processed_at")
    # Enum value removal is not supported in PostgreSQL without recreating the type.
    # No-op for enum downgrade to avoid destructive migrations.
