from typing                                                     import List, Optional
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from mgraph_ai_service_aws.schemas.base.Enum__HTTP__Status      import Enum__HTTP__Status
from mgraph_ai_service_aws.schemas.base.Enum__Error__Type       import Enum__Error__Type


class Schema__Response__Context(Type_Safe):
    """Standard response context with metadata about the request."""
    
    success     : bool                      = False
    status_code : Enum__HTTP__Status        = Enum__HTTP__Status.OK_200
    duration    : float                     = 0.0
    timestamp   : str                       = None
    messages    : List[str]                 = None
    errors      : List[str]                 = None
    error_type  : Enum__Error__Type         = Enum__Error__Type.NONE
