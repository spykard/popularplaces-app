"""New Search Settings for Turbo Search

Revision ID: 0c3836454ec4
Revises: abe6c6c9dc3a
Create Date: 2021-10-11 17:11:59.895437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c3836454ec4'
down_revision = 'abe6c6c9dc3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Search', sa.Column('settings_wkt', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Search', 'settings_wkt')
    # ### end Alembic commands ###