# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, DataRequired, NumberRange, Regexp

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username'         , validators=[DataRequired()])
    password = PasswordField('Password', id='password'         , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username'        , validators=[DataRequired()])
    email    = TextField('Email'        , id='email'           , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='password'        , validators=[DataRequired()])

class EditProfileForm(FlaskForm):   
    username = TextField('Username'     , id='username'        , validators=[DataRequired()])
    email    = TextField('Email'        , id='email'           , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='password')
    first_name = TextField('First Name' , id='first_name'      , validators=[DataRequired()])
    last_name = TextField('Last Name'   , id='last_name')
    address = TextField('Address'       , id='address'         , validators=[DataRequired()])
    city = TextField('City'             , id='city'            , validators=[DataRequired()])
    country = TextField('Country'       , id='country'         , validators=[DataRequired()])
    zipcode = IntegerField('Postal Code', id='zipcode'         , validators=[NumberRange(0, 99999)])
    about_me = TextAreaField('About Me' , id='about_me'        , validators=[DataRequired()])

class EditSettingsForm(FlaskForm):
    city = TextField('API Key'          , id='city'            , validators=[DataRequired()])    
    type1 = SelectField('Type 1'        , id='type1'           , validators=[DataRequired()], choices=[("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    type2 = SelectField('Type 2'        , id='type2'           , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])

class EditSettingsFormAdvanced(FlaskForm):
    api_key = TextField('API Key'         , id='api_key'       , validators=[DataRequired()]) 
    p1 = TextField('Location Point 1'     , id='p1'            , validators=[DataRequired(), Regexp("^([1-8]?\d(\.\d+)?|90(\.0+)?),\s*(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")])
    p2 = TextField('Location Point 2'     , id='p2'            , validators=[DataRequired(), Regexp("^([1-8]?\d(\.\d+)?|90(\.0+)?),\s*(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")])
    radius = IntegerField('Density Radius', id='radius'        , validators=[NumberRange(1, 50000)])
    type1 = SelectField('Type 1'          , id='type1'         , validators=[DataRequired()], choices=[("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    type2 = SelectField('Type 2'          , id='type2'         , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])

class AddPlaceForm(FlaskForm):
    name = TextField('Name'             , id='name'            , validators=[DataRequired()]) 
    address = TextField('Address'       , id='address')
    type_p = SelectField('Type'         , id='type_p'          , validators=[DataRequired()], choices=[("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    city = TextField('City'             , id='city'            , validators=[DataRequired()])
    type_p2 = SelectField('Type 2'         , id='type_p2'      , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    type_p3 = SelectField('Type 3'         , id='type_p3'      , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])    