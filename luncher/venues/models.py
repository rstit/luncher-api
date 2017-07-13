from luncher.extensions import db
from utils.sqla.models import SurrogatePK

from sqlalchemy import Column, ForeignKey, Integer, Table, String
from sqlalchemy.orm import relationship


class Venue(db.Model, SurrogatePK):
    """Represent of concrete Venue"""
    __tablename__ = 'venues'

    name = Column(String)
    description = Column(String)
