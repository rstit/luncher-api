from luncher.database import BaseDao
from luncher.meals.models import Venue


class VenueDao(BaseDao):
    def __init__(self):
        super().__init__(Venue)
