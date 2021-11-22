"""create posts table

Revision ID: 93a339dd7e8b
Revises: 
Create Date: 2021-11-22 11:15:18.044142

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = '93a339dd7e8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title',sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
