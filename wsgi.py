"""WSGI entrypoint for production servers (gunicorn, uwsgi).

Usage:
  gunicorn -w 4 -b 0.0.0.0:3001 wsgi:app
"""
from app import app  # noqa: F401
