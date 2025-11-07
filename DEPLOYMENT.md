# Deployment Guide

This Django Expense Tracker application supports multiple deployment environments through environment variables.

## Environment Configuration

The application uses the `ENVIRONMENT` variable to determine which configuration to use:
- `local` - Local development (default)
- `railway` - Railway.app deployment
- `pythonanywhere` - PythonAnywhere deployment

## Local Development

1. **Copy the local environment template:**
   ```bash
   cp .env.local.example .env
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - URL: http://127.0.0.1:8000/

### Local Configuration Details
- Uses SQLite database (`db.sqlite3`)
- Debug mode enabled
- Allowed hosts: `localhost`, `127.0.0.1`

---

## Railway Deployment

Railway.app provides free hosting for 30 days and supports PostgreSQL databases.

### Initial Setup

1. **Create a Railway account:**
   - Go to https://railway.app/
   - Sign up with GitHub

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your expense tracker repository

3. **Add PostgreSQL database:**
   - In your project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

### Environment Variables

Set these in Railway's dashboard (Project → Variables):

```bash
ENVIRONMENT=railway
DEBUG=False
SECRET_KEY=<generate-a-new-secret-key>
RAILWAY_PUBLIC_DOMAIN=<your-app>.up.railway.app
ALLOWED_HOSTS=<your-app>.up.railway.app,*.railway.app
```

**Generate a new SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Deployment Configuration

Railway automatically detects Django projects. Ensure you have:

1. **Procfile** (create if missing):
   ```
   web: gunicorn expensetracker.wsgi --log-file -
   ```

2. **requirements.txt** includes:
   ```
   Django
   gunicorn
   dj-database-url
   psycopg2-binary
   whitenoise
   ```

### Post-Deployment

After deployment, run migrations:
```bash
railway run python manage.py migrate
```

Or use Railway's CLI:
```bash
railway login
railway link
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### Railway Configuration Details
- Uses PostgreSQL database (via `DATABASE_URL`)
- WhiteNoise for static file serving
- Gunicorn as WSGI server
- Debug mode disabled
- Compressed static files

---

## PythonAnywhere Deployment

PythonAnywhere offers free hosting with some limitations.

### Initial Setup

1. **Create a PythonAnywhere account:**
   - Go to https://www.pythonanywhere.com/
   - Sign up for a free account

2. **Upload your code:**
   - Use Git to clone your repository:
     ```bash
     git clone https://github.com/yourusername/expensetracker.git
     ```

3. **Create a virtual environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 expensetracker-env
   pip install -r requirements.txt
   ```

### Web App Configuration

1. **Create a new web app:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10

2. **Configure WSGI file:**
   Edit the WSGI configuration file (e.g., `/var/www/unkerpaulie_pythonanywhere_com_wsgi.py`):
   
   ```python
   import os
   import sys
   
   # Add your project directory to the sys.path
   path = '/home/unkerpaulie/expensetracker'
   if path not in sys.path:
       sys.path.append(path)
   
   # Set environment variables
   os.environ['ENVIRONMENT'] = 'pythonanywhere'
   os.environ['DEBUG'] = 'False'
   os.environ['SECRET_KEY'] = 'your-production-secret-key'
   os.environ['PYTHONANYWHERE_DOMAIN'] = 'unkerpaulie.pythonanywhere.com'
   os.environ['ALLOWED_HOSTS'] = 'unkerpaulie.pythonanywhere.com'
   
   # Set Django settings module
   os.environ['DJANGO_SETTINGS_MODULE'] = 'expensetracker.settings'
   
   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

3. **Configure static files:**
   In the "Web" tab, set:
   - URL: `/static/`
   - Directory: `/home/unkerpaulie/expensetracker/static`

4. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Reload the web app:**
   Click the "Reload" button in the Web tab

### PythonAnywhere Configuration Details
- Uses SQLite by default (or MySQL if configured)
- Static files served by PythonAnywhere
- Debug mode disabled
- Custom WSGI configuration

---

## Environment Variables Reference

### Common Variables (All Environments)

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `local`, `railway`, `pythonanywhere` |
| `DEBUG` | Enable debug mode | `True` or `False` |
| `SECRET_KEY` | Django secret key | `django-insecure-...` |

### Railway-Specific Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by Railway |
| `RAILWAY_PUBLIC_DOMAIN` | Your Railway domain | `myapp.up.railway.app` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `myapp.up.railway.app,*.railway.app` |

### PythonAnywhere-Specific Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PYTHONANYWHERE_DOMAIN` | Your PythonAnywhere domain | `username.pythonanywhere.com` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `username.pythonanywhere.com` |
| `DATABASE_URL` | MySQL connection (optional) | `mysql://user:pass@host/db` |

---

## Switching Between Environments

To switch between environments locally:

1. **For local development:**
   ```bash
   cp .env.local.example .env
   ```

2. **For Railway testing:**
   ```bash
   cp .env.railway.example .env
   # Edit .env with your Railway settings
   ```

3. **For PythonAnywhere testing:**
   ```bash
   cp .env.pythonanywhere.example .env
   # Edit .env with your PythonAnywhere settings
   ```

---

## Troubleshooting

### Railway Issues

**Static files not loading:**
- Ensure `STATIC_ROOT` is set correctly
- Run `python manage.py collectstatic`
- Check that WhiteNoise is in `MIDDLEWARE`

**Database connection errors:**
- Verify PostgreSQL service is added
- Check `DATABASE_URL` is set automatically

### PythonAnywhere Issues

**500 Internal Server Error:**
- Check error logs in the "Web" tab
- Verify WSGI configuration
- Ensure all environment variables are set

**Static files not loading:**
- Run `python manage.py collectstatic`
- Verify static files path in Web tab
- Check `STATIC_ROOT` setting

### General Issues

**CSRF verification failed:**
- Check `CSRF_TRUSTED_ORIGINS` includes your domain
- Verify `ALLOWED_HOSTS` is configured correctly

**Import errors:**
- Ensure all dependencies are installed
- Check `requirements.txt` is complete

---

## Security Checklist

Before deploying to production:

- [ ] Generate a new `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set up `CSRF_TRUSTED_ORIGINS`
- [ ] Use environment variables for sensitive data
- [ ] Never commit `.env` files to version control
- [ ] Use HTTPS in production
- [ ] Set up proper database backups
- [ ] Review Django security checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

---

## Additional Resources

- **Django Deployment Checklist:** https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- **Railway Documentation:** https://docs.railway.app/
- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **WhiteNoise Documentation:** http://whitenoise.evans.io/

