from app import app, db, Message, User
from flask_testing import TestCase
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_test_db'
        db.create_all()