#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column("password", nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs.get("password"):
            kwargs["password"] = md5(kwargs["password"].encode('utf-8')).hexdigest()
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """ Password getter method"""
        return self.__dict__.get("password")

    @password.setter
    def password(self, password):
        """
        Hash the password using MD5
        Args:
        pwd: the password to be hashed
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexdigest()
