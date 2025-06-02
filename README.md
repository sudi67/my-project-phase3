# Health Tracker CLI Application

## Overview

This project is a Health Tracker CLI application implemented in Python. It uses SQLAlchemy ORM for database operations and Click for command-line interface commands. The application manages users, food entries, meal plans, and goals.

## Project Structure

- `health_tracker/`: Main package containing modules for CLI commands, models, and database operations.
  - `cli.py`: Main CLI entry point using Click.
  - `models/`: Contains SQLAlchemy models and CLI controllers for different entities.
  - `db/`: Database setup, session management, and operations.
  - `tests/`: Unit and integration tests for CLI commands and database operations.

## Database

- Uses SQLite by default for testing (`test.db`).
- Supports PostgreSQL if configured via `DATABASE_URL` environment variable.
- Database schema includes tables for users, food entries, meal plans, and goals.
- Database initialization is done via `init_db()` function.

## CLI Commands

- User management: create, list, delete users.
- Food entry management: create, list, update, delete food entries.
- Meal plan management: create, list, update, delete meal plans.
- Commands are implemented using Click groups and options.

## How to Run

1. Install dependencies from `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```
   python -m health_tracker.cli init
   ```

3. Use CLI commands to manage users, food entries, and meal plans. Examples:
   ```
   python -m health_tracker.cli user create --name Alice --email alice@example.com
   python -m health_tracker.cli foodentry create --user-id 1 --name Apple --calories 95
   python -m health_tracker.cli mealplan create --user-id 1 --date 2024-01-01 --meal-type breakfast
   ```

## Testing

- Unit tests cover individual CLI commands and database operations.
- Integration tests cover user, food entry, and meal plan workflows.
- Tests use Click's `CliRunner` for invoking CLI commands.
- Database is initialized before tests and uses SQLite for isolation.
- Some tests dynamically retrieve user IDs to avoid hardcoded values.

### How to Run Tests

To run all tests, use the following command in the project root directory:

```bash
pytest --disable-warnings -q
```

This will run all unit and integration tests quietly, suppressing warnings.

## Known Issues

- Integration test for food entry creation previously failed due to database session or transaction handling issues but has been fixed.
- Database logs showed rollbacks after user selection, indicating possible session conflicts, now resolved.
- All CLI commands work correctly in integration scenarios.

## Next Steps

- Perform thorough testing of all features and edge cases.
- Add more detailed logging for debugging if needed.
- Continue to improve and extend the application as required.
