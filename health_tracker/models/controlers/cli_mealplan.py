import click
import datetime
from health_tracker.db import SessionLocal
from health_tracker.db.db_operations import create_mealplan, update_mealplan, delete_mealplan
from health_tracker.models import MealPlan

@click.group()
def mealplan():
    pass

@mealplan.command()
@click.option('--user-id', required=True, type=int, help='User ID')
@click.option('--date', required=True, help='Date in YYYY-MM-DD format')
@click.option('--meal-type', required=True, help='Meal type (e.g., breakfast, lunch)')
def create(user_id, date, meal_type):
    """Create a new mealplan."""
    session = SessionLocal()
    try:
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        session.close()
        raise click.BadParameter("Invalid date format. Use YYYY-MM-DD.")
    mealplan = create_mealplan(session, user_id=user_id, date=date_obj, meal_type=meal_type)
    click.echo(f"MealPlan created: {mealplan}")
    session.close()

@mealplan.command()
def list():
    """List all mealplans."""
    session = SessionLocal()
    mealplans = session.query(MealPlan).all()
    if not mealplans:
        click.echo("No mealplans found.")
    else:
        for mp in mealplans:
            click.echo(f"ID: {mp.id}, User ID: {mp.user_id}, Date: {mp.date}, Meal Type: {mp.meal_type}")
    session.close()

@mealplan.command()
@click.option('--mealplan-id', 'mealplan_id', required=True, type=int, help='MealPlan ID')
@click.option('--date', help='New date in YYYY-MM-DD format')
@click.option('--meal-type', help='New meal type')
def update(mealplan_id, date, meal_type):
    """Update a mealplan."""
    session = SessionLocal()
    date_obj = None
    if date:
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            session.close()
            raise click.BadParameter("Invalid date format. Use YYYY-MM-DD.")
    updated = update_mealplan(session, mealplan_id, date=date_obj, meal_type=meal_type)
    if updated:
        click.echo(f"MealPlan updated: {updated}")
    else:
        click.echo("MealPlan not found.")
    session.close()

@mealplan.command()
@click.option('--mealplan-id', 'mealplan_id', required=True, type=int, help='MealPlan ID')
def delete(mealplan_id):
    """Delete a mealplan."""
    session = SessionLocal()
    success = delete_mealplan(session, mealplan_id)
    if success:
        click.echo("MealPlan deleted.")
    else:
        click.echo("MealPlan not found.")
    session.close()

def create_mealplan_cmd(user_id, date, meal_type):
    session = SessionLocal()
    try:
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        session.close()
        raise click.BadParameter("Invalid date format. Use YYYY-MM-DD.")
    mealplan = create_mealplan(session, user_id=user_id, date=date_obj, meal_type=meal_type)
    print(f"MealPlan created: {mealplan}")
    session.close()

def list_mealplans_cmd():
    session = SessionLocal()
    mealplans = session.query(MealPlan).all()
    if not mealplans:
        print("No mealplans found.")
    else:
        for mp in mealplans:
            print(f"ID: {mp.id}, User ID: {mp.user_id}, Date: {mp.date}, Meal Type: {mp.meal_type}")
    session.close()

def update_mealplan_cmd(mealplan_id, date, meal_type):
    session = SessionLocal()
    date_obj = None
    if date:
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            session.close()
            raise click.BadParameter("Invalid date format. Use YYYY-MM-DD.")
    updated = update_mealplan(session, mealplan_id, date=date_obj, meal_type=meal_type)
    if updated:
        print(f"MealPlan updated: {updated}")
    else:
        print("MealPlan not found.")
    session.close()

def delete_mealplan_cmd(mealplan_id):
    session = SessionLocal()
    success = delete_mealplan(session, mealplan_id)
    if success:
        print("MealPlan deleted.")
    else:
        print("MealPlan not found.")
    session.close()
