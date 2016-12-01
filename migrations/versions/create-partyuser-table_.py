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
    sa.Column('pu_id', sa.Integer(), nullable=False),
    sa.Column('party_id', sa.Integer(), sa.ForeignKey('party.party_id'), nullable=False),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
    sa.PrimaryKeyConstraint('pu_id')
    )


def downgrade():
    op.drop_table('partyuser')
