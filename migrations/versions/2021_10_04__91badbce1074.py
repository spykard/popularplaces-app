"""empty message

Revision ID: 91badbce1074
Revises: 43a89e836135
Create Date: 2021-10-04 17:23:26.638444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91badbce1074'
down_revision = '43a89e836135'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_User_active', table_name='User')
    op.drop_index('ix_User_premium_enabled', table_name='User')
    op.drop_index('ix_User_superadmin', table_name='User')
    op.drop_index('ix_User_total_runs', table_name='User')
    op.drop_column('User', 'last_login_ip')
    op.drop_column('User', 'login_count')
    op.drop_column('User', 'premium_notified')
    op.drop_column('User', 'active')
    op.drop_column('User', 'total_runs')
    op.drop_column('User', 'premium_enabled')
    op.drop_column('User', 'superadmin')
    op.drop_column('User', 'last_login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('last_login', sa.DATE(), server_default=sa.text('CURRENT_DATE'), autoincrement=False, nullable=True))
    op.add_column('User', sa.Column('superadmin', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))
    op.add_column('User', sa.Column('premium_enabled', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))
    op.add_column('User', sa.Column('total_runs', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True))
    op.add_column('User', sa.Column('active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.add_column('User', sa.Column('premium_notified', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True))
    op.add_column('User', sa.Column('login_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True))
    op.add_column('User', sa.Column('last_login_ip', sa.VARCHAR(), server_default=sa.text("''::character varying"), autoincrement=False, nullable=True))
    op.create_index('ix_User_total_runs', 'User', ['total_runs'], unique=False)
    op.create_index('ix_User_superadmin', 'User', ['superadmin'], unique=False)
    op.create_index('ix_User_premium_enabled', 'User', ['premium_enabled'], unique=False)
    op.create_index('ix_User_active', 'User', ['active'], unique=False)
    # ### end Alembic commands ###