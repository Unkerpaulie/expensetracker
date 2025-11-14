# Seenode Interface Guide

This guide shows you exactly how to use the Seenode interface based on the actual UI.

## Understanding the Seenode Interface

Based on your screenshot, the Seenode web service interface has these tabs:

1. **Logs** - View build and runtime logs
2. **Variables** - Set environment variables (this is what you need!)
3. **Domains** - Configure custom domains
4. **Usage** - Monitor resource usage
5. **Settings** - General service settings

## Step-by-Step: Adding Variables

### What You See in Your Screenshot

You already have these variables set:
- ✅ `ENVIRONMENT` = `seenode`
- ✅ `DEBUG` = `False`
- ✅ `SECRET_KEY` = `your-production-secret-key-here`

### What You Need to Add

You need to add **3 more variables**:

1. `DATABASE_URL`
2. `ALLOWED_HOSTS`
3. `SEENODE_DOMAIN`

### How to Add Variables

1. **Click the "Variables" tab** (you're already there in your screenshot)
2. **Click the "+ Add variable" button** (blue button at the bottom)
3. **For each variable:**
   - Enter the **Key** (variable name)
   - Enter the **Value** (variable value)
   - Click **Save** or **Add**

## Variable 1: DATABASE_URL

### Where to Get It

1. **Go to Dashboard** → Click "Dashboard" in the top left
2. **Find your PostgreSQL database** (you should have created one)
3. **Click on the database** to open its details
4. **Look for:**
   - "Connection String"
   - "Connection Details"
   - "Database URL"
   - Or similar section

### What It Looks Like

The connection string format is:
```
postgresql://username:password@host:port/database_name
```

**Real example:**
```
postgresql://expensetracker_user:Kj8mN2pQ9xR4@db-us-east-1.seenode.app:5432/expensetracker_db
```

### Add to Variables Tab

- **Key:** `DATABASE_URL`
- **Value:** `postgresql://username:password@host:port/database_name` (paste your actual string)

## Variable 2: ALLOWED_HOSTS

### What to Use

For your first deployment, you can use a wildcard or your expected domain.

**Option A - Wildcard (easiest for first deploy):**
- **Key:** `ALLOWED_HOSTS`
- **Value:** `*.seenode.app`

**Option B - Specific domain (if you know it):**
- **Key:** `ALLOWED_HOSTS`
- **Value:** `expensetracker.seenode.app` (replace with your actual subdomain)

**Note:** You can update this after your first deployment when you know your exact URL.

## Variable 3: SEENODE_DOMAIN

### What to Use

Same as ALLOWED_HOSTS, but without the wildcard.

**For first deployment:**
- **Key:** `SEENODE_DOMAIN`
- **Value:** `expensetracker.seenode.app` (replace with your expected subdomain)

**Note:** Update this after deployment with your actual domain.

## Your Complete Variables List

After adding all variables, your Variables tab should show:

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | `seenode` |
| `DEBUG` | `False` |
| `SECRET_KEY` | `your-production-secret-key-here` |
| `DATABASE_URL` | `postgresql://user:pass@host:port/db` |
| `ALLOWED_HOSTS` | `*.seenode.app` (or your specific domain) |
| `SEENODE_DOMAIN` | `expensetracker.seenode.app` (or your domain) |

## Finding Your Database Connection String

### Method 1: Database Dashboard

1. Click **"Dashboard"** (top left)
2. Look for your database in the list (should show PostgreSQL icon)
3. Click on the database name
4. Look for a section called:
   - "Connection Details"
   - "Connection String"
   - "Database URL"
   - "Connection Info"

### Method 2: Database Settings

1. Go to your database
2. Click **"Settings"** tab
3. Look for connection information

### What to Copy

Copy the **entire connection string**, including:
- Protocol: `postgresql://`
- Username
- Password (after the `:`)
- Host (after the `@`)
- Port (after the `:`)
- Database name (after the `/`)

**Example:**
```
postgresql://myuser:mypassword@db.seenode.app:5432/mydb
```

## Alternative: Use SQLite (No Database Setup)

If you can't find the database connection string or want to test quickly:

### Option: Skip DATABASE_URL

1. **Don't add** the `DATABASE_URL` variable
2. The app will automatically use SQLite (file-based database)
3. This works for testing but is not recommended for production

**Pros:**
- No database configuration needed
- Works immediately
- Good for quick testing

**Cons:**
- Data stored in container (lost on redeploy)
- Not suitable for production
- Limited performance

## After Adding Variables

### 1. Save Your Changes
Make sure all variables are saved in the Variables tab.

### 2. Commit and Push build.sh Fix
```bash
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### 3. Redeploy
Seenode should automatically redeploy when you push to Git.

### 4. Monitor Logs
1. Click the **"Logs"** tab
2. Watch the deployment process
3. Look for:
   - ✅ "Installing Python dependencies..."
   - ✅ "Collecting static files..."
   - ✅ "Running database migrations..."
   - ✅ "Build completed successfully!"

### 5. Check for Errors
If you see errors in the logs:
- Database connection errors → Check `DATABASE_URL` format
- Build errors → Check `build.sh` permissions
- Import errors → Check `requirements.txt`

## Updating Variables After First Deploy

### Get Your Actual Domain

After your first successful deployment:
1. Look at the top of your web service page
2. You should see your URL (e.g., `expensetracker.seenode.app`)
3. Copy this URL

### Update Domain Variables

1. Go to **Variables** tab
2. Find `ALLOWED_HOSTS` and click to edit
3. Change value to your actual domain: `expensetracker.seenode.app`
4. Find `SEENODE_DOMAIN` and click to edit
5. Change value to your actual domain: `expensetracker.seenode.app`
6. Save changes
7. Seenode will automatically redeploy

## Troubleshooting

### Can't Find Database Connection String

**Try:**
1. Check database dashboard
2. Look in database Settings tab
3. Check database Logs for connection info
4. Contact Seenode support
5. Or use SQLite temporarily (skip DATABASE_URL)

### Variables Not Saving

**Try:**
1. Make sure you click Save/Add after entering each variable
2. Refresh the page to verify they're saved
3. Check for any error messages

### Build Still Failing

**Check:**
1. Logs tab for specific error messages
2. That `build.sh` permissions were committed and pushed
3. That all 6 variables are set correctly
4. That `DATABASE_URL` format is correct

## Quick Reference

### Required Variables (6 total)

1. ✅ `ENVIRONMENT` = `seenode`
2. ✅ `DEBUG` = `False`
3. ✅ `SECRET_KEY` = `<generate-new-key>`
4. ❗ `DATABASE_URL` = `postgresql://user:pass@host:port/db`
5. ❗ `ALLOWED_HOSTS` = `your-domain.seenode.app`
6. ❗ `SEENODE_DOMAIN` = `your-domain.seenode.app`

### Commands to Run

```bash
# 1. Fix build.sh permissions (already done)
git add build.sh
git commit -m "Make build.sh executable"
git push

# 2. Generate SECRET_KEY (if needed)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. After deployment, create superuser (in Seenode console)
python manage.py createsuperuser
```

## Next Steps

1. ✅ Add the 3 missing variables (DATABASE_URL, ALLOWED_HOSTS, SEENODE_DOMAIN)
2. ✅ Commit and push the build.sh fix
3. ✅ Wait for automatic redeploy
4. ✅ Monitor Logs tab
5. ✅ Test your application
6. ✅ Update domain variables with actual URL
7. ✅ Create superuser

Good luck! 🚀

