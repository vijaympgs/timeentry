#!/usr/bin/env python
import os
import sys
import django

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User

def reset_admin_password():
    try:
        # Check if admin user exists
        user = User.objects.get(username='admin')
        print(f"Admin user found: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is active: {user.is_active}")
        print(f"Is staff: {user.is_staff}")
        print(f"Is superuser: {user.is_superuser}")
        
        # Reset password
        user.set_password('admin123')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        print("\nPassword reset successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Login URL: http://localhost:8000/admin/")
        
    except User.DoesNotExist:
        print("Admin user not found. Creating new admin user...")
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Login URL: http://localhost:8000/admin/")

if __name__ == '__main__':
    reset_admin_password()
