from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from database_setup import Base, Project, DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todo'
db = SQLAlchemy(app)

@app.route('/')
def home():
    projects = session.query(Project).all()
    output = 'Hello, world!\n'
    for project in projects:
        output += project.name
        output += '<br/>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)