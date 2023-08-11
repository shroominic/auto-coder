FROM --platform=arm64 python:slim

RUN apt-get update && apt-get install -y \
    build-essential gcc libffi-dev \
    libpq-dev git

COPY pyproject.toml poetry.lock /autocodr/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    cd /autocodr && \
    poetry install --no-dev

# RUN apk del build-base gcc libffi-dev && \
#     rm -rf /var/cache/apk/*

WORKDIR /

COPY . /autocodr

EXPOSE 8000

CMD uvicorn autocodr.api.core:app --host 0.0.0.0 --port 8000
