"""fix users.approved_by foreign key

Revision ID: 8d604b754d31
Revises: 34911a04f65c
Create Date: 2026-01-04 14:20:11.325455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d604b754d31'
down_revision: Union[str, Sequence[str], None] = '34911a04f65c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint('users_approved_by_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(
        'users_approved_by_fkey',
        'users',
        'users',
        ['approved_by'],
        ['id'],
        ondelete='SET NULL'
    )

def downgrade():
    op.drop_constraint('users_approved_by_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(
        'users_approved_by_fkey',
        'users',
        'users',
        ['approved_by'],
        ['id']
    )

