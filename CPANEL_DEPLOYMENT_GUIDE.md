# East Eagle Energy - cPanel Deployment Guide

## 🚀 Deploying to www.easteagleenergy.com

This guide will walk you through deploying your Django project to cPanel hosting.

---

## 📋 Prerequisites

- ✅ cPanel access: http://mojito.hostns.io:2083/
- ✅ Domain: www.easteagleenergy.com
- ✅ Python 3.8+ support on cPanel
- ✅ SSH access (optional but recommended)
- ✅ FTP/File Manager access

---

## 📦 Step 1: Prepare Deployment Package

### 1.1 Create a ZIP file of your project

```bash
cd "/Users/joseph/Desktop/East Ealge/project/Energy_storage"
zip -r easteagle-deployment.zip East-Eagle-Energy-website/ \
  -x "*.git*" \
  -x "*__pycache__*" \
  -x "*.pyc" \
  -x "*venv/*" \
  -x "*.venv/*" \
  -x "*node_modules/*" \
  -x "*.DS_Store" \
  -x "*db.sqlite3" \
  -x "*.backup"
```

This creates: `easteagle-deployment.zip` (~5-10MB)

---

## 🌐 Step 2: Login to cPanel

1. Go to: http://mojito.hostns.io:2083/
2. Enter your cPanel username and password
3. Click "Log in"

---

## 📁 Step 3: Upload Project Files

### Option A: Using File Manager (Recommended for First Time)

1. **Open File Manager**
   - In cPanel, find "Files" section
   - Click "File Manager"

2. **Navigate to public_html**
   - Click on `public_html` folder
   - This is your web root directory

3. **Upload ZIP File**
   - Click "Upload" button at top
   - Select `easteagle-deployment.zip`
   - Wait for upload to complete (may take 2-5 minutes)

4. **Extract ZIP File**
   - Go back to File Manager
   - Right-click on `easteagle-deployment.zip`
   - Click "Extract"
   - Select destination: `public_html`
   - Click "Extract Files"

5. **Rename Folder**
   - You'll see `East-Eagle-Energy-website` folder
   - Rename it to `easteagle` (shorter, cleaner)
   - Or move all files directly to `public_html`

### Option B: Using FTP (Alternative)

If you prefer FTP:
- Host: mojito.hostns.io
- Username: Your cPanel username
- Port: 21
- Upload to: /public_html/

---

## 🐍 Step 4: Setup Python Application

### 4.1 Create Python App in cPanel

1. **Find "Setup Python App"**
   - In cPanel dashboard
   - Look in "Software" section
   - Click "Setup Python App"

2. **Create Application**
   - Click "Create Application" button

3. **Configure Application:**
   ```
   Python version: 3.9 or 3.10 (choose highest available)
   Application root: easteagle (or path to your project)
   Application URL: / (or leave blank for root domain)
   Application startup file: passenger_wsgi.py
   Application Entry point: application
   ```

4. **Click "Create"**
   - cPanel will create virtual environment
   - Wait for process to complete (1-2 minutes)

### 4.2 Install Dependencies

After Python app is created:

1. **Note the Virtual Environment Path**
   - cPanel shows: `/home/yourusername/virtualenv/easteagle/3.9/bin/activate`
   - Copy this path

2. **Open Terminal in cPanel**
   - Find "Advanced" section
   - Click "Terminal"

3. **Activate Virtual Environment & Install Packages:**

```bash
# Activate virtual environment (use path from cPanel)
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate

# Navigate to project
cd ~/public_html/easteagle

# Install requirements
pip install -r requirements.txt

# If you get errors, try:
pip install --upgrade pip
pip install Django Pillow python-dotenv
```

---

## ⚙️ Step 5: Configure Django Settings

### 5.1 Create Production .env File

In File Manager or Terminal:

```bash
cd ~/public_html/easteagle
nano .env
```

Add these lines (replace with your actual values):

```env
DEBUG=False
DJANGO_SECRET_KEY=your-super-secret-key-here-change-this
ALLOWED_HOSTS=easteagleenergy.com,www.easteagleenergy.com

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@easteagleenergy.com
EMAIL_HOST_PASSWORD=your-email-app-password
CONTACT_RECIPIENT_EMAIL=info@easteagleenergy.com
```

**Generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5.2 Update passenger_wsgi.py

Make sure `passenger_wsgi.py` is in your project root:

```python
import os
import sys

# Add project directory
sys.path.insert(0, os.path.dirname(__file__))

# Set environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'east_eagle_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🗄️ Step 6: Setup Database

### 6.1 Run Migrations

```bash
cd ~/public_html/easteagle
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate

python manage.py migrate
```

### 6.2 Create Superuser

```bash
python manage.py createsuperuser
```

Enter:
- Username: admin
- Email: info@easteagleenergy.com
- Password: (choose a strong password)

### 6.3 Load Sample Data

```bash
# Seed products
python manage.py seed_products

# Seed blog posts
python manage.py seed_blog

# Seed sidebars
python manage.py seed_sidebars
```

---

## 🎨 Step 7: Collect Static Files

Django needs to collect all CSS, JS, images into one location:

```bash
cd ~/public_html/easteagle
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate

# Create static directory
mkdir -p public/static
mkdir -p public/media

# Collect static files
python manage.py collectstatic --noinput
```

---

## 🌍 Step 8: Configure Domain

### 8.1 Point Domain to Application

1. **In cPanel, go to "Domains"**
2. **Find easteagleenergy.com**
3. **Ensure it points to: `/public_html/easteagle`**

### 8.2 Create .htaccess File

In your project root (`~/public_html/easteagle`), create `.htaccess`:

```apache
RewriteEngine On
RewriteBase /

# Serve static files directly
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule ^(.*)$ public/static/$1 [L]

RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^(.*)$ public/media/$1 [L]

# Pass everything else to Django
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L]
```

---

## 🔄 Step 9: Restart Application

### In cPanel Python App Interface:

1. Go to "Setup Python App"
2. Find your application
3. Click "Restart" button
4. Wait for green checkmark

### Or via Terminal:

```bash
cd ~/public_html/easteagle
touch passenger_wsgi.py
# Touching the file triggers restart
```

---

## ✅ Step 10: Test Your Website

1. **Visit:** https://www.easteagleenergy.com
2. **Check pages:**
   - Homepage: https://www.easteagleenergy.com/
   - Products: https://www.easteagleenergy.com/products/
   - Blog: https://www.easteagleenergy.com/blog/
   - Admin: https://www.easteagleenergy.com/admin/

3. **Test functionality:**
   - Search feature
   - Product categories
   - Contact form
   - Blog posts

---

## 🔐 Step 11: Secure Your Site (Important!)

### 11.1 Setup SSL Certificate (FREE)

1. **In cPanel, go to "SSL/TLS Status"**
2. **Select your domain: easteagleenergy.com**
3. **Click "Run AutoSSL"**
4. **Wait 2-5 minutes for certificate installation**

### 11.2 Force HTTPS (After SSL is installed)

Update `.htaccess`:

```apache
RewriteEngine On
RewriteBase /

# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Static files
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule ^(.*)$ public/static/$1 [L]

RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^(.*)$ public/media/$1 [L]

# Django
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L]
```

Update `.env`:
```env
DEBUG=False
# After SSL is active, set these to True:
# SECURE_SSL_REDIRECT=True
# SESSION_COOKIE_SECURE=True
# CSRF_COOKIE_SECURE=True
```

---

## 📧 Step 12: Configure Email

### Option A: Use cPanel Email

1. **Create email account in cPanel:**
   - Go to "Email Accounts"
   - Create: info@easteagleenergy.com

2. **Update .env:**
```env
EMAIL_HOST=mail.easteagleenergy.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@easteagleenergy.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Option B: Use Gmail (Easier for testing)

1. **Enable 2-Factor Auth on Gmail**
2. **Generate App Password**
3. **Use in .env** (as shown earlier)

---

## 🐛 Troubleshooting

### Issue: "500 Internal Server Error"

**Check Error Logs:**
```bash
tail -f ~/logs/easteagle-error.log
```

**Common fixes:**
```bash
# Fix permissions
chmod 755 ~/public_html/easteagle
chmod 644 ~/public_html/easteagle/passenger_wsgi.py

# Check Python path
which python

# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

### Issue: "Static files not loading"

```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Check permissions
chmod -R 755 ~/public_html/easteagle/public/static
```

### Issue: "Database locked"

```bash
# Set proper permissions
chmod 664 ~/public_html/easteagle/db.sqlite3
chmod 775 ~/public_html/easteagle
```

### Issue: "Module not found"

```bash
# Activate venv first
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate

# Then install
pip install Django Pillow python-dotenv
```

---

## 📱 Step 13: Update Contact Information

Update these files with your actual email:

1. **Admin user email:** (already set during superuser creation)
2. **Contact form recipient:** (set in .env)
3. **Footer email:** templates/includes/footer.html
4. **Header phone:** templates/includes/header.html

---

## 🔄 Making Updates

When you make changes locally:

1. **Test locally first**
2. **Commit to git:**
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

3. **Update on server:**
   ```bash
   # SSH into server
   cd ~/public_html/easteagle
   git pull origin main
   
   # If no git, re-upload changed files via FTP/File Manager
   
   # Collect static if CSS/JS changed
   python manage.py collectstatic --noinput
   
   # Restart app
   touch passenger_wsgi.py
   ```

---

## 📊 Monitoring

### Check Website Status:
- Uptime monitoring: Use services like UptimeRobot (free)
- Error monitoring: Check cPanel error logs regularly

### View Logs:
```bash
# Error log
tail -f ~/logs/easteagle-error.log

# Access log
tail -f ~/logs/easteagle-access.log
```

---

## 🎯 Quick Commands Reference

```bash
# Activate virtual environment
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate

# Navigate to project
cd ~/public_html/easteagle

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Restart application
touch passenger_wsgi.py

# View error logs
tail -f ~/logs/easteagle-error.log
```

---

## 📞 Need Help?

### cPanel Support:
- Contact your hosting provider
- Most shared hosting includes email support

### Django Issues:
- Check Django documentation
- Review error logs in cPanel

### Database Issues:
- Backup db.sqlite3 regularly
- Consider upgrading to MySQL for production (available in cPanel)

---

## ✅ Deployment Checklist

Before going live:

- [ ] Files uploaded to cPanel
- [ ] Python app created and configured
- [ ] Dependencies installed
- [ ] .env file created with production settings
- [ ] Database migrated
- [ ] Superuser created
- [ ] Sample data loaded
- [ ] Static files collected
- [ ] Domain configured
- [ ] .htaccess created
- [ ] Application restarted
- [ ] Website accessible
- [ ] All pages working
- [ ] Search working
- [ ] Contact form working
- [ ] Admin panel accessible
- [ ] SSL certificate installed
- [ ] HTTPS forced
- [ ] Email configured
- [ ] Error logs checked
- [ ] Performance tested
- [ ] Mobile responsive checked
- [ ] Backup created

---

## 🚀 Your Website is Live!

After completing all steps, your website will be live at:

**Public Site:**
- https://www.easteagleenergy.com

**Admin Panel:**
- https://www.easteagleenergy.com/admin/
- Username: admin
- Password: (what you set)

**Management:**
- Products: Add/edit via admin
- Blog: Write new posts via admin
- Ads: Update banners via admin

---

## 🔄 Post-Deployment

### Regular Maintenance:

1. **Weekly:**
   - Check error logs
   - Test contact form
   - Verify search working

2. **Monthly:**
   - Update blog with new content
   - Add new products
   - Update homepage ads
   - Check SSL certificate status

3. **As Needed:**
   - Update Django version
   - Add new features
   - Backup database

---

**East Eagle Energy** — *Energy That Never Grows Weary*

🌐 Now live at www.easteagleenergy.com!
