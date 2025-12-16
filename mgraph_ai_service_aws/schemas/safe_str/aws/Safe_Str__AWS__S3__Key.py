import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__AWS__S3__Key(Safe_Str):
    """AWS S3 Object Key validator.
    
    S3 object keys can contain most characters but we restrict to safe ones:
    - Letters, numbers, hyphens, underscores, dots, slashes
    - Max 1024 bytes (UTF-8)
    
    Examples: folder/file.txt, data/2024/01/report.json
    """
    regex             = re.compile(r'^[a-zA-Z0-9_\-./]+$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 1024
    allow_empty       = True
