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
    sa.Column('party_id', sa.Integer(), nullable=False),
    sa.Column('party_name', sa.String(length=255), nullable=False),
    sa.Column('owner_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
    sa.PrimaryKeyConstraint('party_id')
    )


def downgrade():
    op.drop_table('party')
