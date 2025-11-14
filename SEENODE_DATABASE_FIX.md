# Seenode Database Connection Fix

Great progress! The build worked and deployment succeeded. Now we just need to connect to the database.

## Your Database Connection Parameters

From your screenshot:
```
database = db_4qfhw4met0rd
username = db_4qfhw4met0rd
password = ************************ (click "show password" to reveal)
host = up-de-fra1-postgresql-1.db.run-on-seenode.com
port = 11550
```

## Solution 1: Use DATABASE_URL (Recommended - Try This First!)

Your settings.py is already configured to use `DATABASE_URL`. You just need to construct it from your parameters.

### Step 1: Get Your Password

1. In the Seenode database connection screen (your screenshot)
2. Click **"show password"** (blue link next to the asterisks)
3. Copy the revealed password

### Step 2: Construct DATABASE_URL

Format:
```
postgresql://username:password@host:port/database
```

Using your parameters:
```
postgresql://db_4qfhw4met0rd:YOUR_ACTUAL_PASSWORD@up-de-fra1-postgresql-1.db.run-on-seenode.com:11550/db_4qfhw4met0rd
```

**Replace `YOUR_ACTUAL_PASSWORD` with the password you revealed in Step 1.**

### Step 3: Add to Seenode Variables

1. Go to your web service → **Variables** tab
2. Find `DATABASE_URL` (if you already added it, edit it; if not, add it)
3. Set the value to your constructed URL from Step 2
4. Save

### Step 4: Redeploy

Seenode should automatically redeploy. Monitor the **Logs** tab.

---

## Solution 2: Use Individual Parameters (Alternative)

If Solution 1 doesn't work, I've updated settings.py to support individual database parameters.

### Add These Variables in Seenode

Go to **Variables** tab and add:

| Key | Value |
|-----|-------|
| `DB_NAME` | `db_4qfhw4met0rd` |
| `DB_USER` | `db_4qfhw4met0rd` |
| `DB_PASSWORD` | `YOUR_ACTUAL_PASSWORD` (click "show password" to get it) |
| `DB_HOST` | `up-de-fra1-postgresql-1.db.run-on-seenode.com` |
| `DB_PORT` | `11550` |

**Important:** If you use this method, **remove** the `DATABASE_URL` variable (or leave it empty).

The settings.py will automatically use individual parameters if `DATABASE_URL` is not set.

---

## Which Solution to Use?

### Try Solution 1 First (DATABASE_URL)

**Pros:**
- Already configured in settings.py
- Standard Django practice
- Single variable to manage
- Works with dj-database-url

**Cons:**
- Need to construct the URL correctly
- Password must be URL-encoded if it contains special characters

### Use Solution 2 If Solution 1 Fails

**Pros:**
- Easier to manage individual values
- No URL encoding needed
- Clear separation of parameters

**Cons:**
- More variables to manage
- Less standard approach

---

## Special Characters in Password

If your password contains special characters (like `@`, `:`, `/`, `?`, `#`, `[`, `]`), you need to URL-encode them for Solution 1.

### Common URL Encodings:
- `@` → `%40`
- `:` → `%3A`
- `/` → `%2F`
- `?` → `%3F`
- `#` → `%23`
- `[` → `%5B`
- `]` → `%5D`
- `%` → `%25`
- Space → `%20`

**Example:**
If password is `Pass@word:123`, use `Pass%40word%3A123` in the DATABASE_URL.

**Or just use Solution 2** to avoid URL encoding!

---

## Testing the Connection

### After Adding Variables

1. **Commit and push** (if you haven't already):
   ```bash
   git add expensetracker/settings.py
   git commit -m "Add fallback for individual database parameters"
   git push
   ```

2. **Monitor Logs** tab in Seenode

3. **Look for:**
   - ✅ "Running database migrations..."
   - ✅ "Operations to perform:"
   - ✅ "Applying migrations..."
   - ✅ No database connection errors

### If You See Database Errors

**Check:**
- Password is correct (click "show password" to verify)
- All parameters are copied exactly (no extra spaces)
- Port is `11550` (not `5432`)
- Host is the full domain
- If using DATABASE_URL, check for special characters in password

---

## Quick Reference

### Solution 1: DATABASE_URL

**Single variable in Seenode Variables tab:**

```
DATABASE_URL=postgresql://db_4qfhw4met0rd:YOUR_PASSWORD@up-de-fra1-postgresql-1.db.run-on-seenode.com:11550/db_4qfhw4met0rd
```

### Solution 2: Individual Parameters

**Five variables in Seenode Variables tab:**

```
DB_NAME=db_4qfhw4met0rd
DB_USER=db_4qfhw4met0rd
DB_PASSWORD=YOUR_PASSWORD
DB_HOST=up-de-fra1-postgresql-1.db.run-on-seenode.com
DB_PORT=11550
```

---

## Complete Variables List

After adding database connection, your Variables tab should have:

### Using Solution 1 (DATABASE_URL):
1. `ENVIRONMENT` = `seenode`
2. `DEBUG` = `False`
3. `SECRET_KEY` = `your-secret-key`
4. `DATABASE_URL` = `postgresql://db_4qfhw4met0rd:PASSWORD@up-de-fra1-postgresql-1.db.run-on-seenode.com:11550/db_4qfhw4met0rd`
5. `ALLOWED_HOSTS` = `your-domain.seenode.app`
6. `SEENODE_DOMAIN` = `your-domain.seenode.app`

### Using Solution 2 (Individual Parameters):
1. `ENVIRONMENT` = `seenode`
2. `DEBUG` = `False`
3. `SECRET_KEY` = `your-secret-key`
4. `DB_NAME` = `db_4qfhw4met0rd`
5. `DB_USER` = `db_4qfhw4met0rd`
6. `DB_PASSWORD` = `your-password`
7. `DB_HOST` = `up-de-fra1-postgresql-1.db.run-on-seenode.com`
8. `DB_PORT` = `11550`
9. `ALLOWED_HOSTS` = `your-domain.seenode.app`
10. `SEENODE_DOMAIN` = `your-domain.seenode.app`

---

## Troubleshooting

### "Could not connect to server"

**Check:**
- Database is running (green dot in Seenode)
- Host and port are correct
- Password is correct (no typos)

### "password authentication failed"

**Check:**
- Password is exactly as shown (click "show password")
- No extra spaces before/after password
- If using DATABASE_URL, check for special characters that need encoding

### "SSL connection required"

**Don't worry:** Settings.py is already configured with `sslmode: require` for Seenode.

### "database does not exist"

**Check:**
- Database name is `db_4qfhw4met0rd` (matches username)
- No typos in database name

---

## Next Steps After Database Connects

1. ✅ Verify migrations run successfully (check Logs)
2. ✅ Access your application URL
3. ✅ Create superuser via Seenode console:
   ```bash
   python manage.py createsuperuser
   ```
4. ✅ Test login and functionality
5. ✅ Update `ALLOWED_HOSTS` and `SEENODE_DOMAIN` with actual domain

---

## Summary

**Recommended Approach:**

1. Click "show password" in Seenode database screen
2. Construct DATABASE_URL: `postgresql://db_4qfhw4met0rd:PASSWORD@up-de-fra1-postgresql-1.db.run-on-seenode.com:11550/db_4qfhw4met0rd`
3. Add/update `DATABASE_URL` variable in Seenode Variables tab
4. Commit and push the updated settings.py
5. Monitor Logs for successful migration
6. Create superuser and test!

You're almost there! 🚀

