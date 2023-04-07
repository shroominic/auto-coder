FROM --platform=arm64 python:3.11.3-alpine3.17

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt
RUN pip install psycopg2

COPY autocoder /app
WORKDIR /app

EXPOSE 80

CMD uvicorn main:app