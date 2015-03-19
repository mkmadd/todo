from app import db
from app.models import Project, Todo

Todo.query.delete()
Project.query.delete()

p1 = Project("Udacity's Project 3")
p2 = Project("Udacity's Project 4")
p3 = Project("Udacity's Project 5")
p4 = Project("Coursera Data Science Capstone")
p5 = Project("Get Cool Job")

td1 = Todo('Populate database with some items', p1)
td2 = Todo('Change index to display items', p1)
td3 = Todo('Go to bed', p1)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(td1)
db.session.add(td2)
db.session.add(td3)

db.session.commit()
