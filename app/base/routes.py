# -*- encoding: utf-8 -*-
from flask import jsonify, render_template, redirect, request, url_for, session, current_app
from flask_mail import Message
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager, mail
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, RecoverPasswordForm, SetPasswordForm
from app.base.models import User
from datetime import datetime
import os

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
            current_user.last_login = datetime.utcnow()
            current_user.last_login_ip = request.remote_addr
            current_user.login_count += 1
            db.session.commit()
            
            return redirect(url_for('base_blueprint.route_default'))
        else:
            # Something (user or pass) is not ok
            logout_user()  # Bug Fix: current_user.is_authenticated turns True
            return render_template( 'accounts/login.html', 
                                    msg='Wrong user or password', 
                                    success=False,
                                    form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html', form=login_form)
    else:
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

        # Else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        send_email_register(email, username) 
        logout_user()  # Bug Fix: current_user.is_authenticated turns True

        return render_template( 'accounts/register.html', 
                                msg='User created, please <a href="/login">Login</a>', 
                                success=True,
                                form=create_account_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/register.html', form=create_account_form)
    else:
        return redirect(url_for('home_blueprint.search'))
 
@blueprint.route('/recover-password', methods=['GET', 'POST'])
def forgot_password():
    forgot_form = RecoverPasswordForm(request.form)
    if 'recover' in request.form:
        
        # Read form data
        email = request.form['email']

        # Validate form data
        if not forgot_form.validate():
            return render_template( 'accounts/recover-password.html', 
                                    msg='Input does not follow the Appropriate Form',
                                    success=False,
                                    form=forgot_form)

        # Locate user
        user = User.query.filter_by(email=email).first()
        
        # Check the password
        if not user:
            return render_template( 'accounts/recover-password.html', 
                                    msg='There is no User Account registered with the Selected E-mail',
                                    success=False,
                                    form=forgot_form)
        else: 
            send_email_recover(user, email)
            return render_template( 'accounts/recover-password.html', 
                                    msg='Check your E-mail for Further Instructions, the Reset Link will be valid for 600 Seconds',
                                    success=True,
                                    form=forgot_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/recover-password.html', form=forgot_form)
    else:
        return redirect(url_for('home_blueprint.search'))

@blueprint.route('/set-password', methods=['GET', 'POST'])
def set_password():
    # Get message parameters
    if 'token' in request.args:
        token = request.args['token']
        user = User.verify_reset_password_token(token)
        if not user:
            return render_template( 'errors/recover-password-error.html') 

        set_password_form = SetPasswordForm(request.form)
        if 'password' in request.form:  
            # Read form data
            password = request.form['password']

            # Validate form data
            if not set_password_form.validate():
                return render_template( 'accounts/set-password.html', 
                                        msg='Input does not follow the Appropriate Form',
                                        success=False,
                                        form=set_password_form)

            if len(password) < 4:
                return render_template( 'accounts/set-password.html', 
                                        msg='Password is too short',
                                        success=False,
                                        form=set_password_form)                                        

            # Update Password 
            user.set_password(password)
            db.session.commit()

            return render_template( 'accounts/set-password.html', 
                                msg='Password Reset was Successful, please <a href="/login">Login</a>', 
                                success=True,
                                form=set_password_form)

        return render_template( 'accounts/set-password.html', form=set_password_form)
    else:
        return render_template( 'errors/recover-password-error.html')  
      

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

# Helper - Send E-mail regarding User Register
def send_email_register(email, username):
    email_template_create_path = os.path.join(os.getcwd(),'app', 'base', 'static', 'assets', 'html', 'email-template-create.html')
    email_template_create_path_img = os.path.join(os.getcwd(),'app', 'base', 'static', 'assets', 'html', 'images', 'image-1.png')
    email_template_create_html = ""
          
    f = open(email_template_create_path, 'r', encoding='utf-8')
    for line in f: 
        email_template_create_html += line
    f.close()

    msg = Message("Welcome to PopularTimes.app - Account Registration",
                  recipients=[email])
    msg.html = email_template_create_html.replace('XXX', username)
    # https://stackoverflow.com/a/55837389
    msg.attach('image.png', 'image/png', open(email_template_create_path_img, 'rb').read(), 'inline', headers=[['Content-ID','<MyImage>'],])
    mail.send(msg) 

# Helper - Send E-mail regarding Password Recover
def send_email_recover(user, email):
    # Generate JWT Expirable Tokens
    token = user.get_reset_password_token()

    email_template_recover_path = os.path.join(os.getcwd(),'app', 'base', 'static', 'assets', 'html', 'email-template-recover.html')
    email_template_recover_html = ""
          
    f = open(email_template_recover_path, 'r', encoding='utf-8')
    for line in f: 
        email_template_recover_html += line
    f.close()

    msg = Message("PopularTimes.app - Password Reset Request",
                  recipients=[email])
    msg.html = email_template_recover_html.replace('https://popularplaces.app/XXX', 'https://popularplaces.app/set-password?token=' + token)
    mail.send(msg)     

## Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page-500.html'), 500
