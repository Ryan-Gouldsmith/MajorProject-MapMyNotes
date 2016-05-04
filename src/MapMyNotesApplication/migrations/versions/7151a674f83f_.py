"""empty message

Revision ID: 7151a674f83f
Revises: 8cd8bfa570f8
Create Date: 2016-03-05 12:03:50.687628

"""

# revision identifiers, used by Alembic.
revision = '7151a674f83f'
down_revision = '8cd8bfa570f8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('notes_meta_data',sa.Column('location', sa.String(100)))


def downgrade():
    op.drop_column('notes_meta_data', 'location')
