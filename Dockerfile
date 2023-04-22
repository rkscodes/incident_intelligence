FROM python:3.9.16

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry --trusted-host pypi.python.org --no-cache-dir
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without dev

RUN mkdir -p pipeline/flows
COPY pipeline/flows/ pipeline/flows

RUN mkdir transform_dbt
COPY transform_dbt/ transform_dbt/