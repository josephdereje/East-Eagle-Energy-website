# cPanel Deployment Commands - Quick Reference

## Why CSS looks wrong after `git pull`

The site loads styles from **`/css/styles.css`** and **`/css/dark-mode.css`**.

On cPanel, Apache often serves those from **`public_html/css/`**, not from Django’s `collectstatic` folder (`public/static/`).

So after every pull you must:

1. Update the Django app (`git pull` + `collectstatic` + restart)
2. **Copy CSS / JS / images into `public_html`**

---

## All commands (copy & paste)

```bash
# 1) Project + venv
cd /home/easteagl/easteagle
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate

# 2) Pull latest code
git pull origin main

# 3) Database + Django static (WhiteNoise /static/)
python manage.py migrate
python manage.py collectstatic --no-input

# 4) Sync files Apache serves at /css /js /images
mkdir -p /home/easteagl/public_html/css \
         /home/easteagl/public_html/js \
         /home/easteagl/public_html/images

cp -f /home/easteagl/easteagle/css/*.css /home/easteagl/public_html/css/
cp -f /home/easteagl/easteagle/js/*.js   /home/easteagl/public_html/js/
cp -f /home/easteagl/easteagle/images/*  /home/easteagl/public_html/images/

# 5) Restart Passenger
touch /home/easteagl/easteagle/passenger_wsgi.py
```

### If your app lives under `public_html` instead

```bash
cd ~/public_html/easteagle
# or: cd ~/public_html/east_eagle

source /home/easteagl/virtualenv/easteagle/3.9/bin/activate
# adjust venv path if different:
# source ~/virtualenv/public_html/easteagle/3.9/bin/activate

git pull origin main
python manage.py migrate
python manage.py collectstatic --no-input

mkdir -p ~/public_html/css ~/public_html/js ~/public_html/images
cp -f css/*.css ~/public_html/css/
cp -f js/*.js   ~/public_html/js/
cp -f images/*  ~/public_html/images/

touch passenger_wsgi.py
```

---

## Files that must land in `public_html/css/`

| File | Purpose |
|------|---------|
| `styles.css` | Main layout, mobile, products |
| `dark-mode.css` | Night mode |
| `admin.css` | Admin (if used from /css/) |

Also sync:

- `public_html/js/` → `theme.js`, `main.js`, `home-animations.js`, `product-detail.js`, …
- `public_html/images/` → `logo-transparent.png`, `logo-light.png`, favicons, …

---

## Hard refresh after deploy

Browsers cache CSS heavily. After upload:

1. Open the site
2. Hard refresh: **Ctrl+Shift+R** (Windows) or **Cmd+Shift+R** (Mac)
3. Or open DevTools → Network → “Disable cache” → reload

Check the CSS URL loads the new file:

- https://www.easteagleenergy.com/css/styles.css
- https://www.easteagleenergy.com/css/dark-mode.css

---

## Quick check on the server

```bash
ls -la /home/easteagl/public_html/css/
ls -la /home/easteagl/easteagle/css/
# timestamps / sizes should match after cp
diff -q /home/easteagl/easteagle/css/styles.css /home/easteagl/public_html/css/styles.css
diff -q /home/easteagl/easteagle/css/dark-mode.css /home/easteagl/public_html/css/dark-mode.css
```

If `diff` prints nothing, the public_html CSS matches the app.

---

## File Manager (no Terminal)

1. cPanel → **File Manager**
2. Open `/home/easteagl/easteagle/css/`
3. Select `styles.css` and `dark-mode.css` → **Copy**
4. Paste into `/home/easteagl/public_html/css/` (overwrite)
5. Repeat for `js/` and `images/` if needed
6. Setup Python App → **Restart**
