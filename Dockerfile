FROM python:3.7-alpine
MAINTAINER Sheracore App

# This is running python unbuffered mode
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D means in running application only
# If you dont do this the app is running just on root user that is not recommende
RUN adduser -D user
USER user