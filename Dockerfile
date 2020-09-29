FROM python:3.6-alpine
MAINTAINER Sheracore App

# This is running python unbuffered mode
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# These installations is requiered for installing psycopg2
# After finishing the project this command will un commented
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D means in running application only
# If you don't do this, the app just on root user can be run that is not recommended
RUN adduser -D user
USER user
