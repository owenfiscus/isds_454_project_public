FROM python:3.9-slim

WORKDIR /usr/src/api


RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/api/requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

RUN mkdir /usr/src/api/warehouse

COPY . /usr/src/api/