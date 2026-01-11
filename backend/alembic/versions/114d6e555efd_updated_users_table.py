"""updated users table

Revision ID: 114d6e555efd
Revises: a463800c4ec3
Create Date: 2026-01-04 13:08:41.761180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '114d6e555efd'
down_revision: Union[str, Sequence[str], None] = 'a463800c4ec3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1 Add columns as NULLABLE first
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('status', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('approved_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('approved_by', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_logout_at', sa.DateTime(), nullable=True))

    # 2 Backfill existing rows
    op.execute("""
        UPDATE users
        SET
            is_active = TRUE,
            status = 'approved'
        WHERE is_active IS NULL
    """)

    # 3 Enforce NOT NULL after data is safe
    op.alter_column('users', 'is_active', nullable=False)
    op.alter_column('users', 'status', nullable=False)

    # 4 Password hash length fix (safe cast)
    # Backfill NULL password_hash values
    op.execute("""
        UPDATE users
        SET password_hash = 'DISABLED_ACCOUNT'
        WHERE password_hash IS NULL
    """)

    # Enforce NOT NULL
    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.TEXT(),
        type_=sa.String(length=255),
        nullable=False
    )

    # 5 Index + FK
    op.create_index('ix_users_status', 'users', ['status'], unique=False)

    op.create_foreign_key(
        'fk_users_approved_by',
        'users',
        'users',
        ['approved_by'],
        ['id'],
        ondelete='SET NULL'
    )
    
    
def downgrade() -> None:
    op.drop_constraint('fk_users_approved_by', 'users', type_='foreignkey')
    op.drop_index('ix_users_status', table_name='users')

    op.alter_column('users', 'password_hash',
        existing_type=sa.String(length=255),
        type_=sa.TEXT(),
        nullable=True
    )

    op.drop_column('users', 'last_logout_at')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'approved_by')
    op.drop_column('users', 'approved_at')
    op.drop_column('users', 'status')
    op.drop_column('users', 'is_active')
