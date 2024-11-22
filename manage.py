#!/usr/bin/env python
# Django's command-line utility for administrative tasks like migrations, runserver, etc.
import os
import sys


def main():
    # Set the default Django settings module for the 'server' project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        # Import Django's command-line management module
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error message if Django isn't installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command passed via command line (e.g., runserver, migrate, etc.)
    execute_from_command_line(sys.argv)


# Only run the main() function if this script is executed directly
if __name__ == '__main__':
    main()
