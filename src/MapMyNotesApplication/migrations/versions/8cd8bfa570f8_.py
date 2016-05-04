"""empty message

Revision ID: 8cd8bfa570f8
Revises: 547c53ba8832
Create Date: 2016-03-05 09:48:56.898128

"""

# revision identifiers, used by Alembic.
revision = '8cd8bfa570f8'
down_revision = '547c53ba8832'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('notes', 'module_code_id')
    op.add_column('notes', sa.Column('note_meta_data_id', sa.Integer, sa.ForeignKey('notes_meta_data.id')))



def downgrade():
    op.drop_column('notes', 'note_meta_data_id')
