#!/bin/bash

# Wait for the database to be ready using pg_isready
# while ! pg_isready -h db -p 5432 -U user; do
#   echo "Waiting for the database to be ready..."
#   sleep 1
# done

# Run database migrations
# echo "initializing alembic"
# alembic init alembic

# makemigrations
# alembic revision --autogenerate -m "Initial migration"


# echo "Running migrations..."
# alembic upgrade head

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
