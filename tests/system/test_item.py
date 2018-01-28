from models.item import ItemModel
from tests.test_base import BaseTest
from models.store import StoreModel
from models.user import UserModel
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'Test', 'password': 'Test'})
                self.assertEqual(request.status_code, 201)
                auth_request = client.post('/auth', data=json.dumps({
                    'username': 'Test', 'password': 'Test'
                }),
                    headers={'Content-Type': 'application/json'}
                )
                self.assertIn('access_token', json.loads(auth_request.data.decode('utf-8')).keys())
                self.auth_token = json.loads(auth_request.data.decode('utf-8'))['access_token']

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)

                request = client.get('/item/Test')

                self.assertEqual(request.status_code, 400)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)
                get_request = client.get('/item/Test2', headers={
                    'Authorization': 'JWT {}'.format(self.auth_token)
                })
                self.assertEqual(get_request.status_code, 404)
                self.assertDictEqual(json.loads(get_request.data.decode('utf-8')), {'message': 'Item not found'})

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)
                get_request = client.get('/item/Test', headers={
                    'Authorization': 'JWT {}'.format(self.auth_token)
                })
                self.assertEqual(get_request.status_code, 201)
                self.assertDictEqual(json.loads(get_request.data.decode('utf-8')), {'name': 'Test', 'price': 19.99})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)

                request = client.delete('/item/Test')

                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'name': 'Test', 'price': 19.99})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                request = client.post('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 400)
                self.assertDictEqual(json.loads(request.data.decode('utf-8')),
                                     {'message': "An item with name '{}' already exists.".format('Test')})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.put('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'name': 'Test', 'price': 19.99})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.put('/item/Test', data={'price': 19.99, 'store_id': 1})
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'name': 'Test', 'price': 19.99})
                request = client.put('/item/Test', data={'price': 39.99, 'store_id': 1})
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'name': 'Test', 'price': 39.99})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')
                self.assertEqual(response.status_code, 201)
                request = client.post('/item/Test1', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)
                request = client.post('/item/Test2', data={'price': 29.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)
                request = client.post('/item/Test3', data={'price': 39.99, 'store_id': 1})
                self.assertEqual(request.status_code, 201)
                request = client.get('/items')
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'items': [
                    {'name': 'Test1', 'price': 19.99},
                    {'name': 'Test2', 'price': 29.99},
                    {'name': 'Test3', 'price': 39.99}
                ]})
