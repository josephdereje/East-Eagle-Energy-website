from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from blog.models import HeroSlide

HERO_IMAGES_DIR = Path(settings.BASE_DIR) / 'images' / 'hero'

DEFAULT_SLIDES = [
    {
        'eyebrow': 'Est. 2022 · Global Energy Solutions',
        'title': 'Energy That Never Grows Weary',
        'subtitle': 'Dependable solar power, inverters, and battery storage for homes and businesses worldwide.',
        'gradient': 'linear-gradient(135deg, #1B365D 0%, #2E6EB3 50%, #F39200 100%)',
        'image_file': 'slide-solar.jpg',
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
        'image_file': 'slide-farm.jpg',
        'primary_btn_text': 'Our Services',
        'primary_btn_url': '/#services',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 1,
    },
    {
        'eyebrow': 'Energy Storage Systems',
        'title': 'Stable Energy Storage',
        'subtitle': 'LiFePO4 batteries and ESS solutions built to store, manage, and deliver power through every condition.',
        'gradient': 'linear-gradient(135deg, #1B365D 0%, #2E6EB3 50%, #F39200 100%)',
        'image_file': 'slide-battery.jpg',
        'primary_btn_text': 'Explore ESS',
        'primary_btn_url': '/products/ess/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 2,
    },
    {
        'eyebrow': 'Grid & Commercial',
        'title': 'Clean Power at Scale',
        'subtitle': 'Integrated solar, storage, and grid solutions for commercial and industrial projects worldwide.',
        'gradient': 'linear-gradient(135deg, #0d1f35 0%, #1B365D 60%, #2E6EB3 100%)',
        'image_file': 'slide-grid.jpg',
        'primary_btn_text': 'Get a Quote',
        'primary_btn_url': '/contact/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 3,
    },
    {
        'eyebrow': 'Residential Solutions',
        'title': 'Solar For Every Home',
        'subtitle': 'Rooftop solar systems that cut bills, boost independence, and keep your family powered day and night.',
        'gradient': 'linear-gradient(135deg, #1B365D 0%, #2E6EB3 45%, #FFCB05 100%)',
        'image_file': 'slide-rooftop.jpg',
        'primary_btn_text': 'View Products',
        'primary_btn_url': '/products/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 4,
    },
    {
        'eyebrow': 'Smart Inverters',
        'title': 'Convert Power Intelligently',
        'subtitle': 'Hybrid and string inverters from trusted global partners — built for efficiency and long-term performance.',
        'gradient': 'linear-gradient(135deg, #142E4B 0%, #2E6EB3 55%, #F39200 100%)',
        'image_file': 'slide-inverter.jpg',
        'primary_btn_text': 'Browse Inverters',
        'primary_btn_url': '/products/inverters/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 5,
    },
    {
        'eyebrow': 'Sustainable Future',
        'title': 'Harness The Sun',
        'subtitle': 'From sunrise to sunset — capture clean energy and store it for when you need it most.',
        'gradient': 'linear-gradient(135deg, #0d1f35 0%, #F39200 50%, #FFCB05 100%)',
        'image_file': 'slide-sunset.jpg',
        'primary_btn_text': 'Learn More',
        'primary_btn_url': '/about/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 6,
    },
    {
        'eyebrow': 'Expert Installation',
        'title': 'Built Right, Built To Last',
        'subtitle': 'Professional design, installation, and commissioning — from rooftop arrays to full ESS deployments across Africa and beyond.',
        'gradient': 'linear-gradient(135deg, #142E4B 0%, #1B365D 55%, #2E6EB3 100%)',
        'image_file': 'slide-install.jpg',
        'primary_btn_text': 'Our Services',
        'primary_btn_url': '/#services',
        'secondary_btn_text': 'Get a Quote',
        'secondary_btn_url': '/contact/',
        'display_order': 7,
    },
    {
        'eyebrow': 'EV & Future Mobility',
        'title': 'Charge With Clean Energy',
        'subtitle': 'Pair solar and battery storage with EV charging — power your vehicles from the sun and cut fuel costs for good.',
        'gradient': 'linear-gradient(135deg, #0d1f35 0%, #2E6EB3 50%, #FFCB05 100%)',
        'image_file': 'slide-evcharge.jpg',
        'primary_btn_text': 'Explore Solutions',
        'primary_btn_url': '/products/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 8,
    },
    {
        'eyebrow': 'Commercial & Industrial',
        'title': 'Enterprise-Grade Solar',
        'subtitle': 'Cut operating costs and meet sustainability goals with tailored C&I systems — engineered for performance at scale.',
        'gradient': 'linear-gradient(135deg, #1B365D 0%, #142E4B 50%, #F39200 100%)',
        'image_file': 'slide-commercial.jpg',
        'primary_btn_text': 'Get a Quote',
        'primary_btn_url': '/contact/',
        'secondary_btn_text': 'About Us',
        'secondary_btn_url': '/about/',
        'display_order': 9,
    },
    {
        'eyebrow': 'Premium Components',
        'title': 'World-Class Solar Panels',
        'subtitle': 'Tier-1 modules from leading manufacturers — high efficiency, proven reliability, and warranties you can trust.',
        'gradient': 'linear-gradient(135deg, #142E4B 0%, #2E6EB3 60%, #FFCB05 100%)',
        'image_file': 'slide-panels.jpg',
        'primary_btn_text': 'View Panels',
        'primary_btn_url': '/products/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 10,
    },
    {
        'eyebrow': 'Off-Grid Solutions',
        'title': 'Power Where The Grid Cannot Reach',
        'subtitle': 'Standalone solar and battery systems for remote homes, farms, and communities — reliable energy, anywhere.',
        'gradient': 'linear-gradient(135deg, #0d1f35 0%, #1B365D 45%, #F39200 100%)',
        'image_file': 'slide-offgrid.jpg',
        'primary_btn_text': 'Explore ESS',
        'primary_btn_url': '/products/ess/',
        'secondary_btn_text': 'Contact Us',
        'secondary_btn_url': '/contact/',
        'display_order': 11,
    },
]


class Command(BaseCommand):
    help = 'Seed homepage hero slides with background images'

    def handle(self, *args, **options):
        created = 0
        for item in DEFAULT_SLIDES:
            image_file = item.pop('image_file', None)
            slide, was_created = HeroSlide.objects.update_or_create(
                title=item['title'],
                defaults={**item, 'is_active': True},
            )
            if was_created:
                created += 1

            if image_file:
                image_path = HERO_IMAGES_DIR / image_file
            if image_path.exists():
                if not slide.image:
                    with image_path.open('rb') as fh:
                        slide.image.save(image_file, File(fh), save=True)
                elif not (HERO_IMAGES_DIR / image_file).exists():
                    with image_path.open('rb') as fh:
                        slide.image.save(image_file, File(fh), save=True)
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Missing image: {image_path}'
                    ))

        self.stdout.write(self.style.SUCCESS(
            f'Hero slides seeded. {created} new, total: {HeroSlide.objects.count()}. '
            f'Edit slides in Admin → Hero Slides.'
        ))
