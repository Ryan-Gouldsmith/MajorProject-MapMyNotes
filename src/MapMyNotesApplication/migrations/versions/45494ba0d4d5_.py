"""empty message

Revision ID: 45494ba0d4d5
Revises: 7151a674f83f
Create Date: 2016-03-05 15:17:43.494638

"""

# revision identifiers, used by Alembic.
revision = '45494ba0d4d5'
down_revision = '7151a674f83f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('notes_meta_data',sa.Column('date', sa.DateTime))



def downgrade():
    op.drop_column('notes_meta_data', 'date')
