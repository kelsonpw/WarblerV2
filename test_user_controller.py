from app import app, db, User, Message, bcrypt
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
            username="kelson", email="kelson@rithm.com", password=password1)
        user2 = User(
            username="rithmrithm", email="rithm@rithm.com", password=password2)
        msg1 = Message(text="rithmrithm I was here", user_id=user1.id)
        msg2 = Message(text="Its a good good day", user_id=user2.id)
        db.session.add_all([msg1, msg2, user1, user2])
        db.session.commit()

    def tearDown(self):
        """ teardown after tests run """
        db.session.close()
        db.drop_all()

    def login(self, username, password):
        """ login method for users tests """
        return self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    def logout(self):
        """ logout method for users tests """
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        """ testing login and logout for users """
        result = self.login('kelson', 'password')
        self.assertIn(b'Hello, kelson!', result.data)
        result = self.logout()
        self.assertIn(b'You have successfully logged out.', result.data)

# Test Root

    def test_root(self):
        """ testing root page for guests """
        result = self.client.get("/")

        self.assertIn(b'<h4>New to Warbler?</h4>', result.data)


# #Root when loged in

    def test_loggedin_root(self):
        """ testing root page for logged in user """
        self.login('kelson', 'password')
        result = self.client.get('/')
        self.assertIn(b'<p>@kelson</p>', result.data)

    def test_user_create(self):
        """ testing signup for users """
        result = self.client.post(
            '/signup',
            data={
                'username': 'usercreate',
                'password': 'testing',
                'email': 'email@testuser.com'
            },
            follow_redirects=True)
        self.assertIn(b'usercreate', result.data)

    def test_user_update(self):
        """ edit method for users tests """
        self.login('kelson', 'password')
        result = self.client.patch(
            '/users/1',
            data={
                'username': 'kelson',
                'password': 'password',
                'email': 'updatedemail@gmail.com'
            },
            follow_redirects=True)
        self.assertIn(b'updatedemail@gmail.com', result.data)

    def test_user_destroy(self):
        """ delete method for users tests """
        self.login('kelson', 'password')
        result = self.client.delete('/users/1', follow_redirects=True)
        testuser = User.query.all()[0]
        self.assertNotEqual(testuser.username, 'kelson')
        self.assertNotEqual(testuser.id, '1')

if __name__ == '__main__':
    unittest.main()