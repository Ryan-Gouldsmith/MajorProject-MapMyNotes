"""empty message

Revision ID: 00d6fc184a31
Revises: None
Create Date: 2016-02-29 18:20:30.467131

"""

# revision identifiers, used by Alembic.
revision = '00d6fc184a31'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('image_path', sa.String(150), nullable=False)
    )


def downgrade():
    op.drop_table('notes')
