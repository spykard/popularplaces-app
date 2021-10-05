# -*- encoding: utf-8 -*-
import os
from decouple import config

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    FLASK_APP = config('FLASK_APP', default='run.py')
    FLASK_ENV = config('FLASK_ENV', default='development')

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='gE2c!HRRP3avx2^a')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    # Mail Settings
    MAIL_SERVER = config('MAIL_SERVER', default='localhost')
    MAIL_PORT = config('MAIL_PORT', default=25)
    MAIL_USE_TLS = config('MAIL_USE_TLS', default=False, cast=bool)
    MAIL_USE_SSL = config('MAIL_USE_SSL', default=False, cast=bool)
    MAIL_DEBUG = config('MAIL_DEBUG', default=False, cast=bool)
    MAIL_USERNAME = config('MAIL_USERNAME', default=None)
    MAIL_PASSWORD = config('MAIL_PASSWORD', default=None)
    MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER', default=None)
    MAIL_SUPPRESS_SEND = config('MAIL_SUPPRESS_SEND', default=False, cast=bool)

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='unreal'        ),
        config( 'DB_PASS'     , default='pass'          ),
        config( 'DB_HOST'     , default='localhost'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='unreal-flask'  )
    )

class DebugConfig(Config):
    DEBUG = True

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='unreal'       ),
        config( 'DB_PASS'     , default='pass'          ),
        config( 'DB_HOST'     , default='localhost'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='unreal-flask'  )
    )    

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
