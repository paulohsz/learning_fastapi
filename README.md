# FastAPI Learning Project

This is a FastAPI project set up to run inside a Docker container using Debian Bookworm and Python 3.13. The project demonstrates FastAPI's capabilities along with SQLAlchemy ORM, database migrations with Alembic, and testing with pytest.

## Project Features

- FastAPI REST API with modern Python 3.13
- SQLAlchemy 2.0 ORM for database operations
- Alembic for database migrations
- Pydantic for data validation and settings management
- Docker-based development environment
- Comprehensive test suite with pytest
- Code quality tools (ruff, pre-commit hooks)

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Build the Docker image:

   ```bash
   docker-compose build --no-cache
   ```

2. Run the application:

   ```bash
   docker-compose up -d
   ```

3. Open your browser and go to `http://localhost:8070` to see the API documentation.

## Database Management

The project uses SQLAlchemy for ORM operations and Alembic for migrations:

### Running Migrations

Apply all pending migrations:

```bash
docker exec learning_fastapi-fastapi-app-1 alembic upgrade head
```

Create a new migration after model changes:

```bash
docker exec learning_fastapi-fastapi-app-1 alembic revision --autogenerate -m "description of changes"
```

Rollback to a previous migration:

```bash
docker exec learning_fastapi-fastapi-app-1 alembic downgrade -1
```

## API Endpoints

- `GET /`: Returns a simple "Hello World" message
- User management endpoints (create, read, update, delete)

## Development

### Code Organization

- `app/main.py` - FastAPI application setup and endpoints
- `app/models.py` - SQLAlchemy models
- `app/schemas.py` - Pydantic schemas for request/response validation
- `tests/` - Test suite
- `migrations/` - Alembic migration scripts

### Local Development

To make changes to the code, edit the files in the `app/` directory. The volume mount in `docker-compose.yml` reflects changes automatically.

### Using VS Code Dev Containers

To enable VS Code to recognize imports directly from the container:

1. Install the "Dev Containers" extension in VS Code
2. Open the Command Palette (`Ctrl+Shift+P`) and select "Dev Containers: Reopen in Container"
3. VS Code will build and open the project inside the container with full IntelliSense and debugging

## Testing

Run the test suite:

```bash
docker exec learning_fastapi-fastapi-app-1 task test
```

This will:

1. Format the code with ruff
2. Run pytest with coverage reporting
3. Show a coverage report for all modules

### Mocking in Tests

The project includes utilities for mocking time-dependent tests to ensure consistent test results:

```python
def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as mocked_time:
        # Test code here
        # mocked_time contains the fixed datetime
```

## Development Tools and Linting

Development dependencies include:

- ruff - Fast Python linter and formatter
- pre-commit - Git hooks for code quality
- pytest & pytest-cov - Test framework with coverage reporting
- taskipy - Task runner for common commands

### Setup Local Development Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
```

### Common Tasks

Run linting:

```bash
ruff check .
```

Format code:

```bash
ruff format .
```

Run these tasks through taskipy:

```bash
task lint      # Run linting
task format    # Format code
task test      # Run tests
task coverage  # Run tests with coverage
```

## Docker Configuration

The Docker image installs `requirements.txt` by default. For development tools:

```bash
docker-compose build --build-arg INSTALL_DEV=true
```

Or use the included override file which sets this automatically:

```bash
docker-compose up -d
```

## Stopping the Application

```bash
docker-compose down
```

Note: installing dev dependencies increases image size and is usually not
required for production images. For local development, prefer using the local
`.venv` and `requirements-dev.txt`.
