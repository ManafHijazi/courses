"""Add first name, last name, and profile picture to User model

Revision ID: 662cd276c0af
Revises:
Create Date: 2024-10-07 12:59:05.661943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662cd276c0af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=150), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('last_name', sa.String(length=150), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=200), nullable=True))

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('first_name')
        batch_op.drop_column('last_name')
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###
