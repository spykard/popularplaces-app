"""New Search Settings for Turbo Search

Revision ID: abe6c6c9dc3a
Revises: 1f4b2a944c59
Create Date: 2021-10-11 12:12:46.459875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abe6c6c9dc3a'
down_revision = '1f4b2a944c59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Search', sa.Column('settings_osm_id', sa.BigInteger(), nullable=True))
    op.add_column('Search', sa.Column('settings_area_id', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Search', 'settings_area_id')
    op.drop_column('Search', 'settings_osm_id')
    # ### end Alembic commands ###
