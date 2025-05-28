<<<<<<< HEAD
"""
Health Simplified CLI Application Package Initialization

This file initializes the Health Simplified package, making it easier to import
and use the main components of the application. It defines what is available
when someone uses `from health_simplified import *` and imports the main
components for direct access.
"""

__all__ = ['models', 'cli']

# Import the main components of the package for easy access
from .models import Base, User, FoodEntry, Goal, MealPlan
from .cli import cli

=======
# This file makes health_tracker a package
>>>>>>> e08c1f3 (Add database connection setup and comprehensive CRUD tests for models)
