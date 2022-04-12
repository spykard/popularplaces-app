# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, DataRequired, NumberRange, Regexp

## login and registration

class LoginForm(FlaskForm):
    username = StringField    ('Username', id='username'         , validators=[DataRequired()])
    password = PasswordField('Password', id='password'         , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = StringField('Username'     , id='username'        , validators=[DataRequired()])
    email    = StringField('Email'        , id='email'           , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='password'        , validators=[DataRequired()])

class RecoverPasswordForm(FlaskForm):
    email    = StringField('Email'        , id='email'           , validators=[DataRequired(), Email()])  

class SetPasswordForm(FlaskForm):
    password = PasswordField('Password', id='password'         , validators=[DataRequired()])      

class EditProfileForm(FlaskForm):   
    username = StringField('Username'     , id='username'        , validators=[DataRequired()])
    email    = StringField('Email'        , id='email'           , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='password')
    first_name = StringField('First Name' , id='first_name'      , validators=[DataRequired()])
    last_name = StringField('Last Name'   , id='last_name')
    address = StringField('Address'       , id='address'         , validators=[DataRequired()])
    city = StringField('City'             , id='city'            , validators=[DataRequired()])
    country = StringField('Country'       , id='country'         , validators=[DataRequired()])
    zipcode = IntegerField('Postal Code', id='zipcode'         , validators=[NumberRange(0, 99999)])
    about_me = TextAreaField('About Me' , id='about_me'        , validators=[DataRequired()])

class EditSettingsForm(FlaskForm):
    city = StringField('API Key'          , id='city'            , validators=[DataRequired()])    
    type1 = SelectField('Type 1'        , id='type1'           , validators=[DataRequired()], choices=[("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    type2 = SelectField('Type 2'        , id='type2'           , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])

class EditSettingsTurboForm(FlaskForm):
    location = StringField('Location'     , id='location'        , validators=[DataRequired()])    
    type = StringField('Type'           , id='type1'           , validators=[DataRequired()])

class EditSettingsAdvancedForm(FlaskForm):
    api_key = StringField('API Key'         , id='api_key'       , validators=[DataRequired()]) 
    p1 = StringField('Location Point 1'     , id='p1'            , validators=[DataRequired(), Regexp("^([1-8]?\d(\.\d+)?|90(\.0+)?),\s*(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")])
    p2 = StringField('Location Point 2'     , id='p2'            , validators=[DataRequired(), Regexp("^([1-8]?\d(\.\d+)?|90(\.0+)?),\s*(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")])
    radius = IntegerField('Density Radius', id='radius'        , validators=[NumberRange(1, 50000)])
    type1 = SelectField('Type 1'          , id='type1'         , validators=[DataRequired()], choices=[("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    type2 = SelectField('Type 2'          , id='type2'         , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])

class AddPlaceForm(FlaskForm):
    name = StringField('Name'             , id='name'            , validators=[DataRequired()]) 
    address = StringField('Address'       , id='address')
    type_p = SelectField('Type'         , id='type_p'          , validators=[DataRequired()], choices=[("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    city = StringField('City'             , id='city'            , validators=[DataRequired()])
    type_p2 = SelectField('Type 2'         , id='type_p2'      , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])
    type_p3 = SelectField('Type 3'         , id='type_p3'      , choices=[("Choose..."), ("Bar"), ("Night Club"), ("Restaurant"), ("Cafe"), ("Bakery"), ("Food"), ("Subway Station"), ("Gas Station"), ("Bank"), ("Pharmacy"), ("Health"), ("Place of Worship"), ("Department Store"), ("Establishment"), ("University"), ("Library"), ("Book Store"), ("Gym"), ("Clothing Store"), ("Casino"), ("Liquor Store"), ("Other")])    