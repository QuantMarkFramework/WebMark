FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ARG LIBMARK_VERSION

RUN apt-get update && apt-get -y install git
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
