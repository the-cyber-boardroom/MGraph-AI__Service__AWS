import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__AWS__S3__Bucket_Name(Safe_Str):
    """AWS S3 Bucket Name validator.
    
    Rules:
    - 3-63 characters long
    - Lowercase letters, numbers, hyphens, periods
    - Must start and end with letter or number
    - Cannot be formatted as IP address
    - Cannot contain consecutive periods
    - Cannot contain hyphens adjacent to periods
    
    Examples: my-bucket, my.bucket.name, bucket123
    """
    regex             = re.compile(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 63
    allow_empty       = True
