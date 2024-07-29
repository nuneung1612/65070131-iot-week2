from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base
from typing import Optional
from pydantic import BaseModel


class Book(Base):
     __tablename__ = 'books'

     id = Column(Integer, primary_key=True, index=True)
     title = Column(String, index=True)
     author = Column(String, index=True)
     year = Column(Integer, index=True)
     is_published = Column(Boolean, index=True)
     des = Column(String, index=True)
     preview = Column(String, index=True)
     genre = Column(String, index=True)

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    des = Column(String, index=True)

class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    id = Column(Integer, index=True)
    quan = Column(Integer, index=True)
    detail = Column(String, index=True) 

class Student(Base):
    __tablename__ = 'students'

    id = Column(String, primary_key=True, index=True)
    fname = Column(String, index=True)
    lname = Column(String, index=True)
    dob = Column(String, index=True)
    gender = Column(String, index=True)

class StudentUpdate(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        from_attributes = True
