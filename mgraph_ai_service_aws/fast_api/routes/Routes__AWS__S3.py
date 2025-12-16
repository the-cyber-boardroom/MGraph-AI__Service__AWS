import base64
from datetime                                                               import datetime, timezone
from typing                                                                 import List
from fastapi                                                                import Response
from osbot_fast_api.api.routes.Fast_API__Routes                             import Fast_API__Routes
from mgraph_ai_service_aws.fast_api.dependencies.AWS__Client__From__Request import AWS__Client__From__Request
from mgraph_ai_service_aws.schemas.base.Enum__HTTP__Status                  import Enum__HTTP__Status
from mgraph_ai_service_aws.schemas.aws.base.Enum__AWS__Error__Type          import Enum__AWS__Error__Type
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response__Context  import Schema__AWS__Response__Context
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Bucket
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Object__Content
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Object__Head
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Put__Result
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Delete__Result
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Request__S3          import Schema__AWS__Request__S3__List_Buckets
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Request__S3          import Schema__AWS__Request__S3__List_Objects
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Request__S3          import Schema__AWS__Request__S3__Get_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Request__S3          import Schema__AWS__Request__S3__Put_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Request__S3          import Schema__AWS__Request__S3__Head_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Request__S3          import Schema__AWS__Request__S3__Delete_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__AWS__Response__S3__List_Buckets
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__AWS__Response__S3__List_Objects
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__AWS__Response__S3__Get_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__AWS__Response__S3__Put_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__AWS__Response__S3__Head_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__AWS__Response__S3__Delete_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__Response__Data__S3__List_Buckets
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__Response__Data__S3__List_Objects
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__Response__Data__S3__Get_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__Response__Data__S3__Put_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__Response__Data__S3__Head_Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__Response__S3         import Schema__Response__Data__S3__Delete_Object


TAG__ROUTES_AWS_S3 = 'aws-s3'

ROUTES_PATHS__AWS_S3 = [
    f'/{TAG__ROUTES_AWS_S3}/list-buckets' ,
    f'/{TAG__ROUTES_AWS_S3}/list-objects' ,
    f'/{TAG__ROUTES_AWS_S3}/get-object'   ,
    f'/{TAG__ROUTES_AWS_S3}/put-object'   ,
    f'/{TAG__ROUTES_AWS_S3}/head-object'  ,
    f'/{TAG__ROUTES_AWS_S3}/delete-object',
]


# todo: all non-fastapi code below needs to be refactored into services
#       also this code is not leveraging the OSBot-AWS methods
class Routes__AWS__S3(Fast_API__Routes):        # Routes for AWS S3 operations.
    
    tag                : str                        = TAG__ROUTES_AWS_S3
    aws_client_factory : AWS__Client__From__Request = None
    
    def _handle_aws_error(self, error: Exception, response_context: Schema__AWS__Response__Context):
        """Map boto3 exceptions to HTTP status and error type."""
        error_code = getattr(error, 'response', {}).get('Error', {}).get('Code', '')
        error_msg  = getattr(error, 'response', {}).get('Error', {}).get('Message', str(error))
        
        mapping = {
            'InvalidClientTokenId'      : (Enum__HTTP__Status.UNAUTHORIZED_401    , Enum__AWS__Error__Type.INVALID_CREDENTIALS ),
            'ExpiredToken'              : (Enum__HTTP__Status.UNAUTHORIZED_401    , Enum__AWS__Error__Type.EXPIRED_CREDENTIALS ),
            'AccessDenied'              : (Enum__HTTP__Status.FORBIDDEN_403       , Enum__AWS__Error__Type.ACCESS_DENIED       ),
            'NoSuchBucket'              : (Enum__HTTP__Status.NOT_FOUND_404       , Enum__AWS__Error__Type.RESOURCE_NOT_FOUND  ),
            'NoSuchKey'                 : (Enum__HTTP__Status.NOT_FOUND_404       , Enum__AWS__Error__Type.RESOURCE_NOT_FOUND  ),
            '404'                       : (Enum__HTTP__Status.NOT_FOUND_404       , Enum__AWS__Error__Type.RESOURCE_NOT_FOUND  ),
            'Throttling'                : (Enum__HTTP__Status.RATE_LIMITED_429    , Enum__AWS__Error__Type.THROTTLING          ),
            'SlowDown'                  : (Enum__HTTP__Status.RATE_LIMITED_429    , Enum__AWS__Error__Type.THROTTLING          ),
            'ServiceUnavailable'        : (Enum__HTTP__Status.SERVER_ERROR_500    , Enum__AWS__Error__Type.SERVICE_UNAVAILABLE ),
            'InvalidBucketName'         : (Enum__HTTP__Status.BAD_REQUEST_400     , Enum__AWS__Error__Type.VALIDATION_ERROR    ),
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
    
    def _format_datetime(self, dt) -> str:
        """Format datetime to ISO string."""
        if dt is None:
            return None
        if hasattr(dt, 'isoformat'):
            return dt.isoformat()
        return str(dt)
    
    # Route methods
    
    def list_buckets(self, request : Schema__AWS__Request__S3__List_Buckets ,
                           response: Response
                     ) -> Schema__AWS__Response__S3__List_Buckets:
        """List S3 buckets."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__S3__List_Buckets()
        
        try:
            s3_client = self.aws_client_factory.get_s3_client(request)
            
            aws_response = s3_client.list_buckets()
            self._extract_aws_metadata(aws_response, response_context)
            
            buckets = []
            for bucket in aws_response.get('Buckets', []):
                buckets.append(Schema__AWS__S3__Bucket(
                    name          = bucket.get('Name'),
                    creation_date = self._format_datetime(bucket.get('CreationDate'))
                ))
            
            response_data.buckets = buckets
            
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
        return Schema__AWS__Response__S3__List_Buckets(
            response_context = response_context,
            response_data    = response_data
        )
    
    def list_objects(self, request : Schema__AWS__Request__S3__List_Objects ,
                           response: Response
                     ) -> Schema__AWS__Response__S3__List_Objects:
        """List objects in an S3 bucket."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__S3__List_Objects()
        
        try:
            s3_client = self.aws_client_factory.get_s3_client(request)
            req_data  = request.request_data
            
            kwargs = {
                'Bucket' : str(req_data.bucket) ,
                'MaxKeys': req_data.max_keys
            }
            if req_data.prefix:
                kwargs['Prefix'] = req_data.prefix
            if req_data.delimiter:
                kwargs['Delimiter'] = req_data.delimiter
            if req_data.continuation_token:
                kwargs['ContinuationToken'] = req_data.continuation_token
            
            aws_response = s3_client.list_objects_v2(**kwargs)
            self._extract_aws_metadata(aws_response, response_context)
            
            objects = []
            for obj in aws_response.get('Contents', []):
                objects.append(Schema__AWS__S3__Object(
                    key           = obj.get('Key')                                 ,
                    last_modified = self._format_datetime(obj.get('LastModified')) ,
                    etag          = obj.get('ETag')                                ,
                    size          = obj.get('Size', 0)                             ,
                    storage_class = obj.get('StorageClass')
                ))
            
            # Common prefixes (when using delimiter)
            prefixes = [cp.get('Prefix') for cp in aws_response.get('CommonPrefixes', [])]
            
            response_data.objects                 = objects
            response_data.common_prefixes         = prefixes if prefixes else None
            response_data.is_truncated            = aws_response.get('IsTruncated', False)
            response_data.next_continuation_token = aws_response.get('NextContinuationToken')
            
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
        return Schema__AWS__Response__S3__List_Objects(
            response_context = response_context,
            response_data    = response_data
        )
    
    def get_object(self, request : Schema__AWS__Request__S3__Get_Object ,
                         response: Response
                   ) -> Schema__AWS__Response__S3__Get_Object:
        """Get an S3 object."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__S3__Get_Object()
        
        try:
            s3_client = self.aws_client_factory.get_s3_client(request)
            req_data  = request.request_data
            
            aws_response = s3_client.get_object(
                Bucket = str(req_data.bucket),
                Key    = str(req_data.key)
            )
            self._extract_aws_metadata(aws_response, response_context)
            
            # Read body and base64 encode
            body_bytes   = aws_response['Body'].read()
            body_base64  = base64.b64encode(body_bytes).decode('utf-8')
            
            response_data.content = Schema__AWS__S3__Object__Content(
                body           = body_base64                                          ,
                content_type   = aws_response.get('ContentType')                      ,
                content_length = aws_response.get('ContentLength', 0)                 ,
                last_modified  = self._format_datetime(aws_response.get('LastModified')),
                etag           = aws_response.get('ETag')                             ,
                metadata       = aws_response.get('Metadata')
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
        return Schema__AWS__Response__S3__Get_Object(
            response_context = response_context,
            response_data    = response_data
        )
    
    def put_object(self, request : Schema__AWS__Request__S3__Put_Object ,
                         response: Response
                   ) -> Schema__AWS__Response__S3__Put_Object:
        """Put an S3 object."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__S3__Put_Object()
        
        try:
            s3_client = self.aws_client_factory.get_s3_client(request)
            req_data  = request.request_data
            
            # Decode body from base64
            body_bytes = base64.b64decode(req_data.body)
            
            kwargs = {
                'Bucket'     : str(req_data.bucket)    ,
                'Key'        : str(req_data.key)       ,
                'Body'       : body_bytes              ,
                'ContentType': req_data.content_type
            }
            if req_data.metadata:
                kwargs['Metadata'] = req_data.metadata
            
            aws_response = s3_client.put_object(**kwargs)
            self._extract_aws_metadata(aws_response, response_context)
            
            response_data.result = Schema__AWS__S3__Put__Result(
                etag       = aws_response.get('ETag')      ,
                version_id = aws_response.get('VersionId')
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
        return Schema__AWS__Response__S3__Put_Object(
            response_context = response_context,
            response_data    = response_data
        )
    
    def head_object(self, request : Schema__AWS__Request__S3__Head_Object ,
                          response: Response
                    ) -> Schema__AWS__Response__S3__Head_Object:
        """Get S3 object metadata."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__S3__Head_Object()
        
        try:
            s3_client = self.aws_client_factory.get_s3_client(request)
            req_data  = request.request_data
            
            aws_response = s3_client.head_object(
                Bucket = str(req_data.bucket),
                Key    = str(req_data.key)
            )
            self._extract_aws_metadata(aws_response, response_context)
            
            response_data.metadata = Schema__AWS__S3__Object__Head(
                content_type   = aws_response.get('ContentType')                      ,
                content_length = aws_response.get('ContentLength', 0)                 ,
                last_modified  = self._format_datetime(aws_response.get('LastModified')),
                etag           = aws_response.get('ETag')                             ,
                metadata       = aws_response.get('Metadata')                         ,
                version_id     = aws_response.get('VersionId')
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
        return Schema__AWS__Response__S3__Head_Object(
            response_context = response_context,
            response_data    = response_data
        )
    
    def delete_object(self, request : Schema__AWS__Request__S3__Delete_Object ,
                            response: Response
                      ) -> Schema__AWS__Response__S3__Delete_Object:
        """Delete an S3 object."""
        start_time       = datetime.now(timezone.utc)
        response_context = Schema__AWS__Response__Context()
        response_data    = Schema__Response__Data__S3__Delete_Object()
        
        try:
            s3_client = self.aws_client_factory.get_s3_client(request)
            req_data  = request.request_data
            
            aws_response = s3_client.delete_object(
                Bucket = str(req_data.bucket),
                Key    = str(req_data.key)
            )
            self._extract_aws_metadata(aws_response, response_context)
            
            response_data.result = Schema__AWS__S3__Delete__Result(
                deleted    = True                              ,
                version_id = aws_response.get('VersionId')
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
        return Schema__AWS__Response__S3__Delete_Object(
            response_context = response_context,
            response_data    = response_data
        )
    
    def setup_routes(self):         # Register all S3 routes.
        self.add_route_post  (self.list_buckets )
        self.add_route_post  (self.list_objects )
        self.add_route_post  (self.get_object   )
        self.add_route_post  (self.put_object   )
        self.add_route_post  (self.head_object  )
        self.add_route_delete(self.delete_object)
        return self
