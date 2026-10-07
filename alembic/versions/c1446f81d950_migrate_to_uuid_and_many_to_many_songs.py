"""migrate to uuid and many to many songs

Revision ID: c1446f81d950
Revises: bb4765629904
Create Date: 2026-10-07 10:56:48.436974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1446f81d950'
down_revision: Union[str, Sequence[str], None] = 'bb4765629904'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
