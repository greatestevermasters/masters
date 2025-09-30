#!/usr/bin/env bash
set -o errexit  

pip install -r requirements.txt

# Run migrations automatically on deploy
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
python manage.py loaddata db.json || true


