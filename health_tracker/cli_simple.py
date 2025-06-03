import click
from health_tracker.db.db import SessionLocal, init_db
from health_tracker.models.user import User
from health_tracker.models.foodentry import FoodEntry
from health_tracker.models.mealplan import MealPlan
from health_tracker.models.goal import Goal

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', required=True, help='Name of the user')
@click.option('--email', required=True, help='Email of the user')
def add_user(name, email):
    session = SessionLocal()
    try:
        if session.query(User).filter_by(username=name).first():
            click.echo(f"User '{name}' already exists.")
            return
        user = User(username=name, email=email)
        session.add(user)
        session.commit()
        click.echo(f"User '{name}' created.")
    except Exception as e:
        click.echo(f"Error creating user: {e}", err=True)
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.option('--user-id', type=int, required=True, help='User ID')
@click.option('--description', required=True, help='Goal description')
def add_goal(user_id, description):
    session = SessionLocal()
    try:
        goal = Goal(user_id=user_id, description=description)
        session.add(goal)
        session.commit()
        click.echo("Goal added:")
        click.echo(f"  User ID: {user_id}")
        click.echo(f"  Description: {description}")
    except Exception as e:
        click.echo(f"Error adding goal: {e}", err=True)
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.option('--user-id', type=int, required=True, help='User ID')
@click.option('--date', required=True, help='Date in YYYY-MM-DD format')
@click.option('--meal-type', required=True, help='Meal type (e.g., breakfast, lunch)')
@click.option('--calories', type=float, default=0.0, help='Calories')
@click.option('--fat', type=float, default=0.0, help='Fat')
@click.option('--protein', type=float, default=0.0, help='Protein')
def add_mealplan(user_id, date, meal_type, calories, fat, protein):
    import datetime
    session = SessionLocal()
    try:
        # Parse date string to date object
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        mealplan = MealPlan(user_id=user_id, date=date_obj, meal_type=meal_type,
                            calories=calories, fat=fat, protein=protein)
        session.add(mealplan)
        session.commit()
        click.echo(f"Meal plan added for user ID {user_id} on {date} ({meal_type}).")
    except Exception as e:
        click.echo(f"Error adding meal plan: {e}", err=True)
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.option('--user-id', type=int, required=True, help='User ID')
@click.option('--description', required=True, help='Goal description')
def add_goal(user_id, description):
    session = SessionLocal()
    try:
        goal = Goal(user_id=user_id, description=description)
        session.add(goal)
        session.commit()
        click.echo(f"Goal added for user ID {user_id}: {description}")
    except Exception as e:
        click.echo(f"Error adding goal: {e}", err=True)
        session.rollback()
    finally:
        session.close()


@cli.command()
@click.option('--user-id', type=int, required=True, help='User ID')
def view_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            click.echo(f"User with ID {user_id} not found.")
            return
        click.echo(f"User Details:")
        click.echo(f"  ID: {user.id}")
        click.echo(f"  Username: {user.username}")
        click.echo(f"  Email: {user.email}")
        # Optionally, list related meal plans and goals
        if user.mealplans:
            click.echo("  Meal Plans:")
            for mp in user.mealplans:
                click.echo(f"    - {mp.date} {mp.meal_type} Calories: {mp.calories} Fat: {mp.fat} Protein: {mp.protein}")
        if user.goals:
            click.echo("  Goals:")
            for goal in user.goals:
                click.echo(f"    - {goal.description}")
    except Exception as e:
        click.echo(f"Error viewing user: {e}", err=True)
    finally:
        session.close()

import datetime
from sqlalchemy import extract

@cli.command()
@click.option('--user-id', type=int, required=True, help='User ID')
@click.option('--year', type=int, required=True, help='Year of the week')
@click.option('--week', type=int, required=True, help='ISO week number')
@click.option('--meal-type', required=True, help='Meal type (e.g., breakfast, lunch)')
@click.option('--calories', type=float, default=0.0, help='Calories')
@click.option('--fat', type=float, default=0.0, help='Fat')
@click.option('--protein', type=float, default=0.0, help='Protein')
def add_mealplans_week(user_id, year, week, meal_type, calories, fat, protein):
    """
    Add a meal plan for each day of the specified ISO week for the user.
    """
    session = SessionLocal()
    try:
        # Calculate the first day of the ISO week
        first_day = datetime.date.fromisocalendar(year, week, 1)
        for day_offset in range(7):
            date = first_day + datetime.timedelta(days=day_offset)
            day_of_week = date.isoweekday()
            mealplan = MealPlan(user_id=user_id, date=date, week=week, day=day_of_week, meal_type=meal_type,
                                calories=calories, fat=fat, protein=protein)
            session.add(mealplan)
        session.commit()
        click.echo(f"Meal plans added for user ID {user_id} for week {week} of {year} ({meal_type}).")
    except Exception as e:
        click.echo(f"Error adding meal plans for week: {e}", err=True)
        session.rollback()
    finally:
        session.close()

@cli.command()
def init():
    init_db()
    click.echo("Database initialized.")

if __name__ == '__main__':
    cli()
