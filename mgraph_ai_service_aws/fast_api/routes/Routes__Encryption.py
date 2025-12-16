from osbot_fast_api.api.routes.Fast_API__Routes                         import Fast_API__Routes
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from mgraph_ai_service_aws.service.encryption.Service__Encryption       import Service__Encryption


TAG__ROUTES_ENCRYPTION = 'encryption'

ROUTES_PATHS__ENCRYPTION = [f'/{TAG__ROUTES_ENCRYPTION}/public-key' ]


class Schema__Encryption__Public_Key__Response(Type_Safe):                  # Response containing the public key for client-side encryption.
    public_key : str = None


class Routes__Encryption(Fast_API__Routes):                                 # Routes for encryption key exchange
    
    tag                : str                = TAG__ROUTES_ENCRYPTION
    service_encryption : Service__Encryption = None
    
    def public_key(self) -> Schema__Encryption__Public_Key__Response:       # Get the public key for encrypting credentials.
        return Schema__Encryption__Public_Key__Response(public_key = self.service_encryption.public_key())
    
    def setup_routes(self):                                                 # Register encryption routes.
        self.add_route_get(self.public_key)
        return self
