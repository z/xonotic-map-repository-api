from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from xmra.dependency_graph import config



# Initiate connection and create session
engine = create_engine('postgresql://' +
                       str(config['db']['user']) + ':' +
                       str(config['db']['password']) + '@' +
                       str(config['db']['host']) + ':' +
                       str(config['db']['port']) + '/' +
                       str(config['db']['name'])
                       )

Base = declarative_base()
session = Session(engine)
