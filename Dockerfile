# syntax=docker/dockerfile:1

FROM python:3.11-buster

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

CMD ["./start.sh"]

