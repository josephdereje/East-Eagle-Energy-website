import os
import traceback

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Run deployment diagnostics and save results to diagnostic_output.txt'

    def handle(self, *args, **options):
        lines = ['=== East Eagle Energy — Site Diagnostics ===', '']

        def add(line=''):
            lines.append(str(line))
            self.stdout.write(str(line))

        add(f'Project folder: {settings.BASE_DIR}')
        add(f'Settings module: {os.environ.get("DJANGO_SETTINGS_MODULE")}')
        add(f'DEBUG: {settings.DEBUG}')
        add(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        add(f'Database: {settings.DATABASES["default"]["NAME"]}')
        add('')

        env_path = settings.BASE_DIR / '.env'
        add(f'.env exists: {env_path.exists()}')
        add('')

        try:
            call_command('check')
            add('Django check: OK')
        except Exception as exc:
            add(f'Django check: FAILED — {exc}')

        add('')
        add('Migrations:')
        try:
            call_command('showmigrations', '--list')
        except Exception as exc:
            add(f'showmigrations failed: {exc}')

        add('')
        add('Database tables:')
        try:
            tables = connection.introspection.table_names()
            for name in sorted(tables):
                add(f'  - {name}')
        except Exception as exc:
            add(f'Could not list tables: {exc}')

        add('')
        add('Homepage test:')
        try:
            from django.test import Client
            client = Client()
            response = client.get('/')
            add(f'  Status code: {response.status_code}')
            if response.status_code != 200:
                add(f'  Response preview: {response.content[:300]!r}')
        except Exception:
            add('  Homepage test FAILED:')
            add(traceback.format_exc())

        add('')
        add('Health check test:')
        try:
            from django.test import Client
            client = Client()
            response = client.get('/health/')
            add(f'  Status code: {response.status_code}')
        except Exception as exc:
            add(f'  Health check FAILED — {exc}')

        output_path = settings.BASE_DIR / 'diagnostic_output.txt'
        output_path.write_text('\n'.join(lines), encoding='utf-8')
        add('')
        add(f'Results saved to: {output_path}')
