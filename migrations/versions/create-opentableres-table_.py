"""empty message

Revision ID: create-opentableres-table
Revises: create-uber-table
Create Date: 2016-11-26 02:56:19.519663

"""

# revision identifiers, used by Alembic.
revision = 'create-opentableres-table'
down_revision = 'create-uber-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('opentable',
    sa.Column('opentable_id', sa.Integer(), primary_key=True),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
    sa.Column('timestamp', sa.DateTime, server_default=sa.func.current_timestamp()),
    sa.Column('date', sa.Date()),
    sa.Column('timeslot', sa.String(length=255), nullable=False),
    sa.Column('destination', sa.String(length=255), nullable=False),
    sa.Column('partysize', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('opentable_id')
    )


def downgrade():
    op.drop_table('opentable')
