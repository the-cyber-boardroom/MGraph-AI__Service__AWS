from typing                                                                     import Dict, Optional, Any
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_aws.schemas.base.Schema__Request__Data                   import Schema__Request__Data
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Request__Base          import Schema__AWS__Request__Base
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__AWS__Lambda__Function_Name import Safe_Str__AWS__Lambda__Function_Name
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Enum__Lambda__Invocation_Type
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Enum__Lambda__Runtime
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Schema__AWS__Lambda__Code__Upload


# Request Data schemas (operation-specific payloads)

class Schema__Request__Data__Lambda__List(Schema__Request__Data):
    """Request data for listing Lambda functions."""
    max_items : int = 50
    marker    : str = None


class Schema__Request__Data__Lambda__Get(Schema__Request__Data):
    """Request data for getting a Lambda function."""
    function_name : Safe_Str__AWS__Lambda__Function_Name


class Schema__Request__Data__Lambda__Invoke(Schema__Request__Data):
    """Request data for invoking a Lambda function."""
    function_name   : Safe_Str__AWS__Lambda__Function_Name
    payload         : Dict[str, Any]                      = None
    invocation_type : Enum__Lambda__Invocation_Type       = Enum__Lambda__Invocation_Type.REQUEST_RESPONSE
    log_type        : str                                 = 'None'  # 'None' or 'Tail'


class Schema__Request__Data__Lambda__Create(Schema__Request__Data):
    """Request data for creating a Lambda function."""
    function_name : Safe_Str__AWS__Lambda__Function_Name
    runtime       : Enum__Lambda__Runtime
    role          : str                                   # IAM role ARN
    handler       : str                                   # e.g., "lambda_handler.handler"
    code          : Schema__AWS__Lambda__Code__Upload
    description   : str                                   = None
    timeout       : int                                   = 3       # Default 3 seconds
    memory_size   : int                                   = 128     # Default 128 MB
    environment   : Dict[str, str]                        = None


class Schema__Request__Data__Lambda__Update(Schema__Request__Data):
    """Request data for updating a Lambda function."""
    function_name : Safe_Str__AWS__Lambda__Function_Name
    code          : Schema__AWS__Lambda__Code__Upload     = None    # Update code
    description   : str                                   = None    # Update config
    timeout       : int                                   = None
    memory_size   : int                                   = None
    environment   : Dict[str, str]                        = None
    runtime       : Enum__Lambda__Runtime                 = None
    handler       : str                                   = None


class Schema__Request__Data__Lambda__Delete(Schema__Request__Data):
    """Request data for deleting a Lambda function."""
    function_name : Safe_Str__AWS__Lambda__Function_Name


# Full Request schemas (credentials + request data)

class Schema__AWS__Request__Lambda__List(Schema__AWS__Request__Base):
    """Full request for listing Lambda functions."""
    request_data : Schema__Request__Data__Lambda__List = None


class Schema__AWS__Request__Lambda__Get(Schema__AWS__Request__Base):
    """Full request for getting a Lambda function."""
    request_data : Schema__Request__Data__Lambda__Get


class Schema__AWS__Request__Lambda__Invoke(Schema__AWS__Request__Base):
    """Full request for invoking a Lambda function."""
    request_data : Schema__Request__Data__Lambda__Invoke


class Schema__AWS__Request__Lambda__Create(Schema__AWS__Request__Base):
    """Full request for creating a Lambda function."""
    request_data : Schema__Request__Data__Lambda__Create


class Schema__AWS__Request__Lambda__Update(Schema__AWS__Request__Base):
    """Full request for updating a Lambda function."""
    request_data : Schema__Request__Data__Lambda__Update


class Schema__AWS__Request__Lambda__Delete(Schema__AWS__Request__Base):
    """Full request for deleting a Lambda function."""
    request_data : Schema__Request__Data__Lambda__Delete
