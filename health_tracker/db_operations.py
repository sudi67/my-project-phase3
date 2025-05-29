from sqlalchemy.orm import Session
from health_tracker.models.user import User
from health_tracker.models.mealplan import MealPlan
from health_tracker.models.foodentry import FoodEntry


def create_user(db: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, username: str = None, email: str = None) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if username:
        user.username = username
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

# MealPlan CRUD operations
def create_mealplan(db: Session, user_id: int, date, meal_type: str) -> MealPlan:
    mealplan = MealPlan(user_id=user_id, date=date, meal_type=meal_type)
    db.add(mealplan)
    db.commit()
    db.refresh(mealplan)
    return mealplan

def get_mealplan(db: Session, mealplan_id: int) -> MealPlan:
    return db.query(MealPlan).filter(MealPlan.id == mealplan_id).first()

def update_mealplan(db: Session, mealplan_id: int, date = None, meal_type: str = None) -> MealPlan:
    mealplan = db.query(MealPlan).filter(MealPlan.id == mealplan_id).first()
    if not mealplan:
        return None
    if date:
        mealplan.date = date
    if meal_type:
        mealplan.meal_type = meal_type
    db.commit()
    db.refresh(mealplan)
    return mealplan

def delete_mealplan(db: Session, mealplan_id: int) -> bool:
    mealplan = db.query(MealPlan).filter(MealPlan.id == mealplan_id).first()
    if not mealplan:
        return False
    db.delete(mealplan)
    db.commit()
    return True

# FoodEntry CRUD operations
def create_foodentry(db: Session, user_id: int, name: str, calories: float, protein: float = None, fat: float = None, carbs: float = None) -> FoodEntry:
    foodentry = FoodEntry(user_id=user_id, name=name, calories=calories, protein=protein, fat=fat, carbs=carbs)
    db.add(foodentry)
    db.commit()
    db.refresh(foodentry)
    return foodentry

def get_foodentry(db: Session, foodentry_id: int) -> FoodEntry:
    return db.query(FoodEntry).filter(FoodEntry.id == foodentry_id).first()

def update_foodentry(db: Session, foodentry_id: int, name: str = None, calories: float = None, protein: float = None, fat: float = None, carbs: float = None) -> FoodEntry:
    foodentry = db.query(FoodEntry).filter(FoodEntry.id == foodentry_id).first()
    if not foodentry:
        return None
    if name:
        foodentry.name = name
    if calories is not None:
        foodentry.calories = calories
    if protein is not None:
        foodentry.protein = protein
    if fat is not None:
        foodentry.fat = fat
    if carbs is not None:
        foodentry.carbs = carbs
    db.commit()
    db.refresh(foodentry)
    return foodentry

def delete_foodentry(db: Session, foodentry_id: int) -> bool:
    foodentry = db.query(FoodEntry).filter(FoodEntry.id == foodentry_id).first()
    if not foodentry:
        return False
    db.delete(foodentry)
    db.commit()
    return True
