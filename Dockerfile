FROM python:3.10-slim as base_image

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.5.1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install "poetry==$POETRY_VERSION"

# Copy poetry requirements files
WORKDIR /tmp
COPY poetry.lock pyproject.toml /tmp/

# Export prod and dev requirements into pip format, remove poetry
RUN poetry export --without dev -f requirements.txt -o /tmp/requirements.txt && \
    poetry export -f requirements.txt -o /tmp/requirements.dev.txt && \
    rm poetry.lock pyproject.toml  && \
    pip uninstall -y poetry

# Copy project files
WORKDIR /code
COPY . .

# Expose port 8000
EXPOSE 8000

# Entrypoint script for migrations import
ENTRYPOINT ["bash", "entrypoint.sh"]

FROM base_image as prod_image

# Install project's dependencies
RUN pip install -r /tmp/requirements.txt

# Run server
CMD ["gunicorn", "todolist.todolist.wsgi", "-w", "2", "-b", "0.0.0.0:8000"]

FROM base_image as dev_image

# Install project's dependencies
RUN pip install -r /tmp/requirements.dev.txt

# Run server
CMD ["python", "todolist/manage.py", "runserver", "0.0.0.0:8000"]
