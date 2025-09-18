# FastAPI Project

This is a FastAPI project set up to run inside a Docker container using Debian Bookworm and the latest Python version (3.13).

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Build the Docker image:

   ```bash
   docker-compose build
   ```

2. Run the application:

   ```bash
   docker-compose up
   ```

3. Open your browser and go to `http://localhost:8070` to see the API documentation.

## API Endpoints

- `GET /`: Returns a simple "Hello World" message.
- `GET /items/{item_id}`: Returns item details with optional query parameter `q`.

## Development

To make changes to the code, edit the files in the `app/` directory. The volume mount in `docker-compose.yml` will reflect changes automatically when you restart the container.

Note: The `__pycache__` directory and `.pyc` files are generated inside the Docker container but are not mounted back to your local workspace, keeping it clean.

### Using VS Code Dev Containers

To enable VS Code to recognize imports like `from fastapi import FastAPI` directly from the container:

1. Install the "Dev Containers" extension in VS Code.
2. Open the Command Palette (`Ctrl+Shift+P`) and select "Dev Containers: Reopen in Container".
3. VS Code will build and open the project inside the container, providing full IntelliSense, linting, and debugging capabilities.

The dev container configuration is set up to use Python 3.13 from the container and includes recommended extensions.

## Stopping the Application

To stop the application, press `Ctrl+C` in the terminal or run:

```bash
docker-compose down
```

## Development tools and linting

For local development and CI it's useful to install developer dependencies and run linters/formatters.

1. Install dev dependencies (recommended to use a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

1. Install pre-commit hooks:

```bash
pre-commit install
```

1. Run ruff (linter/formatter) across the project:

```bash
ruff --fix .
```

1. Run tests:

```bash
pytest
```

These tools are configured in `pyproject.toml` and `.pre-commit-config.yaml` for consistent code style.

Example: run tests with coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

Optional: build Docker image with development dependencies

The Docker image by default installs only `requirements.txt`. If you want the
image to also include development tools (for example in a CI image or a debug
build), you can pass a build argument when building the image:

```bash
docker-compose build --build-arg INSTALL_DEV=true
```

Note: installing dev dependencies increases image size and is usually not
required for production images. For local development, prefer using the local
`.venv` and `requirements-dev.txt`.
