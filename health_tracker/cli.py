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

def main():
    parser = argparse.ArgumentParser(description="Health Tracker CLI")
    subparsers = parser.add_subparsers(dest='command')

    parser_init = subparsers.add_parser('init', help='Initialize the database')
    parser_init.set_defaults(func=init_command)

    parser_user = subparsers.add_parser('user', help='User related commands')
    user_subparsers = parser_user.add_subparsers(dest='subcommand')

    parser_user_create = user_subparsers.add_parser('create', help='Create a new user')
    parser_user_create.add_argument('--name', required=True, help='Name of the user')
    parser_user_create.add_argument('--email', required=True, help='Email of the user')
    parser_user_create.set_defaults(func=user_create)

    parser_user_list = user_subparsers.add_parser('list', help='List all users')
    parser_user_list.set_defaults(func=user_list)

    parser_foodentry = subparsers.add_parser('foodentry', help='FoodEntry related commands')
    foodentry_subparsers = parser_foodentry.add_subparsers(dest='subcommand')

    parser_fe_create = foodentry_subparsers.add_parser('create', help='Create a new food entry')
    parser_fe_create.add_argument('--user-id', type=int, required=True, help='User ID')
    parser_fe_create.add_argument('--name', required=True, help='Food name')
    parser_fe_create.add_argument('--calories', type=float, required=True, help='Calories')
    parser_fe_create.add_argument('--protein', type=float, help='Protein')
    parser_fe_create.add_argument('--fat', type=float, help='Fat')
    parser_fe_create.add_argument('--carbs', type=float, help='Carbohydrates')
    parser_fe_create.set_defaults(func=lambda args: cli_foodentry.create_foodentry_cmd(args.user_id, args.name, args.calories, args.protein, args.fat, args.carbs))

    parser_fe_list = foodentry_subparsers.add_parser('list', help='List all food entries')
    parser_fe_list.set_defaults(func=lambda args: cli_foodentry.list_foodentries_cmd())

    parser_fe_update = foodentry_subparsers.add_parser('update', help='Update a food entry')
    parser_fe_update.add_argument('--foodentry-id', type=int, required=True, help='FoodEntry ID')
    parser_fe_update.add_argument('--name', help='New food name')
    parser_fe_update.add_argument('--calories', type=float, help='New calories')
    parser_fe_update.add_argument('--protein', type=float, help='New protein')
    parser_fe_update.add_argument('--fat', type=float, help='New fat')
    parser_fe_update.add_argument('--carbs', type=float, help='New carbohydrates')
    parser_fe_update.set_defaults(func=lambda args: cli_foodentry.update_foodentry_cmd(args.foodentry_id, args.name, args.calories, args.protein, args.fat, args.carbs))

    parser_fe_delete = foodentry_subparsers.add_parser('delete', help='Delete a food entry')
    parser_fe_delete.add_argument('--foodentry-id', type=int, required=True, help='FoodEntry ID')
    parser_fe_delete.set_defaults(func=lambda args: cli_foodentry.delete_foodentry_cmd(args.foodentry_id))

    parser_mealplan = subparsers.add_parser('mealplan', help='MealPlan related commands')
    mealplan_subparsers = parser_mealplan.add_subparsers(dest='subcommand')

    parser_mp_create = mealplan_subparsers.add_parser('create', help='Create a new mealplan')
    parser_mp_create.add_argument('--user-id', type=int, required=True, help='User ID')
    parser_mp_create.add_argument('--date', required=True, help='Date in YYYY-MM-DD format')
    parser_mp_create.add_argument('--meal-type', required=True, help='Meal type (e.g., breakfast, lunch)')
    parser_mp_create.set_defaults(func=lambda args: cli_mealplan.create_mealplan_cmd(args.user_id, args.date, args.meal_type))

    parser_mp_list = mealplan_subparsers.add_parser('list', help='List all mealplans')
    parser_mp_list.set_defaults(func=lambda args: cli_mealplan.list_mealplans_cmd())

    parser_mp_update = mealplan_subparsers.add_parser('update', help='Update a mealplan')
    parser_mp_update.add_argument('--mealplan-id', type=int, required=True, help='MealPlan ID')
    parser_mp_update.add_argument('--date', help='New date in YYYY-MM-DD format')
    parser_mp_update.add_argument('--meal-type', help='New meal type')
    parser_mp_update.set_defaults(func=lambda args: cli_mealplan.update_mealplan_cmd(args.mealplan_id, args.date, args.meal_type))

    parser_mp_delete = mealplan_subparsers.add_parser('delete', help='Delete a mealplan')
    parser_mp_delete.add_argument('--mealplan-id', type=int, required=True, help='MealPlan ID')
    parser_mp_delete.set_defaults(func=lambda args: cli_mealplan.delete_mealplan_cmd(args.mealplan_id))

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
