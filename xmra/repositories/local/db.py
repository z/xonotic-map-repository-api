from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from xmra.dependency_graph import config

# Initiate connection and create session
engine = create_engine(
    'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        str(config['db']['user']),
        str(config['db']['password']),
        str(config['db']['host']),
        str(config['db']['port']),
        str(config['db']['name']),
    ),
    # echo=True,
    encoding="utf-8"
)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

Base.metadata.drop_all(engine)

