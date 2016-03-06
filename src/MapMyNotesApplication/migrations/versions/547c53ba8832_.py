"""empty message

Revision ID: 547c53ba8832
Revises: a533873cebfc
Create Date: 2016-03-05 09:45:30.297740

"""

# revision identifiers, used by Alembic.
revision = '547c53ba8832'
down_revision = 'a533873cebfc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'notes_meta_data',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('lecturer', sa.String(100), nullable=False),
        sa.Column('module_code_id', sa.Integer, sa.ForeignKey('notes_module_codes.id'))
    )


def downgrade():
    op.drop_table('notes_meta_data')
