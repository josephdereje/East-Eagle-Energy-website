from django.core.management.base import BaseCommand

from products.models import Product, RecommendedProduct


class Command(BaseCommand):
    help = 'Seed Recommended Products from featured / first active catalog products'

    def handle(self, *args, **options):
        products = list(
            Product.objects.filter(is_active=True)
            .order_by('-is_featured', 'name')[:6]
        )
        if not products:
            self.stdout.write(self.style.WARNING('No active products found to recommend.'))
            return

        badges = [
            RecommendedProduct.Badge.BEST_SELLER,
            RecommendedProduct.Badge.FEATURED,
            RecommendedProduct.Badge.POPULAR,
            RecommendedProduct.Badge.HOT_DEAL,
            RecommendedProduct.Badge.NEW,
            RecommendedProduct.Badge.PROMO,
        ]

        created = 0
        for i, product in enumerate(products):
            obj, was_created = RecommendedProduct.objects.update_or_create(
                product=product,
                defaults={
                    'title': '',
                    'subtitle': product.short_description or 'Trusted energy solution from East Eagle Energy',
                    'badge': badges[i % len(badges)],
                    'button_text': 'View Product',
                    'display_order': i,
                    'is_active': True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Recommended products ready. {created} new, '
                f'total active: {RecommendedProduct.objects.filter(is_active=True).count()}.'
            )
        )
