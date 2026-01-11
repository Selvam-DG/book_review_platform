"""remove legacy indexes

Revision ID: 34911a04f65c
Revises: e752bb360c20
Create Date: 2026-01-04 14:18:17.000616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34911a04f65c'
down_revision: Union[str, Sequence[str], None] = 'e752bb360c20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove legacy / unused indexes
    op.drop_index('idx_books_author', table_name='books')
    op.drop_index('idx_books_genre', table_name='books')

    op.drop_index('idx_reviews_book', table_name='reviews')
    op.drop_index('idx_reviews_rating', table_name='reviews')
    op.drop_index('idx_reviews_user', table_name='reviews')

    op.drop_index('ix_refresh_tokens_expires_at', table_name='refresh_tokens')

    # ### end Alembic commands ###


def downgrade() -> None:
    # Restore legacy indexes if rollback is required
    op.create_index('idx_books_author', 'books', ['author_id'], unique=False)
    op.create_index('idx_books_genre', 'books', ['genre_id'], unique=False)

    op.create_index('idx_reviews_book', 'reviews', ['book_id'], unique=False)
    op.create_index('idx_reviews_rating', 'reviews', ['rating'], unique=False)
    op.create_index('idx_reviews_user', 'reviews', ['user_id'], unique=False)

    op.create_index(
        'ix_refresh_tokens_expires_at',
        'refresh_tokens',
        ['expires_at'],
        unique=False
    )

    # ### end Alembic commands ###
