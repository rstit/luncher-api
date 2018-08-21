from flask import current_app
from itsdangerous import TimestampSigner


class TokenHelper:
    def __init__(self) -> None:
        self.serializer = TimestampSigner(current_app.config.get('SECRET_KEY'))
        self.s = TimestampSigner(current_app.config.get('SECRET_KEY'))

    def create(self, user_id):
        return self.s.sign(str({"user_id": user_id}))

    def unsign(self, token):
        return self.s.unsign(token)
