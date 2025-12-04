"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-12-04 20:48:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create initial tables."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, default=False),
        sa.Column('role', sa.String(), nullable=True, default='user'),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade():
    """Drop tables."""
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
