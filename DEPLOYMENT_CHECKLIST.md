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
- [ ] Rename folder to `east_eagle`

### ☑️ 2. Setup Python App (10 minutes)
- [ ] Find "Setup Python App" in cPanel
- [ ] Click "Create Application"
- [ ] Set Python version: 3.9+
- [ ] Set application root: `public_html/east_eagle`
- [ ] Set application URL: `/`
- [ ] Set startup file: `passenger_wsgi.py`
- [ ] Set entry point: `application`
- [ ] Click Create and wait

### ☑️ 3. Install Dependencies (5 minutes)
- [ ] Open Terminal in cPanel
- [ ] Activate virtual environment (see Quick Commands below)
- [ ] Run: `pip install Django Pillow python-dotenv`

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
- [ ] Domain root stays as `public_html` (normal for main domain)
- [ ] Python App root must be `public_html/east_eagle`
- [ ] Do NOT create a custom `.htaccess` file

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

## Quick Commands (your cPanel paths)

```bash
# 1. Activate virtual environment
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate

# 2. Go to your project folder
cd ~/public_html/east_eagle

# 3. Install packages
pip install Django Pillow python-dotenv

# 4. Create .env file (copy from template, then edit with Gmail + secret key)
cp .env.production .env
nano .env

# 5. Run migrations and load data
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_blog
python manage.py seed_sidebars

# 6. Collect static files
mkdir -p public/static public/media
python manage.py collectstatic --noinput

# 7. Restart the app
touch passenger_wsgi.py
```

## Your server paths

| Item | Path |
|------|------|
| **Project folder** | `/home/easteagl/public_html/east_eagle/` |
| **Virtualenv** | `/home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate` |
| **Domain root** | `/home/easteagl/public_html/` |
| **Python App root** | `public_html/east_eagle` |

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
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate
cd ~/public_html/east_eagle
python manage.py check
python manage.py shell -c "
from django.test import Client
r = Client(HTTP_HOST='www.easteagleenergy.com').get('/')
print('Status:', r.status_code)
"
```

**Static files not loading?**
```bash
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate
cd ~/public_html/east_eagle
python manage.py collectstatic --clear --noinput
chmod -R 755 ~/public_html/east_eagle/public/static
```

**Module not found?**
```bash
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate
cd ~/public_html/east_eagle
pip install --force-reinstall Django Pillow python-dotenv
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
