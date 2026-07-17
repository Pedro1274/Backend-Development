#!/bin/bash

# Roda as migrações do banco de dados
echo "Aplicando migrações do banco de dados..."
poetry run alembic upgrade head

# Inicia a aplicação FastAPI
echo "Iniciando o servidor FastAPI..."
exec poetry run uvicorn --host 0.0.0.0 --port 8000 backend.app:app