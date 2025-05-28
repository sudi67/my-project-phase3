from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class FoodEntry(Base):
    __tablename__ = 'foodentries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)

    user = relationship('User', back_populates='foodentries')

    def __repr__(self):
        return f"<FoodEntry(id={self.id}, name='{self.name}', calories={self.calories})>"
