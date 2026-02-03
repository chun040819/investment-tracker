"""add tags and asset tags

Revision ID: 321bd3024a7a
Revises: 07e5ac06c318
Create Date: 2026-02-02 18:10:48.442493
"""

from alembic import op
import sqlalchemy as sa

revision = "321bd3024a7a"
down_revision = "07e5ac06c318"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_tag_name"),
    )
    op.create_table(
        "asset_tags",
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("asset_id", "tag_id"),
    )


def downgrade() -> None:
    op.drop_table("asset_tags")
    op.drop_table("tags")
