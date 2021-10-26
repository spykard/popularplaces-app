# Popular Places

A Powerful Tool for Live Crowd and Traffic Data.

This application gives you the ability to search Google's [popular times](https://support.google.com/business/answer/6263531) information, particularly popularity and crowd traffic information. Any type of place can be used including shops, establishments and prominent points of interest.

[<img src="media/documentation.gif" width=40% alt="Google's Popular Times">](media/documentation.gif)

It utilizes a set of Geocoder APIs in order to perform the search, while being able to provide both place and time-based live crowd data.

Example: Find out how busy your favorite bars are...

[<img src="media/history_main.png" width=100% alt="Example - History Tab">](media/history_main.png)

## Features

* **DBMS**: PostgreSQL, SQLite
* **APIs**: OSM, Overpass, Nominatim (Geocoder)
* **DB Tools**: SQLAlchemy ORM, Migrations
* **Maps**: Leaflet, Wicket
* **UI**: Boostrap, PerfectScrollbar
* **Visualization**: ChartJS
* **Timezones**: Luxon
* Session-Based authentication and mailing system
Forms validation
* Mobile-focused UX Design
* Advanced Data Analysis
* **Deployment Scripts**: Docker, Gunicorn/Nginx, Heroku

---

## Getting Started

* [Showcase](#showcase)
* [Basic Modules](#basic-modules)
* [How to Use](#how-to-use)
* [Codebase Structure](#codsebase-structure)
* [Deployment](#deployment)
* [Credits](#credits)

## Showcase

[<img src="media/history_graph.png" width=100% alt="Example - History Tab">](media/history_graph.png)

[<img src="media/history_graph_pink.png" width=100% alt="Example - History Tab">](media/history_graph_pink.png)

[<img src="media/history_main.png" width=100% alt="Example - History Tab">](media/history_main.png)

[<img src="media/search.png" width=100% alt="Example - History Tab">](media/search.png)

[<img src="media/search_pink.png" width=100% alt="Example - History Tab">](media/search_pink.png)

## Basic Modules

**Flask Black Dashboard** is an open-source Flask Dashboard initially designed by [AppSeed](https://appseed.us/admin-dashboards/flask) on top of a modern dark-themed UI. Features a beautiful Bootstrap Dashboard with a huge number of components built to fit together and look amazing. It combines colors that are easy on the eye, spacious cards, beautiful typography, and graphics.

**Flask** is a lightweight web application framework written in Python that provides a lightweight codebase and libraries that can be easily extended to complex projects.

**Popular Times** is a Google's Places API-related Service that provides information about popular times, wait times, and visit duration. The initial idea by [m-wrzr](https://github.com/m-wrzr/populartimes) was to query and scrape Google Search itself.

As Google Maps is constantly updated this application can be unstable.

[Official Definition](https://support.google.com/business/answer/6263531): Popular times graph ~ This graph shows how busy your location typically is during different times of the day. Popular times are based on average popularity over the last few months. Popularity for **any given hour is shown relative to the typical peak popularity for the business for the week**. For example, in the image below, 8 PM–9 PM on Saturday is one of the more popular times of the week for this business.

Data is acquired from Google popular times, updated every 15 minutes. Google uses aggregated and anonymised data from users who have opted in to Google location history to make a reasonable estimate of how many users are in a given location at any given time of the day.

Ideas:  
High crowd - places that have more than 50% crowd  
Gaining crowd - places that have more than 10% gain in crowd for the past 15 minutes  
Usual crowd - shows how active a location typically is currently, based on average popularity over the past few months  
Current crowd - shows how active a location is right now as a percentage of its estimated maximum capacity  
Crowd ratio - shows how active a location is right now compared to its usual level of activity  
Crowd changes - shows the percentage change in crowd in the last 15 minutes  

Places API Documentation:  
https://developers.google.com/places/web-service/usage-and-billing  
https://developers.google.com/maps/documentation/places/web-service/usage-and-billing  
https://cloud.google.com/maps-platform/pricing/sheet/#places.

Google's Nearby Search Documentation:  
https://developers.google.com/maps/documentation/places/web-service/search-nearby  
https://developers.google.com/maps/documentation/places/web-service/search?hl=en#PlaceSearchRequests  
https://developers.google.com/maps/documentation/places/web-service/supported_types

Alternative Implementations:
https://besttime.app  
https://github.com/philshem/gmaps_popular_times_scraper  
https://populartimes.herokuapp.com  
https://github.com/bluemelodybox/flask-popularplaces

**Overpass and Nominatim** are APIs based on OpenStreetMaps with the latter also being a Geocoder/Reverse Geocoder. A scientific comparison on the performance of various Geocoders: https://www.thinkmind.org/articles/soft_v8_n34_2015_7.pdf.

Option 1: Pelias (Uses ElasticSearch) (Self-Hosted)

Option 2: Nominatim (Only usable with Text Query, Reverse Geocoder returns just 1 Result) (Hosted Online)

Option 3: Overpass and its online hosted version Overpass Turbo. They both use Nominatim for Geocoding.

OSM Documentation:  
https://taginfo.openstreetmap.org/   
https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide  
https://wiki.openstreetmap.org/wiki/Overpass_turbo/Wizard  
https://boundingbox.klokantech.com/  
https://github.com/wiktorn/Overpass-API  

## How to Use

```bash
$ # Get the code
$ git clone https://github.com/app-generator/flask-black-dashboard.git
$ cd flask-black-dashboard
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$
$ # OR with PostgreSQL connector
$ # pip install -r requirements-pgsql.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

> Note: To use the app, please access the registration page and create a new user.

## Codebase Structure

The project is coded using blueprints, app factory pattern, dual configuration profile (development and production) and an intuitive structure presented bellow:

#### Simplified version

```bash
< PROJECT ROOT >
   |
   |-- app/                      # Implements app logic
   |    |-- base/                # Base Blueprint - handles the authentication
   |    |-- home/                # Home Blueprint - serve UI Kit pages
   |    |
   |   __init__.py               # Initialize the app
   |
   |-- requirements.txt          # Development modules - SQLite storage
   |-- requirements-mysql.txt    # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt    # Production modules  - PostgreSql DMBS
   |
   |-- .env                      # Inject Configuration via Environment
   |-- config.py                 # Set up the app
   |-- run.py                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

#### The bootstrap flow

* `run.py` loads the `.env` file
* Initialize the app using the specified profile: *Debug* or *Production*
  * If env.DEBUG is set to *True* the SQLite storage is used
  * If env.DEBUG is set to *False* the specified DB driver is used (MySql, PostgreSQL)
* Call the app factory method `create_app` defined in app/__init__.py
* Redirect the guest users to Login page
* Unlock the pages served by *home* blueprint for authenticated users

#### App / Base Blueprint

The *Base* blueprint handles the authentication (routes and forms) and assets management. The structure is presented below:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- home/                                # Home Blueprint - serve app pages (private area)
   |    |-- base/                                # Base Blueprint - handles the authentication
   |         |-- static/
   |         |    |-- <css, JS, images>          # CSS files, Javascripts files
   |         |
   |         |-- templates/                      # Templates used to render pages
   |              |
   |              |-- includes/                  #
   |              |    |-- navigation.html       # Top menu component
   |              |    |-- sidebar.html          # Sidebar component
   |              |    |-- footer.html           # App Footer
   |              |    |-- scripts.html          # Scripts common to all pages
   |              |
   |              |-- layouts/                   # Master pages
   |              |    |-- base-fullscreen.html  # Used by Authentication pages
   |              |    |-- base.html             # Used by common pages
   |              |
   |              |-- accounts/                  # Authentication pages
   |                   |-- login.html            # Login page
   |                   |-- register.html         # Registration page
   |
   |-- requirements.txt                          # Development modules - SQLite storage
   |-- requirements-mysql.txt                    # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt                    # Production modules  - PostgreSql DMBS
   |
   |-- .env                                      # Inject Configuration via Environment
   |-- config.py                                 # Set up the app
   |-- run.py                                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

#### App / Home Blueprint

The *Home* blueprint handles UI Kit pages for authenticated users. This is the private zone of the app - the structure is presented below:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- base/                     # Base Blueprint - handles the authentication
   |    |-- home/                     # Home Blueprint - serve app pages (private area)
   |         |
   |         |-- templates/           # UI Kit Pages
   |              |
   |              |-- index.html      # Default page
   |              |-- page-404.html   # Error 404 - mandatory page
   |              |-- page-500.html   # Error 500 - mandatory page
   |              |-- page-403.html   # Error 403 - mandatory page
   |              |-- *.html          # All other HTML pages
   |
   |-- requirements.txt               # Development modules - SQLite storage
   |-- requirements-mysql.txt         # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt         # Production modules  - PostgreSql DMBS
   |
   |-- .env                           # Inject Configuration via Environment
   |-- config.py                      # Set up the app
   |-- run.py                         # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

## Deployment

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/), [Heroku](https://www.heroku.com/), [Gunicorn](https://gunicorn.org/), and [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

### [Docker](https://www.docker.com/)

The application can be easily executed in a docker container. The steps:

> Get the code

```bash
$ git clone https://github.com/app-generator/flask-black-dashboard.git
$ cd flask-black-dashboard
```

> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:5005` in your browser. The app should be up & running.

### [Heroku](https://www.heroku.com/)

https://devcenter.heroku.com/articles/python-gunicorn

Steps to deploy on **Heroku**

* [Create a FREE account](https://signup.heroku.com/) on Heroku platform
* [Install the Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) that match your OS: Mac, Unix or Windows
* Open a terminal window and authenticate via `heroku login` command
* Clone the sources and push the project for LIVE deployment

```bash
$ # Clone the source code:
$ git clone https://github.com/app-generator/flask-black-dashboard.git
$ cd flask-black-dashboard
$
$ # Check Heroku CLI is installed
$ heroku -v
heroku/7.25.0 win32-x64 node-v12.13.0 # <-- All good
$
$ # Check Heroku CLI is installed
$ heroku login
$ # this commaond will open a browser window - click the login button (in browser)
$
$ # Create the Heroku project
$ heroku create
$
$ # Trigger the LIVE deploy
$ git push heroku master
$
$ # Open the LIVE app in browser
$ heroku open
```

### [Gunicorn](https://gunicorn.org/)

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

> Install using pip

```bash
$ pip install gunicorn
```
> Start the app using gunicorn binary

```bash
$ gunicorn --bind 0.0.0.0:8001 run:app
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

### [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)

Waitress (Gunicorn equivalent for Windows) is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones that live in the Python standard library.

> Install using pip

```bash
$ pip install waitress
```
> Start the app using [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)

```bash
$ waitress-serve --port=8001 run:app
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

## Links

Deployment:

* [Digger](https://digger.dev/)
* [amazon web services - AWS - What are the exact differences between EC2, Beanstalk and LightSail- - Stack Overflow](https://stackoverflow.com/questions/54981074/aws-what-are-the-exact-differences-between-ec2-beanstalk-and-lightsail)
* [Affordable Heroku Alternative - node](https://www.reddit.com/r/node/comments/5a4939/affordable_heroku_alternative/d9dlwhh/)
* [AWS Copilot CLI - AWS Copilot CLI](https://aws.github.io/copilot-cli/)
* [Google Cloud Free Program](https://cloud.google.com/free/docs/gcp-free-tier/#compute)

Crawling

* [Important Thread on Google Search Crawling](https://github.com/m-wrzr/populartimes/issues/56#issuecomment-455823942)

## Credits

* [Spyridon Kardakis](https://www.linkedin.com/in/kardakis/)
* [Flask Framework](https://www.palletsprojects.com/p/flask/)
* [Creative Tim](https://bit.ly/3fKQZaL)
* [AppSeed](https://github.com/app-generator/boilerplate-code)
* [m-wrzr](https://github.com/m-wrzr)
