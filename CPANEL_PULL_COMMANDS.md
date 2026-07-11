# cPanel Deployment Commands - Quick Reference

## 📦 Pull Latest Changes from GitHub to cPanel

Follow these commands in order:

### Step 1: Open cPanel Terminal
1. Go to: http://mojito.hostns.io:2083/
2. Login with your credentials
3. Click **"Terminal"** (in Advanced section)

### Step 2: Navigate and Activate Environment
```bash
# Go to your project directory
cd /home/easteagl/easteagle

# Activate the virtual environment
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate
```

### Step 3: Pull Updates from GitHub
```bash
# Pull latest code
git pull origin main
```

### Step 4: Update Static Files
```bash
# Collect static files (CSS, images, JS)
python manage.py collectstatic --no-input
```

### Step 5: Restart Application
Option A - Via Terminal:
```bash
touch passenger_wsgi.py
```

Option B - Via cPanel Interface:
1. Go to **"Setup Python App"** in cPanel
2. Find your application
3. Click **"Restart"** button

---

## ✅ Verification

After deployment, check:

1. **Website loads**: https://www.easteagleenergy.com
2. **Logo appears correctly**: New white background logo
3. **No 500 errors**: Check homepage, products, blog

If you see a 500 error:
```bash
# View error logs
tail -100 ~/error_log

# Or restart the app
touch passenger_wsgi.py
```

---

## 🔍 Test Structured Data

After deploying, test your SEO improvements:

1. Go to: https://search.google.com/test/rich-results
2. Enter: `https://www.easteagleenergy.com`
3. Click **"Test URL"**
4. Verify you see:
   - ✅ Organization schema
   - ✅ WebSite schema
   - ✅ Logo URL
   - ✅ Site name "East Eagle Energy"

---

## 📝 All Commands in One Block (Copy & Paste)

```bash
# Navigate to project
cd /home/easteagl/easteagle

# Activate environment
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate

# Pull latest changes
git pull origin main

# Update static files
python manage.py collectstatic --no-input

# Restart application
touch passenger_wsgi.py
```

---

## 🎯 What's New in This Update

✅ Enhanced SEO schema (Organization + WebSite)  
✅ Site name set to "East Eagle Energy" for Google  
✅ New logo with white background (160px height)  
✅ Header layout optimized (no gap, navigation closer)  
✅ Logo configured for Google search results  
✅ Added comprehensive Google Search Console guide  

---

## ⏱️ Expected Changes

| Change | When You'll See It |
|--------|-------------------|
| Logo on website | Immediately after deployment |
| CSS/layout updates | Immediately (may need cache clear) |
| Google site name change | 1-4 weeks |
| Logo in Google search | 2-4 weeks |

---

## 📚 Additional Resources

- **Google Search Console Guide**: `GOOGLE_SEARCH_CONSOLE_GUIDE.md`
- **Deployment Checklist**: `SEO_LOGO_DEPLOYMENT.md`

---

**Last Updated**: July 11, 2026  
**Git Commit**: `32efa5f` - "Update SEO schema, logo, and add Google Search Console guide"
