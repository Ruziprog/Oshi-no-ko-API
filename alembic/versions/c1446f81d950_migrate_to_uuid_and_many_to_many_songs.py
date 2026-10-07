"""migrate to uuid and many to many songs

Revision ID: c1446f81d950
Revises: bb4765629904
Create Date: 2026-10-07 10:56:48.436974
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c1446f81d950"
down_revision: Union[str, Sequence[str], None] = "bb4765629904"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # 1. Create temporary UUID columns
    # ---------------------------------------------------------

    op.add_column(
        "users",
        sa.Column(
            "new_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    op.add_column(
        "characters",
        sa.Column(
            "new_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    op.add_column(
        "songs",
        sa.Column(
            "new_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    # Generate UUIDs for existing rows
    op.execute(
        sa.text(
            "UPDATE users SET new_id = gen_random_uuid()"
        )
    )

    op.execute(
        sa.text(
            "UPDATE characters SET new_id = gen_random_uuid()"
        )
    )

    op.execute(
        sa.text(
            "UPDATE songs SET new_id = gen_random_uuid()"
        )
    )

    # ---------------------------------------------------------
    # 2. Save old integer IDs
    # ---------------------------------------------------------

    op.add_column(
        "users",
        sa.Column("old_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "characters",
        sa.Column("old_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "songs",
        sa.Column("old_id", sa.Integer(), nullable=True),
    )

    op.execute(
        sa.text(
            "UPDATE users SET old_id = id"
        )
    )

    op.execute(
        sa.text(
            "UPDATE characters SET old_id = id"
        )
    )

    op.execute(
        sa.text(
            "UPDATE songs SET old_id = id"
        )
    )

    # ---------------------------------------------------------
    # 3. Save old song -> idol relationships
    # ---------------------------------------------------------

    op.create_table(
        "_song_idol_mapping",
        sa.Column(
            "song_old_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "idol_old_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.execute(
        sa.text(
            """
            INSERT INTO _song_idol_mapping (
                song_old_id,
                idol_old_id
            )
            SELECT
                id,
                idol_id
            FROM songs
            """
        )
    )

    # ---------------------------------------------------------
    # 4. Remove old foreign keys
    # ---------------------------------------------------------

    op.drop_constraint(
        "songs_idol_id_fkey",
        "songs",
        type_="foreignkey",
    )

    op.drop_constraint(
        "idols_id_fkey",
        "idols",
        type_="foreignkey",
    )

    # ---------------------------------------------------------
    # 5. Remove old primary keys
    # ---------------------------------------------------------

    op.drop_constraint(
        "songs_pkey",
        "songs",
        type_="primary",
    )

    op.drop_constraint(
        "idols_pkey",
        "idols",
        type_="primary",
    )

    op.drop_constraint(
        "characters_pkey",
        "characters",
        type_="primary",
    )

    op.drop_constraint(
        "users_pkey",
        "users",
        type_="primary",
    )

    # ---------------------------------------------------------
    # 6. Replace users.id with UUID
    # ---------------------------------------------------------

    op.drop_column("users", "id")

    op.alter_column(
        "users",
        "new_id",
        new_column_name="id",
        nullable=False,
    )

    op.create_primary_key(
        "users_pkey",
        "users",
        ["id"],
    )

    # ---------------------------------------------------------
    # 7. Replace characters.id with UUID
    # ---------------------------------------------------------

    op.drop_column("characters", "id")

    op.alter_column(
        "characters",
        "new_id",
        new_column_name="id",
        nullable=False,
    )

    op.create_primary_key(
        "characters_pkey",
        "characters",
        ["id"],
    )

    # ---------------------------------------------------------
    # 8. Replace songs.id with UUID
    # ---------------------------------------------------------

    op.drop_column("songs", "id")

    op.alter_column(
        "songs",
        "new_id",
        new_column_name="id",
        nullable=False,
    )

    # IMPORTANT:
    # songs.id must have a primary key before song_idols
    # creates a foreign key referencing it.
    op.create_primary_key(
        "songs_pkey",
        "songs",
        ["id"],
    )

    # ---------------------------------------------------------
    # 9. Convert idols.id to UUID
    # ---------------------------------------------------------

    op.add_column(
        "idols",
        sa.Column(
            "new_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    # Match idols.id (old integer)
    # with characters.old_id and copy the UUID.
    op.execute(
        sa.text(
            """
            UPDATE idols AS i
            SET new_id = c.id
            FROM characters AS c
            WHERE i.id = c.old_id
            """
        )
    )

    op.drop_column(
        "idols",
        "id",
    )

    op.alter_column(
        "idols",
        "new_id",
        new_column_name="id",
        nullable=False,
    )

    op.create_primary_key(
        "idols_pkey",
        "idols",
        ["id"],
    )

    # ---------------------------------------------------------
    # 10. Recreate idols -> characters FK
    # ---------------------------------------------------------

    op.create_foreign_key(
        "idols_id_fkey",
        "idols",
        "characters",
        ["id"],
        ["id"],
        ondelete="CASCADE",
    )

    # ---------------------------------------------------------
    # 11. Create many-to-many table
    # ---------------------------------------------------------

    op.create_table(
        "song_idols",

        sa.Column(
            "song_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "idol_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint(
            "song_id",
            "idol_id",
        ),

        sa.ForeignKeyConstraint(
            ["song_id"],
            ["songs.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["idol_id"],
            ["idols.id"],
            ondelete="CASCADE",
        ),
    )

    # ---------------------------------------------------------
    # 12. Restore song -> idol relationships
    # ---------------------------------------------------------

    op.execute(
        sa.text(
            """
            INSERT INTO song_idols (
                song_id,
                idol_id
            )
            SELECT
                s.id,
                i.id
            FROM _song_idol_mapping AS m

            JOIN songs AS s
                ON s.old_id = m.song_old_id

            JOIN characters AS c
                ON c.old_id = m.idol_old_id

            JOIN idols AS i
                ON i.id = c.id
            """
        )
    )

    # ---------------------------------------------------------
    # 13. Remove old songs.idol_id
    # ---------------------------------------------------------

    op.drop_column(
        "songs",
        "idol_id",
    )

    # ---------------------------------------------------------
    # 14. Remove temporary columns
    # ---------------------------------------------------------

    op.drop_column(
        "users",
        "old_id",
    )

    op.drop_column(
        "characters",
        "old_id",
    )

    op.drop_column(
        "songs",
        "old_id",
    )

    op.drop_table(
        "_song_idol_mapping",
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Downgrade is intentionally disabled for this data migration."
    )