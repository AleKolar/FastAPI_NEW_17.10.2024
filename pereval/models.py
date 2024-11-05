from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class PerevalAdded(Base):
    __tablename__ = 'pereval'
    id = Column(Integer, primary_key=True)
    beauty_title = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(String)

    # Определяем отношения с другими классами
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    coords_id = Column(Integer, ForeignKey('coords.id'))
    coords = relationship("Coords")

    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level")

    images = relationship("Image", backref="pereval")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    fam = Column(String)
    name = Column(String)
    otc = Column(String)
    phone = Column(String)

class Coords(Base):
    __tablename__ = 'coords'
    id = Column(Integer, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)
    height = Column(Integer)

class Level(Base):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True)
    winter = Column(String)
    summer = Column(String)
    autumn = Column(String)
    spring = Column(String)

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    title = Column(String)