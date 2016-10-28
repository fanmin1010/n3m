"""empty message

Revision ID: add-friendship-table
Revises: user-add-avatar
Create Date: 2016-10-28 17:25:26.948578

"""

# revision identifiers, used by Alembic.
revision = 'add-friendship-table'
down_revision = 'user-add-avatar'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('friendship',
    sa.Column('fs_id', sa.Integer(), nullable=False),
    sa.Column('friender', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('friendee', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('est_time', sa.DateTime, nullable = False, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('fs_id'),
    sa.UniqueConstraint('friender', 'friendee')
    )


def downgrade():
    op.drop_table('friendship')
