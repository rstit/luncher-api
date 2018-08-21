from flask import (
    request,
    session,
)
from functools import wraps

from luncher.accounts.daos import UserDao
from luncher.accounts.serializers import UserSchema
from luncher.auth.helpers import TokenHelper
from luncher.common import APIView

import ast
from utils.status import HTTPStatus


class TokenAuthorizationError(Exception):
    pass


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_helper = TokenHelper()
        try:
            token = request.headers.get('Authorization')
            user_dict = token_helper.unsign(token)
            user_id = ast.literal_eval(user_dict.decode())
        except (TokenAuthorizationError, TypeError):
            return '', HTTPStatus.HTTP_401_UNAUTHORIZED
        else:
            session['user_id'] = user_id
        return f(*args, **kwargs)
    return decorated_function


class TokenView(APIView):
    def __init__(self, dao=None, token_helper=None,
                 schema=None, request=None, *args, **kwargs):
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

        return ({"error": "Invalid Credentials"},
                HTTPStatus.HTTP_400_BAD_REQUEST)
