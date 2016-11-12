from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from xmra.config import config

# Initiate connection and create session
engine = create_engine(
    'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        str(config['xmra']['db_user']),
        str(config['xmra']['db_password']),
        str(config['xmra']['db_host']),
        str(config['xmra']['db_port']),
        str(config['xmra']['db_name']),
    ),
    # echo=True,
    encoding="utf-8"
)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

Base.metadata.drop_all(engine)

