# cPanel Deployment — East Eagle Energy

## Correct paths

| Item | Path |
|------|------|
| Django app | `/home/easteagl/public_html/east_eagle/` |
| Virtualenv | `source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate` |
| Public static | `/home/easteagl/public_html/css/`, `js/`, `images/` |

**Do NOT use** `/home/easteagl/easteagle` — that is the wrong folder.

---

## Option A — One command (recommended)

```bash
cd /home/easteagl/public_html/east_eagle
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate
git fetch origin main && git reset --hard origin/main
bash scripts/deploy_cpanel.sh
```

---

## Option B — Manual steps

```bash
cd /home/easteagl/public_html/east_eagle
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate

git fetch origin main
git reset --hard origin/main
git log -1 --oneline

# Must exist — if not, git sync failed
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
cp -rf images/hero/ /home/easteagl/public_html/images/
cp -f images/company-logo.png images/logo*.png /home/easteagl/public_html/images/ 2>/dev/null || true

touch passenger_wsgi.py
```

---

## If `seed_about` or `images/hero` still missing

Git did not sync. Run diagnostics:

```bash
cd /home/easteagl/public_html/east_eagle
pwd
git remote -v
git log -1 --oneline
ls -la blog/management/commands/
```

Expected commit: `b41f515` or newer.

### Re-clone (fixes broken git)

```bash
cd /home/easteagl/public_html
mv east_eagle east_eagle_backup_$(date +%Y%m%d)
git clone https://github.com/josephdereje/East-Eagle-Energy-website.git east_eagle
cd east_eagle
source /home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate

# Restore data from backup
cp ../east_eagle_backup_*/.env . 2>/dev/null || true
cp ../east_eagle_backup_*/db.sqlite3 . 2>/dev/null || true

pip install -r requirements_production.txt
bash scripts/deploy_cpanel.sh
```

Then in cPanel → **Setup Python App** → confirm app root is `public_html/east_eagle` → **Restart**.

---

## After deploy

1. **LiteSpeed Web Cache Manager** → Purge All
2. Hard refresh: **Cmd+Shift+R**
3. Verify:

```bash
curl -s https://www.easteagleenergy.com/ | grep premium.css
```

---

## Live checks

- https://www.easteagleenergy.com/css/premium.css
- https://www.easteagleenergy.com/images/hero/slide-solar.jpg
- https://www.easteagleenergy.com/admin/
