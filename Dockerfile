FROM python:3.11.0-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system tg_parser \
    && adduser --system tg_parser --ingroup tg_parser

# Requirements are installed here to ensure they will be cached.
COPY TGParser/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm /requirements.txt

COPY --chown=tg_parser:tg_parser ./TGParser /app

USER tg_parser
WORKDIR /app
