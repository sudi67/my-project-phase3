from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

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
