"""empty message

Revision ID: user-add-pgp-username
Revises: table-name-and-modification
Create Date: 2016-10-21 00:09:13.935761

"""

# revision identifiers, used by Alembic.
revision = 'user-add-pgp-username'
down_revision = 'table-name-and-modification'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
    	 sa.Column('username', sa.String(length=255), nullable=True),
    )
    op.execute("""
        UPDATE "user"
        SET username = email
    """)
    op.alter_column('user', 'username', nullable=False)


def downgrade():
    op.drop_column('user', 'username')

