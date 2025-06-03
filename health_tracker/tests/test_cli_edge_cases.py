import unittest
from click.testing import CliRunner
from health_tracker.cli import cli
from health_tracker.db.db import init_db

class TestCLIEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        self.runner = CliRunner()
        self.cli = cli

    def test_user_create_missing_email(self):
        result = self.runner.invoke(self.cli, ['user', 'create', '--name', 'user1'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error", result.output)

    def test_user_create_duplicate(self):
        self.runner.invoke(self.cli, ['user', 'create', '--name', 'user2', '--email', 'user2@example.com'])
        result = self.runner.invoke(self.cli, ['user', 'create', '--name', 'user2', '--email', 'user2@example.com'], catch_exceptions=False)
        self.assertIn("already exists", result.output)

    def test_foodentry_create_missing_required(self):
        result = self.runner.invoke(self.cli, ['foodentry', 'create', '--user-id', '1'])
        self.assertNotEqual(result.exit_code, 0)

    def test_mealplan_create_invalid_date(self):
        result = self.runner.invoke(self.cli, ['mealplan', 'create', '--user-id', '1', '--date', 'invalid-date', '--meal-type', 'lunch'], catch_exceptions=False)
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value: Invalid date format. Use YYYY-MM-DD.", result.output)

    def test_mealplan_update_invalid_date(self):
        result = self.runner.invoke(self.cli, ['mealplan', 'update', '--mealplan-id', '1', '--date', 'invalid-date'], catch_exceptions=False)
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value: Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY or MM/DD/YYYY.", result.output)

if __name__ == '__main__':
    unittest.main()
