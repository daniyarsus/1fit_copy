#!/bin/bash
echo "Waiting for 7 seconds..."
sleep 7

# Перейдите в директорию с приложением
cd FastAPI

# Выполните миграции базы данных
alembic upgrade head

# Запустите приложение с Gunicorn и Uvicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000