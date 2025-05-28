# health_tracker/models.py
# Define SQLAlchemy ORM models for the Health Simplified CLI Application

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    food_entries = relationship('FoodEntry', back_populates='user', cascade='all, delete-orphan')
    goals = relationship('Goal', back_populates='user', cascade='all, delete-orphan')
    meal_plans = relationship('MealPlan', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class FoodEntry(Base):
    __tablename__ = 'food_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship('User', back_populates='food_entries')

    def __repr__(self):
        return f"<FoodEntry(id={self.id}, food='{self.food}', calories={self.calories}, date={self.date})>"

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    daily_calories = Column(Integer, nullable=True)
    weekly_calories = Column(Integer, nullable=True)

    user = relationship('User', back_populates='goals')

    def __repr__(self):
        return f"<Goal(id={self.id}, daily_calories={self.daily_calories}, weekly_calories={self.weekly_calories})>"

class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week_number = Column(Integer, nullable=False)
    plan_details = Column(String, nullable=True)  # JSON or text representation of the plan

    user = relationship('User', back_populates='meal_plans')

    def __repr__(self):
        return f"<MealPlan(id={self.id}, week_number={self.week_number})>"
