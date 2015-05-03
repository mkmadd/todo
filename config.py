"""
    Code modified from Flask by Example 
    https://realpython.com/blog/python/flask-by-example-part-1-project-setup/
"""
import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # Enable Flask-WTF CSRF protection
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'development-use-only'
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '470154729788964',
            'secret': '010cc08bd4f51e34f3f3e684fbdea8a7'
        },
        'twitter': {
            'id': '3RzWQclolxWZIMq5LJqzRZPTl',
            'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
        }
    }

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