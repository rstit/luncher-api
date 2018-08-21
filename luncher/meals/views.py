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
    def __init__(self, dao=None, serializer=None, meal_serializer=None):
        self.dao = dao or MealDao()
        self.mealtype_dao = BaseDao(MealType)
        self.venue_dao = VenueDao()
        self.serializer = serializer or MealSchema(many=True)
        self.meal_serializer = meal_serializer or MealSchema()

    def get(self):
        data, _ = self.serializer.dump(
            self.dao.all().options(joinedload(self.dao._model.type),
                                   joinedload(self.dao._model.venue)))
        return dumps(data), HTTPStatus.HTTP_200_OK

    @login_required
    def post(self):
        validated_data, errors = self.meal_serializer.loads(
            dumps(request.json))
        if errors:
            return dumps(errors), HTTPStatus.HTTP_400_BAD_REQUEST

        new_meal = self.dao.create(validated_data)
        return dumps({'new_meal_id': new_meal.id}), HTTPStatus.HTTP_201_CREATED
