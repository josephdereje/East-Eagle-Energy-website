# East Eagle Energy - Admin Guide

## Admin Access

**Admin Panel URL:** http://127.0.0.1:8000/admin/

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT:** Change this password after first login!

## Database Products Summary

Your database now contains **18 real energy storage products**:

### Residential (5 products)
- Deye Hybrid Inverter 5kW SUN-5K-SG04LP3 ⭐ (Featured)
- Deye LiFePO4 Battery 5.12kWh ⭐ (Featured)
- Deye SUN-8K-SG01LP1 Hybrid Inverter 8kW ⭐ (Featured)
- Growatt MIN 3000-6000 TL-XH Hybrid Inverter
- Pylontech US3000C LiFePO4 Battery 3.5kWh

### Commercial (5 products)
- Deye Three-Phase Hybrid Inverter 12kW ⭐ (Featured)
- Growatt SPF 5000-12000 ES Plus Off-Grid ⭐ (Featured)
- Deye SUN-50K-SG01HP3 Commercial 50kW ⭐ (Featured)
- BYD Battery-Box Premium LVL 15.4kWh
- Solis S6 Series Three-Phase 30kW

### Industrial (4 products)
- Deye SUN-100K-SG01HP3 Industrial 100kW ⭐ (Featured)
- Growatt MAX 100-125KTL3-X LV ⭐ (Featured)
- Tesla Powerpack 2 Industrial Storage
- Sungrow ST2236UX Liquid-Cooled ESS 2.5MWh

### ESS Solutions (4 products)
- Deye All-in-One ESS 10.24kWh ⭐ (Featured)
- Growatt AXE All-in-One ESS 5kW/10kWh ⭐ (Featured)
- Sonnen Eco ESS 10kWh ⭐ (Featured)
- Victron Energy ESS Package with MultiPlus-II 5kW

## Managing Homepage Featured Products

### Current Featured Products on Homepage:
1. Deye All-in-One ESS 10.24kWh Hybrid System
2. Deye Hybrid Inverter 5kW SUN-5K-SG04LP3
3. Deye LiFePO4 Battery 5.12kWh (Wall-Mount)
4. Deye SUN-100K-SG01HP3 Industrial Inverter 100kW

### How to Update Featured Products:

1. **Login to Admin Panel:**
   - Go to http://127.0.0.1:8000/admin/
   - Login with username: `admin`, password: `admin123`

2. **Navigate to Products:**
   - Click on "Products" in the admin menu

3. **Edit Any Product:**
   - Click on the product name
   - Check/uncheck the "Is featured" checkbox
   - Click "Save"

4. **Add Product Images:**
   - In the product edit page
   - Scroll to "Image" field
   - Click "Choose File" and upload product image
   - Recommended image size: 800x600px or similar aspect ratio
   - Click "Save"

5. **Add New Products:**
   - Click "Add Product" button
   - Fill in all fields:
     - Name
     - Slug (auto-filled from name)
     - Category (Residential/Commercial/Industrial/ESS Solution)
     - Short description (for product cards)
     - Description (full details)
     - Price (optional)
     - Is featured (check to show on homepage)
     - Is active (check to make visible)
     - Image (upload product photo)
   - Click "Save"

## Product Image Recommendations

For best results, use product images with these specifications:
- **Format:** JPG or PNG
- **Size:** 800x600px (4:3 ratio) or 1200x900px
- **Background:** White or transparent for clean look
- **Content:** Show product clearly from front angle

### Where to Find Product Images:
1. **Deye Official Website:** https://www.deyeinverter.com/
2. **Growatt Official:** https://www.ginverter.com/
3. **Manufacturer Websites:** Most brands provide high-quality product photos
4. **Request from Your Supplier:** They usually have product image libraries

## Viewing Contact Inquiries

1. Login to admin panel
2. Click "Contact inquiries"
3. View all customer quote requests
4. Check if email was sent successfully
5. Export or respond to inquiries

## Quick Commands

```bash
# Start the server
source .venv/bin/activate && python manage.py runserver

# Create new admin user
python manage.py createsuperuser

# View all products in database
python manage.py shell -c "from products.models import Product; print([p.name for p in Product.objects.all()])"

# Reset admin password (if forgotten)
python manage.py changepassword admin
```

## Next Steps

1. ✅ Django installed and running
2. ✅ Database seeded with 18 real products
3. ✅ Admin user created
4. ⏳ **TODO:** Add product images through admin panel
5. ⏳ **TODO:** Customize featured products
6. ⏳ **TODO:** Test contact form
7. ⏳ **TODO:** Change admin password to something secure

## Support

For questions about the products or technical specifications:
- Tel: +251 93 321 9802
- Email: info@easteagleenergy.com

---

**East Eagle Energy** — *Energy That Never Grows Weary*
Est. 2022
