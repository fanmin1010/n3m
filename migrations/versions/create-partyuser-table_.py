"""empty message

Revision ID: create-partyuser-table
Revises: create-partymessage-table
Create Date: 2016-10-31 01:09:27.376402

"""

# revision identifiers, used by Alembic.
revision = 'create-partyuser-table'
down_revision = 'create-partymessage-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('partyuser',
    sa.Column('puID', sa.Integer(), nullable=False),
    sa.Column('partyID', sa.Integer(), sa.ForeignKey('party.partyID'), nullable=False),
    sa.Column('userID', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.PrimaryKeyConstraint('puID')
    )


def downgrade():
    op.drop_table('partyuser')
