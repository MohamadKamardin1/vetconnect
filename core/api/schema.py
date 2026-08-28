ERROR_ENVELOPE_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "example": "validation_error"},
                "message": {"type": "string", "example": "Request validation failed."},
                "fields": {"type": "object", "additionalProperties": True, "nullable": True},
            },
            "required": ["code", "message"],
        }
    },
    "required": ["error"],
}

COMMON_ERROR_RESPONSE_DESCRIPTIONS = {
    "400": "Validation failed or the request could not be parsed.",
    "401": "Authentication credentials were not provided or are invalid.",
    "403": "The authenticated user does not have permission to perform this action.",
    "404": "The requested resource does not exist.",
    "429": "The request was throttled. Retry after the interval given by the Retry-After header.",
    "500": "An unexpected internal error occurred.",
}


def add_common_error_responses(result, generator, request, public):
    """
    drf-spectacular postprocessing hook. Every error response across this API uses the same JSON
    envelope (core.api.exceptions.api_exception_handler: {"error": {"code", "message", "fields?"}}).
    Register that shape once as a shared component and reference it from every operation for the
    status codes it doesn't already document, so the schema explains error shapes as completely as
    success shapes without hand-annotating every view. Never overwrites a response an operation
    already defines (e.g. a 404 a view documents with more specific detail), and never touches
    anything outside "responses" on real operations.
    """
    schemas = result.setdefault("components", {}).setdefault("schemas", {})
    schemas.setdefault("ErrorEnvelope", ERROR_ENVELOPE_SCHEMA)
    schema_ref = {"$ref": "#/components/schemas/ErrorEnvelope"}

    for path_item in result.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if not isinstance(operation, dict) or "responses" not in operation:
                continue
            responses = operation["responses"]
            for status_code, description in COMMON_ERROR_RESPONSE_DESCRIPTIONS.items():
                if status_code in responses:
                    continue
                responses[status_code] = {"description": description, "content": {"application/json": {"schema": schema_ref}}}
    return result
