# Simple Dockerfile of official Python image on Docker Hub
# https://hub.docker.com/_/python/

FROM python:3

RUN mkdir -p /usr/src/app/output

WORKDIR /usr/src/app

COPY ./docker/pip_requirements.txt .
RUN pip install --no-cache-dir -r pip_requirements.txt

COPY ./app .

CMD [ "python", "./script.py" ]
