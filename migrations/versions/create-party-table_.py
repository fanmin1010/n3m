"""empty message

Revision ID: create-party-table
Revises: 20e05bec257b
Create Date: 2016-10-30 22:38:32.062727

"""

# revision identifiers, used by Alembic.
revision = 'create-party-table'
down_revision = '20e05bec257b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('party',
    sa.Column('partyID', sa.Integer(), nullable=False),
    sa.Column('partyName', sa.String(length=255), nullable=False),
    sa.Column('ownerID', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.PrimaryKeyConstraint('partyID')
    )


def downgrade():
    op.drop_table('party')
