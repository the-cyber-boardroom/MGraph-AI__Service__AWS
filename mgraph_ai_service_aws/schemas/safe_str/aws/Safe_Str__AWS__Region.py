import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__AWS__Region(Safe_Str):
    """AWS Region validator.
    
    Format: {continent}-{location}-{number}
    Examples: us-east-1, eu-west-2, ap-southeast-1
    """
    regex             = re.compile(r'^[a-z]{2}-[a-z]+-[0-9]+$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 20
    allow_empty       = True
