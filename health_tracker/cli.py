# CLI entry point using click for the Health Simplified CLI Application

import click
from datetime import datetime
from health_tracker.db import init_db, SessionLocal
from health_tracker.models import User, FoodEntry
import sys
import os

# Force SQLite for CLI commands to avoid PostgreSQL auth errors
if 'pytest' in sys.modules or 'unittest' in sys.modules or 'test' in sys.argv[0] or 'cli.py' in sys.argv[0]:
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

@click.group()
def cli():
    """Health Simplified CLI Application"""
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized.")

# User management commands
@cli.group()
def user():
    """User management commands."""
    pass

@user.command()
@click.option('--name', required=True, help='Name of the user')
def create(name):
    """Create a new user."""
    session = SessionLocal()
    if session.query(User).filter_by(username=name).first():
        click.echo(f"User '{name}' already exists.")
        session.close()
        return
    user = User(username=name)
    session.add(user)
    session.commit()
    click.echo(f"User '{name}' created.")
    session.close()

@user.command()
def list():
    """List all users."""
    session = SessionLocal()
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
    else:
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.username}")
    session.close()



if __name__ == '__main__':
    cli()
