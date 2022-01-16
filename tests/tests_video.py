from json import loads
import unittest

from app import create_app, db


class VideoModelTestCase(unittest.TestCase):
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

    def post(self):
        data = {
            'name': 'Unit Tests',
            'description': 'Unittest tutorial'
        }
        return self.client.post('/tutorials', json=data)

    def get(self):
        return self.client.get('/tutorials')

    def test_post(self):
        res = self.post()
        video = loads(res.get_json())

        self.assertTrue(res.status_code == 200)
        self.assertTrue(video['name'] == 'Unit Tests')

    def test_get(self):
        self.post()
        res = self.get()
        videos = loads(res.get_json())

        self.assertTrue(res.status_code == 200)
        self.assertTrue(len(videos) == 1)
        self.assertTrue(videos[0]['id'] == 1)

    def test_put(self):
        self.post()
        res = self.client.put('/tutorials/1', json={'name': 'PUT Method'})
        video = loads(res.get_json())

        self.assertTrue(res.status_code == 200)
        self.assertTrue(video['name'] == 'PUT Method')

    def test_delete(self):
        self.post()
        res = self.client.delete('/tutorials/1')
        videos = loads(self.get().get_json())

        self.assertTrue(res.status_code == 204)
        self.assertTrue(len(videos) == 0)
