# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User
from datetime import date

from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/update-ui-color-preference', methods=['POST'])
def update_ui_color_preferences():
    if current_user.is_authenticated:
        current_user.ui_color = request.form['color']
        db.session.commit() 
        return "true"
    else:
        return "false"

@blueprint.route('/update-ui-theme-preference', methods=['POST'])
def update_ui_theme_preferences():
    if current_user.is_authenticated:
        current_user.ui_theme = request.form['theme']
        db.session.commit() 
        return "true"
    else:
        return "false"

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():    
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # Read form data
        username = request.form['username']
        password = request.form['password']

        # Validate form data
        if not login_form.validate():
            return render_template( 'accounts/login.html', 
                                    msg='Input does not follow the Appropriate Form',
                                    success=False,
                                    form=login_form)

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            current_user.last_login = date.today()
            db.session.commit()
            
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        logout_user()  # Bug Fix: current_user.is_authenticated turns True
        return render_template( 'accounts/login.html', 
                                msg='Wrong user or password', 
                                success=False,
                                form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html', form=login_form)

    return redirect(url_for('home_blueprint.search'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)    
    if 'register' in request.form:

        # Read form data
        username  = request.form['username']
        email     = request.form['email'   ]

        # Validate Form Data
        if not create_account_form.validate():
            return render_template( 'accounts/register.html', 
                                    msg='Input does not follow the Appropriate Form',
                                    success=False,
                                    form=create_account_form)

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        logout_user()  # Bug Fix: current_user.is_authenticated turns True

        return render_template( 'accounts/register.html', 
                                msg='User created, please <a href="/login">Login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
