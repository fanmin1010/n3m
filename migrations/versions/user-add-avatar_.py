"""empty message

Revision ID: user-add-avatar
Revises: create-friend-table
Create Date: 2016-10-27 19:20:47.097918

"""

# revision identifiers, used by Alembic.
revision = 'user-add-avatar'
down_revision = 'create-friend-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
    	 sa.Column('avatar', sa.String(length=128), nullable=False, default='dist/images/default_avatar.png'),
    )


def downgrade():
    op.drop_column('user', 'avatar')

