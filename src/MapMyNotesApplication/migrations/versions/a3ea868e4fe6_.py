"""empty message

Revision ID: a3ea868e4fe6
Revises: c71259f48a98
Create Date: 2016-03-28 15:54:49.692343

"""

# revision identifiers, used by Alembic.
revision = 'a3ea868e4fe6'
down_revision = 'c71259f48a98'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('notes',sa.Column('calendar_url', sa.String(256)))



def downgrade():
    op.drop_column('notes', 'calendar_url')
