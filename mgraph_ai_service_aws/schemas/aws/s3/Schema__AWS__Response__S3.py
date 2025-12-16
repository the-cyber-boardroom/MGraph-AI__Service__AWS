from typing                                                                 import List, Optional
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from mgraph_ai_service_aws.schemas.base.Schema__Response__Data              import Schema__Response__Data
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response           import Schema__AWS__Response
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response__Context  import Schema__AWS__Response__Context
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Bucket
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Object
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Object__Content
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Object__Head
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Put__Result
from mgraph_ai_service_aws.schemas.aws.s3.Schema__AWS__S3__Data             import Schema__AWS__S3__Delete__Result


# Response Data schemas (operation-specific payloads)

class Schema__Response__Data__S3__List_Buckets(Schema__Response__Data):
    """Response data from listing S3 buckets."""
    buckets : List[Schema__AWS__S3__Bucket] = None


class Schema__Response__Data__S3__List_Objects(Schema__Response__Data):
    """Response data from listing objects in a bucket."""
    objects            : List[Schema__AWS__S3__Object] = None
    common_prefixes    : List[str]                     = None  # For delimiter queries
    is_truncated       : bool                          = False
    next_continuation_token : str                      = None


class Schema__Response__Data__S3__Get_Object(Schema__Response__Data):
    """Response data from getting an object."""
    content : Schema__AWS__S3__Object__Content = None


class Schema__Response__Data__S3__Put_Object(Schema__Response__Data):
    """Response data from putting an object."""
    result : Schema__AWS__S3__Put__Result = None


class Schema__Response__Data__S3__Head_Object(Schema__Response__Data):
    """Response data from getting object metadata."""
    metadata : Schema__AWS__S3__Object__Head = None


class Schema__Response__Data__S3__Delete_Object(Schema__Response__Data):
    """Response data from deleting an object."""
    result : Schema__AWS__S3__Delete__Result = None


# Full Response schemas (context + response data)

class Schema__AWS__Response__S3__List_Buckets(Schema__AWS__Response):
    """Full response for listing S3 buckets."""
    response_data : Schema__Response__Data__S3__List_Buckets = None


class Schema__AWS__Response__S3__List_Objects(Schema__AWS__Response):
    """Full response for listing objects in a bucket."""
    response_data : Schema__Response__Data__S3__List_Objects = None


class Schema__AWS__Response__S3__Get_Object(Schema__AWS__Response):
    """Full response for getting an object."""
    response_data : Schema__Response__Data__S3__Get_Object = None


class Schema__AWS__Response__S3__Put_Object(Schema__AWS__Response):
    """Full response for putting an object."""
    response_data : Schema__Response__Data__S3__Put_Object = None


class Schema__AWS__Response__S3__Head_Object(Schema__AWS__Response):
    """Full response for getting object metadata."""
    response_data : Schema__Response__Data__S3__Head_Object = None


class Schema__AWS__Response__S3__Delete_Object(Schema__AWS__Response):
    """Full response for deleting an object."""
    response_data : Schema__Response__Data__S3__Delete_Object = None
