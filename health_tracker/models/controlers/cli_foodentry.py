import click
import logging
from typing import Optional
from health_tracker.db import SessionLocal
from health_tracker.db.db_operations import create_foodentry, update_foodentry, delete_foodentry
from health_tracker.models import FoodEntry

logger = logging.getLogger(__name__)

@click.group()
def foodentry():
    """Commands to manage food entries."""
    pass

@foodentry.command()
@click.option('--user-id', required=True, type=int, help='User ID')
@click.option('--name', required=True, help='Food name')
@click.option('--calories', required=True, type=float, help='Calories')
@click.option('--protein', type=float, help='Protein')
@click.option('--fat', type=float, help='Fat')
@click.option('--carbs', type=float, help='Carbohydrates')
def create(user_id: int, name: str, calories: float, protein: Optional[float], fat: Optional[float], carbs: Optional[float]):
    """Create a new food entry."""
    session = SessionLocal()
    try:
        logger.info(f"Creating food entry for user_id={user_id}, name={name}")
        foodentry = create_foodentry(session, user_id=user_id, name=name, calories=calories, protein=protein, fat=fat, carbs=carbs)
        click.echo(f"FoodEntry created with ID: {foodentry.id}")
        logger.info(f"FoodEntry created with ID: {foodentry.id}")
    except Exception as e:
        logger.error(f"Error creating FoodEntry: {e}", exc_info=True)
        session.rollback()
        click.echo(f"Error creating FoodEntry: {e}", err=True)
        raise
    finally:
        session.close()

@foodentry.command()
def list():
    """List all food entries."""
    session = SessionLocal()
    foodentries = session.query(FoodEntry).all()
    if not foodentries:
        click.echo("No food entries found.")
    else:
        for fe in foodentries:
            click.echo(f"ID: {fe.id}, User ID: {fe.user_id}, Name: {fe.name}, Calories: {fe.calories}")
    session.close()

@foodentry.command()
@click.option('--user-id', required=True, type=int, help='User ID')
def list_by_user(user_id):
    """List food entries for a specific user."""
    session = SessionLocal()
    foodentries = session.query(FoodEntry).filter(FoodEntry.user_id == user_id).all()
    if not foodentries:
        click.echo(f"No food entries found for user ID {user_id}.")
    else:
        for fe in foodentries:
            click.echo(f"ID: {fe.id}, Name: {fe.name}, Calories: {fe.calories}")
    session.close()

@foodentry.command()
@click.option('--foodentry-id', 'foodentry_id', required=True, type=int, help='FoodEntry ID')
@click.option('--name', help='New food name')
@click.option('--calories', type=float, help='New calories')
@click.option('--protein', type=float, help='New protein')
@click.option('--fat', type=float, help='New fat')
@click.option('--carbs', type=float, help='New carbohydrates')
def update(foodentry_id, name, calories, protein, fat, carbs):
    """Update a food entry."""
    session = SessionLocal()
    updated = update_foodentry(session, foodentry_id, name=name, calories=calories, protein=protein, fat=fat, carbs=carbs)
    if updated:
        click.echo(f"FoodEntry updated: {updated}")
    else:
        click.echo("FoodEntry not found.")
    session.close()

@foodentry.command()
@click.option('--foodentry-id', 'foodentry_id', required=True, type=int, help='FoodEntry ID')
def delete(foodentry_id):
    """Delete a food entry."""
    session = SessionLocal()
    try:
        click.echo("DEBUG: Starting delete_foodentry", err=True)
        success = delete_foodentry(session, foodentry_id)
        if success:
            click.echo("FoodEntry deleted.")
        else:
            click.echo("FoodEntry not found.")
        click.echo("DEBUG: Finished delete_foodentry", err=True)
    except Exception as e:
        click.echo(f"Error deleting FoodEntry: {e}", err=True)
        session.rollback()
        import traceback
        click.echo(traceback.format_exc(), err=True)
        raise
    finally:
        click.echo("DEBUG: Closing session in delete_foodentry", err=True)
        session.close()
