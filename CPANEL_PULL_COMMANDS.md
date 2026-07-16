# cPanel Deployment — East Eagle Energy

## Your folder (do not rename)

| Item | Path |
|------|------|
| **Django app** | `/home/easteagl/easteagle/` |
| **Virtualenv** | `source /home/easteagl/virtualenv/easteagle/3.9/bin/activate` |
| **Public CSS/JS/images** | `/home/easteagl/public_html/css/`, `js/`, `images/` |

Stay in **`easteagle`** — no need to change to `east_eagle`.

---

## Deploy (copy & paste)

```bash
cd /home/easteagl/easteagle
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate

git fetch origin main
git reset --hard origin/main
git log -1 --oneline

bash scripts/deploy_cpanel.sh
```

---

## If `git fetch` fails (not a git repo yet)

Run once in your **existing** `easteagle` folder — nothing is moved:

```bash
cd /home/easteagl/easteagle
git init
git remote add origin https://github.com/josephdereje/East-Eagle-Energy-website.git
git fetch origin main
git reset --hard origin/main
```

Then run `bash scripts/deploy_cpanel.sh` again.

---

## Manual steps (without script)

```bash
cd /home/easteagl/easteagle
source /home/easteagl/virtualenv/easteagle/3.9/bin/activate

git fetch origin main
git reset --hard origin/main

ls -la blog/management/commands/seed_about.py
ls -la css/premium.css
ls -la images/hero/slide-solar.jpg

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py seed_hero_slides
python manage.py seed_about

mkdir -p /home/easteagl/public_html/css /home/easteagl/public_html/js /home/easteagl/public_html/images/hero
cp -f css/*.css /home/easteagl/public_html/css/
cp -f js/*.js   /home/easteagl/public_html/js/
cp -rf images/hero/* /home/easteagl/public_html/images/hero/
cp -f images/company-logo.png images/logo*.png /home/easteagl/public_html/images/ 2>/dev/null || true

touch /home/easteagl/easteagle/passenger_wsgi.py
```

---

## After deploy

1. cPanel → **LiteSpeed Web Cache Manager** → **Purge All**
2. Hard refresh: **Cmd+Shift+R**
3. Check:

```bash
curl -s https://www.easteagleenergy.com/ | grep premium.css
```

---

## cPanel Python App setting

In **Setup Python App**, Application root should be:

`easteagle`

(not `east_eagle`)
