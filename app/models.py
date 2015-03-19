from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    
    def __init__(self, name):
        self.name = name
        self.completed = False
        
    def __repr__(self):
        return '<Project: {}>'.format(self.name)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    project = db.relationship('Project', 
                backref=db.backref('todos', lazy='dynamic'))

    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.completed = False

    def __repr__(self):
        return '<Todo: {}>'.format(self.name)
