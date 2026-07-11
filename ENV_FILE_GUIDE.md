# How to Create .env File and Restart Django

## ✅ .env File Created!

Your `.env` file has been created at:
`/Users/joseph/Desktop/East Ealge/project/Energy_storage/East-Eagle-Energy-website/.env`

---

## 📝 What's in Your .env File

```env
# Django Settings
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 🔄 How to Restart Django Application

### Option 1: Using Terminal Commands

```bash
# Navigate to your project
cd "/Users/joseph/Desktop/East Ealge/project/Energy_storage/East-Eagle-Energy-website"

# Activate virtual environment
source .venv/bin/activate

# Stop any running server (if exists)
# Press Ctrl+C in the terminal where server is running

# Or kill by port
lsof -ti:8000 | xargs kill -9

# Start the server
python manage.py runserver
```

### Option 2: Quick Restart Script

Save this as `restart.sh`:

```bash
#!/bin/bash
cd "/Users/joseph/Desktop/East Ealge/project/Energy_storage/East-Eagle-Energy-website"
source .venv/bin/activate
lsof -ti:8000 | xargs kill -9 2>/dev/null
python manage.py runserver
```

Make executable and run:
```bash
chmod +x restart.sh
./restart.sh
```

### Option 3: Using Cursor Terminal

1. Open Terminal in Cursor (Ctrl+` or Cmd+`)
2. Run these commands:
```bash
cd "/Users/joseph/Desktop/East Ealge/project/Energy_storage/East-Eagle-Energy-website"
source .venv/bin/activate
python manage.py runserver
```

---

## 🔧 Editing .env File

### Method 1: In Cursor/VS Code
1. Open the file: `.env`
2. Edit values
3. Save (Cmd+S or Ctrl+S)
4. Restart server

### Method 2: Using Terminal
```bash
nano .env
# Or
code .env
```

### Method 3: Using File Manager
1. Navigate to project folder
2. Show hidden files (Cmd+Shift+. on Mac)
3. Open `.env` in text editor
4. Edit and save

---

## 📋 Common .env Variables

### Development (Local)

```env
DEBUG=True
DJANGO_SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# Console email (prints in terminal)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production (cPanel)

```env
DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key-change-this
ALLOWED_HOSTS=easteagleenergy.com,www.easteagleenergy.com

# Real email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@easteagleenergy.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_RECIPIENT_EMAIL=info@easteagleenergy.com
```

---

## 🔐 Generating Secret Key

### Method 1: Using Django
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Method 2: Using Python
```python
import secrets
print(secrets.token_urlsafe(50))
```

---

## ✅ Verify .env is Working

### Check if variables load:

```bash
python manage.py shell
```

Then in Python shell:
```python
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('DEBUG'))
print(os.getenv('DJANGO_SECRET_KEY'))
```

---

## 🚫 Important: .env Security

### ✅ DO:
- Keep `.env` file local only
- Never commit to Git (already in .gitignore)
- Use different values for development and production
- Generate unique SECRET_KEY for production

### ❌ DON'T:
- Don't share .env file
- Don't commit to GitHub
- Don't use same SECRET_KEY in production
- Don't leave DEBUG=True in production

---

## 🔄 When to Restart Server

Restart Django after changing:
- ✅ .env file values
- ✅ settings.py
- ✅ models.py
- ✅ urls.py
- ✅ Installing new packages

No restart needed for:
- ❌ Template changes (HTML)
- ❌ Static files (CSS, JS)
- ❌ Database data changes

---

## 📊 Server Status Commands

### Check if server is running:
```bash
lsof -i:8000
```

### Check server response:
```bash
curl http://127.0.0.1:8000/
```

### Stop server:
```bash
# In terminal where server runs
Ctrl+C

# Or by port
lsof -ti:8000 | xargs kill -9
```

### View server logs:
```bash
# Server logs appear in terminal where you ran runserver
```

---

## 🌐 cPanel Restart (for Production)

When deployed to cPanel:

### Method 1: Touch passenger_wsgi.py
```bash
cd ~/public_html/easteagle
touch passenger_wsgi.py
```

### Method 2: cPanel Python App Interface
1. Login to cPanel
2. Go to "Setup Python App"
3. Find your application
4. Click "Restart" button

### Method 3: Via Terminal
```bash
# Restart through passenger
passenger-config restart-app ~/public_html/easteagle
```

---

## 🐛 Troubleshooting

### Server won't start:
```bash
# Check for port conflicts
lsof -i:8000

# Kill conflicting process
kill -9 <PID>

# Try different port
python manage.py runserver 8001
```

### .env not loading:
```bash
# Check file exists
ls -la .env

# Check python-dotenv installed
pip list | grep dotenv

# If not installed
pip install python-dotenv
```

### Changes not applying:
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Restart server
python manage.py runserver
```

---

## 📝 Quick Reference

### Restart Django (Development):
```bash
# Stop: Ctrl+C
# Start: python manage.py runserver
```

### Restart Django (Production cPanel):
```bash
touch passenger_wsgi.py
```

### Edit .env:
```bash
nano .env
# or open in Cursor
```

### Check .env loaded:
```bash
python manage.py shell
>>> import os
>>> os.getenv('DEBUG')
```

---

## ✅ Current Status

Your server is running at:
- **Local:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

.env file is:
- ✅ Created
- ✅ Configured for development
- ✅ Protected (in .gitignore)
- ✅ Ready to use

---

**Need to update .env?** Just edit the file and restart the server!
