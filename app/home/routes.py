# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db, login_manager
from jinja2 import TemplateNotFound
from app.base.forms import EditProfileForm
from app.base.models import User, Place
from app.base.util import hash_pass

@blueprint.route('/index')
@login_required
def index():

    if current_user.premium_enabled == 1 and current_user.premium_notified == 0:
        to_notify = "true"
        current_user.premium_notified = 1
        db.session.commit()        
    else:
        to_notify = "false"
    
    return render_template('index.html', segment='index', to_notify=to_notify)

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:
        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

@blueprint.route('/populartimes')
@login_required
def populartimes():

    query = 1
    # Locate user
    user = Place.query.filter_by(id=query).first()

    return render_template('populartimes.html', segment='populartimes', data=user.rating)

@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    return render_template('search.html', segment='search')    

@blueprint.route('/page-user', methods=['GET', 'POST'])
@login_required
def page_user():
    profile_form = EditProfileForm(request.form)
    if 'save' in request.form:

        # Read form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        zipcode = request.form['zipcode']
        about_me = request.form['about_me']

        # Validate Form Data
        if not profile_form.validate():
            return render_template( 'page-user.html', 
                                     segment='page-user',
                                     msg='Input does not follow the Appropriate Form',
                                     success=False)

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if current_user.username != username and user:
            return render_template( 'page-user.html',
                                    segment='page-user',
                                    msg='Username already registered',
                                    success=False)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if current_user.email != email and user:
            return render_template( 'page-user.html', 
                                    segment='page-user',
                                    msg='Email already registered', 
                                    success=False)

        current_user.username = username
        if password:
            current_user.password = hash_pass( password ) # we need bytes here (not plain str)
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.address = address
        current_user.city = city
        current_user.country = country
        current_user.zipcode = zipcode
        current_user.about_me = about_me
        db.session.commit()

        return render_template( 'page-user.html', 
                        segment='page-user',
                        msg='Changes saved successfully!', 
                        success=False)

    return render_template( 'page-user.html', 
                            segment='page-user')

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
