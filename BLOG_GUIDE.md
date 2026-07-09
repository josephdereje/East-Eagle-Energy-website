# Blog & Homepage Ads - Feature Guide

## What's New

I've added three major features to your East Eagle Energy website:

### 1. Blog Section (/blog/)
A complete blog system for company news and energy industry articles

### 2. Homepage Ads/Banners Database
Manage promotional banners that appear on your homepage

### 3. Updated Navigation
Added "Blog" tab between "Products" and "Contact" in the main menu

---

## Blog Features

### Current Content (6 Articles)

1. **East Eagle Energy Launches New Line of Deye Hybrid Inverters** (Featured)
   - Company announcement about new products
   
2. **Understanding LiFePO4 Battery Technology: Why It Matters** (Featured)
   - Educational content about battery technology
   
3. **Solar Energy Incentives and Opportunities in Ethiopia 2026** (Featured)
   - Industry insights and opportunities
   
4. **Choosing the Right Inverter Size for Your Home**
   - Practical guide for customers
   
5. **Maintenance Tips for Your Solar Power System**
   - Customer education and service tips
   
6. **Commercial Solar: Reducing Business Operating Costs**
   - B2B focused content

### Blog URLs

- **All Blog Posts:** http://127.0.0.1:8000/blog/
- **Individual Post:** http://127.0.0.1:8000/blog/post-slug/
- **Example:** http://127.0.0.1:8000/blog/east-eagle-energy-launches-deye-hybrid-inverters/

---

## Managing Blog Posts (Admin Panel)

### How to Add New Blog Post

1. **Login to Admin:**
   - Go to http://127.0.0.1:8000/admin/
   - Username: `admin` | Password: `admin123`

2. **Navigate to Blog Posts:**
   - Click "Blog Posts" in the admin menu
   - Click "Add Blog Post" button

3. **Fill in the Form:**
   - **Title:** Your blog post title (e.g., "New Solar Products Available")
   - **Slug:** Auto-filled from title (used in URL)
   - **Author:** Author name (default: East Eagle Energy)
   - **Excerpt:** Short summary (max 300 characters) - shown on blog list page
   - **Content:** Full article content (supports paragraphs, lists, headings)
   - **Featured Image:** Upload blog header image (optional but recommended)
   - **Is Published:** Check to make post visible on website
   - **Is Featured:** Check to show on homepage and featured section
   
4. **Click Save**

### Blog Post Best Practices

**Title:**
- Keep it under 60 characters for SEO
- Make it engaging and descriptive
- Include relevant keywords (solar, energy, Ethiopia, etc.)

**Excerpt:**
- Write a compelling 1-2 sentence summary
- Include a call-to-action or hook
- Max 300 characters

**Content:**
- Break into short paragraphs (2-3 sentences each)
- Use subheadings (**Bold text** for section titles)
- Include bullet points or numbered lists
- Add relevant details: phone number, product names, etc.
- Typical length: 500-1500 words

**Featured Image:**
- Size: 1200x600px or 800x400px (2:1 ratio)
- Format: JPG or PNG
- Subject: Product photos, solar installations, team photos, infographics
- Use bright, professional images

### Editing Existing Posts

1. Go to admin → Blog Posts
2. Click on the post title
3. Make your changes
4. Click "Save"

### Featured vs Regular Posts

- **Featured Posts (3):** Show on homepage and at top of blog page
- **Regular Posts:** Show in "All Articles" section only

---

## Homepage Ads/Banners

### Current Homepage Ads (3 Active)

1. **Deye Hybrid Inverters Now Available**
   - Links to residential products
   
2. **Free Solar System Assessment**
   - Links to contact form
   
3. **Commercial Solar Solutions**
   - Links to commercial products

### Managing Homepage Ads

1. **Login to Admin:**
   - Go to http://127.0.0.1:8000/admin/
   - Click "Homepage Ads/Banners"

2. **Add New Ad:**
   - Click "Add Homepage Ad/Banner"
   - **Title:** Main headline (e.g., "Summer Sale - 20% Off")
   - **Subtitle:** Supporting text (optional)
   - **Image:** Banner image (recommended: 1200x400px)
   - **Link URL:** Where clicking should go (e.g., `/products/` or `/#quote`)
   - **Button Text:** Call-to-action text (e.g., "Shop Now", "Learn More")
   - **Is Active:** Check to show on homepage
   - **Display Order:** Lower numbers appear first (1, 2, 3...)
   - Click "Save"

3. **Quick Edit:**
   - From the ads list, you can quickly toggle "Is Active" and change "Display Order"
   - Click "Save" at bottom

### Banner Image Recommendations

**Dimensions:**
- Desktop: 1200x400px or 1920x600px
- Aspect ratio: 3:1 or 16:5

**Content:**
- Large readable text
- Product images or lifestyle photos
- Company branding (logo optional)
- Clear call-to-action

**File Format:**
- JPG for photos
- PNG for graphics with text
- Keep file size under 500KB

**Design Tips:**
- Use brand colors (Navy #1B365D, Orange #F39200)
- Ensure text contrasts with background
- Mobile-friendly (text should be readable on small screens)

---

## Blog Categories & Topics

### Content Ideas

**Company News:**
- New product launches
- Team updates
- Company milestones
- Partnership announcements
- Event participation

**Educational Content:**
- How solar systems work
- Battery technology explained
- Installation guides
- Maintenance tips
- System sizing guides

**Industry News:**
- Ethiopian energy policy updates
- Global solar trends
- Technology advancements
- Success stories

**Customer Stories:**
- Installation case studies
- Customer testimonials
- Before/after comparisons
- ROI examples

**Seasonal Content:**
- Rainy season solar tips
- Summer energy savings
- Year-end reviews
- New year promotions

### Publishing Schedule Recommendation

- **Frequency:** 2-4 posts per month (one every 1-2 weeks)
- **Best Days:** Tuesday, Wednesday, Thursday
- **Featured Posts:** Rotate featured status to keep content fresh

---

## SEO & Social Sharing

### Built-in Features

**Share Buttons:**
Each blog post includes share buttons for:
- Facebook
- Twitter
- LinkedIn

**View Counter:**
- Automatically tracks and displays view count
- Shows on both list and detail pages

**Meta Information:**
- Publication date
- Author name
- Read time (calculated automatically)

---

## Quick Commands

```bash
# Add new blog posts to database
source .venv/bin/activate
python manage.py seed_blog

# Check blog statistics
python manage.py shell -c "
from blog.models import BlogPost, HomepageAd
print(f'Blog Posts: {BlogPost.objects.count()}')
print(f'Published: {BlogPost.objects.filter(is_published=True).count()}')
print(f'Featured: {BlogPost.objects.filter(is_featured=True).count()}')
print(f'Homepage Ads: {HomepageAd.objects.filter(is_active=True).count()}')
"
```

---

## Navigation Menu

The main navigation now includes:
- Home
- About
- Services
- Products
- **Blog** ← NEW!
- Contact

The Blog link is active when viewing blog pages (highlighted in blue).

---

## Admin Panel Sections

Your admin now has these sections:

1. **Authentication and Authorization**
   - Users, Groups

2. **Blog** ← NEW!
   - Blog Posts (articles)
   - Homepage Ads/Banners (promotional content)

3. **Contact**
   - Contact Inquiries (customer messages)

4. **Products**
   - Products (18 energy storage products)

---

## Tips for Success

### Growing Your Blog

1. **Consistency:** Post regularly (weekly or bi-weekly)
2. **Quality:** Focus on helpful, informative content
3. **Images:** Always include featured images
4. **Promotion:** Share new posts on social media
5. **Keywords:** Use relevant energy/solar terms naturally
6. **Links:** Link to your products within blog posts
7. **CTAs:** Include calls-to-action (contact, quote, view products)

### Homepage Ads Strategy

1. **Rotate Regularly:** Update ads every 2-4 weeks
2. **Seasonal Offers:** Create ads for holidays, seasons
3. **Product Launches:** Promote new arrivals
4. **Events:** Highlight special events or promotions
5. **Testimonials:** Feature customer success stories
6. **A/B Testing:** Try different headlines and images

### Content Calendar Example

**Month 1:**
- Week 1: Product announcement
- Week 2: Educational article
- Week 3: Customer story
- Week 4: Industry news

**Month 2:**
- Week 1: How-to guide
- Week 2: Company update
- Week 3: Seasonal tips
- Week 4: Technical deep-dive

---

## Support & Resources

### Getting Help

- **Admin URL:** http://127.0.0.1:8000/admin/
- **Blog URL:** http://127.0.0.1:8000/blog/
- **Phone:** +251 93 321 9802
- **Email:** info@easteagleenergy.com

### Image Resources

**Free Stock Photos:**
- Unsplash.com (solar panels, energy)
- Pexels.com (business, technology)
- Pixabay.com (free commercial use)

**Manufacturer Images:**
- Deye: deyeinverter.com
- Growatt: ginverter.com
- Request from your suppliers

### Writing Tips

- Use simple, clear language
- Write for your customer (not other engineers)
- Include specific numbers and data
- Add your contact info
- Proofread before publishing

---

## What to Do Next

1. ✅ Blog system is installed and working
2. ✅ 6 sample blog posts added
3. ✅ 3 homepage ads created
4. ✅ Navigation updated with Blog link
5. ⏳ **TODO:** Add featured images to blog posts
6. ⏳ **TODO:** Upload custom homepage ad banners
7. ⏳ **TODO:** Write and publish your first original blog post
8. ⏳ **TODO:** Share blog posts on social media

---

**East Eagle Energy** — *Energy That Never Grows Weary*

Blog & Content Management System v1.0
