"""
    Code modified from Flask by Example https://realpython.com/blog/python/flask-by-example-part-1-project-setup/
"""
import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # Enable Flask-WTF CSRF protection
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'development-use-only'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True