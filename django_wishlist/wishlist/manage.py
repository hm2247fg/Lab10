#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Set the DJANGO_SETTINGS_MODULE environment variable to 'wishlist.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wishlist.settings')
    try:
        # Import execute_from_command_line function from Django's management module
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise ImportError with a helpful message if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute Django management commands from the command line arguments
    execute_from_command_line(sys.argv)


# Call the main function if this script is executed directly
if __name__ == '__main__':
    main()
