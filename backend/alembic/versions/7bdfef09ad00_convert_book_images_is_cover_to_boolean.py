"""convert book_images.is_cover to boolean

Revision ID: e62813b1125b
Revises: 7eaf54298408
Create Date: 2026-01-04 13:28:10.399524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e62813b1125b'
down_revision: Union[str, Sequence[str], None] = '7eaf54298408'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convert INTEGER -> BOOLEAN with explicit casting
    op.execute("""
        ALTER TABLE book_images
        ALTER COLUMN is_cover
        TYPE BOOLEAN
        USING CASE
            WHEN is_cover IS NULL THEN FALSE
            WHEN is_cover = 1 THEN TRUE
            ELSE FALSE
        END
    """)

    # Optional but recommended: enforce NOT NULL
    op.alter_column(
        'book_images',
        'is_cover',
        nullable=False
    )

def downgrade() -> None:
    # Convert BOOLEAN -> INTEGER safely
    op.execute("""
        ALTER TABLE book_images
        ALTER COLUMN is_cover
        TYPE INTEGER
        USING CASE
            WHEN is_cover THEN 1
            ELSE 0
        END
    """)

