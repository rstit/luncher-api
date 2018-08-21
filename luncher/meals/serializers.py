from marshmallow.fields import Int, Nested, Str

from luncher.extensions import ma
from luncher.meals.models import Meal
from luncher.venues.serializers import VenueSchema


class MealSchema(ma.ModelSchema):

    name = Str(required=True)
    price = Int(required=True)
    venue = Nested(VenueSchema())

    class Meta:
        model = Meal
        fields = ('id', 'name', 'price', 'description', 'type', 'venue')
