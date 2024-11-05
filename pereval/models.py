from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base

from pydantic import BaseModel, conint
from typing import List, Union


class ImagePydantic(BaseModel):
    data: str
    title: str

class LevelPydantic(BaseModel):
    winter: str
    summer: str
    autumn: str
    spring: str

class CoordsPydantic(BaseModel):
    latitude: str
    longitude: str
    height: int

class UserPydantic(BaseModel):
    email: str
    fam: str
    name: str
    otc: str
    phone: str

class PerevalAddedPydantic(BaseModel):
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    add_time: str
    user: UserPydantic
    coords: CoordsPydantic
    level: LevelPydantic
    images: List[ImagePydantic]

class DetailItem(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str
    height: conint(ge=0, strict=True)

class ErrorResponse(BaseModel):
    detail: List[DetailItem]


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
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

class PerevalAdded(Base):
    __tablename__ = 'pereval'
    id = Column(Integer, primary_key=True)
    beauty_title = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    coords_id = Column(Integer, ForeignKey('coords.id'))
    coords = relationship("Coords")

    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level")

    images = relationship("Image", backref="pereval")