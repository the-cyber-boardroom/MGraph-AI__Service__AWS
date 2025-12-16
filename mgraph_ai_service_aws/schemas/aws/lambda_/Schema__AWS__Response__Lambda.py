from typing                                                                     import List, Optional
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_aws.schemas.base.Schema__Response__Data                  import Schema__Response__Data
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response               import Schema__AWS__Response
from mgraph_ai_service_aws.schemas.aws.base.Schema__AWS__Response__Context      import Schema__AWS__Response__Context
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Schema__AWS__Lambda__Function__Summary
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Schema__AWS__Lambda__Configuration
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Schema__AWS__Lambda__Code__Location
from mgraph_ai_service_aws.schemas.aws.lambda_.Schema__AWS__Lambda__Data        import Schema__AWS__Lambda__Invoke__Result


# Response Data schemas (operation-specific payloads)

class Schema__Response__Data__Lambda__List(Schema__Response__Data):
    """Response data from listing Lambda functions."""
    functions   : List[Schema__AWS__Lambda__Function__Summary] = None
    next_marker : str = None


class Schema__Response__Data__Lambda__Get(Schema__Response__Data):
    """Response data from getting a Lambda function."""
    configuration : Schema__AWS__Lambda__Configuration = None
    code          : Schema__AWS__Lambda__Code__Location = None


class Schema__Response__Data__Lambda__Invoke(Schema__Response__Data):
    """Response data from invoking a Lambda function."""
    result : Schema__AWS__Lambda__Invoke__Result = None


class Schema__Response__Data__Lambda__Create(Schema__Response__Data):
    """Response data from creating a Lambda function."""
    configuration : Schema__AWS__Lambda__Configuration = None


class Schema__Response__Data__Lambda__Update(Schema__Response__Data):
    """Response data from updating a Lambda function."""
    configuration : Schema__AWS__Lambda__Configuration = None


class Schema__Response__Data__Lambda__Delete(Schema__Response__Data):
    """Response data from deleting a Lambda function."""
    deleted : bool = False


# Full Response schemas (context + response data)

class Schema__AWS__Response__Lambda__List(Schema__AWS__Response):
    """Full response for listing Lambda functions."""
    response_data : Schema__Response__Data__Lambda__List = None


class Schema__AWS__Response__Lambda__Get(Schema__AWS__Response):
    """Full response for getting a Lambda function."""
    response_data : Schema__Response__Data__Lambda__Get = None


class Schema__AWS__Response__Lambda__Invoke(Schema__AWS__Response):
    """Full response for invoking a Lambda function."""
    response_data : Schema__Response__Data__Lambda__Invoke = None


class Schema__AWS__Response__Lambda__Create(Schema__AWS__Response):
    """Full response for creating a Lambda function."""
    response_data : Schema__Response__Data__Lambda__Create = None


class Schema__AWS__Response__Lambda__Update(Schema__AWS__Response):
    """Full response for updating a Lambda function."""
    response_data : Schema__Response__Data__Lambda__Update = None


class Schema__AWS__Response__Lambda__Delete(Schema__AWS__Response):
    """Full response for deleting a Lambda function."""
    response_data : Schema__Response__Data__Lambda__Delete = None
