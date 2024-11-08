from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


from pydantic import BaseModel, conint, Field
from typing import List, Union, Optional

from database import Base


class ImagePydantic(BaseModel):
    data: str
    title: str

    class Config:
        from_attributes = True

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
    user: UserPydantic
    coords: CoordsPydantic
    level: LevelPydantic
    images: List[ImagePydantic]


class DetailItem(BaseModel):
    loc: str
    msg: str
    type: str

class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="Error code")
    additional_message: str = Field(..., description="Additional error message")
    more_details: str = Field(..., description="More details about the error")


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

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    coords_id = Column(Integer, ForeignKey('coords.id'))
    coords = relationship("Coords")

    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level")

    images = relationship("Image", backref="pereval")
    image_id = Column(Integer, ForeignKey('image.id'))
