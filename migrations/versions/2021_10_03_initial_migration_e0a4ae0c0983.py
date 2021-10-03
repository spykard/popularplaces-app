"""Initial migration.

Revision ID: e0a4ae0c0983
Revises: 
Create Date: 2021-10-03 23:06:27.236000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0a4ae0c0983'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('City',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('City_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), server_default='', nullable=True),
    sa.Column('image_link', sa.String(), server_default='/static/assets/img/blank.png', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_City_name'), 'City', ['name'], unique=True)
    op.create_table('User',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('User_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.Binary(), nullable=False),
    sa.Column('first_name', sa.String(), server_default='', nullable=True),
    sa.Column('last_name', sa.String(), server_default='', nullable=True),
    sa.Column('address', sa.String(), server_default='', nullable=True),
    sa.Column('city', sa.String(), server_default='', nullable=True),
    sa.Column('country', sa.String(), server_default='', nullable=True),
    sa.Column('zipcode', sa.Integer(), server_default='0', nullable=True),
    sa.Column('about_me', sa.String(), server_default='A Strange Game. The only winning Move is not to Play. How about a nice game of Chess?', nullable=True),
    sa.Column('google_api_key', sa.String(), server_default='', nullable=True),
    sa.Column('premium_enabled', sa.Integer(), server_default='0', nullable=False),
    sa.Column('premium_notified', sa.Integer(), server_default='0', nullable=True),
    sa.Column('free_runs_remaining', sa.Integer(), server_default='5', nullable=True),
    sa.Column('settings_p1', sa.String(), server_default='', nullable=True),
    sa.Column('settings_p2', sa.String(), server_default='', nullable=True),
    sa.Column('settings_radius', sa.Integer(), server_default='180', nullable=True),
    sa.Column('settings_type1', sa.String(), server_default='Choose...', nullable=True),
    sa.Column('settings_type2', sa.String(), server_default='Choose...', nullable=True),
    sa.Column('settings_all_places', sa.Integer(), server_default='0', nullable=True),
    sa.Column('last_login', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=True),
    sa.Column('ui_color', sa.String(), server_default='blue', nullable=False),
    sa.Column('ui_theme', sa.String(), server_default='dark', nullable=False),
    sa.Column('ui_button', sa.String(), server_default='info', nullable=False),
    sa.Column('superadmin', sa.Integer(), server_default='0', nullable=False),
    sa.Column('total_runs', sa.Integer(), server_default='0', nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username', 'email')
    )
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    op.create_index(op.f('ix_User_free_runs_remaining'), 'User', ['free_runs_remaining'], unique=False)
    op.create_index(op.f('ix_User_premium_enabled'), 'User', ['premium_enabled'], unique=False)
    op.create_index(op.f('ix_User_total_runs'), 'User', ['total_runs'], unique=False)
    op.create_index(op.f('ix_User_ui_button'), 'User', ['ui_button'], unique=False)
    op.create_index(op.f('ix_User_ui_color'), 'User', ['ui_color'], unique=False)
    op.create_index(op.f('ix_User_ui_theme'), 'User', ['ui_theme'], unique=False)
    op.create_index(op.f('ix_User_username'), 'User', ['username'], unique=True)
    op.create_table('PlaceGlobal',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('PlaceGlobal_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), server_default='', nullable=False),
    sa.Column('address', sa.String(), server_default='', nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['City.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_PlaceGlobal_city_id'), 'PlaceGlobal', ['city_id'], unique=False)
    op.create_index(op.f('ix_PlaceGlobal_name'), 'PlaceGlobal', ['name'], unique=True)
    op.create_table('Search',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('Search_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('google_api_key', sa.String(), nullable=True),
    sa.Column('settings_p1', sa.String(), nullable=True),
    sa.Column('settings_p2', sa.String(), nullable=True),
    sa.Column('settings_radius', sa.Integer(), nullable=True),
    sa.Column('settings_type1', sa.String(), nullable=False),
    sa.Column('settings_type2', sa.String(), nullable=False),
    sa.Column('settings_all_places', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_Search_city'), 'Search', ['city'], unique=False)
    op.create_index(op.f('ix_Search_name'), 'Search', ['name'], unique=True)
    op.create_index(op.f('ix_Search_user_id'), 'Search', ['user_id'], unique=False)
    op.create_table('CrowdInput',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('CrowdInput_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), server_default='0', nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('global_id', sa.Integer(), server_default='0', nullable=True),
    sa.Column('input', sa.Float(precision=24), nullable=False),
    sa.ForeignKeyConstraint(['global_id'], ['PlaceGlobal.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CrowdInput_global_id'), 'CrowdInput', ['global_id'], unique=False)
    op.create_index(op.f('ix_CrowdInput_input'), 'CrowdInput', ['input'], unique=False)
    op.create_table('Place',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('Place_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), server_default='', nullable=False),
    sa.Column('address', sa.String(), server_default='', nullable=False),
    sa.Column('type_p', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('global_place', sa.Integer(), server_default='0', nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('verification', sa.String(), server_default='N/A', nullable=True),
    sa.Column('global_id', sa.Integer(), nullable=False),
    sa.Column('type_p2', sa.String(), nullable=True),
    sa.Column('type_p3', sa.String(), nullable=True),
    sa.Column('name_verified', sa.String(), nullable=True),
    sa.Column('address_verified', sa.String(), nullable=True),
    sa.Column('latitude', sa.Float(precision=53), nullable=True),
    sa.Column('longtitude', sa.Float(precision=53), nullable=True),
    sa.Column('type_verified', sa.String(), nullable=True),
    sa.Column('place_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['City.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['global_id'], ['PlaceGlobal.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Place_global_id'), 'Place', ['global_id'], unique=False)
    op.create_index(op.f('ix_Place_global_place'), 'Place', ['global_place'], unique=False)
    op.create_index(op.f('ix_Place_type_p'), 'Place', ['type_p'], unique=False)
    op.create_index(op.f('ix_Place_user_id'), 'Place', ['user_id'], unique=False)
    op.create_index(op.f('ix_Place_verification'), 'Place', ['verification'], unique=False)
    op.create_table('PlaceResult',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('PlaceResult_id_seq')"), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Float(precision=24), nullable=True),
    sa.Column('rating_num', sa.Integer(), nullable=True),
    sa.Column('time_spent', sa.String(), nullable=True),
    sa.Column('popular_times', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), server_default='0', nullable=True),
    sa.Column('search_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), server_default='', nullable=False),
    sa.Column('address', sa.String(), server_default='', nullable=False),
    sa.Column('usual_popularity', sa.Integer(), nullable=True),
    sa.Column('difference', sa.Integer(), nullable=True),
    sa.Column('global_id', sa.Integer(), server_default='0', nullable=True),
    sa.Column('live_popularity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['global_id'], ['PlaceGlobal.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['search_id'], ['Search.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_PlaceResult_global_id'), 'PlaceResult', ['global_id'], unique=False)
    op.create_index(op.f('ix_PlaceResult_search_id'), 'PlaceResult', ['search_id'], unique=False)
    op.create_index(op.f('ix_PlaceResult_user_id'), 'PlaceResult', ['user_id'], unique=False)
    # ### end Alembic commands ###

