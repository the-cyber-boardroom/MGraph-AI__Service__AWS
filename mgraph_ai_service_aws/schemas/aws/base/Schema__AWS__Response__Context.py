from typing                                                             import Optional
from mgraph_ai_service_aws.schemas.base.Schema__Response__Context       import Schema__Response__Context
from mgraph_ai_service_aws.schemas.aws.base.Enum__AWS__Error__Type      import Enum__AWS__Error__Type


class Schema__AWS__Response__Context(Schema__Response__Context):
    """AWS-specific response context with AWS metadata."""
    
    aws_request_id  : str                   = None      # AWS request ID from response metadata
    aws_http_status : int                   = None      # HTTP status from boto3 response
    retries         : int                   = 0         # Number of retries if any
    aws_error_type  : Enum__AWS__Error__Type = Enum__AWS__Error__Type.NONE
