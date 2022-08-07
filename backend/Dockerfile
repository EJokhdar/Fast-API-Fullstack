FROM python:3.10-slim-buster AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
HEALTHCHECK CMD curl --fail http://localhost:8000/healthcheck || exit 1 
EXPOSE 8000

FROM builder AS dev
RUN pip install -r dev_requirements.txt
