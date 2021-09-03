# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])

class EditProfileForm(FlaskForm):
    user_id = IntegerField('UserID'     , id='user_id'         , validators=[DataRequired()])    
    username = TextField('Username'     , id='username'        , validators=[DataRequired()])
    email    = TextField('Email'        , id='email'           , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='password'        , validators=[DataRequired()])
    first_name = TextField('First Name' , id='first_name'      , validators=[DataRequired()])
    last_name = TextField('Last Name'   , id='last_name'       , validators=[DataRequired()])
    address = TextField('Address'       , id='address'         , validators=[DataRequired()])
    city = TextField('City'             , id='city'            , validators=[DataRequired()])
    country = TextField('Country'       , id='country'         , validators=[DataRequired()])
    zipcode = IntegerField('Postal Code', id='zipcode'         , validators=[DataRequired()])
    description = TextField('About Me'  , id='description'     , validators=[DataRequired()])