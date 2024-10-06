FROM python:3.12

FROM ubuntu:latest
LABEL authors="User"

ENTRYPOINT ["top", "-b"]

ENV PYTHONDONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD . .