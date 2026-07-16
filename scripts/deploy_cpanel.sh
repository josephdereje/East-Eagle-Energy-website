#!/bin/bash
# East Eagle Energy — cPanel deploy script
# Run from: /home/easteagl/public_html/east_eagle

set -e

APP_DIR="/home/easteagl/public_html/east_eagle"
VENV="/home/easteagl/virtualenv/public_html/east_eagle/3.9/bin/activate"
PUBLIC="/home/easteagl/public_html"
REPO="https://github.com/josephdereje/East-Eagle-Energy-website.git"
EXPECTED_FILE="blog/management/commands/seed_about.py"

echo "=== East Eagle Energy deploy ==="

# --- 1) Ensure project directory ---
if [ ! -f "$APP_DIR/manage.py" ]; then
  echo "ERROR: manage.py not found at $APP_DIR"
  echo "Find your project:"
  find /home/easteagl -name "manage.py" 2>/dev/null
  exit 1
fi

cd "$APP_DIR"
echo "Working in: $(pwd)"

# --- 2) Activate virtualenv ---
if [ -f "$VENV" ]; then
  # shellcheck source=/dev/null
  source "$VENV"
  echo "Virtualenv activated."
else
  echo "WARN: venv not found at $VENV — using system python."
fi

# --- 3) Sync from GitHub ---
if [ -d ".git" ]; then
  echo "Pulling from GitHub..."
  git fetch origin main
  git reset --hard origin/main
  echo "Commit: $(git log -1 --oneline)"
else
  echo "ERROR: This folder is not a git repository."
  echo "Re-clone with:"
  echo "  cd $(dirname "$APP_DIR")"
  echo "  mv $(basename "$APP_DIR") $(basename "$APP_DIR")_old"
  echo "  git clone $REPO $(basename "$APP_DIR")"
  exit 1
fi

# --- 4) Verify new files arrived ---
if [ ! -f "$EXPECTED_FILE" ]; then
  echo "ERROR: $EXPECTED_FILE still missing after git pull."
  echo "Your server code is out of date. Try:"
  echo "  git remote -v"
  echo "  git fetch origin main && git reset --hard origin/main"
  exit 1
fi

for f in css/premium.css images/hero/slide-solar.jpg; do
  if [ ! -f "$f" ]; then
    echo "ERROR: Missing $f"
    exit 1
  fi
done
echo "New files verified OK."

# --- 5) Django ---
python manage.py migrate
python manage.py collectstatic --no-input

python manage.py seed_hero_slides || echo "WARN: seed_hero_slides failed"
python manage.py seed_about || echo "WARN: seed_about failed"

# --- 6) Copy static to public_html ---
mkdir -p "$PUBLIC/css" "$PUBLIC/js" "$PUBLIC/images/hero"

cp -f css/*.css "$PUBLIC/css/"
cp -f js/*.js   "$PUBLIC/js/"

if [ -d "images/hero" ]; then
  cp -rf images/hero/* "$PUBLIC/images/hero/"
fi
for img in images/company-logo.png images/logo.png images/logo-transparent.png images/logo-light.png images/favicon.ico; do
  [ -f "$img" ] && cp -f "$img" "$PUBLIC/images/"
done

# --- 7) Restart Passenger ---
touch "$APP_DIR/passenger_wsgi.py"
echo "App restarted."

# --- 8) Verify live site ---
if curl -sf "https://www.easteagleenergy.com/css/premium.css" > /dev/null; then
  echo "OK: premium.css is live."
else
  echo "WARN: premium.css not reachable yet."
fi

if curl -s "https://www.easteagleenergy.com/" | grep -q "premium.css"; then
  echo "OK: Homepage references premium.css."
else
  echo "WARN: Homepage still missing premium.css — purge LiteSpeed cache and hard refresh."
fi

echo "=== Deploy finished ==="
echo "Next: cPanel → LiteSpeed Web Cache Manager → Purge All"
echo "Then hard refresh: Cmd+Shift+R"
