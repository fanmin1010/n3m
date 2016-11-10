"""empty message

Revision ID: user-mkae-username-uniq
Revises: create-friendmessage-table
Create Date: 2016-11-10 19:05:08.063321

"""

# revision identifiers, used by Alembic.
revision = 'user-mkae-username-uniq'
down_revision = 'create-friendmessage-table'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint("uq_user_name", "user", ["username"])

def downgrade():
    op.drop_constraint("uq_user_name", "user")

