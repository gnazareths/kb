import os
import unittest

from .. import app, db
from .models import User, Task

test_db = 'test.db'

class Tests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
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
        response = self.register("guilherme@minerva.kgi.edu", "Guilherme", "password", "password")
        self.assertEqual(response.status_code, 200)
