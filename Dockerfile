FROM python:3.10.11-alpine AS builder
WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10.11-alpine
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn


# for docker container development
ENV ENVIRONMENT=TEST
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "100", "--log-level", "debug", "--reload", "main:app"]
# waiting 10 seconds for MariaDb container
# CMD ["sh", "-c", "sleep 10 && gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 100 --log-level debug --reload main:app"]


## for container in production - change ENVIRONMENT to PRODUCTION, change ip address and port, remove debug
# COPY --exclude=components/documentation_generator.py . /app/
# ENV ENVIRONMENT=PRODUCTION
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "100", "--log-level", "info", "main:app"]
