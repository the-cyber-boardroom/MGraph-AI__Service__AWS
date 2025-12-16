from typing                                 import Dict, List, Optional, Any
from enum                                   import Enum
from osbot_utils.type_safe.Type_Safe        import Type_Safe


class Enum__Lambda__Invocation_Type(str, Enum):
    """Lambda invocation types."""
    REQUEST_RESPONSE = 'RequestResponse'  # Synchronous
    EVENT            = 'Event'            # Asynchronous
    DRY_RUN          = 'DryRun'           # Validate only


class Enum__Lambda__Runtime(str, Enum):
    """Supported Lambda runtimes."""
    PYTHON_3_9   = 'python3.9'
    PYTHON_3_10  = 'python3.10'
    PYTHON_3_11  = 'python3.11'
    PYTHON_3_12  = 'python3.12'
    PYTHON_3_13  = 'python3.13'
    NODEJS_18_X  = 'nodejs18.x'
    NODEJS_20_X  = 'nodejs20.x'
    JAVA_11      = 'java11'
    JAVA_17      = 'java17'
    JAVA_21      = 'java21'
    DOTNET_6     = 'dotnet6'
    DOTNET_8     = 'dotnet8'
    PROVIDED_AL2 = 'provided.al2'
    PROVIDED_AL2023 = 'provided.al2023'


class Schema__AWS__Lambda__Function__Summary(Type_Safe):
    """Summary of a Lambda function (from list operation)."""
    function_name : str  = None
    function_arn  : str  = None
    runtime       : str  = None
    handler       : str  = None
    code_size     : int  = 0
    memory_size   : int  = 0
    timeout       : int  = 0
    last_modified : str  = None
    state         : str  = None
    description   : str  = None


class Schema__AWS__Lambda__Configuration(Type_Safe):
    """Full Lambda function configuration."""
    function_name     : str       = None
    function_arn      : str       = None
    runtime           : str       = None
    role              : str       = None
    handler           : str       = None
    code_size         : int       = 0
    description       : str       = None
    timeout           : int       = 0
    memory_size       : int       = 0
    last_modified     : str       = None
    code_sha256       : str       = None
    version           : str       = None
    environment       : Dict[str, str] = None
    state             : str       = None
    state_reason      : str       = None
    state_reason_code : str       = None
    architectures     : List[str] = None


class Schema__AWS__Lambda__Code__Location(Type_Safe):
    """Lambda function code location."""
    repository_type : str = None
    location        : str = None


class Schema__AWS__Lambda__Code__Upload(Type_Safe):
    """Lambda function code for create/update (ZIP bytes as base64)."""
    zip_file       : str = None     # Base64-encoded ZIP
    s3_bucket      : str = None     # Or use S3
    s3_key         : str = None
    s3_object_version : str = None


class Schema__AWS__Lambda__Invoke__Result(Type_Safe):
    """Result of Lambda invocation."""
    status_code      : int       = None     # Lambda response status (200, 202, etc.)
    payload          : Dict[str, Any] = None  # Response payload (if sync)
    function_error   : str       = None     # Error type if function failed
    log_result       : str       = None     # Base64 encoded logs (if LogType=Tail)
    executed_version : str       = None     # Version that was invoked
