"""updated reviews table

Revision ID: 7eaf54298408
Revises: 0458c46a7b50
Create Date: 2026-01-04 13:21:43.353344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7eaf54298408'
down_revision: Union[str, Sequence[str], None] = '0458c46a7b50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #  Backfill NULL values safely
    op.execute("""
        UPDATE reviews
        SET
            rating = COALESCE(rating, 1),
            helpful_count = COALESCE(helpful_count, 0),
            created_at = COALESCE(created_at, NOW())
    """)

    #  Enforce NOT NULL after data is safe
    op.alter_column('reviews', 'rating', nullable=False)
    op.alter_column('reviews', 'helpful_count', nullable=False)
    op.alter_column('reviews', 'created_at', nullable=False)

    #  Remove duplicate reviews BEFORE unique constraint
    op.execute("""
        DELETE FROM reviews r1
        USING reviews r2
        WHERE
            r1.id > r2.id
            AND r1.book_id = r2.book_id
            AND r1.user_id = r2.user_id
    """)

    #  Add unique constraint
    op.drop_constraint(
        'reviews_book_id_user_id_key',
        'reviews',
        type_='unique'
    )

    op.create_unique_constraint(
        'unique_book_user_review',
        'reviews',
        ['book_id', 'user_id']
    )

def downgrade() -> None:
    op.drop_constraint('unique_book_user_review', 'reviews', type_='unique')

    op.create_unique_constraint(
        'reviews_book_id_user_id_key',
        'reviews',
        ['book_id', 'user_id']
    )

    op.alter_column('reviews', 'created_at', nullable=True)
    op.alter_column('reviews', 'helpful_count', nullable=True)
    op.alter_column('reviews', 'rating', nullable=True)
