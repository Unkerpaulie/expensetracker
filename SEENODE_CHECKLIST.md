# Seenode Deployment Checklist

Use this checklist to ensure a smooth deployment to Seenode.

## Pre-Deployment Checklist

### Local Preparation
- [ ] All code changes committed to Git
- [ ] `requirements.txt` is up to date
- [ ] `build.sh` exists and is ready
- [ ] `.env.seenode.example` reviewed
- [ ] Code pushed to GitHub/GitLab

### Generate Production Secrets
- [ ] Generate new `SECRET_KEY`:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- [ ] Save the key securely (you'll need it for Seenode)

## Seenode Dashboard Setup

### Step 1: Create Database
- [ ] Log in to [cloud.seenode.com](https://cloud.seenode.com)
- [ ] Click "New" → "Database"
- [ ] Select "PostgreSQL"
- [ ] Choose plan (free tier available)
- [ ] Name: `expensetracker-db` (or your choice)
- [ ] Click "Create Database"
- [ ] Wait for provisioning to complete
- [ ] Note: Database connection details (for reference)

### Step 2: Create Web Service
- [ ] Click "New" → "Web Service"
- [ ] Connect Git repository:
  - [ ] Select GitHub or GitLab
  - [ ] Authorize Seenode
  - [ ] Select your repository
  - [ ] Choose branch (main/master)

### Step 3: Configure Build Settings
- [ ] Set **Build Command**: `./build.sh`
- [ ] Set **Start Command**: `gunicorn expensetracker.wsgi --bind 0.0.0.0:80`
- [ ] Set **Port**: `80`
- [ ] ⚠️ **IMPORTANT**: Port must match the port in start command!

### Step 4: Get Database Connection URL
- [ ] Go to your PostgreSQL database in Seenode dashboard
- [ ] Find "Connection Details" or "Connection String"
- [ ] Copy the full `DATABASE_URL` (format: `postgresql://user:password@host:port/database`)
- [ ] Keep this ready for the next step

### Step 5: Set Environment Variables
Add these variables in the **Variables** tab (click "+ Add variable" for each):

- [ ] `ENVIRONMENT` = `seenode`
- [ ] `DEBUG` = `False`
- [ ] `SECRET_KEY` = `<your-generated-secret-key>`
- [ ] `DATABASE_URL` = `<your-database-connection-string>`
- [ ] `ALLOWED_HOSTS` = `your-app.seenode.app` (update after first deploy)
- [ ] `SEENODE_DOMAIN` = `your-app.seenode.app` (update after first deploy)

**Note:** For first deployment, you can use placeholder values for domain-related variables.

### Step 6: Choose Plan
- [ ] Select instance size (free tier or paid)
- [ ] Review configuration
- [ ] Click "Create Web Service"

## During Deployment

### Monitor Deployment
- [ ] Watch the **Logs** tab
- [ ] Verify build script runs successfully:
  - [ ] Dependencies installed
  - [ ] Static files collected
  - [ ] Migrations run
- [ ] Check for any error messages
- [ ] Wait for "Deployment successful" message

### Common Build Issues to Watch For
- [ ] Missing dependencies in `requirements.txt`
- [ ] Build script errors
- [ ] Database connection issues
- [ ] Static file collection errors

## Post-Deployment

### Step 7: Update Domain Settings
After first successful deployment:

- [ ] Note your actual Seenode URL (e.g., `your-app.seenode.app`)
- [ ] Go back to **Variables** tab
- [ ] Update `ALLOWED_HOSTS` with actual domain
- [ ] Update `SEENODE_DOMAIN` with actual domain
- [ ] Save changes
- [ ] Redeploy (automatic)

### Step 8: Create Superuser
- [ ] Open Seenode Console/Shell for your service
- [ ] Run: `python manage.py createsuperuser`
- [ ] Enter username, email, and password
- [ ] Verify superuser created successfully

### Step 9: Test Your Application
- [ ] Visit your application URL: `https://your-app.seenode.app`
- [ ] Verify homepage loads
- [ ] Test login functionality
- [ ] Visit admin panel: `https://your-app.seenode.app/admin`
- [ ] Log in with superuser credentials
- [ ] Test creating an expense
- [ ] Test creating an income
- [ ] Verify dashboard displays correctly
- [ ] Check that charts render properly

### Step 10: Verify Static Files
- [ ] Check that CSS loads correctly
- [ ] Check that JavaScript works
- [ ] Check that images display
- [ ] Verify Font Awesome icons appear
- [ ] Test responsive design on mobile

## Troubleshooting Checklist

### If You Get 502 Bad Gateway
- [ ] Check Port field in dashboard (should be `80`)
- [ ] Verify start command: `gunicorn expensetracker.wsgi --bind 0.0.0.0:80`
- [ ] Ensure port in command matches Port field
- [ ] Check Logs tab for specific errors
- [ ] Verify application is starting correctly

### If Build Fails
- [ ] Check Logs tab for error messages
- [ ] Verify `requirements.txt` includes all dependencies
- [ ] Check that `build.sh` is in repository
- [ ] Verify build command is set correctly
- [ ] Check for Python version compatibility

### If Static Files Don't Load
- [ ] Verify `build.sh` runs `collectstatic`
- [ ] Check Logs for collectstatic errors
- [ ] Verify WhiteNoise is in MIDDLEWARE (already configured)
- [ ] Check STATIC_ROOT setting (already configured)

### If Database Connection Fails
- [ ] Verify database is created and running
- [ ] Check that `DATABASE_URL` is set correctly in Variables tab
- [ ] Verify the connection string format: `postgresql://user:pass@host:port/db`
- [ ] Check that `psycopg2-binary` is in `requirements.txt`
- [ ] Review database logs in Seenode dashboard
- [ ] Test connection string from your database dashboard

### If CSRF Errors Occur
- [ ] Verify `SEENODE_DOMAIN` is set correctly
- [ ] Check that `ALLOWED_HOSTS` includes your domain
- [ ] Ensure you're using HTTPS (automatic with Seenode)
- [ ] Clear browser cookies and try again

## Security Checklist

### Production Security
- [ ] `DEBUG` is set to `False`
- [ ] New `SECRET_KEY` generated (not default)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `CSRF_TRUSTED_ORIGINS` includes your domain
- [ ] Database uses strong password (Seenode default)
- [ ] Environment variables are secure
- [ ] HTTPS is enabled (automatic)

### Post-Launch Security
- [ ] Change default admin password
- [ ] Review user permissions
- [ ] Set up regular database backups
- [ ] Monitor application logs
- [ ] Keep dependencies updated

## Maintenance Checklist

### Regular Maintenance
- [ ] Monitor application performance
- [ ] Check error logs regularly
- [ ] Review database size and performance
- [ ] Update dependencies periodically
- [ ] Test backup restoration process

### Updating Your Application
When you make changes:
- [ ] Test changes locally first
- [ ] Commit changes to Git
- [ ] Push to repository
- [ ] Seenode auto-deploys
- [ ] Monitor deployment logs
- [ ] Test changes on live site

## Documentation Reference

For more detailed information, see:

- **Quick Start**: `QUICKSTART.md` (Seenode section)
- **Detailed Guide**: `SEENODE_DEPLOYMENT.md`
- **Platform Comparison**: `PLATFORM_COMPARISON.md`
- **Summary**: `SEENODE_SUMMARY.md`

## Support Resources

If you need help:

- [ ] Check Seenode documentation: [seenode.com/docs](https://seenode.com/docs)
- [ ] Review application logs in Seenode dashboard
- [ ] Join Seenode Discord community
- [ ] Contact Seenode support through dashboard
- [ ] Review this project's documentation

## Success Criteria

Your deployment is successful when:

- ✅ Application loads at your Seenode URL
- ✅ Admin panel is accessible
- ✅ Can log in with superuser account
- ✅ Can create and view expenses
- ✅ Can create and view income
- ✅ Dashboard displays correctly
- ✅ Charts render properly
- ✅ Static files load correctly
- ✅ No errors in logs
- ✅ HTTPS works automatically

## Next Steps After Successful Deployment

- [ ] Set up custom domain (optional)
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Add more users/test accounts
- [ ] Customize application for your needs
- [ ] Share your success! 🎉

---

**Congratulations on your Seenode deployment!** 🚀

If you followed this checklist, your Django Expense Tracker should be running smoothly on Seenode.

