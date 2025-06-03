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
def add_mealplan(user_id, date, meal_type):
    session = SessionLocal()
    try:
        mealplan = MealPlan(user_id=user_id, date=date, meal_type=meal_type)
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
def init():
    init_db()
    click.echo("Database initialized.")

if __name__ == '__main__':
    cli()
