"""
Add a title field to the note_meta data relation

Revision ID: c71259f48a98
Revises: e2226b291035
Create Date: 2016-03-21 20:08:22.960759

"""

# revision identifiers, used by Alembic.
revision = 'c71259f48a98'
down_revision = 'e2226b291035'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('notes_meta_data',  sa.Column('title', sa.String(100), nullable=False))


def downgrade():
    op.drop_column('notes_meta_data', 'title')
