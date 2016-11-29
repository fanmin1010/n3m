"""empty message

Revision ID: cleanuber
Revises: part-add-constraint
Create Date: 2016-11-28 23:20:58.382766

"""

# revision identifiers, used by Alembic.
revision = 'cleanuber'
down_revision = 'part-add-constraint'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('uber')
    op.drop_table('opentable')
    op.execute("""
        INSERT INTO "user" ("email", "password", "username", "pgp_key", "avatar") VALUES ('uber_aid@party.io', 'uber_aid', 'uberpwd', '123','dist/images/uber.png')
    """)
    op.execute("""
        INSERT INTO "user" ("email", "password", "username", "pgp_key", "avatar") VALUES ('opentable_aid@party.io', 'opentable_aid', 'oppwd', '123','dist/images/opentable.png')
    """)



def downgrade():
    pass
