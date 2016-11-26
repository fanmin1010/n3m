"""empty message

Revision ID: party-add-avatar
Revises: create-opentableres-table
Create Date: 2016-11-26 19:35:12.593129

"""

# revision identifiers, used by Alembic.
revision = 'party-add-avatar'
down_revision = 'create-opentableres-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
      'party',
      sa.Column('avatar', sa.String(length=128), nullable=False, default='dist/images/default_team.png')
      )

def downgrade():
    op.drop_column('party', 'avatar')
