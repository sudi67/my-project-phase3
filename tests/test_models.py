import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from health_tracker.models.base import Base
from health_tracker.models.user import User
from health_tracker.models.foodentry import FoodEntry
from health_tracker.models.mealplan import MealPlan
from datetime import date

class TestModels(unittest.TestCase):
    def setUp(self):
        # Use in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_user_model(self):
        user = User(name='testuser')
        self.session.add(user)
        self.session.commit()

        queried_user = self.session.query(User).filter_by(name='testuser').one()
        self.assertEqual(queried_user.name, 'testuser')
        self.assertEqual(repr(queried_user), f"<User(id={queried_user.id}, name='testuser')>")

    def test_foodentry_model(self):
        user = User(name='testuser')
        self.session.add(user)
        self.session.commit()

        food_entry = FoodEntry(user_id=user.id, food='Apple', calories=95, date=date.today())
        self.session.add(food_entry)
        self.session.commit()

        queried_entry = self.session.query(FoodEntry).filter_by(food='Apple').one()
        self.assertEqual(queried_entry.food, 'Apple')
        self.assertEqual(queried_entry.calories, 95)
        self.assertEqual(repr(queried_entry), f"<FoodEntry(id={queried_entry.id}, food='Apple', calories=95, date={queried_entry.date})>")

    def test_mealplan_model(self):
        user = User(name='testuser')
        self.session.add(user)
        self.session.commit()

        meal_plan = MealPlan(user_id=user.id, week_number=1, plan_details='{"Monday": "Salad"}')
        self.session.add(meal_plan)
        self.session.commit()

        queried_plan = self.session.query(MealPlan).filter_by(week_number=1).one()
        self.assertEqual(queried_plan.week_number, 1)
        self.assertEqual(repr(queried_plan), f"<MealPlan(id={queried_plan.id}, week_number=1)>")

if __name__ == '__main__':
    unittest.main()
