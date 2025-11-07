# Changes Made for Multi-Environment Support

## Summary

The Django Expense Tracker has been updated to support multiple deployment environments (local, Railway, PythonAnywhere) using environment variables. You can now easily switch between environments without manually editing the settings file.

## Files Modified

### 1. `expensetracker/settings.py`
**Changes:**
- Added `import os` for environment variable support
- Added `ENVIRONMENT` variable detection (defaults to 'local')
- Made `SECRET_KEY` configurable via environment variable
- Made `DEBUG` configurable via environment variable
- Updated `ALLOWED_HOSTS` to be environment-specific:
  - **Local:** `['localhost', '127.0.0.1']`
  - **Railway:** Configurable via `ALLOWED_HOSTS` env var
  - **PythonAnywhere:** Configurable via `ALLOWED_HOSTS` env var
- Updated `MIDDLEWARE` to conditionally include WhiteNoise for Railway
- Updated `DATABASES` configuration:
  - **Local:** SQLite (default)
  - **Railway:** PostgreSQL via `DATABASE_URL`
  - **PythonAnywhere:** SQLite or MySQL via `DATABASE_URL`
- Updated `STATIC_ROOT` and static file handling:
  - **Local:** No STATIC_ROOT needed
  - **Railway:** Uses `staticfiles/` with WhiteNoise compression
  - **PythonAnywhere:** Uses `static/` directory
- Updated `CSRF_TRUSTED_ORIGINS` to be environment-specific

### 2. `.gitignore`
**Changes:**
- Added `.env` and environment-specific `.env.*` files
- Added `staticfiles/` and `static/` directories
- Added IDE directories (`.vscode/`, `.idea/`)

## Files Created

### Configuration Files

1. **`.env.example`**
   - Comprehensive template showing all available environment variables
   - Includes documentation for each environment type
   - Instructions for generating secure SECRET_KEY

2. **`.env.local.example`**
   - Quick setup template for local development
   - Minimal configuration needed

3. **`.env.railway.example`**
   - Template for Railway deployment
   - Includes Railway-specific variables

4. **`.env.pythonanywhere.example`**
   - Template for PythonAnywhere deployment
   - Includes PythonAnywhere-specific variables

### Documentation Files

5. **`DEPLOYMENT.md`**
   - Comprehensive deployment guide for all three environments
   - Step-by-step instructions for each platform
   - Environment variables reference table
   - Troubleshooting section
   - Security checklist

6. **`CHANGES.md`** (this file)
   - Summary of all changes made
   - Migration guide for existing deployments

### Helper Files

7. **`Procfile`**
   - Railway deployment configuration
   - Specifies Gunicorn as the WSGI server

8. **`setup_env.py`**
   - Interactive script to help switch between environments
   - Copies appropriate `.env` template
   - Provides next steps for each environment

## How to Use

### For Local Development

```bash
# Option 1: Use the helper script
python setup_env.py
# Select option 1

# Option 2: Manual setup
cp .env.local.example .env
python manage.py migrate
python manage.py runserver
```

### For Railway Deployment

```bash
# Option 1: Use the helper script locally for testing
python setup_env.py
# Select option 2, then edit .env with your settings

# Option 2: Set environment variables in Railway dashboard
# Go to your Railway project → Variables
# Add the following:
ENVIRONMENT=railway
DEBUG=False
SECRET_KEY=<your-secret-key>
RAILWAY_PUBLIC_DOMAIN=<your-app>.up.railway.app
ALLOWED_HOSTS=<your-app>.up.railway.app,*.railway.app

# Railway automatically sets DATABASE_URL when you add PostgreSQL
```

### For PythonAnywhere Deployment

```bash
# Option 1: Use the helper script
python setup_env.py
# Select option 3, then edit .env

# Option 2: Set environment variables in WSGI file
# Edit your WSGI configuration file and add:
os.environ['ENVIRONMENT'] = 'pythonanywhere'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['PYTHONANYWHERE_DOMAIN'] = 'username.pythonanywhere.com'
os.environ['ALLOWED_HOSTS'] = 'username.pythonanywhere.com'
```

## Migration Guide for Existing Deployments

### If You're Currently on Railway

1. Go to your Railway project dashboard
2. Navigate to Variables section
3. Add these new variables:
   ```
   ENVIRONMENT=railway
   DEBUG=False
   SECRET_KEY=<generate-new-key>
   RAILWAY_PUBLIC_DOMAIN=<your-current-domain>
   ALLOWED_HOSTS=<your-current-domain>,*.railway.app
   ```
4. Redeploy your application
5. The `DATABASE_URL` should already be set by Railway

### If You're Currently on PythonAnywhere

1. Edit your WSGI configuration file
2. Add these environment variables at the top:
   ```python
   os.environ['ENVIRONMENT'] = 'pythonanywhere'
   os.environ['DEBUG'] = 'False'
   os.environ['SECRET_KEY'] = '<generate-new-key>'
   os.environ['PYTHONANYWHERE_DOMAIN'] = 'your-username.pythonanywhere.com'
   os.environ['ALLOWED_HOSTS'] = 'your-username.pythonanywhere.com'
   ```
3. Reload your web app

### If You're Running Locally

1. Run the setup script:
   ```bash
   python setup_env.py
   ```
2. Select option 1 (Local Development)
3. Continue using `python manage.py runserver` as before

## Environment Variables Reference

### Required for All Environments

- `ENVIRONMENT` - Set to `local`, `railway`, or `pythonanywhere`
- `SECRET_KEY` - Django secret key (use default for local, generate new for production)
- `DEBUG` - Set to `True` for development, `False` for production

### Railway-Specific

- `DATABASE_URL` - Auto-set by Railway when PostgreSQL is added
- `RAILWAY_PUBLIC_DOMAIN` - Your Railway app domain
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### PythonAnywhere-Specific

- `PYTHONANYWHERE_DOMAIN` - Your PythonAnywhere domain
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - Optional, for MySQL configuration

## Benefits of This Approach

1. **No More Manual Editing** - Switch environments by changing one variable
2. **Version Control Safe** - Sensitive data stays in `.env` files (not committed)
3. **Easy Collaboration** - Team members can use `.env.example` templates
4. **Production Ready** - Proper security settings for each environment
5. **Flexible** - Easy to add new environments in the future
6. **Clear Documentation** - Everything is documented in DEPLOYMENT.md

## Backward Compatibility

The changes are backward compatible:
- If no `ENVIRONMENT` variable is set, defaults to `local`
- If no `.env` file exists, uses sensible defaults
- Existing deployments continue to work with minimal changes

## Security Improvements

1. `SECRET_KEY` is now environment-specific (not hardcoded)
2. `DEBUG` is properly disabled in production environments
3. `ALLOWED_HOSTS` is restricted per environment
4. `CSRF_TRUSTED_ORIGINS` is environment-specific
5. `.env` files are excluded from version control

## Testing

To test the configuration:

```bash
# Test local environment
python setup_env.py  # Select 1
python manage.py check --deploy

# Test Railway environment (locally)
python setup_env.py  # Select 2
# Edit .env with test values
python manage.py check --deploy

# Test PythonAnywhere environment (locally)
python setup_env.py  # Select 3
# Edit .env with test values
python manage.py check --deploy
```

## Support

For detailed deployment instructions, see `DEPLOYMENT.md`.

For questions or issues, refer to:
- Django documentation: https://docs.djangoproject.com/
- Railway documentation: https://docs.railway.app/
- PythonAnywhere help: https://help.pythonanywhere.com/

