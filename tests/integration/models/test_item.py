from models.item import ItemModel
from models.store import StoreModel
from tests.test_base import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test Store')
            store.save_to_db()
            item = ItemModel('test', 19.99, store.id)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test Store')
            store.save_to_db()
            item = ItemModel('test', 19.99, store.id)
            item.save_to_db()

            self.assertEqual(item.store.name, 'Test Store')
