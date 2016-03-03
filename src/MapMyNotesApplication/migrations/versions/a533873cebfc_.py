"""empty message

Revision ID: a533873cebfc
Revises: 6a19b5a07897
Create Date: 2016-03-03 17:58:46.629869

"""

# revision identifiers, used by Alembic.
revision = 'a533873cebfc'
down_revision = '6a19b5a07897'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('notes', sa.Column('module_code_id', sa.Integer, sa.ForeignKey('notes_module_codes.id')))


def downgrade():
    op.drop_column('notes', 'module_code_id')
