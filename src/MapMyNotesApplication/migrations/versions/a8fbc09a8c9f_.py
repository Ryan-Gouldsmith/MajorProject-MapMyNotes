"""Update the notes relation to store a foreign key to the user id

Revision ID: a8fbc09a8c9f
Revises: a3ea868e4fe6
Create Date: 2016-03-29 12:32:31.864611

"""

# revision identifiers, used by Alembic.
revision = 'a8fbc09a8c9f'
down_revision = 'a3ea868e4fe6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('notes', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')))


def downgrade():
    op.drop_column('notes', 'user_id')
