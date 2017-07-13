from datetime import datetime

from flask import current_app
from itsdangerous import TimestampSigner


class TokenHelper:
    def __init__(self) -> None:
        self.serializer = TimestampSigner(current_app.config.SECRET_KEY)

    def create(self, user_id):
        s = TimestampSigner(current_app.config.SECRET_KEY)
        return s.sign({
            "datetime": datetime.now(),
            "user_id": user_id
        })
