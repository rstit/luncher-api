from luncher.extensions import ma
from luncher.venues.models import Venue


class VenueSchema(ma.ModelSchema):
    class Meta:
        model = Venue
        fields = ('id', 'name', 'description')
