FROM --platform=arm64 python:alpine

RUN apk update && \
    apk add --no-cache \
    build-base \
    gcc \
    libffi-dev \
    postgresql-dev \
    git

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

RUN pip install psycopg2

COPY autocoder /autocoder

EXPOSE 80

CMD uvicorn autocoder.api.app:app --host 0.0.0.0 --port 8000