FROM python:3.12


RUN pip install poetry

WORKDIR /bot


COPY pyproject.toml ./
COPY poetry.lock ./


RUN poetry config virtualenvs.create false && poetry install --no-dev
