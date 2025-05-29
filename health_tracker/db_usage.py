from health_tracker.db import SessionLocal, init_db
from health_tracker.db_operations import (
    create_user, get_user, update_user, delete_user,
    create_mealplan, get_mealplan, update_mealplan, delete_mealplan,
    create_foodentry, get_foodentry, update_foodentry, delete_foodentry
)
from datetime import date

def main():
   
    init_db()

    
    db = SessionLocal()

   
    user = create_user(db, username="john_doe", email="john@example.com")
    print(f"Created user: {user}")

    fetched_user = get_user(db, user.id)
    print(f"Fetched user: {fetched_user}")

    updated_user = update_user(db, user.id, username="john_doe_updated")
    print(f"Updated user: {updated_user}")

    mealplan = create_mealplan(db, user_id=user.id, date=date.today(), meal_type="lunch")
    print(f"Created mealplan: {mealplan}")

    fetched_mealplan = get_mealplan(db, mealplan.id)
    print(f"Fetched mealplan: {fetched_mealplan}")

    updated_mealplan = update_mealplan(db, mealplan.id, meal_type="dinner")
    print(f"Updated mealplan: {updated_mealplan}")

   
    foodentry = create_foodentry(db, user_id=user.id, name="Apple", calories=95.0, protein=0.5, fat=0.3, carbs=25.0)
    print(f"Created foodentry: {foodentry}")

    fetched_foodentry = get_foodentry(db, foodentry.id)
    print(f"Fetched foodentry: {fetched_foodentry}")

    updated_foodentry = update_foodentry(db, foodentry.id, calories=100.0)
    print(f"Updated foodentry: {updated_foodentry}")

    
    delete_foodentry(db, foodentry.id)
    delete_mealplan(db, mealplan.id)
    delete_user(db, user.id)

    db.close()

if __name__ == "__main__":
    main()
