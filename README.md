Much Todo About Nothing
=======================
Udacity Fullstack Nanodegree Project 3
--------------------------------------

My very own ToDo app.  This project required "an application that provides a  
list of items within a variety of categories as well as provide a user  
registration and authentication system. Registered users will have the ability  
to post, edit and delete their own items."

Much Todo About Nothing allows users to login, then create their own projects  
(categories) and then create todo items within those projects.  As a further  
enhancement, a user can create todo items within those todo items, and so on.  

Both projects and todo items can be created, read, updated, and deleted.  
Persistent data storage is handled by a Postgresql database.

The project was setup following the structure Miguel Grinberg set out in his  
excellent [Flask Mega Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).  
The OAuth code was also heavily based off the code in his OAuth Authentication  
in Flask [tutorial](https://github.com/miguelgrinberg/flask-oauth-example).

Other code contributions came from the Flask by Example [tutorial](https://realpython.com/blog/python/flask-by-example-part-1-project-setup/) at Real  
Python.  My config.py and manage.py files were copied from theirs for app  
configuration and Alembic database migration.  Modifications were naturally  
made to the config file, but the manage.py code was unaltered.

The Social login buttons frontend code was obtained from [bootstrap-social](http://lipis.github.io/bootstrap-social/).  
The datepicker library came from [bootstrap-datepicker](https://github.com/eternicode/bootstrap-datepicker).


## Features

Besides the basic CRUD features, the app features:  
* user registration and authentication using OAuth - Users can sign  
up via Google, Facebook, Github, or Twitter.  Each sign up is unique,  
so signing up under a different provider is considered logging in as  
a different user.  
* Cross Site Request Forgery protection - all post requests are  
protected from csrf attacks using Flask-WTForms' CSRFProtect().  
* images - users can add an image url at creation or editing.  A default  
inspirational image is shown if the user does not provide one.  
* JSON and XML endpoints - user can get a JSON or XML download of their  
todos by navigating to `/todos/json` or `/todos/xml`.  A single todo  
can be obtained by going to `/todos/<id>/json` or `/todos/<id>/xml`.  
(A list of users can also be obtained, but is only available to  
administrators.)  
* single page app - as a challenge, I made this a single page app to  
work with AJAX and jquery with Flask


## Using the App

The app is currently hosted on heroku and can be accessed at  
[https://todo-pro.herokuapp.com/](https://todo-pro.herokuapp.com/).  
Or one can download and run the code.  `$ python run.py` will run the Flask app.  
Though one will first need to provide env vars for:  

* DATABASE_URL			# e.g. "postgresql:///todo"
* TODO_SECRET_KEY		# e.g. "my ultra secret key"
* OAUTH_CREDENTIALS		# { "google" : { "id": "my id", "secret": "123..."} }
* TODO_ROOT_ADMIN_ID	# for google, google$<your google id>
* APP_SETTINGS  		# e.g. config.ProductionConfig

## Code Layout

The entry point into the code is run.py, which simply imports app from app and  
runs it.  The other files in the base directory are notes, configuration files,  
and helper scripts.

The app directory contains the application code proper:  
* `__init__.py` - initializes the Flask app, SQLAlchemy, and LoginManager
* form.py - defines the form used on create and edit pages
* models.py - defines database models
* oauth.py - defines oauth classes for each social provider
* views.py - defines all route handling functions
* /static - static assets (css, js, images)
* /templates - html page templates

