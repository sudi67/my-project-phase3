import unittest
from click.testing import CliRunner
from health_tracker.cli import main
from health_tracker.db.db import init_db, SessionLocal
from health_tracker.models.base import Base

class TestCLIUser(unittest.TestCase):
    def setUp(self):
        init_db()
        self.runner = CliRunner()
        self.session = SessionLocal()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(bind=self.session.bind)

    def test_create_and_list_user(self):
        # Create user
        result = self.runner.invoke(main, ['user', 'create', '--name', 'testuser', '--email', 'testuser@example.com'])
        self.assertIn("User 'testuser' created.", result.output)

        # Create duplicate user
        result = self.runner.invoke(main, ['user', 'create', '--name', 'testuser', '--email', 'testuser@example.com'])
        self.assertIn("User 'testuser' already exists.", result.output)

        # List users
        result = self.runner.invoke(main, ['user', 'list'])
        self.assertIn('testuser', result.output)

if __name__ == '__main__':
    unittest.main()
