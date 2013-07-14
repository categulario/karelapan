# -*- coding:utf-8 -*-
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
preload_app = False #Carga el código de la aplicación antes de iniciar los trabajadores
# Disminuye el uso de RAM pero hace más lento el reinicio del servidor
daemon = False
pidfile = '/home/abraham/Desarrollo/django/KarelapanDjango/gunicorn.pid'
accesslog = '/home/abraham/Desarrollo/django/KarelapanDjango/access.log'
errorlog = '/home/abraham/Desarrollo/django/KarelapanDjango/error.log'
loglevel = 'info'
