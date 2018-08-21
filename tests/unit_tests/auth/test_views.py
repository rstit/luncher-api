from unittest import TestCase
from unittest.mock import Mock

from luncher.auth.views import TokenView
from utils.status import HTTPStatus


class TokenViewTest(TestCase):
    def setUp(self):
        self.user_id = 1
        self.user_mock = Mock(id=self.user_id)
        self.token_mock = Mock()
        self.mock_dao = Mock(get=Mock(return_value=self.user_mock))
        self.mock_token_helper = Mock(create=Mock(
            return_value=self.token_mock))
        self.request_mock = Mock(get_json=Mock(return_value={}))
        self.schema_mock = Mock()
        self.view = TokenView(self.mock_dao, self.mock_token_helper,
                              self.schema_mock, self.request_mock)

    def test_post_invalid_data(self):
        error_dict = Mock()
        request_dict = Mock()
        self.schema_mock.loads = Mock(return_value=({}, error_dict))
        self.request_mock.get_json = Mock(return_value=request_dict)

        result = self.view.post()

        self.schema_mock.loads.assert_called_once_with(request_dict)
        assert result == (error_dict, HTTPStatus.HTTP_400_BAD_REQUEST)

    def test_post_valid_data_user_not_exist(self):
        data_dict = {"login": "pythonista", "password": "password123"}
        request_dict = Mock()
        self.schema_mock.loads = Mock(return_value=(data_dict, {}))
        self.request_mock.get_json = Mock(return_value=request_dict)
        self.mock_dao.get.return_value = None

        result = self.view.post()

        self.schema_mock.loads.assert_called_once_with(request_dict)
        self.mock_dao.get.assert_called_once_with(**data_dict)

        assert result == ({"error": "Invalid Credentials"},
                          HTTPStatus.HTTP_400_BAD_REQUEST)

    def test_post_valid_data_user_exist(self):
        data_dict = {"login": "pythonista", "password": "password123"}
        request_dict = Mock()
        self.schema_mock.loads = Mock(return_value=(data_dict, {}))
        self.request_mock.get_json = Mock(return_value=request_dict)

        result = self.view.post()

        self.schema_mock.loads.assert_called_once_with(request_dict)
        self.mock_dao.get.assert_called_once_with(**data_dict)
        self.mock_token_helper.create.assert_called_once_with(self.user_id)

        assert result == ({"token": self.token_mock}, HTTPStatus.HTTP_200_OK)
