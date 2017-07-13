from luncher.database import BaseDao
from luncher.meals.models import Meal


class MealDao(BaseDao):
    def __init__(self):
        super().__init__(Meal)
