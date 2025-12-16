import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__AWS__Account_Id(Safe_Str):
    """AWS Account ID validator.
    
    Format: Exactly 12 digits.
    Example: 123456789012
    """
    regex             = re.compile(r'^[0-9]{12}$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 12
    exact_length      = True
    allow_empty       = True
