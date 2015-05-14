"""
    Set application configuration variables for different environments
    
    Code modified from Flask by Example 
    https://realpython.com/blog/python/flask-by-example-part-1-project-setup/
    
    Use by setting environment variable APP_SETTINGS to class below
    Example: $ export APP_SETTINGS="config.DevelopmentConfig"
"""
import os
import json

class Config(object):
    DEBUG = False
    TESTING = False
    # for Flask-SQLAlchemy e.g. 'postgres:///database_name'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # Enable Flask-WTF CSRF protection
    WTF_CSRF_ENABLED = True
    # Used to sign session cookies and other cryptographic stuff (e.g. CSRF)
    SECRET_KEY = os.environ.get('TODO_SECRET_KEY')
    # client id and secrets for different social network providers.  In the 
    # form { "google": { "id": "<client_id>", "secret": "<client_secret>"} }
    OAUTH_CREDENTIALS = json.load(os.environ.get('OAUTH_CREDENTIALS'))
    ROOT_ADMIN_ID = os.environ.get('TODO_ROOT_ADMIN_ID')

class ProductionConfig(Config):
    DEBUG = False

    
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # with open('secrets.txt', 'rt') as f:
        # OAUTH_CREDENTIALS = json.load(f)
    SECRET_KEY = 'development-use-only'

class TestingConfig(Config):
    TESTING = True
