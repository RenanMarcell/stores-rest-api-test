from models.store import StoreModel
from tests.test_base import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/Test')

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Test'))
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'name': 'Test', 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test')
                request = client.post('/store/Test')

                self.assertEqual(request.status_code, 400)
                self.assertIsNotNone(StoreModel.find_by_name('Test'))
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {
                    'message': "A store with name '{}' already exists.".format('Test')
                })

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('Test'))
                request = client.post('/store/Test')

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Test'))
                request = client.delete('/store/Test')
                self.assertIsNone(StoreModel.find_by_name('Test'))

                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/Test')

                self.assertEqual(request.status_code, 201)
                request = client.get('/store/Test')
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'name': 'Test', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                request = client.get('/store/Test')

                self.assertEqual(request.status_code, 404)
                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/Test')
                request_item = client.post('/item/TestItem', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(request.status_code, 201)
                self.assertEqual(request_item.status_code, 201)

                request = client.get('/store/Test')

                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {
                    'name': 'Test', 'items': [{'name': 'TestItem', 'price': 19.99}]
                })

        pass

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/Test1')
                request2 = client.post('/store/Test2')

                self.assertEqual(request.status_code, 201)
                self.assertEqual(request2.status_code, 201)

                request = client.get('/stores')

                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'stores': [{
                            'name': 'Test1', 'items': []
                        },
                        {
                            'name': 'Test2', 'items': []
                        }
                ]})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/Test1')
                request2 = client.post('/store/Test2')
                request_item1 = client.post('/item/TestItem1', data={'price': 19.99, 'store_id': 1})
                request_item2 = client.post('/item/TestItem2', data={'price': 29.99, 'store_id': 1})

                self.assertEqual(request.status_code, 201)
                self.assertEqual(request2.status_code, 201)
                self.assertEqual(request_item1.status_code, 201)
                self.assertEqual(request_item2.status_code, 201)

                request = client.get('/stores')

                self.assertDictEqual(json.loads(request.data.decode('utf-8')), {'stores': [{
                            'name': 'Test1', 'items': [{'name': 'TestItem1', 'price': 19.99},
                                                       {'name': 'TestItem2', 'price': 29.99}]
                        },
                        {
                            'name': 'Test2', 'items': []
                        }
                ]})
