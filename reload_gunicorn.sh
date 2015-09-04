#!/usr/bin/bash
kill $(cat gunicorn.pid) && ../bin/gunicorn -c gconfig_dev.py karelapan.wsgi:application
