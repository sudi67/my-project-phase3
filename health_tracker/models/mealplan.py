from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class MealPlan(Base):
    __tablename__ = 'mealplans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    week = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    food_name = Column(String, nullable=True)
    meal_type = Column(String, nullable=False)  # e.g., breakfast, lunch, dinner, snack
    calories = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)

    user = relationship('User', back_populates='mealplans')

    def __init__(self, user_id, date, meal_type, week=None, day=None, food_name=None, calories=None, fat=None, protein=None):
        if isinstance(date, str):
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format for MealPlan. Use YYYY-MM-DD.")
        elif not isinstance(date, datetime.date):
            raise TypeError("date must be a datetime.date object or a valid date string")
        self.user_id = user_id
        self.date = date
        self.meal_type = meal_type
        self.week = week
        self.day = day
        self.food_name = food_name
        self.calories = calories
        self.fat = fat
        self.protein = protein

    def __repr__(self):
        return f"<MealPlan(id={self.id}, date={self.date}, week={self.week}, day={self.day}, meal_type='{self.meal_type}', calories={self.calories}, fat={self.fat}, protein={self.protein})>"
