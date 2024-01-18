FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

VOLUME [ "/app" ]

# Install psql
RUN apt-get update && apt-get install -y postgresql-client

EXPOSE 8000

# Run the app:
CMD python manage.py runserver 0.0.0.0:8000
