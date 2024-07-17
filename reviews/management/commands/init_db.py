import psycopg2
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Initializes the PostgreSQL database if it does not exist and runs migrations'

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        try:
            conn = psycopg2.connect(
                dbname="postgres", 
                user=db_user, 
                password=db_password, 
                host=db_host, 
                port=db_port
            )
            conn.autocommit = True
            cursor = conn.cursor()

            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f'CREATE DATABASE {db_name}')
                self.stdout.write(self.style.SUCCESS(f'Database "{db_name}" created successfully'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Database "{db_name}" already exists'))

            cursor.close()
            conn.close()

            call_command('migrate')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
