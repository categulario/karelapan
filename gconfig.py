# -*- coding:utf-8 -*-
import multiprocessing
import os

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
preload_app = True #Carga el código de la aplicación antes de iniciar los trabajadores
# Disminuye el uso de RAM pero hace más lento el reinicio del servidor
daemon = True
pidfile = os.path.normpath(os.path.join(os.path.dirname(__file__),'gunicorn.pid'))
accesslog = os.path.normpath(os.path.join(os.path.dirname(__file__),'access.log'))
errorlog = os.path.normpath(os.path.join(os.path.dirname(__file__),'error.log'))
loglevel = 'info'
