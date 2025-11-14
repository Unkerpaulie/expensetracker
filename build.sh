#!/usr/bin/env bash
# Seenode Build Script
# This script runs during deployment to prepare your application

# Exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
echo "=== Database Configuration Check ==="
python -c "
import os
print('ENVIRONMENT:', os.environ.get('ENVIRONMENT', 'NOT SET'))
print('DATABASE_URL:', 'SET' if os.environ.get('DATABASE_URL') else 'NOT SET')
print('DB_NAME:', os.environ.get('DB_NAME', 'NOT SET'))
print('DB_USER:', os.environ.get('DB_USER', 'NOT SET'))
print('DB_HOST:', os.environ.get('DB_HOST', 'NOT SET'))
print('DB_PORT:', os.environ.get('DB_PORT', 'NOT SET'))
"
echo "==================================="

echo "Testing database connection..."
python manage.py check --database default 2>&1 || {
    echo ""
    echo "❌ ERROR: Database check failed!"
    echo "This usually means the database connection is not configured."
    echo ""
    echo "Please verify in Seenode Variables tab that you have either:"
    echo "  Option 1: DATABASE_URL variable set"
    echo "  Option 2: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT variables set"
    echo ""
    exit 1
}

echo "✓ Database connection successful!"
echo ""
echo "Running migrations..."
python manage.py migrate --verbosity 2 2>&1 || {
    echo ""
    echo "❌ ERROR: Migration failed!"
    echo "Check the error messages above for details."
    echo ""
    exit 1
}

echo "Build completed successfully!"

