import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from health_tracker.models.base import Base
from health_tracker.models.user import User
from health_tracker.models.foodentry import FoodEntry
from health_tracker.models.mealplan import MealPlan
from health_tracker.models.goal import Goal
from health_tracker.db import engine, SessionLocal
from datetime import date

class TestCRUDOperations(unittest.TestCase):
    def setUp(self):
        # Use the actual engine from health_tracker.db for integration testing
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_update_delete_user(self):
        user = User(name='cruduser')
        self.session.add(user)
        self.session.commit()

        # Update
        user.name = 'updateduser'
        self.session.commit()

        queried_user = self.session.query(User).filter_by(name='updateduser').one()
        self.assertEqual(queried_user.name, 'updateduser')

        # Delete
        self.session.delete(queried_user)
        self.session.commit()

        users = self.session.query(User).filter_by(name='updateduser').all()
        self.assertEqual(len(users), 0)

    def test_create_update_delete_foodentry(self):
        user = User(name='fooduser')
        self.session.add(user)
        self.session.commit()

        food_entry = FoodEntry(user_id=user.id, food='Banana', calories=105, date=date.today())
        self.session.add(food_entry)
        self.session.commit()

        # Update
        food_entry.calories = 110
        self.session.commit()

        queried_entry = self.session.query(FoodEntry).filter_by(food='Banana').one()
        self.assertEqual(queried_entry.calories, 110)

        # Delete
        self.session.delete(queried_entry)
        self.session.commit()

        entries = self.session.query(FoodEntry).filter_by(food='Banana').all()
        self.assertEqual(len(entries), 0)

    def test_create_update_delete_mealplan(self):
        user = User(name='mealuser')
        self.session.add(user)
        self.session.commit()

        meal_plan = MealPlan(user_id=user.id, week_number=2, plan_details='{"Tuesday": "Soup"}')
        self.session.add(meal_plan)
        self.session.commit()

        # Update
        meal_plan.plan_details = '{"Tuesday": "Steak"}'
        self.session.commit()

        queried_plan = self.session.query(MealPlan).filter_by(week_number=2).one()
        self.assertEqual(queried_plan.plan_details, '{"Tuesday": "Steak"}')

        # Delete
        self.session.delete(queried_plan)
        self.session.commit()

        plans = self.session.query(MealPlan).filter_by(week_number=2).all()
        self.assertEqual(len(plans), 0)

    def test_create_update_delete_goal(self):
        user = User(name='goaluser')
        self.session.add(user)
        self.session.commit()

        goal = Goal(user_id=user.id, description='Lose weight')
        self.session.add(goal)
        self.session.commit()

        # Update
        goal.description = 'Gain muscle'
        self.session.commit()

        queried_goal = self.session.query(Goal).filter_by(description='Gain muscle').one()
        self.assertEqual(queried_goal.description, 'Gain muscle')

        # Delete
        self.session.delete(queried_goal)
        self.session.commit()

        goals = self.session.query(Goal).filter_by(description='Gain muscle').all()
        self.assertEqual(len(goals), 0)

if __name__ == '__main__':
    unittest.main()
