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
    __tablename__ = 'map_package'
    map_package_id = Column(Integer, primary_key=True)
    pk3_file = Column(String(255))
    shasum = Column(String(64))
    bsp_id = Column(ForeignKey('bsp.bsp_id'))
    bsp = relationship("Bsp", foreign_keys=[bsp_id])
    date = Column(DateTime, nullable=False, default=datetime.now())
    filesize = Column(Integer)

    def __json__(self):
        return {
            'id': self.map_package_id,
            'bsp_id': self.bsp_id,
            'pk3': self.pk3_file,
            'shasum': self.shasum,
            'filesize': self.filesize,
            'date': str(self.date),
        }

    __table_args__ = (UniqueConstraint('pk3_file', name='uix_pk3_file'),)


class Bsp(Base):
    __tablename__ = 'bsp'
    bsp_id = Column(Integer, primary_key=True)
    map_package_id = Column(Integer, ForeignKey('map_package.map_package_id'))
    pk3_file = Column(String(255))
    bsp_name = Column(String(255))
    bsp_file = Column(String(255))
    map_file = Column(String(255))
    mapshot = Column(String(255))
    radar = Column(String(255))
    title = Column(String(255))
    description = Column(String(600))
    mapinfo = Column(String(255))
    author = Column(String(100))
    gametype_id = Column(ForeignKey('gametype.gametype_id'))
    gametype = relationship("Gametype", foreign_keys=[gametype_id])
    entity_id = Column(ForeignKey('entity.entity_id'))
    entity = relationship("Entity", foreign_keys=[entity_id])
    entities_file = Column(String(255))
    waypoints = Column(Boolean)
    license = Column(Boolean)


class MapPackageBsp(Base):
    __tablename__ = 'map_package_bsp'
    map_package_bsp_id = Column(Integer, primary_key=True)
    map_package_id = Column(ForeignKey('map_package.map_package_id'))
    map_package = relationship("MapPackage", foreign_keys=[map_package_id])
    bsp_id = Column(ForeignKey('bsp.bsp_id'))
    bsp = relationship("Bsp", foreign_keys=[bsp_id])


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
    bsp = relationship("Bsp", foreign_keys=[bsp_id])
    gametype_id = Column(ForeignKey('gametype.gametype_id'))
    gametype = relationship("Gametype", foreign_keys=[gametype_id])


class BspEntity(Base):
    __tablename__ = 'bsp_entity'
    bsp_entity_id = Column(Integer, primary_key=True)
    bsp_id = Column(ForeignKey('bsp.bsp_id'))
    bsp = relationship("Bsp", foreign_keys=[bsp_id])
    entity_id = Column(ForeignKey('entity.entity_id'))
    entity = relationship("Entity", foreign_keys=[entity_id])


def setup_db():
    Base.metadata.create_all(engine)
