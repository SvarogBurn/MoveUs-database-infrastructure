FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

RUN pip install --no-cache-dir \
    Django>=4.2 \
    psycopg2-binary>=2.9

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
