from django.core.management.base import BaseCommand

from blog.models import HeroSlide


DEFAULT_SLIDES = [
    {
        'eyebrow': 'Est. 2022 · Global Energy Solutions',
        'title': 'Energy That Never Grows Weary',
        'subtitle': 'Dependable solar power, inverters, and battery storage for homes and businesses worldwide.',
        'gradient': 'linear-gradient(135deg, #1B365D 0%, #2E6EB3 50%, #F39200 100%)',
        'primary_btn_text': 'View Products',
        'primary_btn_url': '/products/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 0,
    },
    {
        'eyebrow': 'Solar Energy Systems',
        'title': 'Power You Can Rely On',
        'subtitle': 'Comprehensive solar solutions designed for consistent, resilient energy — even when the grid fails.',
        'gradient': 'linear-gradient(135deg, #142E4B 0%, #1B365D 50%, #FFCB05 100%)',
        'primary_btn_text': 'Our Services',
        'primary_btn_url': '/#services',
        'secondary_btn_text': '',
        'secondary_btn_url': '',
        'display_order': 1,
    },
    {
        'eyebrow': 'Energy Storage Systems',
        'title': 'Stable Energy Storage',
        'subtitle': 'LiFePO4 batteries and ESS solutions built to store, manage, and deliver power through every condition.',
        'gradient': 'linear-gradient(135deg, #1B365D 0%, #2E6EB3 50%, #F39200 100%)',
        'primary_btn_text': 'Explore ESS',
        'primary_btn_url': '/products/ess/',
        'secondary_btn_text': '',
        'secondary_btn_url': '',
        'display_order': 2,
    },
]


class Command(BaseCommand):
    help = 'Seed default homepage hero slides (upload images via admin)'

    def handle(self, *args, **options):
        created = 0
        for item in DEFAULT_SLIDES:
            _, was_created = HeroSlide.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Hero slides seeded. {created} new, total: {HeroSlide.objects.count()}. '
            f'Upload images in Admin → Hero Slides.'
        ))
