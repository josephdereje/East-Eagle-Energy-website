#!/bin/bash
# East Eagle Energy — cPanel deploy (keeps your existing easteagle folder)

set -e

APP_DIR="/home/easteagl/easteagle"
VENV="/home/easteagl/virtualenv/easteagle/3.9/bin/activate"
PUBLIC="/home/easteagl/public_html"
REPO="https://github.com/josephdereje/East-Eagle-Energy-website.git"
EXPECTED_FILE="blog/management/commands/seed_about.py"

echo "=== East Eagle Energy deploy ==="

if [ ! -f "$APP_DIR/manage.py" ]; then
  echo "ERROR: manage.py not found at $APP_DIR"
  find /home/easteagl -name "manage.py" 2>/dev/null
  exit 1
fi

cd "$APP_DIR"
echo "Working in: $(pwd)"

if [ -f "$VENV" ]; then
  # shellcheck source=/dev/null
  source "$VENV"
  echo "Virtualenv activated."
else
  echo "WARN: venv not found at $VENV"
fi

# Sync GitHub into THIS folder (no rename, no move)
if [ ! -d ".git" ]; then
  echo "Initializing git in existing folder..."
  git init
  git remote add origin "$REPO" 2>/dev/null || git remote set-url origin "$REPO"
fi

git fetch origin main
git reset --hard origin/main
echo "Commit: $(git log -1 --oneline)"

if [ ! -f "$EXPECTED_FILE" ]; then
  echo "ERROR: $EXPECTED_FILE still missing."
  exit 1
fi

for f in css/premium.css images/hero/slide-solar.jpg; do
  [ -f "$f" ] || { echo "ERROR: Missing $f"; exit 1; }
done
echo "Files verified OK."

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py seed_hero_slides || true
python manage.py seed_about || true

mkdir -p "$PUBLIC/css" "$PUBLIC/js" "$PUBLIC/images/hero"
cp -f css/*.css "$PUBLIC/css/"
cp -f js/*.js   "$PUBLIC/js/"
[ -d "images/hero" ] && cp -rf images/hero/* "$PUBLIC/images/hero/"
for img in images/company-logo.png images/logo.png images/logo-transparent.png images/logo-light.png images/favicon.ico; do
  [ -f "$img" ] && cp -f "$img" "$PUBLIC/images/"
done

touch "$APP_DIR/passenger_wsgi.py"
echo "=== Done. Purge LiteSpeed cache, then hard refresh. ==="
