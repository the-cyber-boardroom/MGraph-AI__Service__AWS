from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from mgraph_ai_service_aws.service.encryption.NaCl__Key_Management      import NaCl__Key_Management


class Schema__Encryption__Result(Type_Safe):
    """Result of an encryption/decryption operation."""
    success   : bool = False
    encrypted : str  = None
    decrypted : str  = None
    error     : str  = None


class Service__Encryption(Type_Safe):
    """Service layer for encryption operations."""
    
    nacl_key_management : NaCl__Key_Management = None
    
    def public_key(self) -> str:
        """Get the public key for client-side encryption."""
        return self.nacl_key_management.public_key_base64()
    
    def encrypt_text(self, plaintext: str) -> Schema__Encryption__Result:
        """Encrypt plaintext. Primarily for testing - clients should encrypt locally."""
        try:
            encrypted = self.nacl_key_management.encrypt(plaintext)
            return Schema__Encryption__Result(success=True, encrypted=encrypted)
        except Exception as e:
            return Schema__Encryption__Result(success=False, error=str(e))
    
    def decrypt_text(self, ciphertext_base64: str) -> Schema__Encryption__Result:
        """Decrypt base64-encoded ciphertext."""
        try:
            decrypted = self.nacl_key_management.decrypt(ciphertext_base64)
            return Schema__Encryption__Result(success=True, decrypted=decrypted)
        except Exception as e:
            return Schema__Encryption__Result(success=False, error=str(e))
