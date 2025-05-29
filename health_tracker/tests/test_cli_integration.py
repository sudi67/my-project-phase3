import unittest
import subprocess
import sys

class TestCLIIntegration(unittest.TestCase):
    def run_cli(self, args):
        cmd = [sys.executable, '-m', 'health_tracker.cli'] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_user_foodentry_mealplan_flow(self):
        # Initialize the database first
        result = self.run_cli(['init'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('Database initialized', result.stdout)

        # Create a user
        result = self.run_cli(['user', 'create', '--name', 'intuser', '--email', 'intuser@example.com'])
        self.assertEqual(result.returncode, 0)
        self.assertIn("User 'intuser' created.", result.stdout)

        # Create a food entry for the user
        result = self.run_cli(['foodentry', 'create', '--user-id', '1', '--name', 'Banana', '--calories', '105'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('FoodEntry created', result.stdout)

        # Create a meal plan for the user
        result = self.run_cli(['mealplan', 'create', '--user-id', '1', '--date', '2024-01-01', '--meal-type', 'breakfast'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('MealPlan created', result.stdout)

        # Update the meal plan
        result = self.run_cli(['mealplan', 'update', '--mealplan-id', '1', '--meal-type', 'lunch'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('MealPlan updated', result.stdout)

        # Delete the food entry
        result = self.run_cli(['foodentry', 'delete', '--foodentry-id', '1'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('FoodEntry deleted', result.stdout)

        # Delete the user
        result = self.run_cli(['user', 'delete', '--user-id', '1'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('User deleted', result.stdout)

if __name__ == '__main__':
    unittest.main()
