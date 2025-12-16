import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__AWS__Access_Key_Id(Safe_Str):
    """AWS Access Key ID validator.
    
    Format: AKIA or ASIA prefix followed by 16 uppercase alphanumeric characters.
    - AKIA: Long-term IAM user credentials
    - ASIA: Temporary STS credentials (session tokens)
    
    Example: AKIAIOSFODNN7EXAMPLE or ASIAXXX...
    """
    regex             = re.compile(r'^(AKIA|ASIA)[A-Z0-9]{16}$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 20
    exact_length      = False  # Allow None/empty for Type_Safe defaults
    allow_empty       = True   # Allow None for Type_Safe defaults
