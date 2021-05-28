FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get -y install git
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
