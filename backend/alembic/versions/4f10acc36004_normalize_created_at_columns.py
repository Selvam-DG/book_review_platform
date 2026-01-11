"""normalize created_at columns

Revision ID: 81cf855db96c
Revises: e62813b1125b
Create Date: 2026-01-04 13:28:21.412116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81cf855db96c'
down_revision: Union[str, Sequence[str], None] = 'e62813b1125b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #  Backfill NULL created_at values safely
    op.execute("""
        UPDATE authors SET created_at = NOW() WHERE created_at IS NULL;
        UPDATE books SET created_at = NOW() WHERE created_at IS NULL;
        UPDATE genres SET created_at = NOW() WHERE created_at IS NULL;
        UPDATE reviews SET created_at = NOW() WHERE created_at IS NULL;
        UPDATE users SET created_at = NOW() WHERE created_at IS NULL;
    """)

    #  Enforce NOT NULL constraints
    op.alter_column('authors', 'created_at', nullable=False)
    op.alter_column('books', 'created_at', nullable=False)
    op.alter_column('genres', 'created_at', nullable=False)
    op.alter_column('reviews', 'created_at', nullable=False)
    op.alter_column('users', 'created_at', nullable=False)


def downgrade() -> None:
    # Relax NOT NULL constraints (no data loss)
    op.alter_column('users', 'created_at', nullable=True)
    op.alter_column('reviews', 'created_at', nullable=True)
    op.alter_column('genres', 'created_at', nullable=True)
    op.alter_column('books', 'created_at', nullable=True)
    op.alter_column('authors', 'created_at', nullable=True)
