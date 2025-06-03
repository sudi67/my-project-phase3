from health_tracker.models.foodentry import FoodEntry
from health_tracker.models.mealplan import MealPlan
from health_tracker.models.goal import Goal

def create_foodentry(session, user_id, name, calories, protein=None, fat=None, carbs=None):
    foodentry = FoodEntry(
        user_id=user_id,
        name=name,
        calories=calories,
        protein=protein,
        fat=fat,
        carbs=carbs
    )
    session.add(foodentry)
    session.commit()
    session.refresh(foodentry)
    return foodentry

def update_foodentry(session, foodentry_id, name=None, calories=None, protein=None, fat=None, carbs=None):
    foodentry = session.query(FoodEntry).filter(FoodEntry.id == foodentry_id).first()
    if not foodentry:
        return None
    if name is not None:
        foodentry.name = name
    if calories is not None:
        foodentry.calories = calories
    if protein is not None:
        foodentry.protein = protein
    if fat is not None:
        foodentry.fat = fat
    if carbs is not None:
        foodentry.carbs = carbs
    session.commit()
    session.refresh(foodentry)
    return foodentry

def delete_foodentry(session, foodentry_id):
    foodentry = session.query(FoodEntry).filter(FoodEntry.id == foodentry_id).first()
    if not foodentry:
        return False
    session.delete(foodentry)
    session.commit()
    return True

def create_mealplan(session, user_id, date, meal_type, week=None, day=None, food_name=None, calories=None, fat=None, protein=None):
    mealplan = MealPlan(
        user_id=user_id,
        date=date,
        meal_type=meal_type,
        week=week,
        day=day,
        food_name=food_name,
        calories=calories,
        fat=fat,
        protein=protein
    )
    session.add(mealplan)
    session.commit()
    session.refresh(mealplan)
    return mealplan

def update_mealplan(session, mealplan_id, date=None, meal_type=None, week=None, day=None, food_name=None, calories=None, fat=None, protein=None):
    mealplan = session.query(MealPlan).filter(MealPlan.id == mealplan_id).first()
    if not mealplan:
        return None
    if date is not None:
        mealplan.date = date
    if meal_type is not None:
        mealplan.meal_type = meal_type
    if week is not None:
        mealplan.week = week
    if day is not None:
        mealplan.day = day
    if food_name is not None:
        mealplan.food_name = food_name
    if calories is not None:
        mealplan.calories = calories
    if fat is not None:
        mealplan.fat = fat
    if protein is not None:
        mealplan.protein = protein
    session.commit()
    session.refresh(mealplan)
    return mealplan

def delete_mealplan(session, mealplan_id):
    mealplan = session.query(MealPlan).filter(MealPlan.id == mealplan_id).first()
    if not mealplan:
        return False
    session.delete(mealplan)
    session.commit()
    return True

def create_goal(session, user_id, description):
    goal = Goal(
        user_id=user_id,
        description=description
    )
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal

def update_goal(session, goal_id, description=None):
    goal = session.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        return None
    if description is not None:
        goal.description = description
    session.commit()
    session.refresh(goal)
    return goal

def delete_goal(session, goal_id):
    goal = session.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        return False
    session.delete(goal)
    session.commit()
    return True

def list_goals_by_user(session, user_id):
    return session.query(Goal).filter(Goal.user_id == user_id).all()
