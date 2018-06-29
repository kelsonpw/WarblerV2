from app import app, db, Message, User
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
        msg1 = Message(text="rithmrithm I was here", user_id=user1.id)
        msg2 = Message(text="Its a good good day", user_id=user2.id)
        db.session.add_all([msg1, msg2, user1, user2])
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_user(self):
        msg1 = Message.query.filter(
            Message.text.like(f"%{'rithmrithm I was here'}%")).one()
        msg2 = Message.query.filter(
            Message.text.like(f"%{'Its a good good day'}%")).one()
        self.assertIsNotNone(msg1)
        self.assertIsNotNone(msg2)


if __name__ == '__main__':
    unittest.main()