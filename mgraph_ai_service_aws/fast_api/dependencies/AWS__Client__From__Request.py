from typing                                                              import Any
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe
from osbot_aws.apis.Session                                              import Session
from mgraph_ai_service_aws.service.encryption.Service__Encryption        import Service__Encryption
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Request__Base   import Schema__AWS__Request__Base


DEFAULT_REGION = 'us-east-1'


class AWS__Client__From__Request(Type_Safe):
    """Factory for creating AWS clients from encrypted request credentials.
    
    Uses OSBot-AWS Session class for boto3 client creation.
    Decrypts credentials and creates boto3 session with provided credentials.
    """
    
    service_encryption : Service__Encryption = None
    
    def get_boto3_session(self, request: Schema__AWS__Request__Base) -> Any:
        """Create a boto3.Session from the request's encrypted credentials.
        
        Args:
            request: AWS request containing encrypted credentials
            
        Returns:
            boto3.Session configured with decrypted credentials
            
        Raises:
            ValueError: If decryption fails
        """
        # Decrypt secret_access_key
        secret_key_result = self.service_encryption.decrypt_text(str(request.encrypted_secret_access_key))
        if not secret_key_result.success:
            raise ValueError(f"Failed to decrypt secret_access_key: {secret_key_result.error}")
        
        # Decrypt session_token if present
        session_token = None
        if request.encrypted_session_token:
            token_result = self.service_encryption.decrypt_text(str(request.encrypted_session_token))
            if not token_result.success:
                raise ValueError(f"Failed to decrypt session_token: {token_result.error}")
            session_token = token_result.decrypted
        
        # Use OSBot-AWS Session.botocore_session() which supports all credential parameters
        region = str(request.region) if request.region else DEFAULT_REGION
        
        session = Session().botocore_session(
            aws_access_key_id     = str(request.access_key_id)           ,
            aws_secret_access_key = secret_key_result.decrypted          ,
            aws_session_token     = session_token                        ,
            region_name           = region
        )
        
        return session
    
    def get_lambda_client(self, request: Schema__AWS__Request__Base) -> Any:
        """Get a Lambda client configured with request credentials."""
        return self.get_boto3_session(request).client('lambda')
    
    def get_s3_client(self, request: Schema__AWS__Request__Base) -> Any:
        """Get an S3 client configured with request credentials."""
        return self.get_boto3_session(request).client('s3')
