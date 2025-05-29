import unittest
from click.testing import CliRunner
from health_tracker.cli import cli

class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_user_foodentry_mealplan_flow(self):
        # Initialize the database first
        result = self.runner.invoke(cli, ['init'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Database initialized', result.output)

        # Create a user
        result = self.runner.invoke(cli, ['user', 'create', '--name', 'intuser', '--email', 'intuser@example.com'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("User 'intuser' created.", result.output)

        # Get user id dynamically by listing users
        result = self.runner.invoke(cli, ['user', 'list'])
        self.assertEqual(result.exit_code, 0)
        user_id = None
        for line in result.output.splitlines():
            if 'intuser' in line:
                parts = line.split(',')
                for part in parts:
                    if part.strip().startswith('ID:'):
                        user_id = part.strip().split(' ')[1]
                        break
        self.assertIsNotNone(user_id)

        # Create a food entry for the user
        result = self.runner.invoke(cli, ['foodentry', 'create', '--user-id', user_id, '--name', 'Banana', '--calories', '105'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('FoodEntry created', result.output)

        # Create a meal plan for the user
        result = self.runner.invoke(cli, ['mealplan', 'create', '--user-id', user_id, '--date', '2024-01-01', '--meal-type', 'breakfast'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('MealPlan created', result.output)

        # Update the meal plan
        result = self.runner.invoke(cli, ['mealplan', 'update', '--mealplan-id', '1', '--meal-type', 'lunch'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('MealPlan updated', result.output)

        # Delete the food entry
        result = self.runner.invoke(cli, ['foodentry', 'delete', '--foodentry-id', '1'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('FoodEntry deleted', result.output)

        # Delete the user
        result = self.runner.invoke(cli, ['user', 'delete', '--user-id', user_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('User deleted', result.output)

if __name__ == '__main__':
    unittest.main()
