# cPanel Deployment Commands - Quick Reference

## ⚠️ CORRECT PROJECT PATH (read this first)

Your live site runs from **`public_html/east_eagle`** — NOT `/home/easteagl/easteagle`.

| Item | Path |
|------|------|
| **Django app (git pull here)** | `/home/easteagl/public_html/east_eagle/` |
| **Virtualenv** | `source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate` |
| **Apache static (CSS/JS/images)** | `/home/easteagl/public_html/css/`, `js/`, `images/` |
| **Restart** | `touch ~/public_html/east_eagle/passenger_wsgi.py` |

If you pull in the wrong folder, the website will look unchanged.

---

## Full deploy (copy & paste)

```bash
# 1) CORRECT folder + venv
cd /home/easteagl/public_html/east_eagle
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate

# 2) Force sync from GitHub
git fetch origin main
git reset --hard origin/main
git log -1 --oneline
# Must show: 08c05cf Redesign public site and admin...

# 3) Verify new files exist
ls -la blog/management/commands/seed_about.py
ls -la css/premium.css
ls -la images/hero/ | head

# 4) Database + static
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py seed_hero_slides
python manage.py seed_about

# 5) Copy CSS/JS/images to public_html (Apache serves /css /js /images)
mkdir -p /home/easteagl/public_html/css \
         /home/easteagl/public_html/js \
         /home/easteagl/public_html/images/hero

cp -f css/*.css /home/easteagl/public_html/css/
cp -f js/*.js   /home/easteagl/public_html/js/
cp -f images/*  /home/easteagl/public_html/images/ 2>/dev/null || true
cp -rf images/hero/* /home/easteagl/public_html/images/hero/

# 6) Restart Passenger
touch /home/easteagl/public_html/east_eagle/passenger_wsgi.py
```

---

## Clear LiteSpeed cache (important)

cPanel → **LiteSpeed Web Cache Manager** → **Purge All**

Or: **Setup Python App** → **Restart**

Then hard refresh: **Ctrl+Shift+R** / **Cmd+Shift+R**

---

## How to know deploy worked

Homepage HTML must include **`premium.css`** (not only styles.css):

```bash
curl -s https://www.easteagleenergy.com/ | grep premium.css
```

If that prints nothing, you are still on old templates (wrong folder or cache).

Check these URLs return **200**:

- https://www.easteagleenergy.com/css/premium.css
- https://www.easteagleenergy.com/css/admin.css
- https://www.easteagleenergy.com/images/company-logo.png
- https://www.easteagleenergy.com/images/hero/slide-solar.jpg

---

## Files that must land in `public_html/css/`

| File | Purpose |
|------|---------|
| `styles.css` | Main layout |
| `dark-mode.css` | Night mode |
| `premium.css` | Hero animations, About page, premium UI |
| `admin.css` | Admin login + dashboard |

---

## First-time admin login

```bash
cd /home/easteagl/public_html/east_eagle
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate
python manage.py createsuperuser
```

Admin: https://www.easteagleenergy.com/admin/
