from enum import Enum


class Enum__AWS__Error__Type(str, Enum):
    """AWS-specific error types mapped from boto3 exceptions."""
    
    NONE                    = "none"
    INVALID_CREDENTIALS     = "invalid_credentials"
    EXPIRED_CREDENTIALS     = "expired_credentials"
    ACCESS_DENIED           = "access_denied"
    RESOURCE_NOT_FOUND      = "resource_not_found"
    THROTTLING              = "throttling"
    SERVICE_UNAVAILABLE     = "service_unavailable"
    VALIDATION_ERROR        = "validation_error"
    DECRYPTION_FAILED       = "decryption_failed"
    AWS_API_ERROR           = "aws_api_error"
