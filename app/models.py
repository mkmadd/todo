from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def __init__(self, email):
        self.email = email

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
    parent_id = db.Column(db.Integer, db.ForeignKey('todo.id'))
    parent = db.relationship('Todo', remote_side=[id], 
                backref=db.backref('children', 
                                   cascade="all, delete-orphan", 
                                   lazy='dynamic'))
    image = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('todos', 
                                    cascade='all, delete-orphan', 
                                    lazy='dynamic'))

    def __init__(self, name, owner, parent=None):
        self.name = name
        self.owner = owner
        self.parent = parent
        self.completed = False

    def __repr__(self):
        return '<Todo: {}>'.format(self.name)
