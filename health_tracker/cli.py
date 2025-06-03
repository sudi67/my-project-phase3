import argparse
import os
from health_tracker.db.db import init_db
from health_tracker.models import User
from health_tracker.db import SessionLocal
from health_tracker.models.controlers import cli_foodentry, cli_mealplan

def set_sqlite_for_cli():
    db_url = os.getenv('DATABASE_URL')
    if not db_url or db_url.startswith('postgresql://user:password'):
        os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

set_sqlite_for_cli()

def init_command(args):
    init_db()
    print("Database initialized.")

def user_create(args):
    session = SessionLocal()
    if session.query(User).filter_by(username=args.name).first():
        print(f"User '{args.name}' already exists.")
        session.close()
        return
    user = User(username=args.name, email=args.email)
    session.add(user)
    session.commit()
    print(f"User '{args.name}' created.")
    session.close()

def user_list(args):
    session = SessionLocal()
    users = session.query(User).all()
    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"ID: {user.id}, Name: {user.username}")
    session.close()

import click
from health_tracker.db.db import init_db
from health_tracker.models import User
from health_tracker.db import SessionLocal
from health_tracker.models.controlers import cli_foodentry, cli_mealplan

@click.group()
def cli():
    pass

@cli.command()
def init():
    init_db()
    click.echo("Database initialized.")

@cli.group()
def user():
    pass

@user.command()
@click.option('--name', required=True, help='Name of the user')
@click.option('--email', required=True, help='Email of the user')
def create(name, email):
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
        raise
    finally:
        try:
            session.close()
        except Exception as e:
            click.echo(f"Error closing session: {e}", err=True)

@user.command()
def list():
    session = SessionLocal()
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
    else:
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.username}")
    session.close()

@user.command()
@click.option('--user-id', type=int, required=True, help='User ID')
def delete(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            click.echo("User not found.")
            return
        session.delete(user)
        session.commit()
        click.echo("User deleted.")
    except Exception as e:
        click.echo(f"Error deleting user: {e}", err=True)
        session.rollback()
        raise
    finally:
        click.echo("DEBUG: Closing session in user delete", err=True)
        session.close()

@cli.group()
def foodentry():
    pass

@foodentry.command()
@click.option('--user-id', type=int, required=True, help='User ID')
@click.option('--name', required=True, help='Food name')
@click.option('--calories', type=float, required=True, help='Calories')
@click.option('--protein', type=float, help='Protein')
@click.option('--fat', type=float, help='Fat')
@click.option('--carbs', type=float, help='Carbohydrates')
def create(user_id, name, calories, protein, fat, carbs):
    cli_foodentry.create_foodentry_cmd(user_id, name, calories, protein, fat, carbs)

@foodentry.command()
def list():
    cli_foodentry.list_foodentries_cmd()

@foodentry.command()
@click.option('--foodentry-id', type=int, required=True, help='FoodEntry ID')
@click.option('--name', help='New food name')
@click.option('--calories', type=float, help='New calories')
@click.option('--protein', type=float, help='New protein')
@click.option('--fat', type=float, help='New fat')
@click.option('--carbs', type=float, help='New carbohydrates')
def update(foodentry_id, name, calories, protein, fat, carbs):
    cli_foodentry.update_foodentry_cmd(foodentry_id, name, calories, protein, fat, carbs)

@foodentry.command()
@click.option('--foodentry-id', type=int, required=True, help='FoodEntry ID')
def delete(foodentry_id):
    cli_foodentry.delete_foodentry_cmd(foodentry_id)

@cli.group()
def mealplan():
    pass

from datetime import datetime
import click
from health_tracker.models.controlers import cli_mealplan

@mealplan.command()
@click.option('--user-id', type=int, required=True, help='User ID')
@click.option('--date', required=True, help='Date in YYYY-MM-DD format')
@click.option('--meal-type', required=True, help='Meal type (e.g., breakfast, lunch)')
@click.option('--week', type=int, help='Week number')
@click.option('--day', type=int, help='Day number')
@click.option('--food-name', help='Food name')
@click.option('--calories', type=float, help='Calories')
@click.option('--fat', type=float, help='Fat')
@click.option('--protein', type=float, help='Protein')
def create(user_id, date, meal_type, week=None, day=None, food_name=None, calories=None, fat=None, protein=None):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise click.BadParameter("Invalid date format. Use YYYY-MM-DD.")
    cli_mealplan.create_mealplan_cmd(user_id, date_obj, meal_type, week=week, day=day, food_name=food_name, calories=calories, fat=fat, protein=protein)

@mealplan.command()
def list():
    cli_mealplan.list_mealplans_cmd()

@mealplan.command()
@click.option('--mealplan-id', type=int, required=True, help='MealPlan ID')
@click.option('--date', help='New date in YYYY-MM-DD format')
@click.option('--meal-type', help='New meal type')
@click.option('--week', type=int, help='New week number')
@click.option('--day', type=int, help='New day number')
@click.option('--food-name', help='New food name')
@click.option('--calories', type=float, help='New calories')
@click.option('--fat', type=float, help='New fat')
@click.option('--protein', type=float, help='New protein')
def update(mealplan_id, date, meal_type, week=None, day=None, food_name=None, calories=None, fat=None, protein=None):
    cli_mealplan.update_mealplan_cmd(mealplan_id, date, meal_type, week=week, day=day, food_name=food_name, calories=calories, fat=fat, protein=protein)

@mealplan.command()
@click.option('--mealplan-id', type=int, required=True, help='MealPlan ID')
def delete(mealplan_id):
    cli_mealplan.delete_mealplan_cmd(mealplan_id)

if __name__ == '__main__':
    cli()
