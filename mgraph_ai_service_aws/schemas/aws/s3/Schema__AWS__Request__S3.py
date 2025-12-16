from typing                                                                 import Dict, Optional
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from mgraph_ai_service_aws.schemas.base.Schema__Request__Data               import Schema__Request__Data
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Request__Base      import Schema__AWS__Request__Base
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__AWS__S3__Bucket_Name import Safe_Str__AWS__S3__Bucket_Name
from mgraph_ai_service_aws.schemas.safe_str.aws.Safe_Str__AWS__S3__Key      import Safe_Str__AWS__S3__Key


# Request Data schemas (operation-specific payloads)

class Schema__Request__Data__S3__List_Buckets(Schema__Request__Data):
    """Request data for listing S3 buckets."""
    pass  # No parameters needed


class Schema__Request__Data__S3__List_Objects(Schema__Request__Data):
    """Request data for listing objects in a bucket."""
    bucket          : Safe_Str__AWS__S3__Bucket_Name
    prefix          : str = ''
    delimiter       : str = None
    max_keys        : int = 1000
    continuation_token : str = None


class Schema__Request__Data__S3__Get_Object(Schema__Request__Data):
    """Request data for getting an object."""
    bucket : Safe_Str__AWS__S3__Bucket_Name
    key    : Safe_Str__AWS__S3__Key


class Schema__Request__Data__S3__Put_Object(Schema__Request__Data):
    """Request data for putting an object."""
    bucket       : Safe_Str__AWS__S3__Bucket_Name
    key          : Safe_Str__AWS__S3__Key
    body         : str                          # Base64 encoded if binary
    content_type : str                          = 'application/octet-stream'
    metadata     : Dict[str, str]               = None


class Schema__Request__Data__S3__Head_Object(Schema__Request__Data):
    """Request data for getting object metadata."""
    bucket : Safe_Str__AWS__S3__Bucket_Name
    key    : Safe_Str__AWS__S3__Key


class Schema__Request__Data__S3__Delete_Object(Schema__Request__Data):
    """Request data for deleting an object."""
    bucket : Safe_Str__AWS__S3__Bucket_Name
    key    : Safe_Str__AWS__S3__Key


# Full Request schemas (credentials + request data)

class Schema__AWS__Request__S3__List_Buckets(Schema__AWS__Request__Base):
    """Full request for listing S3 buckets."""
    request_data : Schema__Request__Data__S3__List_Buckets = None


class Schema__AWS__Request__S3__List_Objects(Schema__AWS__Request__Base):
    """Full request for listing objects in a bucket."""
    request_data : Schema__Request__Data__S3__List_Objects


class Schema__AWS__Request__S3__Get_Object(Schema__AWS__Request__Base):
    """Full request for getting an object."""
    request_data : Schema__Request__Data__S3__Get_Object


class Schema__AWS__Request__S3__Put_Object(Schema__AWS__Request__Base):
    """Full request for putting an object."""
    request_data : Schema__Request__Data__S3__Put_Object


class Schema__AWS__Request__S3__Head_Object(Schema__AWS__Request__Base):
    """Full request for getting object metadata."""
    request_data : Schema__Request__Data__S3__Head_Object


class Schema__AWS__Request__S3__Delete_Object(Schema__AWS__Request__Base):
    """Full request for deleting an object."""
    request_data : Schema__Request__Data__S3__Delete_Object
