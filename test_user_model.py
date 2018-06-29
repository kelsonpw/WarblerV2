from app import app, db, User
from flask_testing import TestCase
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_test_db'
        db.create_all()

        user1 = User(
            username="kelson", email="kelson@rithm.com", password="password")
        user2 = User(
            username="rithmrithm",
            email="rithm@rithm.com",
            password="rithmrithm")
        db.session.add_all([user1, user2])
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_user(self):
        user1 = User.query.filter(User.username.like(f"%{'kelson'}%")).one()
        user2 = User.query.filter(
            User.username.like(f"%{'rithmrithm'}%")).one()
        self.assertEqual(user1.email, 'kelson@rithm.com')
        self.assertEqual(user2.email, 'rithm@rithm.com')


if __name__ == '__main__':
    unittest.main()