"""Generate favicon and app icon files from the East Eagle Energy logo."""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'images'
SOURCE = IMAGES / 'logo-transparent.png'

SIZES = {
    'favicon-16.png': 16,
    'favicon-32.png': 32,
    'favicon-48.png': 48,
    'favicon-192.png': 192,
    'favicon-512.png': 512,
    'apple-touch-icon.png': 180,
}


def _fit_logo_on_canvas(size, background=(255, 255, 255, 255)):
    logo = Image.open(SOURCE).convert('RGBA')
    canvas = Image.new('RGBA', (size, size), background)
    padding = max(2, round(size * 0.08))
    inner = size - (padding * 2)
    logo.thumbnail((inner, inner), Image.Resampling.LANCZOS)
    offset = ((size - logo.width) // 2, (size - logo.height) // 2)
    canvas.paste(logo, offset, logo)
    return canvas


def _rounded_square(size, radius_ratio=0.18, fill=(255, 255, 255, 255)):
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    radius = max(2, int(size * radius_ratio))
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=fill)
    return canvas


def build_icon(size):
    """Square icon with white rounded background so the logo reads at small sizes."""
    base = _rounded_square(size)
    logo = Image.open(SOURCE).convert('RGBA')
    padding = max(2, round(size * 0.12))
    inner = size - (padding * 2)
    logo.thumbnail((inner, inner), Image.Resampling.LANCZOS)
    offset = ((size - logo.width) // 2, (size - logo.height) // 2)
    base.paste(logo, offset, logo)
    return base


def save_png(path, image):
    image.save(path, format='PNG', optimize=True)


def save_ico(path, sizes=(16, 32, 48)):
    icons = [build_icon(size).convert('RGBA') for size in sizes]
    icons[0].save(
        path,
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=icons[1:],
    )


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f'Missing logo source: {SOURCE}')

    for filename, size in SIZES.items():
        save_png(IMAGES / filename, build_icon(size))

    save_png(IMAGES / 'favicon.png', build_icon(32))
    save_ico(IMAGES / 'favicon.ico', sizes=(16, 32, 48))
    print('Generated favicon assets in', IMAGES)


if __name__ == '__main__':
    main()
