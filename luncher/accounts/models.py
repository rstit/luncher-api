from luncher.extensions import db
from utils.sqla.models import SurrogatePK

from sqlalchemy import Column, String


class User(db.Model, SurrogatePK):
    """Dummy user model"""
    __tablename__ = 'users'

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
