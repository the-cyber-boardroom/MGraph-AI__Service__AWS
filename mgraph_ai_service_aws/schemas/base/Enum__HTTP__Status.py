from enum import Enum


class Enum__HTTP__Status(int, Enum):
    """HTTP status codes used by the service."""
    
    OK_200                    = 200
    CREATED_201               = 201
    ACCEPTED_202              = 202
    NO_CONTENT_204            = 204
    BAD_REQUEST_400           = 400
    UNAUTHORIZED_401          = 401
    FORBIDDEN_403             = 403
    NOT_FOUND_404             = 404
    METHOD_NOT_ALLOWED_405    = 405
    CONFLICT_409              = 409
    GONE_410                  = 410
    UNPROCESSABLE_ENTITY_422  = 422
    RATE_LIMITED_429          = 429
    SERVER_ERROR_500          = 500
    NOT_IMPLEMENTED_501       = 501
    SERVICE_UNAVAILABLE_503   = 503
