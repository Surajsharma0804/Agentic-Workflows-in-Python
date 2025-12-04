"""Add password reset fields

Revision ID: 002
Revises: 001
Create Date: 2024-12-04 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    """Add reset_token and reset_token_expires columns to users table."""
    op.add_column('users', sa.Column('reset_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(), nullable=True))


def downgrade():
    """Remove reset_token and reset_token_expires columns from users table."""
    op.drop_column('users', 'reset_token_expires')
    op.drop_column('users', 'reset_token')
