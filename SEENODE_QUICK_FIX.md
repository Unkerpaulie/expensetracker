# Seenode Quick Fix Guide

## Issue 1: Build Script Permissions ✅ FIXED

**Problem:** `build.sh` doesn't have execute permissions

**Solution:**
```bash
git update-index --chmod=+x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

This has been done! Just commit and push the change.

---

## Issue 2: Database Connection

**Problem:** Seenode interface doesn't have "Environment" tab or "Link Database" button

**Solution:** Manually add `DATABASE_URL` in the **Variables** tab

### Step-by-Step:

#### 1. Get Your Database Connection URL

1. In Seenode dashboard, go to your **PostgreSQL database**
2. Look for **Connection Details**, **Connection String**, or **Database URL**
3. Copy the full connection string, which looks like:
   ```
   postgresql://username:password@host:port/database_name
   ```
   
   Example:
   ```
   postgresql://expensetracker_user:abc123xyz@db.seenode.app:5432/expensetracker_db
   ```

#### 2. Add DATABASE_URL to Variables Tab

1. Go to your **Web Service** (expensetracker)
2. Click the **Variables** tab (you can see it in your screenshot)
3. Click **"+ Add variable"** button
4. Add:
   - **Key:** `DATABASE_URL`
   - **Value:** `postgresql://username:password@host:port/database_name` (paste your actual connection string)
5. Click Save

#### 3. Your Complete Variables List Should Be:

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | `seenode` |
| `DEBUG` | `False` |
| `SECRET_KEY` | `your-production-secret-key-here` |
| `DATABASE_URL` | `postgresql://user:pass@host:port/db` |
| `ALLOWED_HOSTS` | `your-app.seenode.app` |
| `SEENODE_DOMAIN` | `your-app.seenode.app` |

**Note:** For `ALLOWED_HOSTS` and `SEENODE_DOMAIN`, you can use placeholder values initially, then update them after your first deployment when you know your actual domain.

---

## Alternative: Use SQLite (No Database Setup Needed)

If you're having trouble with PostgreSQL, you can temporarily use SQLite:

### Option A: Remove DATABASE_URL Variable

1. In the **Variables** tab, **don't add** `DATABASE_URL`
2. The app will automatically use SQLite (file-based database)
3. This is fine for testing, but not recommended for production

**Pros:**
- No database setup needed
- Works immediately
- Good for testing

**Cons:**
- Data stored in container (can be lost on redeploy)
- Not suitable for production
- Limited scalability

### Option B: Keep PostgreSQL (Recommended)

Follow the steps above to add `DATABASE_URL` manually.

---

## Build Configuration

Make sure your Seenode web service has these settings:

### In Settings Tab:

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn expensetracker.wsgi --bind 0.0.0.0:80
```

**Port:**
```
80
```

---

## Deployment Checklist

- [x] Make `build.sh` executable (done via git command)
- [ ] Commit and push the permission change
- [ ] Get PostgreSQL connection URL from database dashboard
- [ ] Add `DATABASE_URL` to Variables tab
- [ ] Verify all 6 variables are set (see table above)
- [ ] Redeploy your application
- [ ] Check Logs tab for any errors
- [ ] Update `ALLOWED_HOSTS` and `SEENODE_DOMAIN` after first deploy

---

## Quick Commands

### 1. Commit the build.sh fix:
```bash
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### 2. Generate a new SECRET_KEY (if needed):
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. After deployment, create superuser:
In Seenode console/shell:
```bash
python manage.py createsuperuser
```

---

## Troubleshooting

### If build still fails after fixing permissions:

**Check Logs tab for:**
- Python version issues
- Missing dependencies
- Database connection errors

**Common fixes:**
- Ensure all packages in `requirements.txt`
- Verify `DATABASE_URL` is correct
- Check that database is running

### If you see "No DATABASE_URL" warning:

**Two options:**
1. Add `DATABASE_URL` variable (recommended)
2. Let it use SQLite (temporary solution)

### If you get database connection errors:

**Verify:**
- Database is created and running in Seenode
- `DATABASE_URL` format is correct
- Username and password are correct
- Host and port are correct
- Database name matches

---

## Next Steps After Fixing

1. **Commit and push** the build.sh permission fix
2. **Add DATABASE_URL** to Variables tab
3. **Redeploy** (Seenode will auto-redeploy on git push)
4. **Monitor Logs** tab during deployment
5. **Test your app** at your Seenode URL
6. **Create superuser** via console
7. **Update domain variables** with actual URL

---

## Summary of Changes

### What Was Fixed:
1. ✅ `build.sh` now has execute permissions
2. ✅ Documentation updated to reflect actual Seenode interface
3. ✅ Clear instructions for manual `DATABASE_URL` setup

### What You Need to Do:
1. Commit and push the build.sh change
2. Get your PostgreSQL connection URL
3. Add `DATABASE_URL` to Variables tab in Seenode
4. Redeploy and test

Good luck! 🚀

