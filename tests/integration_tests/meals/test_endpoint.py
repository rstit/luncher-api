from json import dumps

from luncher.accounts.daos import UserDao
from luncher.auth.helpers import TokenHelper
from luncher.meals.daos import MealDao
from luncher.venues.daos import VenueDao
from tests.integration_tests.base import BaseIntegrationTest
from utils.content_type import ContentType
from utils.status import HTTPStatus
from utils.tests import QueriesCounter


class MealsListEndpointTest(BaseIntegrationTest):
    def test_status_ok(self):
        response = self.client.get("/meals/")

        assert response.status_code == HTTPStatus.HTTP_200_OK

    def create_data(self):
        kfc = VenueDao().create(name="KFC")
        mcdonald = VenueDao().create(name="McDonald")

        MealDao().create(name="Grander", venue=kfc)
        MealDao().create(name="BigMac", venue=mcdonald)

    def test_performance(self):
        self.create_data()

        with QueriesCounter(print_sql=True) as counter:

            self.client.get("/meals/")

            assert counter.count == 1


class CreateMealEndpointTest(BaseIntegrationTest):
    def test_unauthorized(self):
        response = self.client.post("/meals/")

        assert response.status_code == HTTPStatus.HTTP_401_UNAUTHORIZED

    def get_authorization_header(self):
        user = UserDao().create(login="test", password="test")

        return {
            "Authorization": TokenHelper().create(user.id)
        }

    def test_created_with_success(self):
        response = self.client.post(
            "/meals/",
            content_type=ContentType.APPLICATION_JSON,
            headers=self.get_authorization_header(),
            data=dumps({
                "name": "McFlurry2",
                "price": 1090,
            })
        )

        assert response.status_code == HTTPStatus.HTTP_201_CREATED

    def test_created_with_database_populate(self):
        self.client.post(
            "/meals/",
            content_type=ContentType.APPLICATION_JSON,
            headers=self.get_authorization_header(),
            data=dumps({
                "name": "McFlurry",
                "price": 1090,
            })
        )

        assert MealDao().count() == 1

    def test_created_with_failure_missing_price(self):
        response = self.client.post(
            "/meals/",
            content_type=ContentType.APPLICATION_JSON,
            headers=self.get_authorization_header(),
            data=dumps({
                "name": "McFlurry"
            })
        )

        assert response.status_code == HTTPStatus.HTTP_400_BAD_REQUEST

    def test_created_with_failure_missing_price_not_populate(self):
        self.client.post(
            "/meals/",
            content_type=ContentType.APPLICATION_JSON,
            headers=self.get_authorization_header(),
            data=dumps({
                "name": "McFlurry",
            })
        )

        assert MealDao().count() == 0

    def test_not_allowed(self):
        response = self.client.post(
            "/meals/",
            content_type=ContentType.APPLICATION_JSON,
            data=dumps({
                "name": "McFlurry",
                "price": 1090,
            })
        )

        assert response.status_code == HTTPStatus.HTTP_401_UNAUTHORIZED
