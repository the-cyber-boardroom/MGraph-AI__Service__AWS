import base64
import json
from datetime                                                               import datetime, timezone
from typing                                                                 import List
from fastapi                                                                import Response
from osbot_fast_api.api.routes.Fast_API__Routes                             import Fast_API__Routes
from mgraph_ai_service_aws.fast_api.dependencies.AWS__Client__From__Request import AWS__Client__From__Request
from mgraph_ai_service_aws.schemas.base.Enum__HTTP__Status                  import Enum__HTTP__Status
from mgraph_ai_service_aws.schemas.aws.base.Enum__AWS__Error__Type          import Enum__AWS__Error__Type
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response__Context  import Schema__AWS__Response__Context
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data    import Schema__AWS__Lambda__Function__Summary
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data    import Schema__AWS__Lambda__Configuration
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data    import Schema__AWS__Lambda__Code__Location
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data    import Schema__AWS__Lambda__Invoke__Result
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Request__Lambda import Schema__AWS__Request__Lambda__List
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Request__Lambda import Schema__AWS__Request__Lambda__Get
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Request__Lambda import Schema__AWS__Request__Lambda__Invoke
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Request__Lambda import Schema__AWS__Request__Lambda__Create
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Request__Lambda import Schema__AWS__Request__Lambda__Update
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Request__Lambda import Schema__AWS__Request__Lambda__Delete
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__AWS__Response__Lambda__List
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__AWS__Response__Lambda__Get
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__AWS__Response__Lambda__Invoke
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__AWS__Response__Lambda__Create
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__AWS__Response__Lambda__Update
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__AWS__Response__Lambda__Delete
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__Response__Data__Lambda__List
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__Response__Data__Lambda__Get
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__Response__Data__Lambda__Invoke
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__Response__Data__Lambda__Create
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__Response__Data__Lambda__Update
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Response__Lambda import Schema__Response__Data__Lambda__Delete


TAG__ROUTES_AWS_LAMBDA = 'aws-lambda'

ROUTES_PATHS__AWS_LAMBDA = [
    f'/{TAG__ROUTES_AWS_LAMBDA}/list'   ,
    f'/{TAG__ROUTES_AWS_LAMBDA}/get'    ,
    f'/{TAG__ROUTES_AWS_LAMBDA}/invoke' ,
    f'/{TAG__ROUTES_AWS_LAMBDA}/create' ,
    f'/{TAG__ROUTES_AWS_LAMBDA}/update' ,
    f'/{TAG__ROUTES_AWS_LAMBDA}/delete' ,
]

# todo: all non-fastapi code below needs to be refactored into services
#       also this code is not leveraging the OSBot-AWS methods
class Routes__AWS__Lambda(Fast_API__Routes):            # Routes for AWS Lambda operations.
    
    tag                : str                        = TAG__ROUTES_AWS_LAMBDA
    aws_client_factory : AWS__Client__From__Request = None
    
    def _handle_aws_error(self, error: Exception, response_context: Schema__AWS__Response__Context):
        """Map boto3 exceptions to HTTP status and error type."""
        error_code = getattr(error, 'response', {}).get('Error', {}).get('Code', '')
        error_msg  = getattr(error, 'response', {}).get('Error', {}).get('Message', str(error))
        
        mapping = {
            'InvalidClientTokenId'      : (Enum__HTTP__Status.UNAUTHORIZED_401    , Enum__AWS__Error__Type.INVALID_CREDENTIALS ),
            'ExpiredToken'              : (Enum__HTTP__Status.UNAUTHORIZED_401    , Enum__AWS__Error__Type.EXPIRED_CREDENTIALS ),
            'ExpiredTokenException'     : (Enum__HTTP__Status.UNAUTHORIZED_401    , Enum__AWS__Error__Type.EXPIRED_CREDENTIALS ),
            'AccessDenied'              : (Enum__HTTP__Status.FORBIDDEN_403       , Enum__AWS__Error__Type.ACCESS_DENIED       ),
            'AccessDeniedException'     : (Enum__HTTP__Status.FORBIDDEN_403       , Enum__AWS__Error__Type.ACCESS_DENIED       ),
            'ResourceNotFoundException' : (Enum__HTTP__Status.NOT_FOUND_404       , Enum__AWS__Error__Type.RESOURCE_NOT_FOUND  ),
            'Throttling'                : (Enum__HTTP__Status.RATE_LIMITED_429    , Enum__AWS__Error__Type.THROTTLING          ),
            'TooManyRequestsException'  : (Enum__HTTP__Status.RATE_LIMITED_429    , Enum__AWS__Error__Type.THROTTLING          ),
            'ServiceException'          : (Enum__HTTP__Status.SERVER_ERROR_500    , Enum__AWS__Error__Type.SERVICE_UNAVAILABLE ),
            'ValidationException'       : (Enum__HTTP__Status.BAD_REQUEST_400     , Enum__AWS__Error__Type.VALIDATION_ERROR    ),
        }
        
        status, error_type = mapping.get(error_code, 
            (Enum__HTTP__Status.SERVER_ERROR_500, Enum__AWS__Error__Type.AWS_API_ERROR))
        
        response_context.success        = False
        response_context.status_code    = status
        response_context.aws_error_type = error_type
        response_context.errors         = [error_msg]
    
    def _extract_aws_metadata(self, aws_response: dict, response_context: Schema__AWS__Response__Context):
        """Extract AWS metadata from boto3 response."""
        metadata = aws_response.get('ResponseMetadata', {})
        response_context.aws_request_id  = metadata.get('RequestId')
        response_context.aws_http_status = metadata.get('HTTPStatusCode')
        response_context.retries         = metadata.get('RetryAttempts', 0)
    
    def _map_function_summary(self, func: dict) -> Schema__AWS__Lambda__Function__Summary:
        """Map boto3 function to summary schema."""
        return Schema__AWS__Lambda__Function__Summary(
            function_name = func.get('FunctionName')  ,
            function_arn  = func.get('FunctionArn')   ,
            runtime       = func.get('Runtime')       ,
            handler       = func.get('Handler')       ,
            code_size     = func.get('CodeSize', 0)   ,
            memory_size   = func.get('MemorySize', 0) ,
            timeout       = func.get('Timeout', 0)    ,
            last_modified = func.get('LastModified')  ,
            state         = func.get('State')         ,
            description   = func.get('Description')
        )
    
    def _map_configuration(self, config: dict) -> Schema__AWS__Lambda__Configuration:
        """Map boto3 configuration to schema."""
        env_vars = config.get('Environment', {}).get('Variables', {})
        return Schema__AWS__Lambda__Configuration(
            function_name     = config.get('FunctionName')    ,
            function_arn      = config.get('FunctionArn')     ,
            runtime           = config.get('Runtime')         ,
            role              = config.get('Role')            ,
            handler           = config.get('Handler')         ,
            code_size         = config.get('CodeSize', 0)     ,
            description       = config.get('Description')     ,
            timeout           = config.get('Timeout', 0)      ,
            memory_size       = config.get('MemorySize', 0)   ,
            last_modified     = config.get('LastModified')    ,
            code_sha256       = config.get('CodeSha256')      ,
            version           = config.get('Version')         ,
            environment       = env_vars if env_vars else None,
            state             = config.get('State')           ,
            state_reason      = config.get('StateReason')     ,
            state_reason_code = config.get('StateReasonCode') ,
            architectures     = config.get('Architectures')
        )
    
    # Route methods
    
    def list(self, request : Schema__AWS__Request__Lambda__List ,
                   response: Response
             ) -> Schema__AWS__Response__Lambda__List:
        """List Lambda functions."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__Lambda__List()
        
        try:
            lambda_client = self.aws_client_factory.get_lambda_client(request)
            
            kwargs = {}
            if request.request_data:
                if request.request_data.max_items:
                    kwargs['MaxItems'] = request.request_data.max_items
                if request.request_data.marker:
                    kwargs['Marker'] = request.request_data.marker
            
            aws_response = lambda_client.list_functions(**kwargs)
            self._extract_aws_metadata(aws_response, response_context)
            
            functions = [self._map_function_summary(f) for f in aws_response.get('Functions', [])]
            response_data.functions   = functions
            response_data.next_marker = aws_response.get('NextMarker')
            
            response_context.success     = True
            response_context.status_code = Enum__HTTP__Status.OK_200
            
        except ValueError as e:
            response_context.success        = False
            response_context.status_code    = Enum__HTTP__Status.UNAUTHORIZED_401
            response_context.aws_error_type = Enum__AWS__Error__Type.DECRYPTION_FAILED
            response_context.errors         = [str(e)]
        except Exception as e:
            self._handle_aws_error(e, response_context)
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        response_context.duration  = duration
        response_context.timestamp = start_time.isoformat()
        
        response.status_code = response_context.status_code.value
        return Schema__AWS__Response__Lambda__List(
            response_context = response_context,
            response_data    = response_data
        )
    
    def get(self, request : Schema__AWS__Request__Lambda__Get ,
                  response: Response
            ) -> Schema__AWS__Response__Lambda__Get:
        """Get Lambda function details."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__Lambda__Get()
        
        try:
            lambda_client = self.aws_client_factory.get_lambda_client(request)
            function_name = str(request.request_data.function_name)
            
            aws_response = lambda_client.get_function(FunctionName=function_name)
            self._extract_aws_metadata(aws_response, response_context)
            
            response_data.configuration = self._map_configuration(aws_response.get('Configuration', {}))
            
            code_info = aws_response.get('Code', {})
            response_data.code = Schema__AWS__Lambda__Code__Location(
                repository_type = code_info.get('RepositoryType'),
                location        = code_info.get('Location')
            )
            
            response_context.success     = True
            response_context.status_code = Enum__HTTP__Status.OK_200
            
        except ValueError as e:
            response_context.success        = False
            response_context.status_code    = Enum__HTTP__Status.UNAUTHORIZED_401
            response_context.aws_error_type = Enum__AWS__Error__Type.DECRYPTION_FAILED
            response_context.errors         = [str(e)]
        except Exception as e:
            self._handle_aws_error(e, response_context)
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        response_context.duration  = duration
        response_context.timestamp = start_time.isoformat()
        
        response.status_code = response_context.status_code.value
        return Schema__AWS__Response__Lambda__Get(
            response_context = response_context,
            response_data    = response_data
        )
    
    def invoke(self, request : Schema__AWS__Request__Lambda__Invoke ,
                     response: Response
               ) -> Schema__AWS__Response__Lambda__Invoke:
        """Invoke Lambda function."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__Lambda__Invoke()
        
        try:
            lambda_client   = self.aws_client_factory.get_lambda_client(request)
            function_name   = str(request.request_data.function_name)
            invocation_type = request.request_data.invocation_type.value
            log_type        = request.request_data.log_type or 'None'
            
            kwargs = {
                'FunctionName'  : function_name  ,
                'InvocationType': invocation_type,
                'LogType'       : log_type
            }
            
            if request.request_data.payload:
                kwargs['Payload'] = json.dumps(request.request_data.payload)
            
            aws_response = lambda_client.invoke(**kwargs)
            self._extract_aws_metadata(aws_response, response_context)
            
            # Read and parse response payload
            payload_data = None
            if 'Payload' in aws_response:
                payload_bytes = aws_response['Payload'].read()
                if payload_bytes:
                    try:
                        payload_data = json.loads(payload_bytes.decode('utf-8'))
                    except json.JSONDecodeError:
                        payload_data = {'raw': payload_bytes.decode('utf-8', errors='replace')}
            
            response_data.result = Schema__AWS__Lambda__Invoke__Result(
                status_code      = aws_response.get('StatusCode')       ,
                payload          = payload_data                         ,
                function_error   = aws_response.get('FunctionError')    ,
                log_result       = aws_response.get('LogResult')        ,
                executed_version = aws_response.get('ExecutedVersion')
            )
            
            response_context.success     = True
            response_context.status_code = Enum__HTTP__Status.OK_200
            
        except ValueError as e:
            response_context.success        = False
            response_context.status_code    = Enum__HTTP__Status.UNAUTHORIZED_401
            response_context.aws_error_type = Enum__AWS__Error__Type.DECRYPTION_FAILED
            response_context.errors         = [str(e)]
        except Exception as e:
            self._handle_aws_error(e, response_context)
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        response_context.duration  = duration
        response_context.timestamp = start_time.isoformat()
        
        response.status_code = response_context.status_code.value
        return Schema__AWS__Response__Lambda__Invoke(
            response_context = response_context,
            response_data    = response_data
        )
    
    def create(self, request : Schema__AWS__Request__Lambda__Create ,
                     response: Response
               ) -> Schema__AWS__Response__Lambda__Create:
        """Create Lambda function."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__Lambda__Create()
        
        try:
            lambda_client = self.aws_client_factory.get_lambda_client(request)
            req_data      = request.request_data
            
            # Build Code parameter
            code = {}
            if req_data.code.zip_file:
                code['ZipFile'] = base64.b64decode(req_data.code.zip_file)
            elif req_data.code.s3_bucket:
                code['S3Bucket'] = req_data.code.s3_bucket
                code['S3Key']    = req_data.code.s3_key
                if req_data.code.s3_object_version:
                    code['S3ObjectVersion'] = req_data.code.s3_object_version
            
            kwargs = {
                'FunctionName': str(req_data.function_name),
                'Runtime'     : req_data.runtime.value     ,
                'Role'        : req_data.role              ,
                'Handler'     : req_data.handler           ,
                'Code'        : code                       ,
                'Timeout'     : req_data.timeout           ,
                'MemorySize'  : req_data.memory_size
            }
            
            if req_data.description:
                kwargs['Description'] = req_data.description
            if req_data.environment:
                kwargs['Environment'] = {'Variables': req_data.environment}
            
            aws_response = lambda_client.create_function(**kwargs)
            self._extract_aws_metadata(aws_response, response_context)
            
            response_data.configuration = self._map_configuration(aws_response)
            
            response_context.success     = True
            response_context.status_code = Enum__HTTP__Status.CREATED_201
            
        except ValueError as e:
            response_context.success        = False
            response_context.status_code    = Enum__HTTP__Status.UNAUTHORIZED_401
            response_context.aws_error_type = Enum__AWS__Error__Type.DECRYPTION_FAILED
            response_context.errors         = [str(e)]
        except Exception as e:
            self._handle_aws_error(e, response_context)
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        response_context.duration  = duration
        response_context.timestamp = start_time.isoformat()
        
        response.status_code = response_context.status_code.value
        return Schema__AWS__Response__Lambda__Create(
            response_context = response_context,
            response_data    = response_data
        )
    
    def update(self, request : Schema__AWS__Request__Lambda__Update ,
                     response: Response
               ) -> Schema__AWS__Response__Lambda__Update:
        """Update Lambda function code and/or configuration."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__Lambda__Update()
        
        try:
            lambda_client = self.aws_client_factory.get_lambda_client(request)
            req_data      = request.request_data
            function_name = str(req_data.function_name)
            
            latest_config = None
            
            # Update code if provided
            if req_data.code:
                code_kwargs = {'FunctionName': function_name}
                if req_data.code.zip_file:
                    code_kwargs['ZipFile'] = base64.b64decode(req_data.code.zip_file)
                elif req_data.code.s3_bucket:
                    code_kwargs['S3Bucket'] = req_data.code.s3_bucket
                    code_kwargs['S3Key']    = req_data.code.s3_key
                    if req_data.code.s3_object_version:
                        code_kwargs['S3ObjectVersion'] = req_data.code.s3_object_version
                
                aws_response  = lambda_client.update_function_code(**code_kwargs)
                latest_config = aws_response
                self._extract_aws_metadata(aws_response, response_context)
            
            # Update configuration if any config fields provided
            config_updates = {}
            if req_data.description is not None:
                config_updates['Description'] = req_data.description
            if req_data.timeout is not None:
                config_updates['Timeout'] = req_data.timeout
            if req_data.memory_size is not None:
                config_updates['MemorySize'] = req_data.memory_size
            if req_data.runtime is not None:
                config_updates['Runtime'] = req_data.runtime.value
            if req_data.handler is not None:
                config_updates['Handler'] = req_data.handler
            if req_data.environment is not None:
                config_updates['Environment'] = {'Variables': req_data.environment}
            
            if config_updates:
                config_updates['FunctionName'] = function_name
                aws_response  = lambda_client.update_function_configuration(**config_updates)
                latest_config = aws_response
                self._extract_aws_metadata(aws_response, response_context)
            
            if latest_config:
                response_data.configuration = self._map_configuration(latest_config)
            
            response_context.success     = True
            response_context.status_code = Enum__HTTP__Status.OK_200
            
        except ValueError as e:
            response_context.success        = False
            response_context.status_code    = Enum__HTTP__Status.UNAUTHORIZED_401
            response_context.aws_error_type = Enum__AWS__Error__Type.DECRYPTION_FAILED
            response_context.errors         = [str(e)]
        except Exception as e:
            self._handle_aws_error(e, response_context)
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        response_context.duration  = duration
        response_context.timestamp = start_time.isoformat()
        
        response.status_code = response_context.status_code.value
        return Schema__AWS__Response__Lambda__Update(
            response_context = response_context,
            response_data    = response_data
        )
    
    def delete(self, request : Schema__AWS__Request__Lambda__Delete ,
                     response: Response
               ) -> Schema__AWS__Response__Lambda__Delete:
        """Delete Lambda function."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__Lambda__Delete()
        
        try:
            lambda_client = self.aws_client_factory.get_lambda_client(request)
            function_name = str(request.request_data.function_name)
            
            aws_response = lambda_client.delete_function(FunctionName=function_name)
            self._extract_aws_metadata(aws_response, response_context)
            
            response_data.deleted = True
            
            response_context.success     = True
            response_context.status_code = Enum__HTTP__Status.OK_200
            
        except ValueError as e:
            response_context.success        = False
            response_context.status_code    = Enum__HTTP__Status.UNAUTHORIZED_401
            response_context.aws_error_type = Enum__AWS__Error__Type.DECRYPTION_FAILED
            response_context.errors         = [str(e)]
        except Exception as e:
            self._handle_aws_error(e, response_context)
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        response_context.duration  = duration
        response_context.timestamp = start_time.isoformat()
        
        response.status_code = response_context.status_code.value
        return Schema__AWS__Response__Lambda__Delete(
            response_context = response_context,
            response_data    = response_data
        )
    
    def setup_routes(self):
        """Register all Lambda routes."""
        self.add_route_post  (self.list  )
        self.add_route_post  (self.get   )
        self.add_route_post  (self.invoke)
        self.add_route_post  (self.create)
        self.add_route_put   (self.update)
        self.add_route_delete(self.delete)
        return self
