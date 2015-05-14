"""
    Define the SQLAlchemy models used in app

"""

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
    """ Define user model for person logged in """
    __tablename__ = 'client_user'

    id = db.Column(db.Integer, primary_key=True)
    # Unique external identifier for pairing authenticated user with id
    social_id = db.Column(db.String(250), unique=True)
    email = db.Column(db.String(250))   # not currently used
    name = db.Column(db.String(80))
    administrator = db.Column(db.Boolean)   # only admins get user list

    def __init__(self, social_id):
        self.social_id = social_id
        self.administrator = False
    
    def __repr__(self):
        return '<User: {}>'.format(self.name)
    
    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        return {
            'name':             self.name,
            'id':               self.id,
            'social_id':        self.social_id,
            'email':            self.email,
            'administrator':    self.administrator
        }
    
    @property
    def is_admin(self):
        return self.administrator

class Todo(db.Model):
    """ Define shared model for projects and todos """
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
    image = db.Column(db.String)    # url string for file of image for this todo
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
        self.parent = parent    # Projects don't have a parent
        self.completed = False

    def __repr__(self):
        return '<Todo: {}>'.format(self.name)

    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        
        return {
            'name':             self.name,
            'id':               self.id,
            'description':      self.description,
            'start_date':       self.start_date,
            'due_date':         self.due_date,
            'completed':        self.completed,
            'owner':            self.owner.name
        }
