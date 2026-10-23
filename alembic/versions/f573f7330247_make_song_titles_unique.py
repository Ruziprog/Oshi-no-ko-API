
"""make song titles unique

Revision ID: f573f7330247
Revises: c1446f81d950
Create Date: 2026-10-17 10:54:26.954070
"""

from typing import Sequence, Union

from alembic import op

revision: str = "f573f7330247"
down_revision: Union[str, Sequence[str], None] = "c1446f81d950"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
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

    op.create_unique_constraint(
        "uq_songs_title",
        "songs",
        ["title"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_songs_title",
        "songs",
        type_="unique",
    )

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
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "uq_characters_name",
        "characters",
        type_="unique",
    )
