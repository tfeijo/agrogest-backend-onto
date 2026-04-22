"""Structured logging helpers.

Provides:
- configure_logging(): sets up a single-line formatter with correlation-id
  support, driven by env vars AGROGEST_LOG_LEVEL and AGROGEST_LOG_FORMAT
  ('text' or 'json').
- time_reasoner(stage): context manager that logs elapsed milliseconds for
  each reasoning phase (load, classify, save). Used by controllers that
  call sync_reasoner_pellet.
"""
import json
import logging
import os
import time
from contextlib import contextmanager
from typing import Iterator, Optional


class _JsonFormatter(logging.Formatter):
  def format(self, record: logging.LogRecord) -> str:
    payload = {
      'ts': self.formatTime(record, '%Y-%m-%dT%H:%M:%S'),
      'level': record.levelname,
      'logger': record.name,
      'msg': record.getMessage(),
    }
    if record.exc_info:
      payload['exc_info'] = self.formatException(record.exc_info)
    # Attach any extra fields (e.g. stage=, elapsed_ms=).
    for key, value in record.__dict__.items():
      if key in {
        'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
        'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
        'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
        'processName', 'process', 'message', 'asctime',
      }:
        continue
      payload[key] = value
    return json.dumps(payload, default=str)


def configure_logging() -> None:
  level = os.getenv('AGROGEST_LOG_LEVEL', 'INFO').upper()
  fmt = os.getenv('AGROGEST_LOG_FORMAT', 'text').lower()
  root = logging.getLogger()
  # Reset handlers to make configure_logging idempotent (important under gunicorn).
  for handler in list(root.handlers):
    root.removeHandler(handler)
  handler = logging.StreamHandler()
  if fmt == 'json':
    handler.setFormatter(_JsonFormatter())
  else:
    handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s %(name)s - %(message)s'
    ))
  root.addHandler(handler)
  root.setLevel(level)


@contextmanager
def time_reasoner(stage: str, logger: Optional[logging.Logger] = None) -> Iterator[None]:
  log = logger or logging.getLogger('agrogest.reasoner')
  start = time.perf_counter()
  try:
    yield
  finally:
    elapsed_ms = (time.perf_counter() - start) * 1000
    log.info('reasoner stage finished', extra={'stage': stage, 'elapsed_ms': round(elapsed_ms, 2)})
