from models.item import ItemModel
from models.store import StoreModel
from tests.test_base import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        with self.app_context():
            store = StoreModel('Test')

            self.assertEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test')

            self.assertIsNone(StoreModel.find_by_name('Test'),
                              "Found a store with name {}, but expected not to.".format(store.name)
                              )

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('Test'),
                                 "Did not found a store with name {}, but expected to.".format(store.name)
                                 )

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('Test'),
                              "Found a store with name {}, but expected not to.".format(store.name)
                              )

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test')
            store.save_to_db()
            item = ItemModel('Test item', 19.99, store.id)

            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'Test item')

    def test_json(self):
        with self.app_context():
            store = StoreModel('Test')
            store.save_to_db()
            item1 = ItemModel('Test item1', 19.99, store.id)

            self.assertEqual(store.json(), {'name': 'Test', 'items': []})
            item1.save_to_db()
            self.assertEqual(store.json(), {'name': 'Test', 'items': [{'name': 'Test item1', 'price': 19.99}]})
