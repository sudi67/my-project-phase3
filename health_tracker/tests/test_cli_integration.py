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
        # Accept either creation or already exists message
        self.assertTrue(
            "User 'intuser' created." in result.output or
            "User 'intuser' already exists." in result.output
        )

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

        user_id_int = int(user_id) if user_id is not None else None
        result = self.runner.invoke(cli, ['foodentry', 'create', '--user-id', str(user_id_int), '--name', 'Banana', '--calories', '105'])
                     
        result = self.runner.invoke(cli, ['mealplan', 'create', '--user-id', user_id, '--date', '2024-01-01', '--meal-type', 'breakfast'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('MealPlan created', result.output)

        # Parse mealplan ID from create output
        mealplan_id = None
        for line in result.output.splitlines():
            if 'MealPlan created' in line:
                # Example line: MealPlan created: <MealPlan(id=1, date=2024-01-01, week=None, day=None, meal_type='breakfast', calories=None, fat=None, protein=None)>
                start = line.find('id=') + 3
                end = line.find(',', start)
                if start > 2 and end > start:
                    mealplan_id = line[start:end].strip()
                    break
        self.assertIsNotNone(mealplan_id)

        # Update the meal plan
        result = self.runner.invoke(cli, ['mealplan', 'update', '--mealplan-id', mealplan_id, '--meal-type', 'lunch'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('MealPlan updated', result.output)
     
        result = self.runner.invoke(cli, ['user', 'delete', '--user-id', user_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('User deleted', result.output)

if __name__ == '__main__':
    unittest.main()
