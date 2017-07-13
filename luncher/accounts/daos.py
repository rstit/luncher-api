from luncher.accounts.models import User
from luncher.database import BaseDao


class UserDao(BaseDao):
    def __init__(self):
        super().__init__(User)
