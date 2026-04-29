"""Global exception handlers wired into the FastAPI application.

Every error path returns a structured JSON object with ``error`` and
optional ``msg`` keys, matching the legacy Flask responses so the mobile
app keeps deserialising errors the same way.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from owlready2 import OwlReadyError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, dict):
            payload = detail
        else:
            payload = {'error': str(detail)}
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'error': 'Validation error', 'details': exc.errors()},
        )

    @app.exception_handler(OwlReadyError)
    async def owlready_exception_handler(_request: Request, exc: OwlReadyError) -> JSONResponse:
        logger.exception('OwlReady error while handling request')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': 'Ontology operation failed', 'msg': str(exc)},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
        logger.exception('Unhandled error while handling request')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'error': 'Internal server error', 'msg': str(exc)},
        )
