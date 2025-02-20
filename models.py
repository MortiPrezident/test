from sqlalchemy import Column, String, Integer, JSON
from database import Base

class Recipe(Base):
    __tablename__ = 'Recipe'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    count_views = Column(Integer)
    cooking_time = Column(Integer, default=0)
    description = Column(String)
    ingredients = Column(JSON)

