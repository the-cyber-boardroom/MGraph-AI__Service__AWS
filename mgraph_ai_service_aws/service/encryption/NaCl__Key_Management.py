import base64
from typing                                                             import Optional
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                       import cache_on_self

try:
    from nacl.public import PrivateKey, SealedBox, PublicKey
    NACL_AVAILABLE = True
except ImportError:
    NACL_AVAILABLE = False


class NaCl__Key_Management(Type_Safe):
    """NaCl key management for credential encryption/decryption.
    
    Uses Curve25519 keypair with SealedBox (anonymous public-key encryption).
    Keys are generated once and cached in memory - they rotate on each Lambda deployment.
    """
    
    _private_key_bytes : bytes = None
    _public_key_bytes  : bytes = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not NACL_AVAILABLE:
            raise ImportError("PyNaCl is required. Install with: pip install pynacl")
    
    @cache_on_self
    def private_key(self) -> 'PrivateKey':
        """Get or generate the private key."""
        if self._private_key_bytes:
            return PrivateKey(self._private_key_bytes)
        key = PrivateKey.generate()
        self._private_key_bytes = bytes(key)
        self._public_key_bytes  = bytes(key.public_key)
        return key
    
    @cache_on_self
    def public_key(self) -> 'PublicKey':
        """Get the public key (derived from private key)."""
        return self.private_key().public_key
    
    def public_key_base64(self) -> str:
        """Get the public key as base64 string (for client use)."""
        return base64.b64encode(bytes(self.public_key())).decode('utf-8')
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using public key (SealedBox).
        
        Returns base64-encoded ciphertext.
        """
        sealed_box  = SealedBox(self.public_key())
        ciphertext  = sealed_box.encrypt(plaintext.encode('utf-8'))
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def decrypt(self, ciphertext_base64: str) -> str:
        """Decrypt base64-encoded ciphertext using private key.
        
        Returns plaintext string.
        Raises ValueError if decryption fails.
        """
        try:
            ciphertext  = base64.b64decode(ciphertext_base64)
            sealed_box  = SealedBox(self.private_key())
            plaintext   = sealed_box.decrypt(ciphertext)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
