FROM python:3.12


RUN pip install poetry


WORKDIR /web

COPY pyproject.toml poetry.lock* /web


RUN poetry config virtualenvs.create false && poetry install --no-dev
