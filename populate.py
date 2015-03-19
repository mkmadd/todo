from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Project, Base, DATABASE_URI

engine = create_engine(DATABASE_URI)
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()

p1 = Project(name='Write Todo App')
p2 = Project(name='Do Project 4')
p3 = Project(name='Do Project 5')

session.add(p1)
session.add(p2)
session.add(p3)
session.commit()