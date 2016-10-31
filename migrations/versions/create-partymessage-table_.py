"""empty message

Revision ID: create-partymessage-table
Revises: create-message-table
Create Date: 2016-10-31 00:30:34.950457

"""

# revision identifiers, used by Alembic.
revision = 'create-partymessage-table'
down_revision = 'create-message-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('partymessage',
    sa.Column('pmID', sa.Integer(), nullable=False),
    sa.Column('partyID', sa.Integer(), sa.ForeignKey('party.partyID'), nullable=False),
    sa.Column('senderID', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=False)),
    sa.Column('message', sa.String(length=65535), nullable=False),
    sa.PrimaryKeyConstraint('pmID')
    )

def downgrade():
    op.drop_table('partymessage')
  
