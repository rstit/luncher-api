from flask_testing import TestCase

from luncher.app import create_app
from luncher.extensions import db


class BaseIntegrationTest(TestCase):

    def create_app(self):
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
