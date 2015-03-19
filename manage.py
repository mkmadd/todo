"""
    Database migration program
    Code from Flask By Example https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
    
    $ python manage.py db init  # initialize db
    $ python manage.py db migrate   # create first migration
    $ python manage.py db upgrade    # apply migrations to database
"""

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()