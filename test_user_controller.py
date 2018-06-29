from app import app, db, User, Message, bcrypt
from flask_testing import TestCase
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_test_db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        db.create_all()
        password1 = bcrypt.generate_password_hash("password").decode('UTF-8')
        password2 = bcrypt.generate_password_hash("rithmrithm").decode('UTF-8')
        user1 = User(
            username="kelson", email="kelson@rithm.com", password=password1)
        user2 = User(
            username="rithmrithm", email="rithm@rithm.com", password=password2)
        msg1 = Message(text="rithmrithm I was here", user_id=user1.id)
        msg2 = Message(text="Its a good good day", user_id=user2.id)
        db.session.add_all([msg1, msg2, user1, user2])
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    # def login(self, username, password):
    #     client = app.test_client()
    #     return client.post(
    #         '/login',
    #         data={
    #             'username': 'username',
    #             'password': 'password'
    #         },
    #         follow_redirects=True)

# Test Root

    def test_root(self):
        client = app.test_client()
        result = client.get("/")
        self.assertIn(b'<h4>New to Warbler?</h4>', result.data)

#login

    def test_login(self):
        client = app.test_client()
        result = client.post(
            '/login',
            data={
                'username': 'kelson',
                'password': 'password'
            },
            follow_redirects=True)
        self.assertIn(b'Hello, kelson!', result.data)
        result = client.get('/logout', follow_redirects=True)
        self.assertEqual(result.status_code, 200)


#Root when loged in

    def test_loggedin_root(self):
        client = app.test_client()
        client.post(
            '/login', data={
                'username': 'kelson',
                'password': 'password'
            })
        result = client.get('/')
        self.assertIn(b'<p class="small">Messages</p>', result.data)

if __name__ == '__main__':
    unittest.main()