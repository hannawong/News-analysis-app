#!/bin/sh
python manage.py migrate
gunicorn 'app.wsgi' -b 0.0.0.0:80 --access-logfile - --log-level info
# what's the diff with gunicorn 'app:get_app()' -b 0.0.0.0:80 --access-logfile - --log-level info