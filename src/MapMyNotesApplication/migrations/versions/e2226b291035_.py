"""empty message

Revision ID: e2226b291035
Revises: 45494ba0d4d5
Create Date: 2016-03-10 12:09:31.496461

"""

# revision identifiers, used by Alembic.
revision = 'e2226b291035'
down_revision = '45494ba0d4d5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email_address', sa.String(100), nullable=False)
    )


def downgrade():
    op.drop_table('users')
