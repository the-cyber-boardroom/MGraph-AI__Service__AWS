from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response__Context import Schema__AWS__Response__Context
from mgraph_ai_service_aws.schemas.base.Schema__Response__Data          import Schema__Response__Data


class Schema__AWS__Response(Type_Safe):
    """Base AWS response schema with context and data."""
    
    response_context : Schema__AWS__Response__Context = None
    response_data    : Schema__Response__Data         = None
