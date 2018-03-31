import os
import unittest

from app import app, db
from app.models import User, Task

test_db = 'test.db'
basedir = os.path.abspath(os.path.dirname(__file__))

class Tests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, test_db)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def register(self, email, name, password, confirm_password):
        return self.app.post(
            '/register',
            data=dict(email=email, name=name, password=password, password_2=confirm_password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_successful_registration(self):
        response = self.register(email="guilherme@minerva.kgi.edu", name="Guilherme", password="password", confirm_password="password")
        self.assertEqual(response.status_code, 302)

    def test_not_email(self):
        response = self.register(email="guilherme", name="Guilherme", password="password", confirm_password="password")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
