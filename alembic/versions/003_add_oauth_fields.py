"""Add OAuth provider fields

Revision ID: 003
Revises: 002
Create Date: 2024-12-04 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    """Add oauth_provider and oauth_provider_id columns to users table."""
    op.add_column('users', sa.Column('oauth_provider', sa.String(), nullable=True))
    op.add_column('users', sa.Column('oauth_provider_id', sa.String(), nullable=True))
    
    # Create index for faster OAuth lookups
    op.create_index('ix_users_oauth_provider_id', 'users', ['oauth_provider', 'oauth_provider_id'])


def downgrade():
    """Remove oauth_provider and oauth_provider_id columns from users table."""
    op.drop_index('ix_users_oauth_provider_id', table_name='users')
    op.drop_column('users', 'oauth_provider_id')
    op.drop_column('users', 'oauth_provider')
