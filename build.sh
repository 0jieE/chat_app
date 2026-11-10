#!/usr/bin/env bash
# Render runs this on every deploy (see render.yaml).
set -o errexit  # stop on the first error

pip install -r requirements.txt

# Gather CSS/JS into staticfiles/ for WhiteNoise to serve.
python manage.py collectstatic --no-input

# The free plan has no pre-deploy step, so migrations run here.
python manage.py migrate

# Optional: create an admin account from DJANGO_SUPERUSER_USERNAME and
# DJANGO_SUPERUSER_PASSWORD if they are set (the email is left blank).
# On later deploys the user already exists, so a failure here is not fatal.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input --email "" \
    || echo "Superuser not created (it probably exists already)."
fi
