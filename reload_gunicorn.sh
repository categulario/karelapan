kill $(cat gunicorn.pid) && gunicorn -c gconfig.py wsgi:app
