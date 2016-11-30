"""empty message

Revision ID: create-friendmessage-table
Revises: create-partyuser-table
Create Date: 2016-10-31 01:18:02.619653

"""

# revision identifiers, used by Alembic.
revision = 'create-friendmessage-table'
down_revision = 'create-partyuser-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('friendmessage',
    sa.Column('fm_id', sa.Integer(), nullable=False),
    sa.Column('fs_id', sa.Integer(), sa.ForeignKey('friendship.fs_id'), nullable=False),
    sa.Column('sender_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=False)),
    sa.Column('message', sa.String(length=65535), nullable=False),
    sa.PrimaryKeyConstraint('fm_id')
    )

def downgrade():
    op.drop_table('friendmessage')
