# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db, login_manager
from jinja2 import TemplateNotFound
from app.base.forms import EditProfileForm, EditSettingsForm
from app.base.models import User, Place, Search
from app.base.util import hash_pass
from datetime import datetime

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

# @blueprint.route('/populartimes')
# @login_required
# def populartimes():

#     query = 1
#     # Locate user
#     user = Place.query.filter_by(id=query).first()

#     return render_template('populartimes.html', segment='populartimes', data=None)

@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    settings_form = EditSettingsForm(request.form)
    if 'search' in request.form:

        # Read form data
        api_key = request.form['api_key']
        p1 = request.form['p1']
        p2 = request.form['p2']
        radius = request.form['radius']
        type1 = request.form['type1']
        type2 = request.form['type2']
        if request.form.get('all_places') == None:  # If checkboxed not checked, no POST data are sent
            all_places = 0
        else:
            all_places = 1

        # Validate Form Data
        if not settings_form.validate():
            return render_template( 'search.html', 
                                    segment='search',
                                    to_notify='true',
                                    msg='Input does not follow the Appropriate Form',
                                    error_dict=settings_form.errors,
                                    success=False,
                                    form=settings_form)

        # Write to DB
        current_user.google_api_key = api_key
        current_user.settings_p1 = p1
        current_user.settings_p2 = p2
        current_user.settings_radius = radius
        current_user.settings_type1 = type1
        current_user.settings_type2 = type2
        current_user.settings_all_places = all_places
        if current_user.premium_enabled == 0: current_user.free_runs_remaining = current_user.free_runs_remaining-1
        db.session.commit()            

        # Main
        search_success, search_msg = search_populartimes(api_key, p1, p2, radius, type1, type2, all_places)

        if search_success:
            return render_template( 'search.html', 
                            segment='search',
                            msg='Search executed successfully! - ID: ' + search_msg, 
                            error_dict={},
                            success=True,
                            form=settings_form)
        else:
            return render_template( 'search.html', 
                            segment='search',
                            msg='Search executed but returned the following Error: ' + search_msg, 
                            error_dict={},
                            success=False,
                            form=settings_form)                                        

    return render_template( 'search.html', 
                            segment='search',
                            error_dict={},
                            form=settings_form,
                            to_notify_premium=notify_premium())    

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
                                     success=False,
                                     form=profile_form)

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if current_user.username != username and user:
            return render_template( 'page-user.html',
                                    segment='page-user',
                                    msg='Username already registered',
                                    success=False,
                                    form=profile_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if current_user.email != email and user:
            return render_template( 'page-user.html', 
                                    segment='page-user',
                                    msg='Email already registered', 
                                    success=False,
                                    form=profile_form)

        # Write to DB
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
                        success=True,
                        form=profile_form)

    return render_template( 'page-user.html', 
                            segment='page-user',
                            form=profile_form)

# --//----//----//----//----//----//----//----//--

import populartimes
@login_required
# Helper - Run the populartimes Implementation
def search_populartimes(api_key, p1, p2, radius, type1, type2, all_places):
    ''' Query Google's PopularTimes in circles, given latitute and longtitude positions and retrieve data for places/stores '''

    #try:
    p1_conv = eval("(" + p1 + ")")
    p2_conv = eval("(" + p2 + ")")
    radius_conv = int(radius)
    types_conv = type_mapper(type1, type2)  # In general, only one type may be specified (if more than one type is provided, all types following the first entry are ignored)
    all_places_conv = bool(all_places)

    # print(p1_conv)
    # print(p2_conv)
    # print(radius_conv)
    print(types_conv)

    for place_type in types_conv:
        data = populartimes.get(api_key=api_key, types=place_type, p1=p1_conv, p2=p2_conv, n_threads=20, radius=radius_conv, all_places=all_places_conv)
        debug_data_printer(data)
    #except Exception as e:
        #return False, str(e)

    # Write Search Object to DB
    user_id = ("user_id" , current_user.id)
    name = ("name" , datetime.now().strftime("%Y%m%d-%H%M%S.%f") + "-" + str(user_id[1]))
    insert_dict = dict([("google_api_key" , api_key), ("settings_p1" , p1), ("settings_p2" , p2), ("settings_radius" , radius), ("settings_type1" , type1), ("settings_type2" , type2), ("settings_all_places" , all_places), user_id, name])
    search = Search(**insert_dict)
    db.session.add(search)
    db.session.commit()    

    return True, name[1]

# Debug - Print the output Data on Console
def debug_data_printer( data ):
    for place in data:
        print(place['name'])
        print(place['address'])
        print(place['types'])
        print(str(place['rating']) + " (" + str(place['rating_n']) + ")")
        if "current_popularity" in place:
            print(place['current_popularity'])
        else:
            print("N/A")
        print(place['populartimes'])
        if "time_spent" in place:
            print(place['time_spent'])
        else:
            print("N/A")
        print()
    print(len(data))

# Helper - Check whether user must be notified for Premium subscription Enabling
def notify_premium():
    if current_user.premium_enabled == 1 and current_user.premium_notified == 0:
        to_notify = "true"
        current_user.premium_notified = 1
        db.session.commit()        
    else:
        to_notify = "false"
    
    return to_notify

# Helper - Maps a string we receive from a Form to a string that can be used as a parameter inside the code, e.g. "Night Club" -> "night_club"
def type_mapper( type1, type2 ): 
    places_map = {"Bar": "bar", "Night Club": "night_club", "Restaurant": "restaurant", "Cafe": "cafe", "Bakery": "bakery", "Food": "food", "Subway Station": "subway_station", "Gas Station": "gas_station", "Bank": "bank", "Pharmacy": "pharmacy", "Health": "health", "Place of Worship": "place_of_worship", "Department Store": "department_store", "Establishment": "establishment", "University": "university", "Library": "library", "Book Store": "book_store", "Gym": "gym", "Clothing Store": "clothing_store", "Casino": "casino", "Liquor Store": "liquor_store"}
    to_return = []

    if type1 != "Choose...":
        to_return.append([places_map[type1]])
    if type2 != "Choose...":
        to_return.append([places_map[type2]])
    
    return to_return
        
# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
