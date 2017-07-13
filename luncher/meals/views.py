from flask import jsonify
from flask.views import MethodView

from luncher.meals.daos import MealDao
from luncher.meals.serializers import MealSchema
from utils.status import HTTPStatus


class MealListView(MethodView):
    def __init__(self, dao=None, serializer=None):
        self.dao = dao or MealDao()
        self.serializer = serializer or MealSchema(many=True)

    def get(self):
        data, _ = self.serializer.dump(self.dao.all())
        return jsonify(data), HTTPStatus.HTTP_200_OK
