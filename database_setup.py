# https://kite.com/blog/python/flask-sqlalchemy-tutorial/
import sys
#for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

#for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

#for configuration
from sqlalchemy import create_engine

#create declarative_base instance
Base = declarative_base()

class Air(Base):
   __tablename__ = 'book'

   id = Column(Integer, primary_key=True)
   timestamp = Column(String(250), nullable=False)
   airquality = Column(Integer)
   temperature = Column(Integer)
   pressure = Column(Integer)
   humidity = Column(Integer)

#creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///air-data.db')

Base.metadata.create_all(engine)