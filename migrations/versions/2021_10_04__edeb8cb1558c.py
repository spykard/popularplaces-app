"""empty message

Revision ID: edeb8cb1558c
Revises: f0a5a1861a3a
Create Date: 2021-10-04 17:16:11.451275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'edeb8cb1558c'
down_revision = 'f0a5a1861a3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_User_active', table_name='User')
    op.drop_column('User', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('active', postgresql.BYTEA(), autoincrement=False, nullable=False))
    op.create_index('ix_User_active', 'User', ['active'], unique=False)
    # ### end Alembic commands ###