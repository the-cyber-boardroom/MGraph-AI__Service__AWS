from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                import Serverless__Fast_API
from mgraph_ai_service_aws.service.encryption.NaCl__Key_Management          import NaCl__Key_Management
from mgraph_ai_service_aws.service.encryption.Service__Encryption           import Service__Encryption
from mgraph_ai_service_aws.fast_api.dependencies.AWS__Client__From__Request import AWS__Client__From__Request
from mgraph_ai_service_aws.fast_api.routes.Routes__Encryption               import Routes__Encryption
from mgraph_ai_service_aws.fast_api.routes.Routes__AWS__Lambda              import Routes__AWS__Lambda
from mgraph_ai_service_aws.fast_api.routes.Routes__AWS__S3                  import Routes__AWS__S3


class AWS__Service__Fast_API(Serverless__Fast_API):         # Main FastAPI service for AWS operations.
    
    nacl_key_management : NaCl__Key_Management                              # NaCl key management (helps with generating keys)
    service_encryption  : Service__Encryption        = None
    aws_client_factory  : AWS__Client__From__Request = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        self.setup_routes()
        super().setup()
        return self

    def setup__services(self):                                              # Initialize encryption and AWS client services.
        self.service_encryption = Service__Encryption(nacl_key_management = self.nacl_key_management)   # Create encryption service
        self.aws_client_factory = AWS__Client__From__Request(service_encryption = self.service_encryption)  # Create AWS client factory
    
    def setup_routes(self):         # Register all routes.
        app = self.app()


        # todo: BUG: fix OSBOT-Fast-API or OSBOT-Fast-API-Serverless to support using this dependency injection on the self.add_routes
        Routes__Encryption(app                = app                   ,
                           service_encryption = self.service_encryption).setup()    # Encryption route for key exchange

        Routes__AWS__Lambda(app                = app                   ,            # AWS Lambda routes
                            aws_client_factory = self.aws_client_factory).setup()

        Routes__AWS__S3(app                = app                    ,               # AWS S3 routes
                        aws_client_factory = self.aws_client_factory).setup()
        
        return self
