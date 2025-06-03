import click
import datetime
import os
from health_tracker.db.db import SessionLocal, init_db
from health_tracker.models.user import User
from health_tracker.models.foodentry import FoodEntry
from health_tracker.models.mealplan import MealPlan
from health_tracker.models.goal import Goal

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_user(session):
    while True:
        try:
            name = click.prompt("Enter user name")
            email = click.prompt("Enter user email")
            if session.query(User).filter_by(username=name).first():
                click.echo(f"User '{name}' already exists.")
                return
            user = User(username=name, email=email)
            session.add(user)
            session.commit()
            click.echo(f"User '{name}' created.")
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_update_user(session):
    click.echo("Update an existing user:")
    while True:
        try:
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
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_delete_user(session):
    click.echo("Delete a user:")
    while True:
        try:
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
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_list_users(session):
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
    else:
        click.echo("Users:")
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.username}, Email: {user.email}")

def prompt_foodentry(session):
    click.echo("Add a new food entry:")
    while True:
        try:
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
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_list_foodentries(session):
    foodentries = session.query(FoodEntry).all()
    if not foodentries:
        click.echo("No food entries found.")
    else:
        click.echo("Food Entries:")
        for fe in foodentries:
            click.echo(f"ID: {fe.id}, User ID: {fe.user_id}, Name: {fe.name}, Calories: {fe.calories}")

def prompt_list_foodentries_by_user(session):
    while True:
        try:
            user_id = click.prompt("Enter user ID to list food entries", type=int)
            foodentries = session.query(FoodEntry).filter(FoodEntry.user_id == user_id).all()
            if not foodentries:
                click.echo(f"No food entries found for user ID {user_id}.")
            else:
                click.echo(f"Food Entries for user ID {user_id}:")
                for fe in foodentries:
                    click.echo(f"ID: {fe.id}, Name: {fe.name}, Calories: {fe.calories}")
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_mealplan(session):
    click.echo("Add a new meal plan:")
    while True:
        try:
            user_id = click.prompt("Enter user ID", type=int)
            while True:
                date = click.prompt("Enter date (YYYY-MM-DD)")
                try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                    break
                except ValueError:
                    click.echo("Invalid date format. Please use YYYY-MM-DD.")
            meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
            meal_type = click.prompt(f"Enter meal type {meal_types}", type=click.Choice(meal_types, case_sensitive=False))
            week = click.prompt("Enter week number (optional)", type=int, default=None, show_default=False)
            day = click.prompt("Enter day number (optional)", type=int, default=None, show_default=False)
            food_name = click.prompt("Enter food name (optional)", default="", show_default=False)
            calories = click.prompt("Enter calories (optional)", type=float, default=None, show_default=False)
            fat = click.prompt("Enter fat (optional)", type=float, default=None, show_default=False)
            protein = click.prompt("Enter protein (optional)", type=float, default=None, show_default=False)
            mealplan = MealPlan(user_id=user_id, date=date, meal_type=meal_type, week=week, day=day, food_name=food_name or None, calories=calories, fat=fat, protein=protein)
            session.add(mealplan)
            session.commit()
            click.echo(f"Meal plan added for user ID {user_id} on {date} ({meal_type}).")
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_list_mealplans(session):
    mealplans = session.query(MealPlan).all()
    if not mealplans:
        click.echo("No mealplans found.")
    else:
        click.echo("Meal Plans:")
        for mp in mealplans:
            click.echo(f"ID: {mp.id}, User ID: {mp.user_id}, Date: {mp.date}, Meal Type: {mp.meal_type}")

def prompt_list_mealplans_by_user(session):
    while True:
        try:
            user_id = click.prompt("Enter user ID to list meal plans", type=int)
            mealplans = session.query(MealPlan).filter(MealPlan.user_id == user_id).all()
            if not mealplans:
                click.echo(f"No mealplans found for user ID {user_id}.")
            else:
                click.echo(f"Meal Plans for user ID {user_id}:")
                for mp in mealplans:
                    click.echo(f"ID: {mp.id}, Date: {mp.date}, Meal Type: {mp.meal_type}")
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_goal(session):
    click.echo("Add a new goal:")
    while True:
        try:
            user_id = click.prompt("Enter user ID", type=int)
            description = click.prompt("Enter goal description")
            goal = Goal(user_id=user_id, description=description)
            session.add(goal)
            session.commit()
            click.echo(f"Goal added for user ID {user_id}: {description}")
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

def prompt_list_goals(session):
    goals = session.query(Goal).all()
    if not goals:
        click.echo("No goals found.")
    else:
        click.echo("Goals:")
        for g in goals:
            click.echo(f"ID: {g.id}, User ID: {g.user_id}, Description: {g.description}")

def prompt_list_goals_by_user(session):
    while True:
        try:
            user_id = click.prompt("Enter user ID to list goals", type=int)
            goals = session.query(Goal).filter(Goal.user_id == user_id).all()
            if not goals:
                click.echo(f"No goals found for user ID {user_id}.")
            else:
                click.echo(f"Goals for user ID {user_id}:")
                for g in goals:
                    click.echo(f"ID: {g.id}, Description: {g.description}")
            break
        except Exception as e:
            click.echo(f"Error: {e}. Please try again.")

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
            click.echo("4. List Users")
            click.echo("5. Add Food Entry")
            click.echo("6. List Food Entries")
            click.echo("7. List Food Entries by User")
            click.echo("8. Add Meal Plan")
            click.echo("9. List Meal Plans")
            click.echo("10. List Meal Plans by User")
            click.echo("11. Add Goal")
            click.echo("12. List Goals")
            click.echo("13. List Goals by User")
            click.echo("14. Exit")
            choice = click.prompt("Enter choice", type=int)
            if choice == 1:
                prompt_user(session)
            elif choice == 2:
                prompt_update_user(session)
            elif choice == 3:
                prompt_delete_user(session)
            elif choice == 4:
                prompt_list_users(session)
            elif choice == 5:
                prompt_foodentry(session)
            elif choice == 6:
                prompt_list_foodentries(session)
            elif choice == 7:
                prompt_list_foodentries_by_user(session)
            elif choice == 8:
                prompt_mealplan(session)
            elif choice == 9:
                prompt_list_mealplans(session)
            elif choice == 10:
                prompt_list_mealplans_by_user(session)
            elif choice == 11:
                prompt_goal(session)
            elif choice == 12:
                prompt_list_goals(session)
            elif choice == 13:
                prompt_list_goals_by_user(session)
            elif choice == 14:
                click.echo("Exiting interactive mode.")
                break
            else:
                click.echo("Invalid choice. Please try again.")
    finally:
        session.close()

if __name__ == '__main__':
    interactive()
