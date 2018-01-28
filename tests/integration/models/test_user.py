from models.user import UserModel
from tests.test_base import BaseTest


class UserTest(BaseTest):
    def test_find_username(self):
        with self.app_context():
            user = UserModel('Test', 'Test')
            self.assertIsNone(user.find_by_username('Test'))
            user.save_to_db()
            self.assertEqual(user.find_by_username('Test').username, 'Test')

    def test_find_id(self):
        with self.app_context():
            user = UserModel('Test', 'Test')
            self.assertIsNone(user.find_by_id(user.id))
            user.save_to_db()
            self.assertEqual(user.find_by_id(user.id).username, 'Test')
