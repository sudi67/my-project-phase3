from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String, nullable=False)

    user = relationship('User', back_populates='goals')

    def __repr__(self):
        return f"<Goal(id={self.id}, description='{self.description}')>"
