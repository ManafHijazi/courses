"""Add first name, last name, and profile picture to User model

Revision ID: 662cd276c0af
Revises:
Create Date: 2024-10-07 12:59:05.661943

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '662cd276c0af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if column already exists
    inspector = inspect(op.get_bind())
    columns = [column['name'] for column in inspector.get_columns('user')]
    if 'first_name' not in columns:
        op.add_column('user', sa.Column('first_name', sa.String(length=150), nullable=False, server_default=''))
    if 'last_name' not in columns:
        op.add_column('user', sa.Column('last_name', sa.String(length=150), nullable=False, server_default=''))
    if 'profile_picture' not in columns:
        op.add_column('user', sa.Column('profile_picture', sa.String(length=150), nullable=True))

def downgrade():
    op.drop_column('user', 'first_name')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'profile_picture')

    # ### end Alembic commands ###
