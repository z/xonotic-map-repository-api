from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from xmra.config import config
import json


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


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


# http://stackoverflow.com/a/6078058
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
