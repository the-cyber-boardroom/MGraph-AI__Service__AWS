from enum import Enum


class Enum__Error__Type(str, Enum):
    """Base error types for service responses."""
    
    NONE                = "none"
    VALIDATION_ERROR    = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    NOT_FOUND           = "not_found"
    RATE_LIMITED        = "rate_limited"
    SERVER_ERROR        = "server_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    UNKNOWN_ERROR       = "unknown_error"
