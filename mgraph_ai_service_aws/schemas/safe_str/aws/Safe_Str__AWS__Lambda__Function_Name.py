import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__AWS__Lambda__Function_Name(Safe_Str):
    """AWS Lambda Function Name validator.
    
    Format: Letters, numbers, hyphens, underscores. 1-64 characters.
    Can also be a full ARN or partial ARN.
    
    Examples: 
    - my-function
    - my_function_v2
    - arn:aws:lambda:us-east-1:123456789012:function:my-function
    """
    regex             = re.compile(r'^[a-zA-Z0-9_-]+$|^arn:aws:lambda:[a-z0-9-]+:[0-9]+:function:[a-zA-Z0-9_-]+$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 170  # ARN can be up to 170 chars
    allow_empty       = True
