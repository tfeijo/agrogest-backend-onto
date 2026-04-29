"""FastAPI package — application factory and Pydantic schemas live here.

The package replaces the previous Flask-based ``app.py`` + ``src/routes.py``
entry-point pair. The flat ``app.py`` and ``src/routes.py`` modules are kept
as thin shims that re-export the FastAPI ``app`` instance for backwards
compatibility with any existing tooling that imported them by name.
"""
from src.api.factory import create_app

app = create_app()

__all__ = ['app', 'create_app']
