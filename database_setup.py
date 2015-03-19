from datetime import datetime
from application import db

# 'postgresql://yourusername:yourpassword@localhost/yournewdb'
# Using default user (vagrant) with no password


class Project(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    created_on = Column(DateTime, default=datetime.now())
    updated_on = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<Project: {}>'.format(self.name)

if __name__ == '__main__':
    db.create_all()