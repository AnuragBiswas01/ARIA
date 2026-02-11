"""
ARIA Object Storage Configuration
Sets up the MinIO client for file storage.
"""
from minio import Minio
from config.settings import settings

def get_minio_client() -> Minio:
    """
    Returns a configured MinIO client.
    """
    client = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure
    )
    return client

def check_minio_connection() -> bool:
    """
    Verifies connection to MinIO and ensures the configured bucket exists.
    """
    try:
        client = get_minio_client()
        bucket_name = settings.minio_bucket_name
        
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Created MinIO bucket: {bucket_name}")
            
        return True
    except Exception as e:
        print(f"MinIO connection failed: {e}")
        return False
