# 🚀 Quick Deployment Checklist

## Before You Start

- [ ] cPanel login ready: http://mojito.hostns.io:2083/
- [ ] Deployment ZIP created: `easteagle-deployment.zip`
- [ ] Domain confirmed: www.easteagleenergy.com

---

## Step-by-Step Deployment

### ☑️ 1. Upload Files (15 minutes)
- [ ] Login to cPanel
- [ ] Open File Manager
- [ ] Navigate to public_html
- [ ] Upload `easteagle-deployment.zip`
- [ ] Extract ZIP file
- [ ] Rename folder to `easteagle`

### ☑️ 2. Setup Python App (10 minutes)
- [ ] Find "Setup Python App" in cPanel
- [ ] Click "Create Application"
- [ ] Set Python version: 3.9+
- [ ] Set application root: `easteagle`
- [ ] Set startup file: `passenger_wsgi.py`
- [ ] Click Create and wait

### ☑️ 3. Install Dependencies (5 minutes)
- [ ] Open Terminal in cPanel
- [ ] Activate virtual environment
- [ ] Run: `pip install -r requirements.txt`

### ☑️ 4. Configure Settings (10 minutes)
- [ ] Create `.env` file in project root
- [ ] Generate new SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Set ALLOWED_HOSTS
- [ ] Configure email settings

### ☑️ 5. Setup Database (10 minutes)
- [ ] Run: `python manage.py migrate`
- [ ] Run: `python manage.py createsuperuser`
- [ ] Run: `python manage.py seed_products`
- [ ] Run: `python manage.py seed_blog`
- [ ] Run: `python manage.py seed_sidebars`

### ☑️ 6. Collect Static Files (5 minutes)
- [ ] Create directories: `public/static` and `public/media`
- [ ] Run: `python manage.py collectstatic --noinput`

### ☑️ 7. Configure Domain (5 minutes)
- [ ] Verify domain points to project folder
- [ ] Create `.htaccess` file
- [ ] Configure URL rewrites

### ☑️ 8. Restart & Test (5 minutes)
- [ ] Restart Python application
- [ ] Visit: www.easteagleenergy.com
- [ ] Test homepage
- [ ] Test products page
- [ ] Test blog
- [ ] Test search
- [ ] Test contact form
- [ ] Test admin panel

### ☑️ 9. Setup SSL (10 minutes)
- [ ] Go to SSL/TLS Status in cPanel
- [ ] Run AutoSSL for your domain
- [ ] Wait for certificate installation
- [ ] Update .htaccess to force HTTPS

### ☑️ 10. Final Checks (5 minutes)
- [ ] All pages loading correctly
- [ ] Search working
- [ ] Contact form working
- [ ] Admin accessible
- [ ] Mobile responsive
- [ ] No errors in logs

---

## Total Time: ~90 minutes

---

## Quick Commands

```bash
# Activate virtualenv (replace path)
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate

# Navigate to project
cd ~/public_html/easteagle

# Install packages
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load data
python manage.py seed_products
python manage.py seed_blog
python manage.py seed_sidebars

# Collect static
mkdir -p public/static public/media
python manage.py collectstatic --noinput

# Restart app
touch passenger_wsgi.py
```

---

## Files You Need

✅ Already created in your project:
1. `passenger_wsgi.py` - WSGI configuration
2. `settings_production.py` - Production settings
3. `.env.production` - Environment template
4. `requirements_production.txt` - Production packages
5. `CPANEL_DEPLOYMENT_GUIDE.md` - Full guide

---

## Important URLs

- **cPanel:** http://mojito.hostns.io:2083/
- **Your Site:** https://www.easteagleenergy.com
- **Admin:** https://www.easteagleenergy.com/admin/

---

## Troubleshooting

**500 Error?**
```bash
tail -f ~/logs/easteagle-error.log
```

**Static files not loading?**
```bash
python manage.py collectstatic --clear --noinput
chmod -R 755 ~/public_html/easteagle/public/static
```

**Module not found?**
```bash
source /home/yourusername/virtualenv/easteagle/3.9/bin/activate
pip install --force-reinstall -r requirements.txt
```

---

## After Deployment

✅ Your website will be live!
✅ Admin: www.easteagleenergy.com/admin/
✅ 18 products pre-loaded
✅ 6 blog posts pre-loaded
✅ Search functionality working
✅ Contact form ready

---

**Read CPANEL_DEPLOYMENT_GUIDE.md for detailed instructions!**
