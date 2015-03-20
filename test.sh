export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv todo
workon todo

# $ pip freeze > requirements.txt

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
