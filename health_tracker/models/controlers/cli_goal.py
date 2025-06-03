import click
import logging
from typing import Optional
from health_tracker.db import SessionLocal
from health_tracker.db.db_operations import create_goal, update_goal, delete_goal, list_goals_by_user
from health_tracker.models import Goal

logger = logging.getLogger(__name__)

@click.group()
def goal():
    """Commands to manage goals."""
    pass

@goal.command()
@click.option('--user-id', required=True, type=int, help='User ID')
@click.option('--description', required=True, help='Goal description')
def create(user_id: int, description: str):
    """Create a new goal."""
    session = SessionLocal()
    try:
        logger.info(f"Creating goal for user_id={user_id}")
        goal = create_goal(session, user_id=user_id, description=description)
        click.echo(f"Goal created with ID: {goal.id}")
        logger.info(f"Goal created with ID: {goal.id}")
    except Exception as e:
        logger.error(f"Error creating goal: {e}", exc_info=True)
        session.rollback()
        click.echo(f"Error creating goal: {e}", err=True)
        raise
    finally:
        session.close()

@goal.command()
def list():
    """List all goals."""
    session = SessionLocal()
    try:
        goals = session.query(Goal).all()
        if not goals:
            click.echo("No goals found.")
        else:
            for g in goals:
                click.echo(f"ID: {g.id}, User ID: {g.user_id}, Description: {g.description}")
    except Exception as e:
        logger.error(f"Error listing goals: {e}", exc_info=True)
        click.echo(f"Error listing goals: {e}", err=True)
    finally:
        session.close()

@goal.command()
@click.option('--user-id', required=True, type=int, help='User ID')
def list_by_user(user_id: int):
    """List goals for a specific user."""
    session = SessionLocal()
    try:
        goals = list_goals_by_user(session, user_id)
        if not goals:
            click.echo(f"No goals found for user ID {user_id}.")
        else:
            for g in goals:
                click.echo(f"ID: {g.id}, Description: {g.description}")
    except Exception as e:
        logger.error(f"Error listing goals by user: {e}", exc_info=True)
        click.echo(f"Error listing goals by user: {e}", err=True)
    finally:
        session.close()

@goal.command()
@click.option('--goal-id', 'goal_id', required=True, type=int, help='Goal ID')
@click.option('--description', help='New goal description')
def update(goal_id: int, description: Optional[str]):
    """Update a goal."""
    session = SessionLocal()
    try:
        updated = update_goal(session, goal_id, description=description)
        if updated:
            click.echo(f"Goal updated: {updated}")
        else:
            click.echo("Goal not found.")
    except Exception as e:
        logger.error(f"Error updating goal: {e}", exc_info=True)
        click.echo(f"Error updating goal: {e}", err=True)
    finally:
        session.close()

@goal.command()
@click.option('--goal-id', 'goal_id', required=True, type=int, help='Goal ID')
def delete(goal_id: int):
    """Delete a goal."""
    session = SessionLocal()
    try:
        success = delete_goal(session, goal_id)
        if success:
            click.echo("Goal deleted.")
        else:
            click.echo("Goal not found.")
        session.commit()
    except Exception as e:
        logger.error(f"Error deleting goal: {e}", exc_info=True)
        click.echo(f"Error deleting goal: {e}", err=True)
        session.rollback()
        raise
    finally:
        session.close()
