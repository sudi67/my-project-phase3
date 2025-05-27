from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week_number = Column(Integer, nullable=False)
    plan_details = Column(String, nullable=True)  # JSON or text representation of the plan

    user = relationship('User', back_populates='meal_plans')

    def __repr__(self):
        return f"<MealPlan(id={self.id}, week_number={self.week_number})>"
