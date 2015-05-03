from app import db
from app.models import User, Todo
from pickle import dump

todos = Todo.query.all()
projects = Project.query.all()

with open('todos.pkl', 'wb') as ft, open('projects.pkl', 'wb') as fp:
    dump(todos, ft)
    dump(projects, fp)
