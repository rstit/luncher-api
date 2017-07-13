from unittest import TestCase
from unittest.mock import Mock

from luncher.meals.views import MealListView
from utils.status import HTTPStatus


class MealListViewTest(TestCase):
    def setUp(self):
        self.mock_dao = Mock(all=Mock(return_value=[]))
        self.view = MealListView(self.mock_dao)

    def test_get_valid_data(self):
        assert self.view.get()[0] == []

    def test_get_valid_status(self):
        assert self.view.get()[1] == HTTPStatus.HTTP_200_OK
