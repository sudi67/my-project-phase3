import click
import datetime
import logging
from typing import Optional
from health_tracker.db import SessionLocal
from health_tracker.db.db_operations import create_mealplan, update_mealplan, delete_mealplan
from health_tracker.models import MealPlan

logger = logging.getLogger(__name__)

@click.group()
def mealplan():
    """Commands to manage meal plans."""
    pass

@mealplan.command()
@click.option('--user-id', required=True, type=int, help='User ID')
@click.option('--date', required=True, help='Date in YYYY-MM-DD or DD-MM-YYYY format')
@click.option('--week', type=int, help='Week number')
@click.option('--day', type=int, help='Day number')
@click.option('--food-name', help='Food name')
@click.option('--meal-type', required=True, type=click.Choice(['breakfast', 'lunch', 'dinner', 'snack'], case_sensitive=False), help='Meal type')
@click.option('--calories', type=float, help='Calories')
@click.option('--fat', type=float, help='Fat')
@click.option('--protein', type=float, help='Protein')
def create(user_id: int, date: str, week: Optional[int], day: Optional[int], food_name: Optional[str], meal_type: str, calories: Optional[float], fat: Optional[float], protein: Optional[float]):
    """Create a new mealplan."""
    session = SessionLocal()
    try:
        for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
            try:
                date_obj = datetime.datetime.strptime(date, fmt).date()
                break
            except ValueError:
                continue
        else:
            session.close()
            raise click.BadParameter("Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY.")
    except Exception as e:
        session.close()
        raise e
    try:
        logger.info(f"Creating mealplan for user_id={user_id}, date={date}, meal_type={meal_type}")
        mealplan = create_mealplan(session, user_id=user_id, date=date_obj, week=week, day=day, food_name=food_name, meal_type=meal_type, calories=calories, fat=fat, protein=protein)
        click.echo(f"MealPlan created: {mealplan}")
        logger.info(f"MealPlan created with ID: {mealplan.id}")
    except Exception as e:
        logger.error(f"Error creating MealPlan: {e}", exc_info=True)
        session.rollback()
        click.echo(f"Error creating MealPlan: {e}", err=True)
        raise
    finally:
        session.close()

@mealplan.command()
def list():
    """List all mealplans."""
    session = SessionLocal()
    try:
        mealplans = session.query(MealPlan).all()
        if not mealplans:
            click.echo("No mealplans found.")
        else:
            for mp in mealplans:
                click.echo(f"ID: {mp.id}, User ID: {mp.user_id}, Date: {mp.date}, Week: {mp.week}, Day: {mp.day}, Food Name: {mp.food_name}, Meal Type: {mp.meal_type}")
    except Exception as e:
        logger.error(f"Error listing MealPlans: {e}", exc_info=True)
        click.echo(f"Error listing MealPlans: {e}", err=True)
    finally:
        session.close()

@mealplan.command()
@click.option('--user-id', required=True, type=int, help='User ID')
def list_by_user(user_id: int):
    """List mealplans for a specific user."""
    session = SessionLocal()
    try:
        mealplans = session.query(MealPlan).filter(MealPlan.user_id == user_id).all()
        if not mealplans:
            click.echo(f"No mealplans found for user ID {user_id}.")
        else:
            for mp in mealplans:
                click.echo(f"ID: {mp.id}, Date: {mp.date}, Week: {mp.week}, Day: {mp.day}, Food Name: {mp.food_name}, Meal Type: {mp.meal_type}")
    except Exception as e:
        logger.error(f"Error listing MealPlans by user: {e}", exc_info=True)
        click.echo(f"Error listing MealPlans by user: {e}", err=True)
    finally:
        session.close()

@mealplan.command()
@click.option('--mealplan-id', 'mealplan_id', required=True, type=int, help='MealPlan ID')
@click.option('--date', help='New date in YYYY-MM-DD format')
@click.option('--week', type=int, help='New week number')
@click.option('--day', type=int, help='New day number')
@click.option('--food-name', help='New food name')
@click.option('--meal-type', type=click.Choice(['breakfast', 'lunch', 'dinner', 'snack'], case_sensitive=False), help='New meal type')
@click.option('--calories', type=float, help='New calories')
@click.option('--fat', type=float, help='New fat')
@click.option('--protein', type=float, help='New protein')
def update(mealplan_id: int, date: Optional[str], week: Optional[int], day: Optional[int], food_name: Optional[str], meal_type: Optional[str], calories: Optional[float], fat: Optional[float], protein: Optional[float]):
    """Update a mealplan."""
    session = SessionLocal()
    date_obj = None
    try:
        if date:
            for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
                try:
                    date_obj = datetime.datetime.strptime(date, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                raise click.BadParameter("Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY.")
        updated = update_mealplan(session, mealplan_id, date=date_obj, week=week, day=day, food_name=food_name, meal_type=meal_type, calories=calories, fat=fat, protein=protein)
        if updated:
            click.echo(f"MealPlan updated: {updated}")
        else:
            click.echo("MealPlan not found.")
        session.commit()
    except click.BadParameter as e:
        session.rollback()
        logger.error(f"BadParameter error updating mealplan: {e}", exc_info=True)
        click.echo(f"Error updating mealplan: {e}", err=True)
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating mealplan: {e}", exc_info=True)
        click.echo(f"Error updating mealplan: {e}", err=True)
    finally:
        session.close()

@mealplan.command()
@click.option('--mealplan-id', 'mealplan_id', required=True, type=int, help='MealPlan ID')
def delete(mealplan_id: int):
    """Delete a mealplan."""
    session = SessionLocal()
    try:
        success = delete_mealplan(session, mealplan_id)
        if success:
            click.echo("MealPlan deleted.")
        else:
            click.echo("MealPlan not found.")
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting mealplan: {e}", exc_info=True)
        click.echo(f"Error deleting mealplan: {e}", err=True)
    finally:
        session.close()

import datetime
import click
from health_tracker.db import SessionLocal
from health_tracker.db.db_operations import create_mealplan, update_mealplan, delete_mealplan
from health_tracker.models import MealPlan

def create_mealplan_cmd(user_id, date, meal_type, week=None, day=None, food_name=None, calories=None, fat=None, protein=None):
    if not isinstance(date, datetime.date):
        raise click.BadParameter("Date must be a Python date object, not a string.")
    session = SessionLocal()
    mealplan = create_mealplan(session, user_id=user_id, date=date, meal_type=meal_type, week=week, day=day, food_name=food_name, calories=calories, fat=fat, protein=protein)
    print(f"MealPlan created: {mealplan}")
    session.close()

def list_mealplans_cmd():
    session = SessionLocal()
    mealplans = session.query(MealPlan).all()
    if not mealplans:
        print("No mealplans found.")
    else:
        for mp in mealplans:
            print(f"ID: {mp.id}, User ID: {mp.user_id}, Date: {mp.date}, Week: {mp.week}, Day: {mp.day}, Food Name: {mp.food_name}, Meal Type: {mp.meal_type}")
    session.close()

def update_mealplan_cmd(mealplan_id, date, week=None, day=None, food_name=None, meal_type=None, calories=None, fat=None, protein=None):
    session = SessionLocal()
    date_obj = None
    if date:
        for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
            try:
                date_obj = datetime.datetime.strptime(date, fmt).date()
                break
            except ValueError:
                continue
        else:
            session.close()
            raise click.BadParameter("Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY.")
    updated = update_mealplan(session, mealplan_id, date=date_obj, week=week, day=day, food_name=food_name, meal_type=meal_type, calories=calories, fat=fat, protein=protein)
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

