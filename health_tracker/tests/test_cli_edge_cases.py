import unittest
from click.testing import CliRunner
from health_tracker.cli import main

class TestCLIEdgeCases(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.cli = main

    def test_user_create_missing_email(self):
        result = self.runner.invoke(self.cli, ['user', 'create', '--name', 'user1'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error", result.output)

    def test_user_create_duplicate(self):
        self.runner.invoke(self.cli, ['user', 'create', '--name', 'user2', '--email', 'user2@example.com'])
        result = self.runner.invoke(self.cli, ['user', 'create', '--name', 'user2', '--email', 'user2@example.com'])
        self.assertIn("already exists", result.output)

    def test_foodentry_create_missing_required(self):
        result = self.runner.invoke(self.cli, ['foodentry', 'create', '--user-id', '1'])
        self.assertNotEqual(result.exit_code, 0)

    def test_mealplan_create_invalid_date(self):
        result = self.runner.invoke(self.cli, ['mealplan', 'create', '--user-id', '1', '--date', 'invalid-date', '--meal-type', 'lunch'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid date format", result.output)

    def test_mealplan_update_invalid_date(self):
        result = self.runner.invoke(self.cli, ['mealplan', 'update', '--mealplan-id', '1', '--date', 'invalid-date'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid date format", result.output)

if __name__ == '__main__':
    unittest.main()
