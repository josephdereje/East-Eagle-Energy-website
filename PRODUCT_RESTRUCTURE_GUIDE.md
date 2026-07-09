# Product Restructuring Guide - C & I BESS & Sidebar Navigator

## ✅ Changes Completed

### 1. **Merged Commercial & Industrial → C & I BESS**
- Old: "Commercial" and "Industrial" were separate categories
- New: Combined into **"C & I BESS"** (Commercial & Industrial Battery Energy Storage System)
- All 9 products from both categories have been automatically migrated

### 2. **Added Residential Subcategories**
- **Low Voltage** - Modular, scalable battery systems (typically 48V-100V DC)
- **High Voltage** - High-capacity battery systems (typically >100V DC)
- Products automatically categorized based on power ratings

### 3. **Sidebar Navigator** (Similar to Pylontech website)
- Dynamic sidebar shows when viewing specific product categories
- Voltage type filters for Residential products
- Sidebar content fully manageable from admin panel
- Support for sidebar images/banners (editable from admin)

---

## 📊 Product Database Summary

### Current Structure:
```
Total Products: 18

├── Residential (5 products)
│   ├── Low Voltage (2 products)
│   │   ├── Deye Hybrid Inverter 5kW
│   │   └── Deye LiFePO4 Battery 5.12kWh
│   └── High Voltage (2 products)
│       ├── Deye SUN-8K-SG01LP1 8kW
│       └── Growatt MIN 3000-6000 TL-XH
│
├── C & I BESS (9 products) ← NEW!
│   ├── Deye Three-Phase 12kW
│   ├── Growatt SPF 5000-12000 ES Plus
│   ├── BYD Battery-Box Premium 15.4kWh
│   ├── Deye SUN-50K Commercial 50kW
│   ├── Solis S6 Three-Phase 30kW
│   ├── Deye SUN-100K Industrial 100kW
│   ├── Growatt MAX 100-125KTL3-X
│   ├── Tesla Powerpack 2
│   └── Sungrow ST2236UX 2.5MWh
│
└── ESS Solution (4 products)
    ├── Deye All-in-One ESS 10.24kWh
    ├── Growatt AXE All-in-One 5kW/10kWh
    ├── Sonnen Eco ESS 10kWh
    └── Victron Energy ESS Package
```

---

## 🔗 New Product URLs

### Main Categories:
- All Products: `/products/`
- Residential: `/products/category/residential/`
- C & I BESS: `/products/category/c_and_i_bess/`
- ESS Solution: `/products/category/ess_solution/`

### Residential Voltage Filters:
- Low Voltage: `/products/category/residential/low_voltage/`
- High Voltage: `/products/category/residential/high_voltage/`

---

## 🎨 Product Page Features

### Navigation Structure:
```
[All Products] [Residential] [C & I BESS] [ESS Solution]
     ↓ (when clicked Residential)
┌─────────────────────┐  ┌────────────────────┐
│  SIDEBAR            │  │  PRODUCT GRID      │
│                     │  │                    │
│  Residential ESS    │  │  [Product Cards]   │
│  Description...     │  │                    │
│                     │  │                    │
│  Product Type:      │  │                    │
│  ☑ All Types        │  │                    │
│  ☐ Low Voltage      │  │                    │
│  ☐ High Voltage     │  │                    │
│                     │  │                    │
│  [Sidebar Images]   │  │                    │
│                     │  │                    │
│  [Get Consultation] │  │                    │
└─────────────────────┘  └────────────────────┘
```

---

## 🛠️ Managing Product Sidebar (Admin Panel)

### Accessing Sidebar Settings:

1. **Login to Admin:**
   - URL: http://127.0.0.1:8000/admin/
   - Username: `admin` | Password: `admin123`

2. **Navigate to Sidebar Sections:**
   - Click **"Products"** section
   - Click **"Product Sidebar Sections"**

### What You Can Edit:

#### **Sidebar Section Settings:**
- **Category:** Which product category this sidebar is for
- **Title:** Sidebar heading (e.g., "Residential Energy Storage")
- **Description:** Explanatory text shown at top
- **Display Order:** Order if multiple sections exist
- **Is Active:** Toggle sidebar visibility

#### **Sidebar Images/Banners:**
For each sidebar section, you can add multiple images:
- **Image:** Upload promotional banner or product image
- **Title:** Image heading/label
- **Caption:** Descriptive text
- **Link URL:** Where clicking the image goes (optional)
- **Display Order:** Control image sequence
- **Is Active:** Show/hide individual images

### Adding Sidebar Images:

1. Go to **Product Sidebar Sections**
2. Click on a category (e.g., "Residential Sidebar")
3. Scroll to **"Sidebar Images"** section at bottom
4. Click **"Add another Sidebar Image"**
5. Fill in fields:
   - Upload image (recommended: 250x180px or 300x200px)
   - Add title and caption
   - Set link URL if clickable
   - Set display order
   - Check "Is Active"
6. Click **"Save"**

---

## 📝 Managing Products

### Adding New Product:

1. **Go to Admin → Products → Add Product**

2. **Basic Information:**
   - **Name:** Product name (e.g., "Deye Hybrid Inverter 10kW")
   - **Slug:** Auto-filled from name (used in URL)
   - **Category:** Choose from:
     - Residential
     - C & I BESS
     - ESS Solution
   - **Voltage Type:** (Only for Residential)
     - Low Voltage (for 5kW, modular batteries)
     - High Voltage (for 8kW+, large systems)
     - N/A (for non-residential products)

3. **Content:**
   - **Short Description:** Brief summary (max 300 chars)
   - **Description:** Full product details
   - **Image:** Upload product photo
   - **Price:** Product price in Ethiopian Birr (optional)

4. **Status:**
   - **Is Featured:** Check to show on homepage
   - **Is Active:** Check to make product visible

5. **Click Save**

### Editing Existing Products:

1. Go to **Admin → Products**
2. Click on product name
3. Update category or voltage type if needed
4. Click **Save**

---

## 🎯 Voltage Type Guidelines

### Low Voltage Systems:
**Characteristics:**
- Typically 48V or 51.2V DC battery systems
- Modular, stackable design
- Easy expansion
- 3-6kW inverters
- Residential homes, small offices

**Examples:**
- Deye 5kW inverters
- Pylontech US3000C batteries
- Small modular systems

### High Voltage Systems:
**Characteristics:**
- 200V+ DC battery systems
- High-capacity single units
- 8kW+ inverters
- Larger residential or small commercial
- More efficient for high power needs

**Examples:**
- Deye 8kW+ inverters
- High-voltage battery banks
- Larger home systems

---

## 🎨 Sidebar Image Recommendations

### Image Specifications:

**Dimensions:**
- Width: 240-300px
- Height: 180-250px
- Aspect Ratio: 4:3 or 3:2
- Format: JPG or PNG
- Max File Size: 300KB

### Content Ideas:

1. **Product Highlights:**
   - Feature specific products
   - Show product in use
   - Technical specifications graphic

2. **Promotional Banners:**
   - "New Arrival" badges
   - Special offers
   - Seasonal promotions

3. **Educational Content:**
   - "How to Choose" guides
   - Comparison charts
   - Installation examples

4. **Trust Signals:**
   - Certifications
   - Warranty information
   - Customer testimonials

### Design Tips:
- Use brand colors (Navy #1B365D, Orange #F39200)
- Keep text minimal and readable
- High-quality product photos
- Clear call-to-action if clickable

---

## 🔄 Migration Details

### What Changed Automatically:

✅ **Commercial Products → C & I BESS:**
- Deye Three-Phase 12kW
- Growatt SPF 5000-12000 ES Plus
- BYD Battery-Box Premium 15.4kWh
- Deye SUN-50K Commercial 50kW
- Solis S6 Three-Phase 30kW

✅ **Industrial Products → C & I BESS:**
- Deye SUN-100K Industrial 100kW
- Growatt MAX 100-125KTL3-X
- Tesla Powerpack 2
- Sungrow ST2236UX 2.5MWh

✅ **Residential Voltage Assignment:**
- Low Voltage: Deye 5kW, Deye 5.12kWh Battery
- High Voltage: Deye 8kW, Growatt MIN series

### No Action Required:
- All products automatically migrated
- URLs still work (redirects in place)
- No data loss
- Sidebar sections created

---

## 🌐 Live URLs to Test

### Category Pages:
- http://127.0.0.1:8000/products/
- http://127.0.0.1:8000/products/category/residential/
- http://127.0.0.1:8000/products/category/c_and_i_bess/
- http://127.0.0.1:8000/products/category/ess_solution/

### Residential Voltage Filters:
- http://127.0.0.1:8000/products/category/residential/low_voltage/
- http://127.0.0.1:8000/products/category/residential/high_voltage/

---

## 📱 Responsive Design

### Desktop (>992px):
- Sidebar on left (280px width)
- Product grid on right
- Sticky sidebar (stays visible while scrolling)

### Tablet (768-992px):
- Sidebar above products
- Full-width layout
- Sidebar filters in 2 columns

### Mobile (<768px):
- Stacked layout
- Sidebar collapsible
- Single column product grid

---

## 🚀 Next Steps

### Immediate Actions:
1. ✅ Product categories restructured
2. ✅ Sidebar system implemented
3. ✅ Voltage types assigned
4. ⏳ **Add sidebar images through admin**
5. ⏳ **Review and adjust voltage type assignments if needed**
6. ⏳ **Customize sidebar descriptions**

### Content Tasks:
1. **Upload Sidebar Images:**
   - Create promotional banners
   - Add product highlight images
   - Include certification badges

2. **Review Product Assignments:**
   - Check voltage types are correct
   - Ensure all C & I BESS products properly categorized
   - Add any missing products

3. **Update Sidebar Text:**
   - Customize descriptions for each category
   - Add helpful guidance text
   - Include technical specifications

---

## 💡 Tips for Success

### Product Organization:
- **Residential:** Focus on home users, emphasize ease of use
- **C & I BESS:** Highlight ROI, reliability, and scale
- **ESS Solution:** Emphasize all-in-one convenience

### Sidebar Usage:
- Keep sidebar content concise
- Update images seasonally
- Use sidebar for promotions
- Add clear calls-to-action

### Voltage Types:
- Only applicable to Residential category
- Helps customers find right fit
- Based on technical specifications
- Can be changed anytime in admin

---

## 📞 Support

**Admin Panel:** http://127.0.0.1:8000/admin/
**Phone:** +251 93 321 9802
**Email:** info@easteagleenergy.com

---

## 🔧 Technical Details

### Database Changes:
- Added `voltage_type` field to Product model
- Changed `category` choices (removed industrial, added c_and_i_bess)
- Created `ProductSidebarSection` model
- Created `ProductSidebarImage` model

### Commands:
```bash
# View product distribution
python manage.py shell -c "
from products.models import Product, ProductCategory
for cat in ProductCategory:
    count = Product.objects.filter(category=cat).count()
    print(f'{cat.label}: {count}')
"

# Create/update sidebar sections
python manage.py seed_sidebars
```

---

**East Eagle Energy** — *Energy That Never Grows Weary*

Product Management System v2.0 - C & I BESS Edition
