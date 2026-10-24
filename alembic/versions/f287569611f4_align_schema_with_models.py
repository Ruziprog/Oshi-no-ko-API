"""align schema with models

Revision ID: <NEW_REVISION_ID>
Revises: f573f7330247
"""

from alembic import op
import sqlalchemy as sa


# Замени на revision и down_revision из созданного файла.
revision = "<NEW_REVISION_ID>"
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

    op.drop_constraint(
        "characters_name_key",
        "characters",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_characters_name",
        "characters",
        ["name"],
    )

    op.drop_constraint(
        "idols_id_fkey",
        "idols",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_idols_id_characters",
        "idols",
        "characters",
        ["id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_idols_id_characters",
        "idols",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "idols_id_fkey",
        "idols",
        "characters",
        ["id"],
        ["id"],
    )

    op.drop_constraint(
        "uq_characters_name",
        "characters",
        type_="unique",
    )
    op.create_unique_constraint(
        "characters_name_key",
        "characters",
        ["name"],
    )

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "characters",
        "role",
        existing_type=sa.String(length=50),
        nullable=False,
    )
    op.alter_column(
        "characters",
        "description",
        existing_type=sa.String(length=200),
        nullable=False,
    )