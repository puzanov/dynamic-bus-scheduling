#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "route_generator_server.settings")

    from django.core.management import execute_from_command_line

    # execute_from_command_line([os.path.join(os.path.dirname(__file__), 'manage.py'), 'runserver'])
    execute_from_command_line(sys.argv)
