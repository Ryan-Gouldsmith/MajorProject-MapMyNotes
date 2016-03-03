"""empty message

Revision ID: 6a19b5a07897
Revises: 00d6fc184a31
Create Date: 2016-03-03 17:56:53.988603

"""

# revision identifiers, used by Alembic.
revision = '6a19b5a07897'
down_revision = '00d6fc184a31'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'notes_module_codes',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('module_code', sa.String(50), nullable=False)
    )


def downgrade():
    op.drop_table('notes_module_codes')
