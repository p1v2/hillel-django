release: python manage.py migrate
web: gunicorn --bind 0.0.0.0:$PORT hillel_django.wsgi
