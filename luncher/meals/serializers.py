from marshmallow.fields import Nested

from luncher.extensions import ma
from luncher.meals.models import Meal
from luncher.venues.serializers import VenueSchema


class MealSchema(ma.ModelSchema):

    venue = Nested(VenueSchema())

    class Meta:
        model = Meal
        fields = ('id', 'name', 'description', 'type', 'venue')
