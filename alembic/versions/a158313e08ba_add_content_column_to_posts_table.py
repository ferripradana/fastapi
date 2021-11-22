"""add content column to posts table

Revision ID: a158313e08ba
Revises: 93a339dd7e8b
Create Date: 2021-11-22 11:31:24.474651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a158313e08ba'
down_revision = '93a339dd7e8b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", 'content')
    pass
