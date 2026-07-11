# Google Search Console Setup Guide

This guide will help you set up Google Search Console to improve your website's appearance in Google search results.

## 📋 What We Changed

### 1. **Updated Schema.org Structured Data**
We added enhanced structured data to help Google understand your site:
- **Organization schema**: Defines your company name, logo, and details
- **WebSite schema**: Tells Google your preferred site name "East Eagle Energy"
- **SearchAction**: Enables the Google search box for your site

### 2. **SEO Meta Tags**
- Updated title tags
- Enhanced meta descriptions
- Added Open Graph tags (for social media)
- Added Twitter Card tags
- Configured proper favicon references

---

## 🚀 Step 1: Verify Your Website in Google Search Console

### A. Access Google Search Console
1. Go to: https://search.google.com/search-console/
2. Sign in with your Google account (use a company Gmail account if possible)

### B. Add Your Property
1. Click **"Add Property"**
2. Choose **"URL prefix"** method
3. Enter: `https://www.easteagleenergy.com`
4. Click **Continue**

### C. Verify Ownership (Choose ONE method)

#### **Method 1: HTML File Upload (Recommended for cPanel)**
1. Google will give you an HTML file to download (e.g., `google1234567890abcdef.html`)
2. Upload this file to your cPanel:
   - Log into cPanel at http://mojito.hostns.io:2083/
   - Go to **File Manager**
   - Navigate to `/home/easteagl/easteagle/staticfiles/`
   - Click **Upload**
   - Upload the verification file
3. Go back to Google Search Console and click **Verify**

#### **Method 2: HTML Tag (Alternative)**
1. Google will give you a meta tag like:
   ```html
   <meta name="google-site-verification" content="ABC123XYZ..." />
   ```
2. Add this to your website's `header.html` template (after line 11):
   ```html
   <meta name="author" content="East Eagle Energy">
   <meta name="google-site-verification" content="YOUR-VERIFICATION-CODE">
   <link rel="canonical" href="https://www.easteagleenergy.com{{ request.path }}">
   ```
3. Deploy the update to cPanel
4. Click **Verify** in Google Search Console

---

## 🎯 Step 2: Set Your Site Name in Google Search Console

Once verified, Google Search Console may allow you to set your preferred site name:

1. In Google Search Console, select your property
2. Go to **Settings** (gear icon in left sidebar)
3. Look for **"Site Settings"** or **"Site Name"**
4. If available, set it to: **"East Eagle Energy"**

**Note:** This feature is being rolled out gradually. If you don't see it, the structured data we added (WebSite schema) will automatically suggest "East Eagle Energy" to Google.

---

## 🔍 Step 3: Request Indexing

To speed up Google's recognition of your changes:

1. In Google Search Console, go to **URL Inspection** (left sidebar)
2. Enter your homepage URL: `https://www.easteagleenergy.com`
3. Click **"Request Indexing"**
4. Repeat for key pages:
   - `https://www.easteagleenergy.com/products/`
   - `https://www.easteagleenergy.com/blog/`
   - `https://www.easteagleenergy.com/contact/`

---

## 📊 Step 4: Submit Your Sitemap

1. In Google Search Console, go to **Sitemaps** (left sidebar)
2. Enter: `sitemap.xml`
3. Click **Submit**

Your sitemap URL will be: `https://www.easteagleenergy.com/sitemap.xml`

---

## 🖼️ Step 5: Logo Appearance in Search Results

For your logo to appear in Google search results:

### A. Ensure Logo is Accessible
Your logo is already configured at:
- Primary: `https://www.easteagleenergy.com/images/logo.png`
- Favicon: `https://www.easteagleenergy.com/images/favicon.png`

### B. Logo Requirements
✅ Our logo meets Google's requirements:
- Square or rectangular format
- Accessible via HTTPS
- Included in structured data (already done)
- Minimum 112x112px
- Aspect ratio between 1x1 and 4x1

---

## ⏱️ How Long Does It Take?

| Change | Time to Appear |
|--------|----------------|
| Site name change | 1-4 weeks |
| Meta description | 2-7 days |
| Logo in search | 2-4 weeks |
| New pages indexed | 1-7 days |
| Sitemap processing | 1-3 days |

**Important:** Google doesn't instantly update search results. Be patient!

---

## ✅ Best Practices

### 1. **Monitor Your Performance**
Check Google Search Console weekly:
- **Performance**: See search queries, clicks, impressions
- **Coverage**: Check for indexing errors
- **Enhancements**: Monitor mobile usability, Core Web Vitals

### 2. **Keep Content Updated**
- Regularly add blog posts (helps SEO)
- Update product descriptions
- Add new products with detailed specs

### 3. **Build Quality Backlinks**
- List your site in business directories
- Get featured in industry blogs
- Partner with suppliers (Deye, Growatt, etc.)

### 4. **Monitor Search Appearance**
Use Google's **Search Appearance** tools:
- Check if Rich Results are appearing
- Monitor logo display
- Review mobile vs. desktop appearance

---

## 🔧 Troubleshooting

### "Site Name Not Changing"
1. Check that structured data is valid:
   - Go to https://search.google.com/test/rich-results
   - Enter: `https://www.easteagleenergy.com`
   - Verify "Organization" and "WebSite" schemas are detected
2. Request re-indexing in GSC
3. Wait 2-4 weeks for Google to process

### "Logo Not Showing"
1. Verify logo is publicly accessible (not blocked by robots.txt)
2. Check logo dimensions (should be at least 112x112px)
3. Ensure structured data includes logo URL
4. Wait 2-4 weeks

### "Meta Description Not Used"
Google may choose its own description based on search query. This is normal. Your meta description is still important as a suggestion.

---

## 📱 Step 6: Additional SEO Actions

### A. Set Up Google My Business (Optional)
If you have a physical office:
1. Go to: https://business.google.com
2. Create a listing for "East Eagle Energy"
3. Add your address, phone, website
4. Verify the business

### B. Monitor with Google Analytics (Recommended)
1. Create a Google Analytics 4 property
2. Add tracking code to your site
3. Link it to Search Console for deeper insights

### C. Social Media Integration
Make sure your company profiles use:
- Same name: "East Eagle Energy"
- Same logo: `/images/logo.png`
- Consistent description across all platforms

---

## 📞 Need Help?

If you need assistance:
1. **Google Search Console Help**: https://support.google.com/webmasters
2. **Schema.org Validator**: https://validator.schema.org
3. **Rich Results Test**: https://search.google.com/test/rich-results

---

## 📝 Summary of Changes Made

### Files Updated:
1. **`east_eagle_site/urls.py`**:
   - Enhanced Organization schema with logo object
   - Added WebSite schema with site name
   - Added SearchAction for site search box
   - Added social media links (sameAs)

2. **`templates/includes/header.html`**:
   - Already has proper SEO meta tags
   - Open Graph tags configured
   - Twitter Card tags configured
   - Favicon references in place

### What This Does:
- ✅ Tells Google your site name is "East Eagle Energy"
- ✅ Provides logo for search results
- ✅ Enables rich snippets
- ✅ Improves social media sharing appearance
- ✅ Adds site search functionality in Google

---

## 🎯 Next Steps

1. ✅ Deploy these changes to cPanel (see deployment commands below)
2. ⏳ Verify ownership in Google Search Console
3. ⏳ Submit sitemap
4. ⏳ Request indexing for main pages
5. ⏳ Wait 1-4 weeks for changes to appear
6. 📊 Monitor performance weekly

Remember: SEO is a long-term strategy. Results take time but are worth it!
