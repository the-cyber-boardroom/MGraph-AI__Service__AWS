from typing                                 import Dict, List, Optional
from osbot_utils.type_safe.Type_Safe        import Type_Safe


class Schema__AWS__S3__Bucket(Type_Safe):
    """S3 bucket information."""
    name          : str = None
    creation_date : str = None
    region        : str = None


class Schema__AWS__S3__Object(Type_Safe):
    """S3 object metadata."""
    key           : str = None
    last_modified : str = None
    etag          : str = None
    size          : int = 0
    storage_class : str = None
    owner         : str = None


class Schema__AWS__S3__Object__Content(Type_Safe):
    """S3 object with content."""
    body           : str                = None  # Base64 encoded if binary
    content_type   : str                = None
    content_length : int                = 0
    last_modified  : str                = None
    etag           : str                = None
    metadata       : Dict[str, str]     = None


class Schema__AWS__S3__Object__Head(Type_Safe):
    """S3 object metadata (from HEAD request)."""
    content_type   : str                = None
    content_length : int                = 0
    last_modified  : str                = None
    etag           : str                = None
    metadata       : Dict[str, str]     = None
    version_id     : str                = None


class Schema__AWS__S3__Put__Result(Type_Safe):
    """Result of S3 put operation."""
    etag       : str = None
    version_id : str = None


class Schema__AWS__S3__Delete__Result(Type_Safe):
    """Result of S3 delete operation."""
    deleted    : bool = False
    version_id : str  = None
