FROM python:3.11.5-alpine AS builder

WORKDIR /app

COPY group_expense_tracker/ /app/group_expense_tracker
COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11.5-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY group_expense_tracker/ /app/group_expense_tracker

VOLUME /app

CMD ["python", "group_expense_tracker/manage.py", "runserver", "0.0.0.0:8000"]


