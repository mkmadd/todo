export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv todo
workon todo

# pip freeze > requirements.txt

# Setup up cd to project working directory
# echo 'cd ~/../../vagrant/catalog' >> $VIRTUAL_ENV/bin/postactivate

# Set some environment variables
# echo 'export DATABASE_URL="postgresql:///todo"' >> $VIRTUAL_ENV/bin/postactivate
# echo 'export APP_SETTINGS="config.DevelopmentConfig"' >> $VIRTUAL_ENV/bin/postactivate


# FOR Heroku
# create file called Procfile:
# web: gunicorn app:app