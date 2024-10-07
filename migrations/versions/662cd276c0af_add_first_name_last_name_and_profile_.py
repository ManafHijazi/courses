from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

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
