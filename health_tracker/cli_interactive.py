import click
from health_tracker.db.db import SessionLocal, init_db
from health_tracker.models.user import User
from health_tracker.models.foodentry import FoodEntry
from health_tracker.models.mealplan import MealPlan
from health_tracker.models.goal import Goal

def prompt_user(session):

    name = click.prompt("Enter user name")
    email = click.prompt("Enter user email")
    if session.query(User).filter_by(username=name).first():
        click.echo(f"User '{name}' already exists.")
        return
    user = User(username=name, email=email)
    session.add(user)
    session.commit()
    click.echo(f"User '{name}' created.")

def prompt_update_user(session):
    click.echo("Update an existing user:")
    user_id = click.prompt("Enter user ID to update", type=int)
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        click.echo(f"User with ID {user_id} not found.")
        return
    new_name = click.prompt(f"Enter new name (current: {user.username})", default=user.username)
    new_email = click.prompt(f"Enter new email (current: {user.email})", default=user.email)
    user.username = new_name
    user.email = new_email
    session.commit()
    click.echo(f"User ID {user_id} updated.")

def prompt_delete_user(session):
    click.echo("Delete a user:")
    user_id = click.prompt("Enter user ID to delete", type=int)
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        click.echo(f"User with ID {user_id} not found.")
        return
    confirm = click.confirm(f"Are you sure you want to delete user '{user.username}' (ID {user_id})?", default=False)
    if confirm:
        session.delete(user)
        session.commit()
        click.echo(f"User ID {user_id} deleted.")
    else:
        click.echo("Delete operation cancelled.")
def prompt_foodentry(session):
    click.echo("Add a new food entry:")
    user_id = click.prompt("Enter user ID", type=int)
    name = click.prompt("Enter food name")
    calories = click.prompt("Enter calories", type=float)
    protein = click.prompt("Enter protein", type=float, default=0.0)
    fat = click.prompt("Enter fat", type=float, default=0.0)
    carbs = click.prompt("Enter carbohydrates", type=float, default=0.0)
    foodentry = FoodEntry(user_id=user_id, name=name, calories=calories,
                          protein=protein, fat=fat, carbs=carbs)
    session.add(foodentry)
    session.commit()
    click.echo(f"Food entry '{name}' added for user ID {user_id}.")

def prompt_mealplan(session):
    click.echo("Add a new meal plan:")
    user_id = click.prompt("Enter user ID", type=int)
    date = click.prompt("Enter date (YYYY-MM-DD)")
    meal_type = click.prompt("Enter meal type (e.g., breakfast, lunch)")
    mealplan = MealPlan(user_id=user_id, date=date, meal_type=meal_type)
    session.add(mealplan)
    session.commit()
    click.echo(f"Meal plan added for user ID {user_id} on {date} ({meal_type}).")

def prompt_goal(session):
    click.echo("Add a new goal:")
    user_id = click.prompt("Enter user ID", type=int)
    description = click.prompt("Enter goal description")
    goal = Goal(user_id=user_id, description=description)
    session.add(goal)
    session.commit()
    click.echo(f"Goal added for user ID {user_id}: {description}")

@click.command()
def interactive():
    init_db()
    session = SessionLocal()
    try:
        while True:
            click.echo("\nChoose an option:")
            click.echo("1. Add User")
            click.echo("2. Update User")
            click.echo("3. Delete User")
            click.echo("4. Add Food Entry")
            click.echo("5. Add Meal Plan")
            click.echo("6. Add Goal")
            click.echo("7. Exit")
            choice = click.prompt("Enter choice", type=int)
            if choice == 1:
                prompt_user(session)
            elif choice == 2:
                prompt_update_user(session)
            elif choice == 3:
                prompt_delete_user(session)
            elif choice == 4:
                prompt_foodentry(session)
            elif choice == 5:
                prompt_mealplan(session)
            elif choice == 6:
                prompt_goal(session)
            elif choice == 7:
                click.echo("Exiting interactive mode.")
                break
            else:
                click.echo("Invalid choice. Please try again.")
    finally:
        session.close()

if __name__ == '__main__':
    interactive()
