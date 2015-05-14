"""
    Script to populate db with some test data

"""

from app import db
from app.models import User, Todo

User.query.delete()
Todo.query.delete()
db.session.commit()

# Project.query.delete()

u1 = User('github$6936085')
u1.name = 'mkmadd'

db.session.add(u1)
db.session.commit()

p1 = Todo("Udacity's Project 3", u1)
p2 = Todo("Udacity's Project 4", u1)
p3 = Todo("Udacity's Project 5", u1)
p4 = Todo("Coursera Data Science Capstone", u1)
p5 = Todo("Get Cool Job", u1)

td1 = Todo('Implement JSON endpoint with all required content', u1, p1)
td2 = Todo('Implement additional API endpoints, such as RSS, Atom, or XML', u1, p1)
td3 = Todo('3rd party authentication and authorization', u1, p1)
td4 = Todo('Projects and tasks identical models', u1, p1)
td5 = Todo('Front end work', u1, p1)
td6 = Todo('Add prioritization (optional)', u1, p1)


db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(td1)
db.session.add(td2)
db.session.add(td3)
db.session.add(td4)
db.session.add(td5)
db.session.add(td6)

db.session.commit()
