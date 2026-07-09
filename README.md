# East Eagle Energy Website

Django-powered company website with product catalog and email contact form.

## Features

- Company brochure homepage
- **Product list** with category navigation:
  - Residential
  - Commercial
  - Industrial
  - ESS Solution
- **Contact form** saves to database and sends email
- Django admin to manage products and view inquiries

## Setup

```bash
cd ~/East-Eagle-Energy-website
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your email settings
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

Admin: **http://127.0.0.1:8000/admin/**

## Product URLs

- All products: `/products/`
- Residential: `/products/category/residential/`
- Commercial: `/products/category/commercial/`
- Industrial: `/products/category/industrial/`
- ESS Solution: `/products/category/ess_solution/`

## Email setup

Copy `.env.example` to `.env` and set:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_RECIPIENT_EMAIL=info@easteagleenergy.com
```

For local testing without SMTP, use:
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
Messages will print in the terminal.

## Company Info

- **East Eagle Energy** — Est. 2022
- Tel: +251 93 321 9802
- Tagline: *Energy That Never Grows Weary*
