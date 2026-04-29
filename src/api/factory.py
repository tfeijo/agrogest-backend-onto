"""Application factory for the FastAPI service.

Mounts every resource router twice:
- without a prefix (legacy paths consumed by the mobile app today)
- under /api/v1 (versioned namespace for new clients)

Both surfaces share the same router instances, so behaviour is identical;
legacy callers can be migrated incrementally.
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import markdown

from src.api.errors import register_exception_handlers
from src.api.routers import (
    attributes,
    biomes,
    cities,
    farms,
    fullontology,
    parameters,
    productions,
    questions,
    states,
    sustainability,
)
from src.utils.logging_utils import configure_logging

logger = logging.getLogger(__name__)

LEGACY_ROUTERS = [
    cities.router,
    states.router,
    biomes.router,
    farms.router,
    productions.router,
    parameters.router,
    questions.router,
    attributes.router,
    fullontology.router,
    sustainability.router,
]


def _resolve_cors_origins() -> list[str] | str:
    raw = os.getenv('AGROGEST_CORS_ORIGINS', '*')
    if raw == '*':
        return ['*']
    return [o.strip() for o in raw.split(',') if o.strip()]


def create_app() -> FastAPI:
    """Build the FastAPI application instance.

    The function is import-safe: callers that need to spin up multiple
    instances (e.g. tests) can do so without polluting global state.
    """
    configure_logging()

    app = FastAPI(
        title='Agrogest Ambiental — Semantic backend',
        description=(
            'REST API serving the Agrogest @grogest_Ambiental decision '
            'support system. Powered by an OWL ontology (OntoGest) and the '
            'Pellet reasoner.'
        ),
        version='1.0.0',
        openapi_url='/openapi.json',
        docs_url='/docs',
        redoc_url='/redoc',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_resolve_cors_origins(),
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    register_exception_handlers(app)

    # README at root, rendered as HTML
    @app.get('/', response_class=HTMLResponse, include_in_schema=False)
    def readme() -> str:  # pragma: no cover - trivial
        readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'README.md')
        try:
            with open(readme_path, 'r', encoding='utf-8') as fh:
                return markdown.markdown(fh.read())
        except FileNotFoundError:
            return '<h1>Agrogest backend</h1><p>README.md not found.</p>'

    # Mount each router on both the legacy root namespace and /api/v1.
    for router in LEGACY_ROUTERS:
        app.include_router(router)
        app.include_router(router, prefix='/api/v1')

    logger.info('FastAPI app initialised: %d routers mounted on / and /api/v1', len(LEGACY_ROUTERS))
    return app
