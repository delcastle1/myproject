# myapp/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates groups in the Django application'

    def handle(self, *args, **kwargs):
        # Define the groups you want to create
        groups = [
            {'name': 'preacher', 'permissions': []},
            {'name': 'artist', 'permissions': []},
            {'name': 'admin', 'permissions': []},
        ]

        # Create each group if it doesn't already exist
        for group_data in groups:
            group, created = Group.objects.get_or_create(name=group_data['name'])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Group '{group.name}' created successfully."))
            else:
                self.stdout.write(f"Group '{group.name}' already exists.")

