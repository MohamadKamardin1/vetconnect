import logging
from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    response = exception_handler(exc, context)
    if response is None:
        logger.exception("Unhandled API exception", extra={"view": str(context.get("view"))})
        return Response({"error": {"code": "internal_error", "message": "An internal error occurred."}}, status=500)

    detail = response.data
    if isinstance(detail, dict) and "detail" in detail:
        message = str(detail["detail"])
        code = getattr(exc, "default_code", "api_error")
        payload = {"code": code, "message": message}
    else:
        payload = {"code": "validation_error", "message": "Request validation failed.", "fields": detail}
    response.data = {"error": payload}
    return response
