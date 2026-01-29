FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PostGIS, psycopg2, and monitoring
RUN apt-get update \
    && apt-get install -y \
        gcc \
        g++ \
        libpq-dev \
        gdal-bin \
        libgdal-dev \
        graphviz \
        graphviz-dev \
        postgresql-client \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install Python dependencies
RUN pip install --no-cache-dir \
    Django>=4.2 \
    psycopg2-binary>=2.9 \
    django-extensions \
    pydot \
    pygraphviz \
    djangorestframework>=3.14 \
    django-cors-headers \
    gunicorn \
    celery[redis]>=5.3 \
    django-celery-beat \
    django-celery-results \
    redis>=5.0 \
    django-redis>=5.4 \
    django-prometheus>=2.3 \
    prometheus-client \
    geopy \
    requests

# Copy application code
COPY . .

# Create directory for logs
RUN mkdir -p /var/log/django

# Expose port
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["gunicorn", "moveus.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]