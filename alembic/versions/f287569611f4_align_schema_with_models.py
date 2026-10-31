"""align schema with models

Revision ID: f287569611f4
Revises: f573f7330247
"""

from alembic import op
import sqlalchemy as sa

revision = "f287569611f4"
down_revision = "f573f7330247"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "characters",
        "description",
        existing_type=sa.String(length=200),
        nullable=True,
    )
    op.alter_column(
        "characters",
        "role",
        existing_type=sa.String(length=50),
        nullable=True,
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        existing_nullable=False,
    )