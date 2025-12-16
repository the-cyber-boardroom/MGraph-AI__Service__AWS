from typing                                                             import Optional
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from mgraph_ai_service_aws.schemas.base.Schema__Request__Data           import Schema__Request__Data
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__AWS__Access_Key_Id import Safe_Str__AWS__Access_Key_Id
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__AWS__Account_Id    import Safe_Str__AWS__Account_Id
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__AWS__Region        import Safe_Str__AWS__Region
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__Encrypted_Value    import Safe_Str__Encrypted_Value


class Schema__AWS__Request__Base(Type_Safe):
    """Base request schema for all AWS operations.
    
    Credential Model (Partial Encryption):
    - access_key_id: Plaintext (not secret, used for logging/debugging)
    - encrypted_secret_access_key: NaCl encrypted, base64 encoded
    - encrypted_session_token: Optional, for STS temporary credentials
    - account_id: Optional, plaintext (for validation/logging)
    - region: Plaintext, target AWS region
    """
    access_key_id               : Safe_Str__AWS__Access_Key_Id
    encrypted_secret_access_key : Safe_Str__Encrypted_Value
    encrypted_session_token     : Safe_Str__Encrypted_Value       = None
    account_id                  : Safe_Str__AWS__Account_Id       = None
    region                      : Safe_Str__AWS__Region           = None
    request_data                : Schema__Request__Data           = None
