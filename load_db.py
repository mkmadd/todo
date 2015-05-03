from app import db
from app.models import User, Todo
# from pickle import load

# Todo.query.delete()
# Project.query.delete()

# with open('todos.pkl', 'rb') as ft, open('projects.pkl', 'rb') as fp:
    # todos = load(ft)
    # projects = load(fp)

# for project in projects:
    # db.session.add(project)

# db.session.commit()
# p1 = Project("Udacity's Project 3")
# db.session.add(p1)
# db.session.commit()

# test = Project.query.all()
# print len(test)

# for todo in todos:
    # print todo.id
    # print todo.name
    # print todo.description
    # print todo.start_date
    # print todo.due_date
    # print todo.completed
    # print todo.image
    # print todo.project_id
    # print '--------------'
    # db.session.add(todo)

# db.session.commit()

todos = Todo.query.filter_by(parent_id=None).all()

print todos
if not todos:
    print 'ha'

for todo in todos:
    print todo.id
    print todo.owner.email
    print todo.name
    print todo.description
    print todo.start_date
    print todo.due_date
    print todo.completed
    print todo.image
    print todo.parent_id
    for child in todo.children:
        print child.name
    print '--------------'

    
users = User.query.all()

for user in users:
    print user.id
    print user.email
    for todo in user.todos.filter_by(parent_id=None).all():
        print todo.name