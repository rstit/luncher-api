from json import dumps

from flask import (
    request,
)
from flask.views import MethodView
from sqlalchemy.orm import joinedload

from luncher.auth.views import login_required
from luncher.database import BaseDao
from luncher.meals.daos import MealDao
from luncher.meals.models import MealType
from luncher.meals.serializers import MealSchema
from luncher.venues.daos import VenueDao
from utils.status import HTTPStatus


class MealListView(MethodView):
    def __init__(self, dao=None, serializer=None):
        self.dao = dao or MealDao()
        self.mealtype_dao = BaseDao(MealType)
        self.venue_dao = VenueDao()
        self.serializer = serializer or MealSchema(many=True)

    def get(self):
        data, _ = self.serializer.dump(
            self.dao.all().options(joinedload(self.dao._model.type),
                                   joinedload(self.dao._model.venue)))
        return dumps(data), HTTPStatus.HTTP_200_OK

    @login_required
    def post(self):
        meal_name = request.json.get('name')
        meal_price = request.json.get('price')
        meal_type = request.json.get('meal_type')
        venue = request.json.get('venue')
        if not meal_price or not meal_name:
            return '', HTTPStatus.HTTP_400_BAD_REQUEST

        meal_kw = {}
        if meal_type:
            meal_kw['type_id'] = self.mealtype_dao.get(value=meal_type).id
        if venue:
            meal_kw['venue_id'] = self.venue_dao.get(name=venue).id

        new_meal = self.dao.create(name=meal_name, price=meal_price, **meal_kw)
        return dumps({'new_meal_id': new_meal.id}), HTTPStatus.HTTP_201_CREATED
