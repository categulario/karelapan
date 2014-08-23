#!/usr/bin/env python
import os
import sys
import platform

ENVS_MAPPING = {
    'dev': [
        'abraham-master',
    ]
}

if __name__ == "__main__":
    hostname = platform.node()

    for env, hosts in ENVS_MAPPING.iteritems():
        if hostname in hosts:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "karelapan.settings_" + env)
            break
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "karelapan.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
