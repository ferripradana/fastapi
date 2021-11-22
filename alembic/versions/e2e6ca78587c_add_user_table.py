"""add user table

Revision ID: e2e6ca78587c
Revises: a158313e08ba
Create Date: 2021-11-22 11:37:29.956202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2e6ca78587c'
down_revision = 'a158313e08ba'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False ),
        sa.Column('password', sa.String(), nullable=False), 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
