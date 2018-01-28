from models.user import UserModel
from tests.unit.test_unit_base import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Test', 'Test')

        self.assertEqual(user.username, 'Test')
        self.assertEqual(user.password, 'Test')
