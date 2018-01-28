from tests.unit.test_unit_base import UnitBaseTest
from models.item import ItemModel


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        # Since the item is not being saved to the DB, the store id doesn't matter
        item = ItemModel('test', 19.99, 0)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")

    def test_item_json(self):
        # Since the item is not being saved to the DB, the store id doesn't matter
        item = ItemModel('test', 19.99, 0)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))
