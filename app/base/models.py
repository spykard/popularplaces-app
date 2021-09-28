# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Date, DateTime, ForeignKey, Float

from app import db, login_manager

from app.base.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    first_name = Column(String, server_default='first_name')
    last_name = Column(String, server_default='last_name')
    address = Column(String, server_default='address')
    city = Column(String, server_default='city')
    country = Column(String, server_default='country')
    zipcode = Column(Integer, server_default='zipcode')
    about_me = Column(String, server_default='about_me')
    google_api_key = Column(String, server_default='google_api_key') 
    premium_enabled = Column(Integer, server_default='premium_enabled')
    premium_notified = Column(Integer, server_default='premium_notified')
    free_runs_remaining = Column(Integer, server_default='free_runs_remaining')   
    settings_p1 = Column(String, server_default='settings_p1')
    settings_p2 = Column(String, server_default='settings_p2')
    settings_radius = Column(Integer, server_default='settings_radius')  
    settings_type1 = Column(String, server_default='settings_type1')
    settings_type2 = Column(String, server_default='settings_type2')    
    settings_all_places = Column(Integer, server_default='settings_all_places')
    last_login = Column(Date, server_default='last_login')   
    ui_color = Column(String, server_default='ui_color')
    ui_theme = Column(String, server_default='ui_theme')      
    ui_button = Column(String, server_default='ui_theme')       
    superadmin = Column(Integer, server_default='superadmin')     
    total_runs = Column(Integer, server_default='total_runs')      

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

class Place(db.Model):

    __tablename__ = 'Place'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, server_default='name')
    address = Column(String, server_default='address')
    type_p = Column(String, server_default='type_p')
    user_id = Column(Integer, ForeignKey('User.id'))
    global_place = Column(Integer, server_default='global_place')   
    city_id = Column(String, ForeignKey('City.id'))
    time = Column(DateTime, server_default='time') 
    verification = Column(String, server_default='verification')  
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id'))   
    type_p2 = Column(String, server_default='type_p2')
    type_p3 = Column(String, server_default='type_p3')           
    name_verified = Column(String, server_default='name_verified')           
    address_verified = Column(String, server_default='address_verified')
    latitude = Column(Float, server_default='latitude')
    longtitude = Column(Float, server_default='longtitude')                   
    type_verified = Column(String, server_default='type_verified')           
    place_id = Column(String, server_default='place_id')           

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

class Search(db.Model):

    __tablename__ = 'Search'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, server_default='time')     
    google_api_key = Column(String, server_default='google_api_key') 
    settings_p1 = Column(String, server_default='settings_p1')
    settings_p2 = Column(String, server_default='settings_p2')
    settings_radius = Column(Integer, server_default='settings_radius')  
    settings_type1 = Column(String, server_default='settings_type1')
    settings_type2 = Column(String, server_default='settings_type2')    
    settings_all_places = Column(Integer, server_default='settings_all_places')    
    user_id = Column(Integer, ForeignKey('User.id'))
    name = Column(String, unique=True)
    city = Column(String, server_default='city')   
    type = Column(Integer, server_default='type')       

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

class City(db.Model):

    __tablename__ = 'City'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)       
    description = Column(String, server_default='description') 
    image_link = Column(String, server_default='image_link')    

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

class PlaceGlobal(db.Model):

    __tablename__ = 'PlaceGlobal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)       
    address = Column(String, server_default='description') 
    time = Column(DateTime, server_default='time') 
    city_id = Column(String, ForeignKey('City.id'))

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

class PlaceResult(db.Model):

    __tablename__ = 'PlaceResult'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, server_default='rating') 
    rating_num = Column(Integer, server_default='rating_num') 
    time_spent = Column(String, server_default='time_spent') 
    popular_times = Column(String, server_default='popular_times') 
    user_id = Column(Integer, ForeignKey('User.id'))
    search_id = Column(Integer, ForeignKey('Search.id'))
    name = Column(String, server_default='name')       
    address = Column(String, server_default='description')    
    usual_popularity = Column(Integer, server_default='usual_popularity')
    difference = Column(Integer, server_default='difference')
    global_id = Column(Integer, ForeignKey('PlaceGlobal.id'))
    live_popularity = Column(Integer, server_default='live_popularity')                     

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
