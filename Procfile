web: gunicorn --workers 2 -k gevent app:app -b 0.0.0.0:$PORT --log-level=debug
worker: python worker.py