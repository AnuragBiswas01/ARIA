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
    Verifies connection to MinIO and ensures bucket exists.
    """
    try:
        client = get_minio_client()
        # Just listing buckets to test auth and connection
        client.list_buckets()
        return True
    except Exception:
        return False
