# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Local Development

```bash
# 1. Setup environment
python setup_env.py
# Select option 1

# 2. Install and migrate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# 3. Run
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

### Railway Deployment

```bash
# 1. Push to GitHub
git add .
git commit -m "Add multi-environment support"
git push

# 2. In Railway Dashboard:
# - Create new project from GitHub repo
# - Add PostgreSQL database
# - Add environment variables:
ENVIRONMENT=railway
DEBUG=False
SECRET_KEY=<generate-new-key>
RAILWAY_PUBLIC_DOMAIN=<your-app>.up.railway.app
ALLOWED_HOSTS=<your-app>.up.railway.app

# 3. Deploy and migrate
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

### Seenode Deployment

```bash
# 1. Push to GitHub
git add .
git commit -m "Add Seenode deployment configuration"
git push

# 2. In Seenode Dashboard:
# - Create PostgreSQL database
# - Create Web Service from your Git repo
# - Link the database
# - Set build command: ./build.sh
# - Set start command: gunicorn expensetracker.wsgi --bind 0.0.0.0:80
# - Set Port to: 80
# - Add environment variables:
ENVIRONMENT=seenode
DEBUG=False
SECRET_KEY=<generate-new-key>
SEENODE_DOMAIN=<your-app>.seenode.app
ALLOWED_HOSTS=<your-app>.seenode.app

# 3. Deploy and create superuser via console
python manage.py createsuperuser
```

**📖 Detailed Guide:** See `SEENODE_DEPLOYMENT.md`

---

### PythonAnywhere Deployment

```bash
# 1. Clone on PythonAnywhere
git clone <your-repo-url>
cd expensetracker

# 2. Setup virtualenv
mkvirtualenv --python=/usr/bin/python3.10 expensetracker-env
pip install -r requirements.txt

# 3. Configure WSGI file (add these lines):
os.environ['ENVIRONMENT'] = 'pythonanywhere'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = '<your-secret-key>'
os.environ['PYTHONANYWHERE_DOMAIN'] = '<username>.pythonanywhere.com'
os.environ['ALLOWED_HOSTS'] = '<username>.pythonanywhere.com'

# 4. Collect static and migrate
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser

# 5. Reload web app in PythonAnywhere dashboard
```

---

## 🔑 Generate Secret Key

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 📚 Need More Help?

- **Full deployment guide:** See `DEPLOYMENT.md`
- **What changed:** See `CHANGES.md`
- **Environment setup:** Run `python setup_env.py`

---

## 🔄 Switch Environments

```bash
# Switch to local
python setup_env.py  # Select 1

# Switch to Railway (for testing)
python setup_env.py  # Select 2

# Switch to Seenode (for testing)
python setup_env.py  # Select 3

# Switch to PythonAnywhere (for testing)
python setup_env.py  # Select 4
```

---

## ✅ Verify Setup

```bash
# Check for deployment issues
python manage.py check --deploy

# Test database connection
python manage.py migrate --check

# Collect static files (production only)
python manage.py collectstatic --noinput
```

---

## 🆘 Common Issues

**Static files not loading?**
```bash
python manage.py collectstatic
```

**Database errors?**
- Local: Check `db.sqlite3` exists
- Railway: Verify PostgreSQL is added
- PythonAnywhere: Check DATABASE_URL

**CSRF errors?**
- Verify `CSRF_TRUSTED_ORIGINS` includes your domain
- Check `ALLOWED_HOSTS` is set correctly

---

## 📦 Requirements

All environments need:
- Python 3.8+
- Django 5.0.4
- See `requirements.txt` for full list

Railway additionally needs:
- PostgreSQL (added via Railway dashboard)
- Gunicorn (already in requirements.txt)
- WhiteNoise (already in requirements.txt)

