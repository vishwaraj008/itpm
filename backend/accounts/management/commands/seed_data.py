from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Seeds the database with initial users and data'

    def handle(self, *args, **options):
        users_data = [
            {
                'email': 'admin@cems.com',
                'password': 'admin123',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'role': 'admin',
                'department': 'Academic Management',
            },
            {
                'email': 'faculty1@cems.com',
                'password': 'faculty123',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'role': 'faculty',
                'department': 'Computer Science',
            },
            {
                'email': 'student1@cems.com',
                'password': 'student123',
                'first_name': 'Rohan',
                'last_name': 'Patel',
                'role': 'student',
                'department': 'Information Technology',
            },
        ]

        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['email'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password(data['password'])
                user.save()
                user.userprofile.role = data['role']
                user.userprofile.department = data['department']
                user.userprofile.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Created {data['role']}: {data['email']} (password: {data['password']})"
                ))
            else:
                self.stdout.write(self.style.WARNING(f"User {data['email']} already exists."))

        self.stdout.write(self.style.SUCCESS('\n✓ Seed data loaded successfully!'))
