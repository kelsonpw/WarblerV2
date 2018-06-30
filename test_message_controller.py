from app import app, db, Message, User, bcrypt
from flask_testing import TestCase
import unittest


class BaseTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):
        """ set up, create 2 users and commit to test db """
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_test_db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        db.create_all()
        password1 = bcrypt.generate_password_hash("password").decode('UTF-8')
        password2 = bcrypt.generate_password_hash("rithmrithm").decode('UTF-8')
        user1 = User(
            username="vigi", email="vigi1234@rithm.com", password=password1)
        user2 = User(
            username="rithmrithm", email="rithm@rithm.com", password=password2)
        msg1 = Message(text="rithmrithm I was here", user_id=user1.id)
        msg2 = Message(text="Its a good good day", user_id=user2.id)
        db.session.add_all([msg1, msg2, user1, user2])
        db.session.commit()

    def login(self, username, password):
        return self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    def tearDown(self):
        db.session.close()
        db.drop_all()

    #test route for add message
    def test_messageform(self):
        self.login('vigi', 'password')
        result = self.client.get('/users/1/messages/new')
        self.assertIn(b'Add my message!', result.data)

    def test_message_create(self):
        self.login('vigi', 'password')
        result = self.client.post(
            "/users/1/messages",
            data={"text": "here here rithm"},
            follow_redirects=True)

        self.assertIn(b'here here rithm', result.data)
        message1 = Message.query.filter(Message.user_id.in_([1]))[0]
        result = self.client.get('/users/1/messages/' + str(message1.id))
        self.assertIn(b'here here rithm', result.data)

    # def test_message_show(self):
    #     self.login('vigi', 'password')
    #     self.client.post(
    #         "/users/1/messages",
    #         data={
    #             'text': 'Its diffrent !!!!!!!!!',
    #             'user_id': '1'
    #         })
    #     result = self.client.get('/users/1/messages/1')


if __name__ == '__main__':
    unittest.main()