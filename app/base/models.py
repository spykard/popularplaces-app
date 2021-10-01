# -*- encoding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Date, DateTime, ForeignKey, Float, Sequence
from sqlalchemy.sql import func

from app import db, login_manager

from app.base.util import hash_pass

test = Sequence('test')
#test_idnex = Index('gps_report_timestamp_device_id_idx', timestamp.desc(), device_id)

class Test(db.Model):

    __tablename__ = 'Test'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=test.next_value())
    name = Column(String, server_default="''", index=True)
    address = Column(String, server_default="''")
    type_p = Column(String)
    user_id = Column(Integer, ForeignKey('User.id'))
    global_place = Column(Integer, server_default='0')   
    city_id = Column(String)
    time = Column(DateTime, server_default=func.current_timestamp())
    verification = Column(String, server_default='N/A')  
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id', ondelete="CASCADE", onupdate="CASCADE"))   
    type_p2 = Column(String)
    type_p3 = Column(String)          
    name_verified = Column(String)           
    address_verified = Column(String)
    latitude = Column(Float(53))
    longtitude = Column(Float(53))                  
    type_verified = Column(String,)           
    place_id = Column(String)          

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

table_user_id_seq = Sequence('table_user_id_seq')

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=table_user_id_seq.next_value())
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(Binary)
    first_name = Column(String, server_default="''")
    last_name = Column(String, server_default="''")
    address = Column(String, server_default="''")
    city = Column(String, server_default="''")
    country = Column(String, server_default="''")
    zipcode = Column(Integer, server_default='0')
    about_me = Column(String, server_default='A Strange Game. The only winning Move is not to Play. How about a nice game of Chess?')
    google_api_key = Column(String, server_default='') 
    premium_enabled = Column(Integer, index=True, server_default='0')
    premium_notified = Column(Integer, server_default='0')
    free_runs_remaining = Column(Integer, index=True, server_default='5')   
    settings_p1 = Column(String, server_default="''")
    settings_p2 = Column(String, server_default="''")
    settings_radius = Column(Integer, server_default='180')  
    settings_type1 = Column(String, server_default='Choose...')
    settings_type2 = Column(String, server_default='Choose...')    
    settings_all_places = Column(Integer, server_default='0')
    last_login = Column(Date, server_default=func.current_date())   
    ui_color = Column(String, index=True, server_default='blue')
    ui_theme = Column(String, index=True, server_default='dark')      
    ui_button = Column(String, index=True, server_default='info')       
    superadmin = Column(Integer, server_default='0')     
    total_runs = Column(Integer, server_default='0', index=True)    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

table_place_id_seq = Sequence('table_place_id_seq')

class Place(db.Model):

    __tablename__ = 'Place'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=table_place_id_seq.next_value())
    name = Column(String, server_default="''")
    address = Column(String, server_default="''")
    type_p = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    global_place = Column(Integer, index=True, server_default='0')   
    city_id = Column(String)
    time = Column(DateTime, server_default=func.current_timestamp())
    verification = Column(String, index=True, server_default='N/A')  
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)  
    type_p2 = Column(String)
    type_p3 = Column(String)          
    name_verified = Column(String)           
    address_verified = Column(String)
    latitude = Column(Float(53))
    longtitude = Column(Float(53))                  
    type_verified = Column(String,)           
    place_id = Column(String)          

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

table_search_id_seq = Sequence('table_search_id_seq')

class Search(db.Model):

    __tablename__ = 'Search'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=table_search_id_seq.next_value())
    time = Column(DateTime, server_default=func.current_timestamp())     
    google_api_key = Column(String)
    settings_p1 = Column(String)
    settings_p2 = Column(String)
    settings_radius = Column(Integer)
    settings_type1 = Column(String)
    settings_type2 = Column(String)    
    settings_all_places = Column(Integer)   
    user_id = Column(Integer, ForeignKey('User.id', ondelete="SET NULL", onupdate="SET NULL"), index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String, index=True) 
    type = Column(Integer)      

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

table_city_id_seq = Sequence('table_city_id_seq')

class City(db.Model):

    __tablename__ = 'City'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=table_city_id_seq.next_value())  
    name = Column(String, unique=True, index=True)
    description = Column(String, server_default="''") 
    image_link = Column(String, server_default='/static/assets/img/blank.png')    

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

table_placeglobal_id_seq = Sequence('table_placeglobal_id_seq')

class PlaceGlobal(db.Model):

    __tablename__ = 'PlaceGlobal'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=table_placeglobal_id_seq.next_value()) 
    name = Column(String, unique=True, index=True, server_default="''")       
    address = Column(String, server_default="''") 
    time = Column(DateTime, server_default=func.current_timestamp()) 
    city_id = Column(Integer, ForeignKey('City.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)

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

table_placeresult_id_seq = Sequence('table_placeresult_id_seq')

class PlaceResult(db.Model):

    __tablename__ = 'PlaceResult'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, server_default=table_placeresult_id_seq.next_value()) 
    rating = Column(Float(24))
    rating_num = Column(Integer)
    time_spent = Column(String) 
    popular_times = Column(String)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="SET NULL", onupdate="SET NULL"), index=True, server_default='0')
    search_id = Column(Integer, ForeignKey('Search.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    name = Column(String, server_default="''")       
    address = Column(String, server_default="''")    
    usual_popularity = Column(Integer)
    difference = Column(Integer)
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id', ondelete="SET NULL", onupdate="SET NULL"), index=True)
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

class CrowdInput(db.Model):

    __tablename__ = 'CrowdInput'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    time = Column(DateTime, server_default='time') 
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id'))
    input = Column(Integer, server_default='input')                 

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

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
