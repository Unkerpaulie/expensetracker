#!/usr/bin/env python
"""
Environment Setup Helper Script
Helps you quickly switch between different deployment environments
"""

import os
import shutil
import sys

ENVIRONMENTS = {
    '1': ('local', '.env.local.example'),
    '2': ('railway', '.env.railway.example'),
    '3': ('pythonanywhere', '.env.pythonanywhere.example'),
}

def main():
    print("=" * 60)
    print("Django Expense Tracker - Environment Setup")
    print("=" * 60)
    print()
    print("Select the environment you want to configure:")
    print()
    print("1. Local Development (SQLite, Debug mode)")
    print("2. Railway (PostgreSQL, Gunicorn, WhiteNoise)")
    print("3. PythonAnywhere (SQLite/MySQL)")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice not in ENVIRONMENTS:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    
    env_name, template_file = ENVIRONMENTS[choice]
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print()
        print("Warning: .env file already exists!")
        overwrite = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("Cancelled. Your existing .env file was not modified.")
            sys.exit(0)
    
    # Copy the template
    if not os.path.exists(template_file):
        print(f"Error: Template file {template_file} not found!")
        sys.exit(1)
    
    shutil.copy(template_file, '.env')
    
    print()
    print(f"✓ Successfully created .env file for {env_name} environment!")
    print()
    print("Next steps:")
    print()
    
    if choice == '1':
        print("1. Review and edit .env if needed")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py createsuperuser")
        print("4. Run: python manage.py runserver")
    elif choice == '2':
        print("1. Edit .env and set your SECRET_KEY and RAILWAY_PUBLIC_DOMAIN")
        print("2. Set these variables in Railway dashboard:")
        print("   - Copy all variables from .env to Railway")
        print("3. Add PostgreSQL database in Railway")
        print("4. Deploy your code to Railway")
        print("5. Run migrations: railway run python manage.py migrate")
    elif choice == '3':
        print("1. Edit .env and set your SECRET_KEY and PYTHONANYWHERE_DOMAIN")
        print("2. Upload your code to PythonAnywhere")
        print("3. Configure WSGI file with environment variables")
        print("4. Run: python manage.py collectstatic")
        print("5. Run: python manage.py migrate")
        print("6. Reload your web app")
    
    print()
    print("For detailed instructions, see DEPLOYMENT.md")
    print()

if __name__ == '__main__':
    main()

