#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
<<<<<<< HEAD

from dotenv import load_dotenv
=======
import dotenv
>>>>>>> cce2f4e6f4a912d2a6500ee1dcb56d829199844e


def main():
    """Run administrative tasks."""
    load_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebMark.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
