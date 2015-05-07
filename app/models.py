from app import db
from flask.ext.login import UserMixin

# UserMixin from Flask-Login provides default method implementations that
# Flask-Login expects users to have.
# Problem with global uniqueness.  Right now best way to ensure that users 
# logging in on both Google and Facebook get the same list of todos is to use
# email as a unique identifier.  But Github and Twitter either don't provide 
# email or it's optional.  So need to use social id, but that gives different 
# users for each type of social login.
class User(UserMixin, db.Model):
    __tablename__ = 'client_user'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(250), unique=True)
    email = db.Column(db.String(250))
    name = db.Column(db.String(80))
    administrator = db.Column(db.Boolean)

    def __init__(self, social_id):
        self.social_id = social_id
        self.administrator = False

# class Project(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80), nullable=False)
    # start_date = db.Column(db.DateTime)
    # due_date = db.Column(db.DateTime)
    # completed = db.Column(db.Boolean)
    # image = db.Column(db.String)
    
    # def __init__(self, name):
        # self.name = name
        # self.completed = False
        
    # def __repr__(self):
        # return '<Project: {}>'.format(self.name)

class Todo(db.Model):
    __tablename__ = 'todo'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    parent_id = db.Column(db.Integer, 
                          db.ForeignKey('todo.id', ondelete='CASCADE'))
    parent = db.relationship('Todo', remote_side=[id], 
                backref=db.backref('children', 
                                   cascade="all, delete-orphan", 
                                   lazy='dynamic'))
    image = db.Column(db.String)
    owner_id = db.Column(db.Integer, 
                         db.ForeignKey('client_user.id', ondelete='CASCADE'), 
                         nullable=False)
    owner = db.relationship('User',
                            backref=db.backref('todos', 
                                    cascade='all, delete-orphan', 
                                    lazy='dynamic'))

    def __init__(self, name, owner, parent=None):
        self.name = name
        self.owner = owner
        self.parent = parent
        self.completed = False

    def __repr__(self):
        return '<Todo: {}>'.format(self.name)
