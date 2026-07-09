from django.core.management.base import BaseCommand

from products.models import Product, ProductCategory


SAMPLE_PRODUCTS = [
    {
        'name': 'Home Solar Inverter 5kW',
        'slug': 'home-solar-inverter-5kw',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'Reliable inverter for residential solar homes.',
        'description': 'High-efficiency 5kW inverter designed for residential solar installations with stable backup performance.',
        'is_featured': True,
    },
    {
        'name': 'Residential Battery Pack 10kWh',
        'slug': 'residential-battery-pack-10kwh',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'Compact home energy storage unit.',
        'description': '10kWh lithium battery pack for home backup power and off-grid solar systems.',
        'is_featured': True,
    },
    {
        'name': 'Commercial Solar System 50kW',
        'slug': 'commercial-solar-system-50kW',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'Scalable solar solution for businesses.',
        'description': 'Complete 50kW commercial solar package with inverters, monitoring, and installation support.',
        'is_featured': True,
    },
    {
        'name': 'Office Backup Power Unit',
        'slug': 'office-backup-power-unit',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'Stable power for offices and retail spaces.',
        'description': 'Commercial-grade backup power system for offices, shops, and small business operations.',
        'is_featured': False,
    },
    {
        'name': 'Industrial Power Inverter 100kW',
        'slug': 'industrial-power-inverter-100kw',
        'category': ProductCategory.INDUSTRIAL,
        'short_description': 'Heavy-duty inverter for industrial sites.',
        'description': '100kW industrial inverter built for factories, plants, and large-scale operations.',
        'is_featured': True,
    },
    {
        'name': 'Factory Energy Storage Bank',
        'slug': 'factory-energy-storage-bank',
        'category': ProductCategory.INDUSTRIAL,
        'short_description': 'Large-capacity storage for industrial loads.',
        'description': 'Modular industrial battery bank for continuous power in demanding environments.',
        'is_featured': False,
    },
    {
        'name': 'ESS Hybrid Storage System',
        'slug': 'ess-hybrid-storage-system',
        'category': ProductCategory.ESS_SOLUTION,
        'short_description': 'Complete energy storage solution (ESS).',
        'description': 'Integrated ESS platform combining solar input, battery storage, and smart energy management.',
        'is_featured': True,
    },
    {
        'name': 'Grid-Tied ESS Package',
        'slug': 'grid-tied-ess-package',
        'category': ProductCategory.ESS_SOLUTION,
        'short_description': 'Smart ESS for grid-connected projects.',
        'description': 'Grid-tied energy storage system for optimized power use, peak shaving, and backup support.',
        'is_featured': False,
    },
]


class Command(BaseCommand):
    help = 'Seed sample products for all categories'

    def handle(self, *args, **options):
        created = 0
        for item in SAMPLE_PRODUCTS:
            _, was_created = Product.objects.update_or_create(
                slug=item['slug'],
                defaults=item,
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete. {created} new products added. Total: {Product.objects.count()}'
        ))
