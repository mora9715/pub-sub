FROM python:3.9-slim

RUN pip3 install -U poetry
WORKDIR /app

COPY ./poetry.lock ./poetry.toml ./pyproject.toml ./

RUN poetry install --without dev

COPY ./subscriber1.py ./subscriber2.py ./bootstrap.py ./producer.py ./
COPY ./pubsub ./pubsub

ENTRYPOINT ["python3", "-u"]