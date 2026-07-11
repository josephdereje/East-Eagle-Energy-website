# How to Run Your Deployed Website on cPanel

## 🚀 Quick Start - Access Your Website

Once deployed, your website should be accessible at:
- **Main URL:** https://www.easteagleenergy.com
- **Alternative:** http://easteagleenergy.com
- **Admin Panel:** https://www.easteagleenergy.com/admin/

## 🔧 Setup Python Application in cPanel

### Step 1: Login to cPanel
1. Go to: `http://mojito.hostns.io:2083/`
2. Enter your cPanel username and password

### Step 2: Setup Python App
1. In cPanel, find **"Setup Python App"** (under Software section)
2. Click on it

### Step 3: Create New Application
If you haven't created the app yet:

1. Click **"Create Application"**
2. Fill in the form:
   - **Python Version:** 3.9 or higher
   - **Application Root:** `easteagle` (or your folder name)
   - **Application URL:** Choose your domain (easteagleenergy.com)
   - **Application Startup File:** `passenger_wsgi.py`
   - **Application Entry Point:** `application`

3. Click **"Create"**

### Step 4: Configure the Application
After creating:

1. Note the **virtual environment path** (usually `virtualenv`)
2. Copy the activation command shown
3. Click **"Open Terminal"** or go to Terminal separately

### Step 5: Install Dependencies
In the Terminal:

```bash
# Navigate to your project
cd ~/public_html/easteagle

# Activate virtual environment
source virtualenv/bin/activate

# Install requirements
pip install -r requirements.txt

# Or if you have production requirements
pip install -r requirements_production.txt
```

### Step 6: Setup Database
```bash
# Run migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser
# Enter username, email, and password when prompted

# Seed initial data (optional)
python manage.py seed_products
python manage.py seed_blog
python manage.py seed_sidebars
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Create .env File
```bash
nano .env
```

Paste this content (update with your values):
```env
DEBUG=False
DJANGO_SECRET_KEY=GENERATE-NEW-SECRET-KEY-HERE
ALLOWED_HOSTS=easteagleenergy.com,www.easteagleenergy.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@easteagleenergy.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
CONTACT_RECIPIENT_EMAIL=info@easteagleenergy.com
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 9: Restart Application
```bash
touch passenger_wsgi.py
```

Or go back to **"Setup Python App"** and click **"Restart"**

---

## 🌐 Access Your Website

### For Visitors:
- **Homepage:** https://www.easteagleenergy.com
- **Products:** https://www.easteagleenergy.com/products/
- **Blog:** https://www.easteagleenergy.com/blog/
- **Contact:** https://www.easteagleenergy.com/#contact

### For Admin:
- **Admin URL:** https://www.easteagleenergy.com/admin/
- Login with the superuser credentials you created

---

## ✅ Verification Checklist

### 1. Check Application Status
In **"Setup Python App"**:
- Status should show: ✅ **Running**
- No error messages

### 2. Test Website
Visit: https://www.easteagleenergy.com
- Should load homepage
- No 404 or 500 errors

### 3. Check Static Files
- CSS should be loaded (website styled correctly)
- Images should display
- JavaScript should work

### 4. Test Admin Panel
Visit: https://www.easteagleenergy.com/admin/
- Login page should load
- Can login with superuser
- Can see and edit products, blogs, etc.

### 5. Test Features
- Search functionality works
- Product pages load
- Blog posts display
- Contact form submits

---

## 🐛 Troubleshooting

### Issue 1: "502 Bad Gateway" or "Application Not Found"

**Check:**
```bash
cd ~/public_html/easteagle
ls -la passenger_wsgi.py
```

**Fix:**
- Ensure `passenger_wsgi.py` exists
- Check Python App settings in cPanel
- Restart application

### Issue 2: "Application Error" or 500 Error

**Check Logs:**
1. In "Setup Python App" → Click "View Log"
2. Or in Terminal:
```bash
tail -100 ~/logs/error_log
```

**Common fixes:**
```bash
# Ensure dependencies installed
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart
touch passenger_wsgi.py
```

### Issue 3: Static Files Not Loading (No CSS)

**Fix:**
```bash
cd ~/public_html/easteagle
python manage.py collectstatic --noinput
touch passenger_wsgi.py
```

**Check settings:**
- `DEBUG=False` in .env
- `STATIC_ROOT` set correctly
- `.htaccess` configured properly

### Issue 4: "DisallowedHost" Error

**Fix .env:**
```env
ALLOWED_HOSTS=easteagleenergy.com,www.easteagleenergy.com,yourdomain.com
```

Then restart:
```bash
touch passenger_wsgi.py
```

### Issue 5: Database Errors

**Reset database:**
```bash
cd ~/public_html/easteagle
python manage.py migrate --run-syncdb
```

**Or create fresh:**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔄 Common Management Tasks

### Restart Application
```bash
cd ~/public_html/easteagle
touch passenger_wsgi.py
```

### Update Code
```bash
cd ~/public_html/easteagle
git pull origin main  # If using git
touch passenger_wsgi.py
```

### Add New Products/Blog Posts
1. Go to: https://www.easteagleenergy.com/admin/
2. Login with admin credentials
3. Add/edit content
4. No restart needed!

### View Logs
```bash
# Error logs
tail -f ~/logs/error_log

# Application logs (if configured)
tail -f ~/public_html/easteagle/logs/django.log
```

### Run Django Commands
```bash
cd ~/public_html/easteagle
source virtualenv/bin/activate
python manage.py <command>
```

---

## 📋 Quick Command Reference

### Navigate to Project:
```bash
cd ~/public_html/easteagle
```

### Activate Environment:
```bash
source virtualenv/bin/activate
```

### Install/Update Dependencies:
```bash
pip install -r requirements.txt
```

### Database Operations:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Static Files:
```bash
python manage.py collectstatic --noinput
```

### Restart:
```bash
touch passenger_wsgi.py
```

### View Status:
```bash
ps aux | grep python
lsof -i :80
```

---

## 🎯 What You Should See

### When Working:
1. ✅ cPanel Python App status: **Running**
2. ✅ Website loads at: www.easteagleenergy.com
3. ✅ Admin accessible at: www.easteagleenergy.com/admin/
4. ✅ CSS/images display correctly
5. ✅ Search, products, blog all work
6. ✅ No errors in logs

### If Not Working:
1. ❌ Check application status in cPanel
2. ❌ View error logs
3. ❌ Verify .env file exists and correct
4. ❌ Check dependencies installed
5. ❌ Ensure migrations run
6. ❌ Restart application

---

## 📞 Support Commands

### Check Django Configuration:
```bash
cd ~/public_html/easteagle
source virtualenv/bin/activate
python manage.py check
python manage.py check --deploy
```

### Test Database Connection:
```bash
python manage.py dbshell
# Or
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
>>> print("Database connected!")
```

### List All URLs:
```bash
python manage.py show_urls  # If django-extensions installed
# Or
python manage.py shell
>>> from django.urls import get_resolver
>>> print(get_resolver().url_patterns)
```

---

## 🌟 Your Website URLs

### Public Pages:
- Homepage: `/`
- Products: `/products/`
- Residential: `/products/residential/`
- C&I BESS: `/products/c_and_i_bess/`
- Search: `/products/search/`
- Blog: `/blog/`

### Admin Pages:
- Admin: `/admin/`
- Products Admin: `/admin/products/product/`
- Blog Admin: `/admin/blog/blogpost/`
- Homepage Ads: `/admin/blog/homepagead/`
- Sidebar Sections: `/admin/products/productsidebarsection/`

---

## 🎉 Success Indicators

Your website is running correctly when:

1. ✅ No errors in Python App interface
2. ✅ Website loads in browser
3. ✅ Admin panel accessible
4. ✅ Can add/edit products and blogs
5. ✅ Search returns results
6. ✅ Contact form works
7. ✅ All pages styled correctly

---

**Need immediate help?** Check these in order:
1. Python App status in cPanel
2. Error logs: `tail -100 ~/logs/error_log`
3. Restart: `touch ~/public_html/easteagle/passenger_wsgi.py`
4. Test: Visit www.easteagleenergy.com

**Your website should now be live at: https://www.easteagleenergy.com** 🚀
