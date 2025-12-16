"""Configuration for MGraph-AI Service AWS."""

import os


class Config:
    """Service configuration loaded from environment variables."""
    
    # Service metadata
    SERVICE_NAME    = os.getenv('SERVICE_NAME', 'mgraph-ai-service-aws')
    SERVICE_VERSION = os.getenv('SERVICE_VERSION', '0.7.0')
    
    # AWS defaults
    DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    # FastAPI settings
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    @classmethod
    def as_dict(cls):
        return {
            'service_name'   : cls.SERVICE_NAME   ,
            'service_version': cls.SERVICE_VERSION,
            'default_region' : cls.DEFAULT_REGION ,
            'debug'          : cls.DEBUG
        }


config = Config()
