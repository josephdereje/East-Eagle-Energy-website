from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from products.models import Product, ProductImage


VIEW_SPECS = [
    ('Front view', (46, 110, 179)),
    ('Side view', (243, 146, 0)),
    ('Back view', (27, 54, 93)),
    ('Detail view', (255, 203, 5)),
]

SAMPLE_PRODUCTS = [
    'deye-lifepo4-battery-512kwh-wall-mount',
    'deye-hybrid-inverter-5kw-sun5k-sg04lp3',
    'deye-all-in-one-ess-1024kwh-hybrid-system',
]


def make_placeholder(label, color, product_name):
    image = Image.new('RGB', (900, 900), color)
    draw = ImageDraw.Draw(image)

    draw.rectangle((40, 40, 860, 860), outline=(255, 255, 255), width=4)
    draw.rectangle((120, 220, 780, 680), fill=(248, 249, 250), outline=(200, 210, 220), width=3)

    title = product_name[:34] + ('…' if len(product_name) > 34 else '')
    lines = [title, label, 'Sample gallery image']

    y = 760
    for line in reversed(lines):
        draw.text((450, y), line, fill=(255, 255, 255), anchor='mm')
        y -= 34

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    filename = label.lower().replace(' ', '-') + '.png'
    return ContentFile(buffer.read(), name=filename)


class Command(BaseCommand):
    help = 'Add sample placeholder gallery images to demo products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Remove existing gallery images before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = ProductImage.objects.all().delete()
            self.stdout.write(f'Removed {deleted} existing gallery image(s).')

        seeded_products = 0
        gallery_count = 0

        for slug in SAMPLE_PRODUCTS:
            try:
                product = Product.objects.get(slug=slug, is_active=True)
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Skipped missing product: {slug}'))
                continue

            if not product.image:
                main_file = make_placeholder('Main view', VIEW_SPECS[0][1], product.name)
                product.image.save(main_file.name, main_file, save=True)

            product.gallery_images.all().delete()

            for order, (label, color) in enumerate(VIEW_SPECS[1:], start=1):
                image_file = make_placeholder(label, color, product.name)
                ProductImage.objects.create(
                    product=product,
                    label=label,
                    display_order=order,
                    is_active=True,
                    image=image_file,
                )
                gallery_count += 1

            seeded_products += 1
            items = product.get_gallery_items()
            self.stdout.write(
                f'  {product.name}: {len(items)} gallery slide(s) '
                f'({", ".join(item["label"] for item in items)})'
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete. {seeded_products} product(s), {gallery_count} extra gallery image(s).'
        ))
