"""empty message

Revision ID: table-name-and-modification
Revises: ed657e16ce20
Create Date: 2016-10-13 01:48:38.484806

"""

# revision identifiers, used by Alembic.
revision = 'table-name-and-modification'
down_revision = 'ed657e16ce20'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('foo',
    sa.Column('foo_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('foo_id')
    )


def downgrade():
    op.drop_table('foo')
