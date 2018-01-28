from models.user import UserModel
from tests.test_base import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'Test', 'password': 'Test'})

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('Test'))
                self.assertDictEqual(
                    json.loads((request.data.decode('utf-8'))),
                    {
                        'message': 'User created successfully.'
                    }
                )
        pass

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'Test', 'password': 'Test'})
                auth_request = client.post('/auth', data=json.dumps({
                    'username': 'Test', 'password': 'Test'
                }),
                    headers={'Content-Type': 'application/json'}
                )
                self.assertIn('access_token', json.loads(auth_request.data.decode('utf-8')).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'Test', 'password': 'Test'})
                request = client.post('/register', data={'username': 'Test', 'password': 'Test'})

                self.assertEqual(request.status_code, 400)
                self.assertIsNotNone(UserModel.find_by_username('Test'))
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(
                    request.data.decode('utf-8')
                ))
