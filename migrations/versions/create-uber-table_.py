"""empty message

Revision ID: create-uber-table
Revises: user-mkae-username-uniq
Create Date: 2016-11-26 02:55:46.699540

"""

# revision identifiers, used by Alembic.
revision = 'create-uber-table'
down_revision = 'user-mkae-username-uniq'

from alembic import op
import sqlalchemy as sa


def upgrade():
        op.create_table('uber',
        sa.Column('uber_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('duration', sa.Interval()),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('destination', sa.String(length=255), nullable=False),
        sa.Column('cost', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('uber_id')
        )


def downgrade():
    op.drop_table('uber')
