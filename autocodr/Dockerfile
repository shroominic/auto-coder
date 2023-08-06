FROM --platform=arm64 python:slim

RUN apk update && apk add --no-cache \
    build-base gcc libffi-dev \
    postgresql-dev git

COPY pyproject.toml poetry.lock /autocoder/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    cd /autocoder && \
    poetry install --no-dev

# RUN apk del build-base gcc libffi-dev && \
#     rm -rf /var/cache/apk/*

COPY . /autocoder

EXPOSE 8000

CMD uvicorn autocoder.api.core:app --host 0.0.0.0 --port 8000
