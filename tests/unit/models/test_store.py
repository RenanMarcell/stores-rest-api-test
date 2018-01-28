from tests.unit.test_unit_base import UnitBaseTest
from models.store import StoreModel


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('Test')

        self.assertEqual(store.name, 'Test')
