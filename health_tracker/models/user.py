from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)


    mealplans = relationship('MealPlan', back_populates='user', cascade='all, delete-orphan')
    foodentries = relationship('FoodEntry', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
