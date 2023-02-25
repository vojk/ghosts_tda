# syntax=docker/dockerfile:1

FROM python:3.10-buster

WORKDIR /app

RUN pip install pipenv
RUN pip install flask_login
RUN pip install python-dotenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

CMD ["./start.sh"]

