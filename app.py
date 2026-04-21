import logging
import os

from flask import Flask
from flask_cors import CORS

from src.utils.logging_utils import configure_logging


configure_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)

_origins_env = os.getenv('AGROGEST_CORS_ORIGINS', '*')
if _origins_env == '*':
  CORS(app)
else:
  CORS(app, resources={r'/*': {'origins': [o.strip() for o in _origins_env.split(',') if o.strip()]}})

# Route registration relies on `app` being defined; imported for side-effects.
from src.routes import *  # noqa: E402,F401,F403


if __name__ == '__main__':
  debug = os.getenv('AGROGEST_DEBUG', 'false').lower() in ('1', 'true', 'yes')
  host = os.getenv('AGROGEST_HOST', '0.0.0.0')
  port = int(os.getenv('AGROGEST_PORT', '3001'))
  logger.info('starting dev server host=%s port=%s debug=%s', host, port, debug)
  app.run(debug=debug, host=host, port=port)
