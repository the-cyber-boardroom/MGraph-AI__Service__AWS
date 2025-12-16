import re
from osbot_utils.type_safe.primitives.core.Safe_Str                        import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode


class Safe_Str__Encrypted_Value(Safe_Str):
    """Encrypted value validator (Base64-encoded NaCl sealed box).
    
    Format: Base64-encoded string with URL-safe characters.
    NaCl SealedBox encrypted values are typically around 48+ bytes base64 encoded.
    
    Examples: YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo...
    """
    regex             = re.compile(r'^[A-Za-z0-9+/=]+$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    max_length        = 4096  # Generous limit for encrypted values
    allow_empty       = True
