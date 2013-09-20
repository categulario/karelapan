# -*- coding:utf-8 -*-
import os
import psutil
from fabric.api import local, settings, abort, run, env
from fabric.contrib.console import confirm
from fabric.context_managers import cd, lcd, settings, hide

USER = 'covi'
HOST = 'covi.com.mx'
APP_NAME = 'karelapan'

# Host and login username:
env.hosts = ['%s@%s' % (USER, HOST)]

VENV_DIR = "/home/%s/portal/EntornoKarelapan"%USER
WSGI_MODULE = '%s.wsgi' % APP_NAME
DJANGO_APP_ROOT = os.path.join(VENV_DIR, APP_NAME)
GUNICORN_CONFIG = "%s/gconfig.py"%DJANGO_APP_ROOT
GUNICORN_PIDFILE = "%s/gunicorn.pid" % DJANGO_APP_ROOT
STATIC_ROOT = '/home/%s/webapps/%s_media/static' % (USER, APP_NAME)

def start():
    """Prepara todo para comenzar a trabajar"""
    local("git pull -u origin master")
    local("./dev_manage.py migrate")

def end():
    """Deja el directorio de trabajo en limpio para la siguiente sesión"""
    local("git add . && git commit")
    local("git push")

# REMOTO ###############################
def _l_is_webserver_running():
    """Averigua si está corriendo el servidor gunicorn"""
    try:
        pid = int(open(GUNICORN_PIDFILE).read().strip())
    except (IOError, OSError):
        return False
    for ps in psutil.process_iter():
        if ps.pid == pid and any('gunicorn' in c for c in ps.cmdline):
            return True
    return False

def lserver_start():
    """(remoto) Inicia el servidor"""
    local("%(venv_dir)s/bin/gunicorn -c %(config_file)s %(wsgimodule)s:application"%{
        'venv_dir': VENV_DIR,
        'config_file': GUNICORN_CONFIG,
        'wsgimodule': WSGI_MODULE
    })

def lserver_stop():
    """(remoto) Detiene el servidor"""
    local("kill $(cat %s)" % GUNICORN_PIDFILE)
    local("rm %s" % GUNICORN_PIDFILE)

def lensure_gunicorn(debug=False):
    """(remoto) asegura que gunicorn esté corriendo"""
    if not _l_is_webserver_running():
        lserver_start()
    elif debug:
        print "Gunicorn already runing"
# FIN REMOTO############################

def server_start():
    """Inicia el servidor"""
    run("%(venv_dir)s/bin/gunicorn -c %(config_file)s %(wsgimodule)s:application"%{
        'venv_dir': VENV_DIR,
        'config_file': GUNICORN_CONFIG,
        'wsgimodule': WSGI_MODULE
    })

def server_restart():
    """
    Restarts the webserver that is running the Django instance
    """
    try:
        run("kill -HUP $(cat %s)" % GUNICORN_PIDFILE)
    except:
        server_start()

def virtualenv(venv_dir):
    """
    Context manager that establishes a virtualenv to use.
    """
    return settings(venv=venv_dir)

def run_venv(command, **kwargs):
    """
    Runs a command in a virtualenv (which has been specified using
    the virtualenv context manager)
    """
    run("source %s/bin/activate" % env.venv + " && " + command, **kwargs)

def install_dependencies():
    """Instala las nuevas dependencias del paquete en el servidor remoto"""
    with virtualenv(VENV_DIR):
        with cd(DJANGO_APP_ROOT):
            run_venv("pip install -r requirements.txt")

def build_static():
    """Recolecta los archivos estáticos en remoto"""
    with virtualenv(VENV_DIR):
        with cd(DJANGO_APP_ROOT):
            run_venv("./manage.py collectstatic -v 0 --noinput --clear")
    run("chmod -R ugo+r %s" % STATIC_ROOT)

def migrate():
    """Corre las migraciones respectivas"""
    with virtualenv(VENV_DIR):
        with cd(DJANGO_APP_ROOT):
            run_venv("./manage.py migrate")

def pull():
    with cd(DJANGO_APP_ROOT):
        run("git pull")

def memory():
    """Monitorea la memoria usada"""
    run("ps -u %s -o rss,pid,comm"%USER)

def deploy():
    """Actualiza el servidor de producción"""
    pull()
    install_dependencies()
    build_static()
    migrate()
    server_restart()
