from luncher.extensions import db
from luncher.venues.models import Venue

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.sqla.models import SurrogatePK, ValueMixin


class MealType(db.Model, SurrogatePK, ValueMixin):
    """Represent Meal Type. eg. Pizza"""
    __tablename__ = 'meal_types'


class Meal(db.Model, SurrogatePK):
    """Represent of concrete Meal"""
    __tablename__ = 'meals'

    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    type_id = Column(Integer, ForeignKey('meal_types.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))

    type = relationship(MealType)
    venue = relationship(Venue, backref='meals')
