"""merge migration heads

Revision ID: e752bb360c20
Revises: 81cf855db96c, 2e12aa221227
Create Date: 2026-01-04 14:04:13.518670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e752bb360c20'
down_revision: Union[str, Sequence[str], None] = ('81cf855db96c', '2e12aa221227')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
