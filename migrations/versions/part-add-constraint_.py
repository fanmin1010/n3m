"""empty message

Revision ID: part-add-constraint
Revises: party-add-avatar
Create Date: 2016-11-26 22:42:47.015611

"""

# revision identifiers, used by Alembic.
revision = 'part-add-constraint'
down_revision = 'party-add-avatar'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint("uq_party_name", "party", ["partyName","ownerID"])


def downgrade():
    op.drop_constraint("uq_party_name", "party")
