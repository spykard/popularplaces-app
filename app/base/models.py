# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Numeric

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
    google_api_key = Column(Integer, server_default='google_api_key') 
    premium_enabled = Column(Integer, server_default='premium_enabled')
    premium_notified = Column(Integer, server_default='premium_notified')
    free_runs_remaining = Column(Integer, server_default='free_runs_remaining')   
    settings_p1 = Column(String, server_default='settings_p1')
    settings_p2 = Column(String, server_default='settings_p2')
    settings_radius = Column(Integer, server_default='settings_radius')  
    settings_type1 = Column(String, server_default='settings_type1')
    settings_type2 = Column(String, server_default='settings_type2')    
    settings_all_places = Column(Integer, server_default='settings_all_places')       

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

    id = Column(Integer, primary_key=True)
    rating = Column(Numeric)

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
