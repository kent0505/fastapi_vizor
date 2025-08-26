"""changed user age type to int

Revision ID: c3883c0fe7af
Revises: a9cf8499c7fc
Create Date: 2025-08-26 15:18:51.074489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3883c0fe7af'
down_revision: Union[str, Sequence[str], None] = 'a9cf8499c7fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE "user" ALTER COLUMN age TYPE INTEGER USING age::integer')


def downgrade() -> None:
    op.alter_column(
        'user', 'age',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=True
    )
