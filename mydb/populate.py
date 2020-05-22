from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime, time
#Let’s import our Book and Base classes from our database_setup.py file
from database_setup import Air, Base

engine = create_engine('sqlite:///air-data.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.
session = DBSession()

for i in range(10):
	st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	session.add(Air(timestamp=st, airquality=27+i, temperature=12+i, pressure=1150+i, humidity=60+i))

session.commit()