from luncher.accounts.daos import UserDao
from luncher.accounts.serializers import UserSchema
from luncher.auth.helpers import TokenHelper
from luncher.common import APIView

from utils.status import HTTPStatus


class TokenView(APIView):
    def __init__(self, dao=None, token_helper=None, schema=None, request=None, *args, **kwargs):
        self.dao = dao or UserDao()
        self.token_helper = token_helper or TokenHelper()
        self.schema = schema or UserSchema()
        super().__init__(request=request)

    def post(self):
        validated_data, errors = self.schema.loads(self.request.get_json())

        if errors:
            return errors, HTTPStatus.HTTP_400_BAD_REQUEST

        user = self.dao.get(**validated_data)

        if user:
            token = self.token_helper.create(user.id)
            return {"token": token}, HTTPStatus.HTTP_200_OK

        return {"error": "Invalid Credentials"}, HTTPStatus.HTTP_400_BAD_REQUEST
