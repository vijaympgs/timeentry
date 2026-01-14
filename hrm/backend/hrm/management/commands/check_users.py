from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check all Django users in the system'

    def handle(self, *args, **options):
        users = User.objects.all()
        self.stdout.write(f'Total users: {users.count()}')
        
        if users.count() == 0:
            self.stdout.write(self.style.WARNING('No users found in the system'))
            return
        
        for user in users:
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'  Email: {user.email or "None"}')
            self.stdout.write(f'  Staff: {user.is_staff}')
            self.stdout.write(f'  Superuser: {user.is_superuser}')
            self.stdout.write(f'  Active: {user.is_active}')
            self.stdout.write('---')
