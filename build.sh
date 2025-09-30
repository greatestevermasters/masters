#!/usr/bin/env bash
# build.sh - used by Render as the buildCommand

set -euo pipefail
echo "=== Build started ==="

# Show which database Django will connect to (mask password)
if [[ -n "${DATABASE_URL:-}" ]]; then
  echo "🔹 Using DATABASE_URL: $(echo $DATABASE_URL | sed -E 's#(//[^:]+:)[^@]+#\1********#')"
else
  echo "⚠️ DATABASE_URL is not set!"
fi

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate --noinput

# Load initial data (if db.json exists in repo)
if [ -f db.json ]; then
  echo "🔹 Loading db.json..."
  python manage.py loaddata db.json || echo "⚠️ loaddata failed or data already loaded"
fi

echo "✅ Build finished successfully"
