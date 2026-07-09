from django.core.management.base import BaseCommand

from products.models import ProductSidebarSection, ProductCategory


SIDEBAR_SECTIONS = [
    {
        'category': ProductCategory.RESIDENTIAL,
        'title': 'Residential Energy Storage',
        'description': 'Complete battery energy storage systems for homes. Choose from Low Voltage (modular, scalable) or High Voltage (high-capacity) solutions.',
        'display_order': 1,
        'is_active': True,
    },
    {
        'category': ProductCategory.C_AND_I_BESS,
        'title': 'Commercial & Industrial BESS',
        'description': 'High-power battery energy storage systems for businesses, factories, and large-scale installations. Reduce operating costs and ensure uninterrupted power.',
        'display_order': 2,
        'is_active': True,
    },
    {
        'category': ProductCategory.ESS_SOLUTION,
        'title': 'Complete ESS Solutions',
        'description': 'All-in-one energy storage systems combining inverter, battery, and smart management in a single integrated package.',
        'display_order': 3,
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Create product sidebar sections'

    def handle(self, *args, **options):
        created = 0
        
        for item in SIDEBAR_SECTIONS:
            obj, was_created = ProductSidebarSection.objects.update_or_create(
                category=item['category'],
                defaults=item,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created sidebar for {obj.get_category_display()}'))
            else:
                self.stdout.write(f'  Updated sidebar for {obj.get_category_display()}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSidebar sections complete! {created} new, {ProductSidebarSection.objects.count()} total'
        ))
