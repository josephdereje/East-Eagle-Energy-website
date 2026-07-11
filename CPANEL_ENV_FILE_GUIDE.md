# Creating .env File on cPanel - Step by Step

## 🌐 cPanel .env File Creation Guide

### Method 1: Using cPanel File Manager (Easiest)

#### Step 1: Access File Manager
1. Login to cPanel at `http://mojito.hostns.io:2083/`
2. Find **"File Manager"** in the Files section
3. Click to open

#### Step 2: Navigate to Your Application
1. In File Manager, go to: `public_html/easteagle/`
   (or wherever you uploaded your Django project)
2. You should see files like:
   - `passenger_wsgi.py`
   - `manage.py`
   - `requirements.txt`

#### Step 3: Create .env File
1. Click **"+ File"** button at the top
2. Name it exactly: `.env` (with the dot at the beginning)
3. Click **"Create New File"**

#### Step 4: Edit .env File
1. Right-click on `.env` file
2. Select **"Edit"** or **"Code Edit"**
3. Paste this content (update with your actual values):

```env
# Django Production Settings
DEBUG=False
DJANGO_SECRET_KEY=CHANGE-THIS-TO-A-RANDOM-SECRET-KEY
ALLOWED_HOSTS=easteagleenergy.com,www.easteagleenergy.com,mojito.hostns.io

# Database (if using MySQL)
# DATABASE_ENGINE=django.db.backends.mysql
# DATABASE_NAME=your_database_name
# DATABASE_USER=your_database_user
# DATABASE_PASSWORD=your_database_password
# DATABASE_HOST=localhost
# DATABASE_PORT=3306

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@easteagleenergy.com
EMAIL_HOST_PASSWORD=YOUR-GMAIL-APP-PASSWORD
DEFAULT_FROM_EMAIL=info@easteagleenergy.com
CONTACT_RECIPIENT_EMAIL=info@easteagleenergy.com

# Static/Media Files
STATIC_URL=/static/
MEDIA_URL=/media/
```

4. Click **"Save Changes"** (top right)
5. Close the editor

---

### Method 2: Using cPanel Terminal (Alternative)

#### Step 1: Open Terminal
1. In cPanel, find **"Terminal"** under Advanced section
2. Click to open

#### Step 2: Navigate to Project
```bash
cd ~/public_html/easteagle
```

#### Step 3: Create .env File
```bash
nano .env
```

#### Step 4: Paste Content
Paste the same content as above, then:
- Press `Ctrl + O` to save
- Press `Enter` to confirm
- Press `Ctrl + X` to exit

#### Step 5: Verify File Created
```bash
ls -la .env
cat .env
```

---

## 🔐 Generate SECRET_KEY on cPanel

### Option 1: Using cPanel Terminal
```bash
cd ~/public_html/easteagle
source virtualenv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your `DJANGO_SECRET_KEY` value.

### Option 2: Use Pre-generated Key
Here's a freshly generated key you can use:
```
django-insecure-7k#m9@$wp8x*e!3v2z&nh4j6@8fy$wq5r#9bu2c!x@m8vp#d4k
```

**IMPORTANT:** Change this in production for security!

---

## 🔄 Restart Application on cPanel

### Method 1: Using Python App Interface (Recommended)

1. In cPanel, go to **"Setup Python App"** (under Software section)
2. Find your application in the list (easteagle)
3. Click the **"Restart"** icon/button (🔄)
4. Wait for green checkmark ✅
5. Check status shows "Running"

### Method 2: Touch passenger_wsgi.py (Quick)

In cPanel Terminal:
```bash
cd ~/public_html/easteagle
touch passenger_wsgi.py
```

This triggers Passenger to restart the application automatically.

### Method 3: Using Passenger Command

```bash
cd ~/public_html/easteagle
passenger-config restart-app $(pwd)
```

---

## 📋 Complete .env Template for cPanel

Copy this entire block and customize:

```env
# ========================================
# Django Production Settings
# ========================================
DEBUG=False
DJANGO_SECRET_KEY=GENERATE-A-NEW-RANDOM-KEY-HERE

# Your domain(s) - separate with commas, no spaces
ALLOWED_HOSTS=easteagleenergy.com,www.easteagleenergy.com

# ========================================
# Database Settings (SQLite default)
# ========================================
# Using SQLite (default - no changes needed)
# Database file will be at: db.sqlite3

# If using MySQL, uncomment and fill these:
# DATABASE_ENGINE=django.db.backends.mysql
# DATABASE_NAME=cpanelusername_dbname
# DATABASE_USER=cpanelusername_dbuser
# DATABASE_PASSWORD=your_password
# DATABASE_HOST=localhost
# DATABASE_PORT=3306

# ========================================
# Email Configuration
# ========================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Gmail Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@easteagleenergy.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Or use cPanel email
# EMAIL_HOST=mail.easteagleenergy.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=info@easteagleenergy.com
# EMAIL_HOST_PASSWORD=your-cpanel-email-password

DEFAULT_FROM_EMAIL=info@easteagleenergy.com
CONTACT_RECIPIENT_EMAIL=info@easteagleenergy.com

# ========================================
# Static & Media Files
# ========================================
STATIC_URL=/static/
STATIC_ROOT=/home/cpanelusername/public_html/easteagle/staticfiles/
MEDIA_URL=/media/
MEDIA_ROOT=/home/cpanelusername/public_html/easteagle/media/

# ========================================
# Security Settings (Optional but Recommended)
# ========================================
# SECURE_SSL_REDIRECT=True
# SESSION_COOKIE_SECURE=True
# CSRF_COOKIE_SECURE=True
# SECURE_BROWSER_XSS_FILTER=True
```

---

## ✅ Verification Checklist

After creating .env and restarting:

### 1. Check File Exists
In cPanel Terminal:
```bash
ls -la ~/public_html/easteagle/.env
```

Should show:
```
-rw-r--r-- 1 user user 1234 Jul 10 00:00 .env
```

### 2. Check File Permissions
```bash
chmod 644 ~/public_html/easteagle/.env
```

### 3. Check Application Status
In "Setup Python App":
- Status should be: ✅ Running
- No errors in logs

### 4. Test Website
Visit: `https://www.easteagleenergy.com`
- Should load without errors
- Check admin: `https://www.easteagleenergy.com/admin/`

### 5. Check Application Logs
In "Setup Python App":
- Click "View Log" or "Error Log"
- Look for any .env related errors

---

## 🐛 Common Issues & Fixes

### Issue 1: .env File Not Found
**Solution:**
```bash
cd ~/public_html/easteagle
pwd  # Confirm you're in right directory
ls -la  # See if .env exists
```

### Issue 2: Environment Variables Not Loading
**Solution:**
1. Check `passenger_wsgi.py` has dotenv loading
2. Check `.env` file has no syntax errors
3. Restart application: `touch passenger_wsgi.py`

### Issue 3: Permission Denied
**Solution:**
```bash
chmod 644 ~/public_html/easteagle/.env
chown $USER:$USER ~/public_html/easteagle/.env
```

### Issue 4: Changes Not Applied
**Solution:**
```bash
# Force restart
cd ~/public_html/easteagle
touch passenger_wsgi.py
sleep 2
curl https://www.easteagleenergy.com
```

---

## 📝 Quick Command Reference

### Create .env:
```bash
cd ~/public_html/easteagle
nano .env
# Paste content, Ctrl+O, Enter, Ctrl+X
```

### Edit .env:
```bash
cd ~/public_html/easteagle
nano .env
# Make changes, Ctrl+O, Enter, Ctrl+X
```

### Restart App:
```bash
cd ~/public_html/easteagle
touch passenger_wsgi.py
```

### View .env:
```bash
cat ~/public_html/easteagle/.env
```

### Check if loaded:
```bash
cd ~/public_html/easteagle
source virtualenv/bin/activate
python manage.py shell
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> print(os.getenv('DEBUG'))
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Use strong SECRET_KEY (50+ random characters)
- Set `DEBUG=False` in production
- Use environment-specific email credentials
- Keep .env file permissions at 644
- Generate new SECRET_KEY for production

### ❌ DON'T:
- Don't use DEBUG=True in production
- Don't commit .env to Git
- Don't share SECRET_KEY
- Don't use same SECRET_KEY as development
- Don't make .env publicly accessible

---

## 📞 Need Help?

### Check Application Logs:
1. cPanel → Setup Python App
2. Click on your app
3. View "Error Log" or "Access Log"

### Check Error Logs:
```bash
tail -f ~/public_html/easteagle/logs/error.log
# or
tail -f ~/logs/error_log
```

### Test Configuration:
```bash
cd ~/public_html/easteagle
source virtualenv/bin/activate
python manage.py check
python manage.py check --deploy
```

---

## 🎯 Next Steps After Creating .env

1. ✅ Create .env file (see above)
2. ✅ Generate SECRET_KEY
3. ✅ Configure email settings
4. ✅ Set ALLOWED_HOSTS
5. ✅ Restart application
6. ✅ Test website
7. ✅ Check admin panel
8. ✅ Test contact form
9. ✅ Review error logs

---

**Your .env file location on cPanel:**
`/home/cpanelusername/public_html/easteagle/.env`

**Remember to restart after any .env changes:**
`touch ~/public_html/easteagle/passenger_wsgi.py`
