"""fix users approved_by fk

Revision ID: 2e12aa221227
Revises: 81cf855db96c
Create Date: 2026-01-04 13:28:31.758644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e12aa221227'
down_revision: Union[str, Sequence[str], None] = '7eaf54298408'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint("fk_users_approved_by", "users", type_="foreignkey")
    op.create_foreign_key(
        None,
        "users",
        "users",
        ["approved_by"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    op.drop_constraint(None, "users", type_="foreignkey")
    op.create_foreign_key(
        "fk_users_approved_by",
        "users",
        "users",
        ["approved_by"],
        ["id"],
    )