# -*- encoding: utf-8 -*-
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Binary, Boolean, Column, Integer, BigInteger, String, DateTime, ForeignKey, Float, Sequence, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
import jwt

from app import db, login_manager

from app.base.util import hash_pass

# -- #
table_city_id_seq = Sequence('City_id_seq')

class City(db.Model):

    __tablename__ = 'City'

    id = Column(Integer, table_city_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_city_id_seq.next_value())  
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, server_default="") 
    image_link = Column(String, nullable=False, server_default='/static/assets/img/blank.png')  
    UniqueConstraint(name) 

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id) 


# -- #
table_crowdinput_id_seq = Sequence('CrowdInput_id_seq')

class CrowdInput(db.Model):

    __tablename__ = 'CrowdInput'

    id = Column(Integer, table_crowdinput_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_crowdinput_id_seq.next_value()) 
    user_id = Column(Integer, ForeignKey('User.id', ondelete="SET NULL", onupdate="SET NULL"), server_default='0')
    time = Column(DateTime, server_default=func.current_timestamp()) 
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id', ondelete="SET NULL", onupdate="SET NULL"), index=True, server_default='0')
    input = Column(Float(24), nullable=False, index=True)                 

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id) 


# -- #
table_place_id_seq = Sequence('Place_id_seq')

class Place(db.Model):

    __tablename__ = 'Place'

    id = Column(Integer, table_place_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_place_id_seq.next_value())
    name = Column(String, nullable=False, server_default="")
    address = Column(String, nullable=False, server_default="")
    type_p = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    global_place = Column(Integer, nullable=False, index=True, server_default='0')   
    city_id = Column(Integer, ForeignKey('City.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False) 
    time = Column(DateTime, server_default=func.current_timestamp())
    verification = Column(String, index=True, server_default='N/A')  
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)  
    type_p2 = Column(String)
    type_p3 = Column(String)                   

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)


# -- #
table_placeglobal_id_seq = Sequence('PlaceGlobal_id_seq')

class PlaceGlobal(db.Model):

    __tablename__ = 'PlaceGlobal'

    id = Column(Integer, table_placeglobal_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_placeglobal_id_seq.next_value()) 
    name = Column(String, nullable=False, unique=True, index=True, server_default="")       
    address = Column(String, server_default="")
    time = Column(DateTime, server_default=func.current_timestamp()) 
    city_id = Column(Integer, ForeignKey('City.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    name_verified = Column(String)           
    address_verified = Column(String)
    latitude = Column(Float(53))
    longtitude = Column(Float(53))                  
    type_verified = Column(String)
    place_id = Column(String)     
    UniqueConstraint(name)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)   


# -- #
table_placeresult_id_seq = Sequence('PlaceResult_id_seq')

class PlaceResult(db.Model):

    __tablename__ = 'PlaceResult'

    id = Column(Integer, table_placeresult_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_placeresult_id_seq.next_value()) 
    rating = Column(Float(24))
    rating_num = Column(Integer)
    time_spent = Column(String) 
    popular_times = Column(String)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="SET NULL", onupdate="SET NULL"), index=True, server_default='0')
    search_id = Column(Integer, ForeignKey('Search.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False, server_default="")       
    address = Column(String, nullable=False, server_default="")    
    usual_popularity = Column(Integer)
    difference = Column(Integer)
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id', ondelete="SET NULL", onupdate="SET NULL"), index=True, server_default='0')
    live_popularity = Column(Integer)                  

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id) 


# -- #
table_search_id_seq = Sequence('Search_id_seq')

class Search(db.Model):

    __tablename__ = 'Search'

    id = Column(Integer, table_search_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_search_id_seq.next_value())
    time = Column(DateTime, server_default=func.current_timestamp())     
    google_api_key = Column(String)
    settings_p1 = Column(String)
    settings_p2 = Column(String)
    settings_radius = Column(Integer)
    settings_type1 = Column(String, nullable=False)
    settings_type2 = Column(String, nullable=False)    
    settings_all_places = Column(Integer)   
    settings_save_places = Column(Boolean)   
    user_id = Column(Integer, ForeignKey('User.id', ondelete="SET NULL", onupdate="SET NULL"), index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    city = Column(String, index=True) 
    type = Column(Integer, nullable=False)  
    settings_osm_id = Column(BigInteger)  
    settings_area_id = Column(BigInteger)
    settings_lat = Column(String)
    settings_lon = Column(String)
    UniqueConstraint(name)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id) 


# -- #
table_user_id_seq = Sequence('User_id_seq')

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, table_user_id_seq, nullable=False, primary_key=True, autoincrement=True, server_default=table_user_id_seq.next_value())
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(Binary, nullable=False)
    first_name = Column(String, server_default="")
    last_name = Column(String, server_default="")
    address = Column(String, server_default="")
    city = Column(String, server_default="")
    country = Column(String, server_default="")
    zipcode = Column(Integer, server_default='0')
    about_me = Column(String, server_default='A Strange Game. The only winning Move is not to Play. How about a nice game of Chess?')
    google_api_key = Column(String, server_default='') 
    free_runs_remaining = Column(Integer, index=True, server_default='5')   
    settings_p1 = Column(String, server_default="")
    settings_p2 = Column(String, server_default="")
    settings_radius = Column(Integer, server_default='180')  
    settings_type1 = Column(String, server_default='Choose...')
    settings_type2 = Column(String, server_default='Choose...')    
    settings_all_places = Column(Integer, server_default='0')
    ui_color = Column(String, nullable=False, index=True, server_default='blue')
    ui_theme = Column(String, nullable=False, index=True, server_default='dark')      
    ui_button = Column(String, nullable=False, index=True, server_default='info')
    premium_enabled = Column(Boolean, nullable=False, index=True, server_default='False') 
    premium_notified = Column(Boolean, server_default='False')     
    last_login = Column(DateTime, server_default=func.current_timestamp())           
    superadmin = Column(Boolean, nullable=False, index=True, server_default='False')
    total_runs = Column(Integer, index=True, server_default='0') 
    active = Column(Boolean, nullable=False, index=True, server_default='True') 
    last_login_ip = Column(String, server_default="")
    login_count = Column(Integer, server_default='0')
    settings_save_places = Column(Boolean, server_default='False')    
    UniqueConstraint(username) 
    UniqueConstraint(email) 

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def set_password(self, value):
            self.password = hash_pass(value)

    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.now().timestamp() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)            


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
