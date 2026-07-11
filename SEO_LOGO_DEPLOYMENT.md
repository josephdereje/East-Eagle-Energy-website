# SEO & Logo Update - Deployment Checklist

## 🎯 What's Included in This Update

### Changes Made:
1. ✅ Updated logo to new white background version
2. ✅ Enhanced schema markup for Google Search (Organization + WebSite)
3. ✅ Added site name preference ("East Eagle Energy" instead of domain)
4. ✅ Logo display configuration for search results
5. ✅ Header layout optimized (logo size: 160px, minimal gap)

### Files Changed:
- `east_eagle_site/urls.py` - Enhanced structured data
- `css/styles.css` - Header layout and logo sizing
- `images/logo.png` - New logo image
- `images/logo-transparent.png` - New logo image (backup)
- `GOOGLE_SEARCH_CONSOLE_GUIDE.md` - New comprehensive guide

---

## 📦 Deployment to cPanel

### Step 1: Push to GitHub (DONE)
```bash
# These commands push your changes to GitHub
git add .
git commit -m "Update SEO schema, logo, and add Google Search Console guide"
git push origin main
```

### Step 2: Pull on cPanel
```bash
# 1. Connect to cPanel Terminal
# Go to: http://mojito.hostns.io:2083/
# Click: "Terminal" in the Advanced section

# 2. Navigate to your project
cd /home/easteagl/easteagle

# 3. Activate virtual environment
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate

# 4. Pull latest changes from GitHub
git pull origin main

# 5. Collect static files (updates CSS and images)
python manage.py collectstatic --no-input

# 6. Restart the application
# In cPanel, go to "Setup Python App"
# Click on your app, then click "Restart"
```

---

## ✅ Verification Steps

### 1. Check Website Locally
After pulling, verify:
- Logo displays correctly
- Header layout looks good
- No spacing issues

### 2. Test Structured Data
Go to: https://search.google.com/test/rich-results
- Enter: `https://www.easteagleenergy.com`
- Verify "Organization" schema detected
- Verify "WebSite" schema detected
- Check logo URL is correct

### 3. Verify in Browser
Test these URLs after deployment:
- `https://www.easteagleenergy.com` - Homepage
- `https://www.easteagleenergy.com/products/` - Products page
- `https://www.easteagleenergy.com/blog/` - Blog page

Check:
- Logo loads (no broken images)
- Header spacing looks correct
- Page title shows "East Eagle Energy"

---

## 🔍 Google Search Console Setup

After deployment:

1. **Verify Ownership** (choose one method):
   - HTML file upload to `/staticfiles/`
   - OR add meta tag to `header.html`

2. **Submit Sitemap**:
   - URL: `https://www.easteagleenergy.com/sitemap.xml`

3. **Request Indexing** for main pages:
   - Homepage
   - Products page
   - Blog page

See `GOOGLE_SEARCH_CONSOLE_GUIDE.md` for detailed instructions.

---

## ⏱️ Expected Timeline

| Action | Time |
|--------|------|
| Code deployment | Immediate |
| Logo display on site | Immediate |
| Google re-crawl | 1-7 days |
| Site name change in search | 1-4 weeks |
| Logo in search results | 2-4 weeks |

---

## 🚨 Troubleshooting

### Logo Not Displaying After Deployment
```bash
# On cPanel Terminal:
cd /home/easteagl/easteagle
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate
python manage.py collectstatic --no-input --clear
```

### CSS Changes Not Appearing
Clear browser cache or use Incognito/Private mode to test.

### 500 Error After Deployment
```bash
# Check logs in cPanel:
# File Manager > error_log (in your domain's directory)

# Restart the Python app:
# cPanel > Setup Python App > Click app > Restart
```

---

## 📞 Support Resources

- **Google Search Console**: https://search.google.com/search-console/
- **Rich Results Test**: https://search.google.com/test/rich-results
- **Schema Validator**: https://validator.schema.org/
- **cPanel Documentation**: Your hosting provider's help center

---

**Deployment Status**: Ready to push to GitHub and deploy to cPanel
