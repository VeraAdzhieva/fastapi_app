FROM python:3.14-slim

RUN pip install poetry==2.3.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/tmp/poetry_cache' \
    PYTHONPATH=/app

WORKDIR /app

COPY . .

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

EXPOSE 8000

CMD ["uvicorn", "src.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]