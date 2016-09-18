from sqlalchemy import (MetaData, Table, join, Column, Integer, Boolean,
                        String, DateTime, Float, ForeignKey, and_)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import column_property
from sqlalchemy import UniqueConstraint
from datetime import datetime
from xmra.repositories.local.db import engine
from xmra.repositories.local.db import Base


class Author(Base):
    __tablename__ = 'author'
    author_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


class Library(Base):
    __tablename__ = 'library'
    library_id = Column(Integer, primary_key=True)
    name = Column(String(80))
    map_package_id = Column(ForeignKey('map_package.map_package_id'))

    map_package = relationship("MapPackage", foreign_keys=[map_package_id])

    __table_args__ = (UniqueConstraint('name', name='uix_library_name'),)


class MapPackage(Base):
    __tablename__ = 'map_package' # left
    map_package_id = Column(Integer, primary_key=True)
    pk3_file = Column(String(255))
    shasum = Column(String(64))
    date = Column(DateTime, nullable=False, default=datetime.now())
    filesize = Column(Integer)

    bsp = relationship("Bsp", secondary=lambda: map_package_bsp_table)

    __table_args__ = (UniqueConstraint('pk3_file', name='uix_pk3_file'),)

    def __init__(self, pk3_file, shasum, filesize, date=datetime.now()):
        self.pk3_file = pk3_file
        self.shasum = shasum
        self.date = date
        self.filesize = filesize


class Bsp(Base): # right
    __tablename__ = 'bsp'
    bsp_id = Column(Integer, primary_key=True)
    # map_package_id = Column(Integer, ForeignKey('map_package.map_package_id'))
    # pk3_file = Column(String(255))
    bsp_name = Column(String(255))
    bsp_file = Column(String(255))
    map_file = Column(String(255))
    mapshot = Column(String(255))
    radar = Column(String(255))
    title = Column(String(255))
    description = Column(String(600))
    mapinfo = Column(String(255))
    author = Column(String(100))
    # gametype_id = Column(ForeignKey('gametype.gametype_id'))
    # entity_id = Column(ForeignKey('entity.entity_id'))
    entities_file = Column(String(255))
    waypoints = Column(Boolean)
    license = Column(Boolean)

    # map_package = relationship("MapPackage", foreign_keys=[map_package_id], back_populates="bsp", primaryjoin=bsp_id==MapPackage.bsp_id)
    # gametype = relationship("Gametype", foreign_keys=[gametype_id])
    # entity = relationship("Entity", foreign_keys=[entity_id])

    def __init__(self, bsp_name, bsp_file, map_file=None, mapshot=None, radar=None, title=None, description=None, mapinfo=None, author=None, entities_file=None, waypoints=None, license=None):
        self.bsp_name = bsp_name
        self.bsp_file = bsp_file
        self.map_file = map_file
        self.mapshot = mapshot
        self.radar = radar
        self.title = title
        self.description = description
        self.mapinfo = mapinfo
        self.author = author
        self.entities_file = entities_file
        self.waypoints = waypoints
        self.license = license


map_package_bsp_table = Table('map_package_bsp', Base.metadata,
    Column('map_package_bsp_id', Integer, ForeignKey("map_package.map_package_id"),
           primary_key=True),
    Column('bsp_id', Integer, ForeignKey("bsp.bsp_id"),
           primary_key=True)
)


# class MapPackageBsp(Base):
#     __tablename__ = 'map_package_bsp' # association
#     map_package_bsp_id = Column(Integer, primary_key=True)
#     map_package_id = Column(ForeignKey('map_package.map_package_id'))
#     bsp_id = Column(ForeignKey('bsp.bsp_id'))
#
#     map_package = relationship("MapPackage", foreign_keys=[map_package_id])
#     bsp = relationship("Bsp", foreign_keys=[bsp_id])


class Gametype(Base):
    __tablename__ = 'gametype'
    gametype_id = Column(Integer, primary_key=True)
    name = Column(String(255))

    __table_args__ = (UniqueConstraint('name', name='uix_gametype'),)


class Entity(Base):
    __tablename__ = 'entity'
    entity_id = Column(Integer, primary_key=True)
    name = Column(String(255))

    __table_args__ = (UniqueConstraint('name', name='uix_entity'),)


class BspGametype(Base):
    __tablename__ = 'bsp_gametype'
    bsp_gametype_id = Column(Integer, primary_key=True)
    bsp_id = Column(ForeignKey('bsp.bsp_id'))
    gametype_id = Column(ForeignKey('gametype.gametype_id'))

    bsp = relationship("Bsp", foreign_keys=[bsp_id])
    gametype = relationship("Gametype", foreign_keys=[gametype_id])


class BspEntity(Base):
    __tablename__ = 'bsp_entity'
    bsp_entity_id = Column(Integer, primary_key=True)
    bsp_id = Column(ForeignKey('bsp.bsp_id'))
    entity_id = Column(ForeignKey('entity.entity_id'))

    bsp = relationship("Bsp", foreign_keys=[bsp_id])
    entity = relationship("Entity", foreign_keys=[entity_id])


# Using an Association Proxy http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/associationproxy.html

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    kw = relationship("Keyword", secondary=lambda: userkeywords_table)

    __table_args__ = (UniqueConstraint('name', name='uix_user'),)

    def __init__(self, name):
        self.name = name


class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword = Column('keyword', String(64))

    def __init__(self, keyword):
        self.keyword = keyword

userkeywords_table = Table('userkeywords', Base.metadata,
    Column('user_id', Integer, ForeignKey("user.id"),
           primary_key=True),
    Column('keyword_id', Integer, ForeignKey("keyword.id"),
           primary_key=True)
)


def setup_db():
    Base.metadata.create_all(engine)
