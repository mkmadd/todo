export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv todo
workon todo

# $ pip freeze > requirements.txt
# $ sudo pip install -r requirements.txt

# Setup up cd to project working directory
# $ echo 'cd ~/../../vagrant/catalog' >> $VIRTUAL_ENV/bin/postactivate

# Set some environment variables
# $ echo 'export DATABASE_URL="postgresql:///todo"' >> $VIRTUAL_ENV/bin/postactivate
# $ echo 'export APP_SETTINGS="config.DevelopmentConfig"' >> $VIRTUAL_ENV/bin/postactivate
# $ workon todo   # restart the environment


# FOR Heroku
# create file called Procfile:
# web: gunicorn app:app
# create file called runtime.txt:
# python-2.7.6

# Install Heroku Toolbelt
# $ wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
# $ heroku login

# Create production and staging apps on Heroku
# $ heroku create todo-pro
# $ heroku create todo-stage

# Deploy
# $ git remote add pro https://git.heroku.com/todo-pro.git
# $ git remote add stage https://git.heroku.com/todo-stage.git
# $ git push stage master
# $ git push pro master
# $ heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
# $ heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
# $ heroku addons:add heroku-postgresql:dev --app todo-stage	# adds DATABASE_URL environ variable
# $ heroku addons:add heroku-postgresql:dev --app todo-pro
# $ heroku run python run.py --app todo-stage
# $ heroku run python run.py --app todo-stage

# Apply db migrations to Heroku
# $ heroku run python manage.py db upgrade --app todo-stage
# $ heroku run python manage.py db upgrade --app todo-pro
# $ heroku run python populate.py --app todo-stage
# $ heroku run python populate.py --app todo-pro

# To get back up and running after killing VM:
# $ export WORKON_HOME=~/Envs
# $ mkdir -p $WORKON_HOME
# $ source /usr/local/bin/virtualenvwrapper.sh
# $ mkvirtualenv todo
# $ workon todo			# Should just have to run to here on halt/up
# $ echo 'cd ~/../../vagrant/catalog' >> $VIRTUAL_ENV/bin/postactivate
# $ echo 'export DATABASE_URL="postgresql:///todo"' >> $VIRTUAL_ENV/bin/postactivate
# $ echo 'export APP_SETTINGS="config.DevelopmentConfig"' >> $VIRTUAL_ENV/bin/postactivate
# $ workon todo   # restart the environment
# $ sudo apt-get install libpq-dev		# Added to pg_config.sh, shouldn't need
# $ sudo apt-get install python-dev		# Added to pg_config.sh, shouldn't need
# $ sudo apt-get install git			# Added to pg_config.sh, shouldn't need
# $ sudo pip install -r requirements.txt
# $ createdb todo
# $ python manage.py db init  # initialize db
# $ python manage.py db migrate   # create first migration
# $ python manage.py db upgrade    # apply migrations to database
# $ python populate.py