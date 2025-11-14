# Seenode Deployment Guide

This guide provides step-by-step instructions for deploying your Django Expense Tracker to Seenode.

## Why Seenode?

Seenode is a developer-friendly cloud platform that offers:
- Simple deployment from Git repositories
- PostgreSQL and MySQL database support
- Automatic SSL certificates
- Easy environment variable management
- Clear logging and monitoring
- No PORT environment variable confusion (explicit port configuration)

## Prerequisites

Before you begin, ensure you have:
- A Seenode account at [cloud.seenode.com](https://cloud.seenode.com)
- Your code pushed to GitHub or GitLab
- Git configured on your machine

## Step-by-Step Deployment

### 1. Prepare Your Application

Your application is already configured for Seenode! The following files are ready:

- ✅ `build.sh` - Build script for Seenode
- ✅ `requirements.txt` - Python dependencies
- ✅ `expensetracker/settings.py` - Environment-aware settings
- ✅ `.env.seenode.example` - Environment variable template

### 2. Push to Git Repository

If you haven't already, push your code to GitHub or GitLab:

```bash
git add .
git commit -m "Add Seenode deployment configuration"
git push origin main
```

### 3. Create a PostgreSQL Database (Recommended)

1. Log in to [cloud.seenode.com](https://cloud.seenode.com)
2. Click **"New"** → **"Database"**
3. Select **"PostgreSQL"**
4. Choose your preferred plan (free tier available)
5. Name your database (e.g., `expensetracker-db`)
6. Click **"Create Database"**
7. Wait for the database to be provisioned
8. **Important:** Note the database connection details (Seenode will auto-configure `DATABASE_URL`)

### 4. Create a Web Service

1. In the Seenode dashboard, click **"New"** → **"Web Service"**
2. Connect your Git repository:
   - Select **GitHub** or **GitLab**
   - Authorize Seenode to access your repositories
   - Select your `expensetracker` repository
   - Choose the branch to deploy (usually `main` or `master`)

### 5. Configure Build and Start Commands

In the service configuration screen:

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn expensetracker.wsgi --bind 0.0.0.0:80
```

**Port Configuration:**
- Set the **Port** field to `80` (or `8080` if you prefer)
- **IMPORTANT:** This must match the port in your start command
- Seenode does NOT use a `PORT` environment variable

### 6. Get Your Database Connection URL

1. Go to your PostgreSQL database in the Seenode dashboard
2. Find the **Connection Details** or **Connection String**
3. Copy the full `DATABASE_URL` (format: `postgresql://user:password@host:port/database`)
4. Keep this handy for the next step

### 7. Configure Environment Variables

In the **Variables** tab (visible in your web service dashboard), add the following variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `seenode` | Tells Django to use Seenode configuration |
| `DEBUG` | `False` | Disable debug mode in production |
| `SECRET_KEY` | `<your-secret-key>` | Generate a new one (see below) |
| `DATABASE_URL` | `postgresql://user:pass@host:port/db` | Copy from your database connection details |
| `ALLOWED_HOSTS` | `your-app.seenode.app` | Your Seenode domain (update after deployment) |
| `SEENODE_DOMAIN` | `your-app.seenode.app` | For CSRF protection (update after deployment) |

**Generate a SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Note:** You'll need to update `ALLOWED_HOSTS` and `SEENODE_DOMAIN` after your first deployment when you get your actual domain.

### 8. Choose Your Plan

Select your preferred instance size:
- **Free Tier:** Good for testing and small projects
- **Paid Tiers:** More resources for production applications

### 9. Deploy!

1. Click **"Create Web Service"**
2. Seenode will start building your application
3. Watch the **Logs** tab to monitor the deployment process
4. Wait for the build to complete (usually 2-5 minutes)

### 10. Update Domain Settings

After your first deployment:

1. Note your service URL (e.g., `your-app.seenode.app`)
2. Go back to the **Variables** tab
3. Update these variables with your actual domain:
   - `ALLOWED_HOSTS` = `your-app.seenode.app`
   - `SEENODE_DOMAIN` = `your-app.seenode.app`
4. Save and redeploy

### 11. Create a Superuser

After successful deployment, create an admin user:

1. Go to your service in the Seenode dashboard
2. Open the **Console** or **Shell** tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Follow the prompts to create your admin account

### 12. Access Your Application

Your Django Expense Tracker is now live at:
```
https://your-app.seenode.app
```

Admin panel:
```
https://your-app.seenode.app/admin
```

## Troubleshooting

### 502 Bad Gateway Error

This is the most common issue and usually means your app isn't listening on the correct port.

**Solution:**
1. Check the **Port** field in your service configuration
2. Ensure your start command binds to the same port:
   ```bash
   gunicorn expensetracker.wsgi --bind 0.0.0.0:80
   ```
3. The port in `--bind` must match the Port field exactly
4. Redeploy after making changes

### Build Fails

**Check the Logs:**
1. Go to the **Logs** tab in your service dashboard
2. Look for error messages during the build process

**Common issues:**
- Missing dependencies: Check `requirements.txt`
- Build script not executable: Ensure `build.sh` has execute permissions
- Database connection errors: Verify database is linked

### Static Files Not Loading

**Solution:**
1. Ensure `build.sh` runs `collectstatic`:
   ```bash
   python manage.py collectstatic --no-input
   ```
2. Verify WhiteNoise is in `MIDDLEWARE` (already configured)
3. Check that `STATIC_ROOT` is set correctly (already configured)

### CSRF Verification Failed

**Solution:**
1. Verify `SEENODE_DOMAIN` environment variable is set correctly
2. Ensure `ALLOWED_HOSTS` includes your domain
3. Check that your domain uses HTTPS (Seenode provides this automatically)

### Database Connection Errors

**Solution:**
1. Verify database is created and linked in Seenode dashboard
2. Check that `DATABASE_URL` is automatically set (should appear in Environment tab)
3. Ensure `dj-database-url` and `psycopg2-binary` are in `requirements.txt`

### Application Logs

To view application logs:
1. Go to your service in the Seenode dashboard
2. Click the **Logs** tab
3. View real-time logs or filter by time period

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | Yes | - | Must be set to `seenode` |
| `DEBUG` | Yes | `False` | Should be `False` in production |
| `SECRET_KEY` | Yes | - | Django secret key (generate new) |
| `DATABASE_URL` | Auto | - | Auto-set by Seenode when database is linked |
| `ALLOWED_HOSTS` | Yes | - | Your Seenode domain |
| `SEENODE_DOMAIN` | Yes | - | Your Seenode domain (for CSRF) |

## Updating Your Application

To deploy updates:

1. Make changes to your code locally
2. Commit and push to your Git repository:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
3. Seenode will automatically detect the changes and redeploy
4. Monitor the deployment in the **Logs** tab

## Scaling Your Application

As your application grows:

1. **Upgrade Instance Size:** Go to Settings → Change plan
2. **Add More Instances:** Configure horizontal scaling
3. **Optimize Database:** Upgrade to a larger database plan
4. **Add Redis:** For caching and session storage

## Custom Domain (Optional)

To use your own domain:

1. Go to your service settings
2. Click **"Custom Domain"**
3. Follow the instructions to configure DNS
4. Update `ALLOWED_HOSTS` and `SEENODE_DOMAIN` with your custom domain

## Backup and Monitoring

**Database Backups:**
- Seenode provides automatic database backups
- Configure backup frequency in database settings

**Monitoring:**
- Use the Seenode dashboard to monitor:
  - CPU and memory usage
  - Request rates
  - Error rates
  - Response times

## Cost Optimization

**Free Tier:**
- Good for development and testing
- Limited resources and uptime

**Paid Tiers:**
- Production-ready
- Better performance
- 24/7 uptime
- More resources

## Support

If you encounter issues:

1. **Check Logs:** Always start with the Logs tab
2. **Documentation:** Visit [seenode.com/docs](https://seenode.com/docs)
3. **Community:** Join the Seenode Discord or community forums
4. **Support:** Contact Seenode support through the dashboard

## Next Steps

Now that your application is deployed:

- ✅ Set up regular database backups
- ✅ Configure monitoring and alerts
- ✅ Add a custom domain (optional)
- ✅ Set up CI/CD for automated deployments
- ✅ Review security settings
- ✅ Optimize performance

## Comparison: Railway vs Seenode

| Feature | Railway | Seenode |
|---------|---------|---------|
| Port Configuration | Uses PORT env var | Explicit port setting |
| Database Setup | Auto-configured | Link database manually |
| Logging | Can be unclear | Clear, accessible logs |
| Free Tier | 30 days trial | Available |
| Deployment | Git-based | Git-based |
| SSL | Automatic | Automatic |

## Security Checklist

Before going live:

- [ ] `DEBUG` is set to `False`
- [ ] New `SECRET_KEY` generated (not the default)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `CSRF_TRUSTED_ORIGINS` includes your domain
- [ ] Database uses strong password
- [ ] Environment variables are secure
- [ ] HTTPS is enabled (automatic with Seenode)
- [ ] Regular backups configured

## Conclusion

Your Django Expense Tracker is now running on Seenode! The platform provides a straightforward deployment experience with clear configuration and excellent logging.

For more information, visit the [Seenode Documentation](https://seenode.com/docs).

