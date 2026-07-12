from io import BytesIO

from django.core.files.base import ContentFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image, ImageDraw

from products.models import Product, ProductCategory, ProductImage, ProductType


def make_test_image(name, color):
    image = Image.new('RGB', (400, 400), color)
    draw = ImageDraw.Draw(image)
    draw.text((200, 200), name, fill=(255, 255, 255), anchor='mm')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f'{name.lower().replace(" ", "-")}.png')


class ProductGalleryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test ESS Battery',
            slug='test-ess-battery-gallery',
            product_type=ProductType.ENERGY_STORAGE,
            category=ProductCategory.RESIDENTIAL,
            description='Test product for gallery rendering.',
            short_description='Sample ESS battery for gallery tests.',
            is_active=True,
        )
        self.product.image.save(
            'main.png',
            make_test_image('Main view', (46, 110, 179)),
            save=True,
        )
        for order, (label, color) in enumerate(
            [('Side view', (243, 146, 0)), ('Back view', (27, 54, 93))],
            start=1,
        ):
            ProductImage.objects.create(
                product=self.product,
                label=label,
                display_order=order,
                is_active=True,
                image=make_test_image(label, color),
            )

    def test_get_gallery_items_includes_main_and_extra_images(self):
        items = self.product.get_gallery_items()
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]['label'], 'Main view')
        self.assertEqual(items[1]['label'], 'Side view')
        self.assertEqual(items[2]['label'], 'Back view')

    def test_detail_page_renders_gallery(self):
        url = reverse('products:detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('productGalleryRoot', content)
        self.assertIn('productGalleryThumbs', content)
        self.assertIn('gallery-thumb', content)
        self.assertIn('gallery-slide', content)
        self.assertIn('Side view', content)
        self.assertEqual(content.count('data-gallery-index='), 6)
        self.assertIn('galleryPrevBtn', content)
        self.assertIn('galleryNextBtn', content)
