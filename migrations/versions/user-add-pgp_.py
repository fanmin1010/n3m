"""empty message

Revision ID: user-add-pgp
Revises: user-add-pgp-username
Create Date: 2016-10-21 00:20:54.827018

"""

# revision identifiers, used by Alembic.
revision = 'user-add-pgp'
down_revision = 'user-add-pgp-username'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
    	 sa.Column('pgp_key', sa.String(length=510), nullable=True),
    )


def downgrade():
    op.drop_column('user', 'pgp_key')

