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
        INSERT INTO "user" ("email", "username", "password", "pgp_key", "avatar") VALUES ('uber_aid@party.io', 'uber_aid', 'uberpwd', '123','dist/images/uber.png')
    """)
    op.execute("""
        INSERT INTO "user" ("email", "username", "password", "pgp_key", "avatar") VALUES ('opentable_aid@party.io', 'opentable_aid', 'opentablepwd', '123','dist/images/opentable.png')
    """)



def downgrade():
    op.create_table('uber',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('userID', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('timestamp', sa.DateTime, server_default=sa.func.current_timestamp()),
    sa.Column('duration', sa.Interval()),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('destination', sa.String(length=255), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opentable',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('userID', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('timestamp', sa.DateTime, server_default=sa.func.current_timestamp()),
    sa.Column('date', sa.Date()),
    sa.Column('timeslot', sa.String(length=255), nullable=False),
    sa.Column('destination', sa.String(length=255), nullable=False),
    sa.Column('partysize', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute("""
        delete from "user" where email = 'opentable_aid@party.io' or email = 'uber_aid@party.io'
    """)
