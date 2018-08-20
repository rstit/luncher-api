from flask import current_app
from itsdangerous import TimestampSigner


class TokenHelper:
    def __init__(self) -> None:
        self.serializer = TimestampSigner(current_app.config.get('SECRET_KEY'))

    def create(self, user_id):
        s = TimestampSigner(current_app.config.get('SECRET_KEY'))
        return s.sign(str({"user_id": user_id}))
