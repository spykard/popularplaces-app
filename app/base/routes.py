# -*- encoding: utf-8 -*-
from flask import jsonify, render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager, mail
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User
from datetime import datetime

from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    session['colors'] = True 
    session['intro'] = True         
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/hide-colors', methods=['POST'])
def hide_colors():
    session['colors'] = False
    return "true"

@blueprint.route('/hide-intro', methods=['POST'])
def hide_intro():
    session['intro'] = False
    return "true"

@blueprint.route('/update-ui-color-preference', methods=['POST'])
def update_ui_color_preferences():
    color = request.form['color']
    if current_user.is_authenticated:
        current_user.ui_color = color
        if color == "primary":
            current_user.ui_button = "primary"
        elif color == "blue":
            current_user.ui_button = "info"
        elif color == "green":
            current_user.ui_button = "success"            
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

@blueprint.route('/zohoverify/verifyforzoho.html')
def tempp():
    return render_template( 'verifyforzoho.html')

## Login & Registration
from flask_mail import Message
@blueprint.route('/login', methods=['GET', 'POST'])
def login():  
    # msg = Message("Hello",
    #               recipients=["to@example.com"])

    # msg.html = "<b>testing</b>"      
    # mail.send(msg)            

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
            current_user.last_login = datetime.utcnow()
            current_user.last_login_ip = request.remote_addr
            current_user.login_count += 1
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
        email     = request.form['email']

        # Validate Form Data
        if not create_account_form.validate():
            return render_template( 'accounts/register.html', 
                                    msg='Input does not follow the Appropriate Form',
                                    success=False,
                                    form=create_account_form)

        if len(request.form['password']) < 4:
            return render_template( 'accounts/register.html', 
                                    msg='Password is too short',
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
