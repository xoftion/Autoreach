from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Creates an admin user from environment variables if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@xoftion.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Admin user {username} already exists')
            )
