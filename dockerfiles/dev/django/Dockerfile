FROM python:3.10-slim-buster

LABEL maintainer="eskandary.saeed336@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip
RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY ./core .
