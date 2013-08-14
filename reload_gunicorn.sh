kill $(cat gunicorn.pid) && ../bin/gunicorn -c gconfig.py wsgi:app
