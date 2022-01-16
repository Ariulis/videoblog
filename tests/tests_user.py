from json import loads
import unittest

from app import db, create_app


class UserModelTestCase(unittest.TestCase):
    email = 'admin@test.com'
    password = '123456'
    name = 'Admin'

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_user(self):
        return self.client.post('/auth/register', json={'email': self.email, 'password': self.password, 'name': self.name})

    def test_login(self):
        self.add_user()
        res = self.client.post(
            '/auth/login', json={'email': self.email, 'password': self.password})
        data = loads(res.get_json()['user'])

        self.assertTrue(res.status_code == 200)
        self.assertTrue(data['name'] == 'Admin')

    def test_register(self):
        res = self.add_user()
        data = loads(res.get_json()['user'])

        self.assertTrue(res.status_code == 200)
        self.assertTrue(data['name'] == 'Admin')
