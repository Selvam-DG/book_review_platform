"""create audit logs and book suggestions tables

Revision ID: a463800c4ec3
Revises: 0319b9f82600
Create Date: 2026-01-04 13:02:59.836072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a463800c4ec3'
down_revision: Union[str, Sequence[str], None] = '0319b9f82600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('actor_user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('metadata', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['actor_user_id'], ['users.id'], ondelete='SET NULL'),
    )

    op.create_table(
        'book_suggestions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('suggested_by_user_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('author_name', sa.String(length=255), nullable=True),
        sa.Column('genre_name', sa.String(length=100), nullable=True),
        sa.Column('image_object_name', sa.String(length=255), nullable=True),
        sa.Column('image_object_url', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['suggested_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id']),
    )

    op.create_index(
        'ix_book_suggestions_status',
        'book_suggestions',
        ['status'],
        unique=False
    )

def downgrade() -> None:
    op.drop_index('ix_book_suggestions_status', table_name='book_suggestions')
    op.drop_table('book_suggestions')
    op.drop_table('audit_logs')
