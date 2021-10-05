"""Flask Security Revert All

Revision ID: f0a5a1861a3a
Revises: 74a2a87ef603
Create Date: 2021-10-04 17:10:31.340373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f0a5a1861a3a'
down_revision = '74a2a87ef603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Role_username', table_name='Role')
    op.drop_table('Role')
    op.add_column('User', sa.Column('last_login_ip', sa.String(), server_default='', nullable=True))
    op.add_column('User', sa.Column('login_count', sa.Integer(), server_default='0', nullable=True))
    op.alter_column('User', 'active',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    op.drop_constraint('User_fs_uniquifier_key', 'User', type_='unique')
    op.create_index(op.f('ix_User_active'), 'User', ['active'], unique=False)
    op.drop_column('User', 'fs_uniquifier')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('fs_uniquifier', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_User_active'), table_name='User')
    op.create_unique_constraint('User_fs_uniquifier_key', 'User', ['fs_uniquifier'])
    op.alter_column('User', 'active',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.drop_column('User', 'login_count')
    op.drop_column('User', 'last_login_ip')
    op.create_table('Role',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Role_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Role_pkey')
    )
    op.create_index('ix_Role_username', 'Role', ['username'], unique=False)
    # ### end Alembic commands ###