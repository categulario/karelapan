# -*- coding:utf-8 -*-
import multiprocessing
import os

_debug = os.environ.get('DJANGO_SETTINGS_MODULE', 'karelapan.settings').endswith('dev')

bind = "/tmp/gunicorn.sock" # "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
preload_app = True
daemon = not _debug
pidfile = os.path.normpath(os.path.join(os.path.dirname(__file__), 'gunicorn.pid'))
accesslog = os.path.normpath(os.path.join(os.path.dirname(__file__), 'access.log'))
errorlog = os.path.normpath(os.path.join(os.path.dirname(__file__), 'error.log'))
loglevel = 'info'
