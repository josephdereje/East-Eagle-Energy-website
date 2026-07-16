from django.core.management.base import BaseCommand

from blog.models import AboutMilestone, AboutPage, AboutValue

DEFAULT_VALUES = [
    {
        'icon': 'fa-globe',
        'title': 'Global Energy Access',
        'description': 'Deliver solar inverters, LiFePO4 batteries, and ESS solutions across residential, commercial, and industrial markets.',
        'display_order': 0,
    },
    {
        'icon': 'fa-shield-halved',
        'title': 'Reliability First',
        'description': 'Source and supply equipment from trusted global partners — Deye, Growatt, Pylontech, Jinko, and more.',
        'display_order': 1,
    },
    {
        'icon': 'fa-leaf',
        'title': 'Sustainable Future',
        'description': 'Accelerate the transition to renewable energy through smart storage, monitoring, and integrated power systems.',
        'display_order': 2,
    },
    {
        'icon': 'fa-handshake',
        'title': 'Partnership & Support',
        'description': 'Provide end-to-end consultation, installation support, and after-sales service for every project.',
        'display_order': 3,
    },
]

DEFAULT_MILESTONES = [
    {
        'year': '2022',
        'title': 'Company Founded',
        'description': 'East Eagle Energy established in Addis Ababa, Ethiopia — focusing on solar inverters and battery storage.',
        'display_order': 0,
    },
    {
        'year': '2023',
        'title': 'Commercial & Industrial Expansion',
        'description': 'Expanded into C & I BESS solutions, partnering with leading global manufacturers.',
        'display_order': 1,
    },
    {
        'year': '2024',
        'title': 'Global Reach',
        'description': 'Extended operations across Africa, China, Dubai, Israel, and North America.',
        'display_order': 2,
    },
    {
        'year': '2025+',
        'title': 'Full Energy Ecosystem',
        'description': 'Launching EV chargers, solar panels, smart energy management, and cloud monitoring solutions.',
        'display_order': 3,
    },
]


class Command(BaseCommand):
    help = 'Seed About page content (hero, values, milestones)'

    def handle(self, *args, **options):
        AboutPage.load()

        values_created = 0
        for item in DEFAULT_VALUES:
            _, was_created = AboutValue.objects.update_or_create(
                title=item['title'],
                defaults={**item, 'is_active': True},
            )
            if was_created:
                values_created += 1

        milestones_created = 0
        for item in DEFAULT_MILESTONES:
            _, was_created = AboutMilestone.objects.update_or_create(
                year=item['year'],
                title=item['title'],
                defaults={**item, 'is_active': True},
            )
            if was_created:
                milestones_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'About page seeded. Values: {AboutValue.objects.count()} ({values_created} new). '
            f'Milestones: {AboutMilestone.objects.count()} ({milestones_created} new). '
            f'Edit in Admin → About Page / About Values / About Milestones.'
        ))
