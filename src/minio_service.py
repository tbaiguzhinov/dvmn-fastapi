import aioboto3
from aiobotocore.config import AioConfig

from env_settings import settings


class MinioService:
    def __init__(self):
        self.config = AioConfig(
            max_pool_connections=settings.minio.max_pool_connections,
            connect_timeout=settings.minio.connection_timeout,
            read_timeout=settings.minio.read_timeout,
        )

    async def create_s3_client(self):
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=settings.minio.api_endpoint,
            aws_access_key_id=settings.minio.login,
            aws_secret_access_key=settings.minio.password.get_secret_value(),
            region_name='us-east-1',
            config=self.config,
        ) as s3_client:
            return s3_client

    async def upload_file(self, file_content: bytes, file_name: str, content_type: str):
        client = await self.create_s3_client()
        async with client as s3_client:
            upload_params = {
                'Bucket': settings.minio.bucket,
                'Key': file_name,
                'Body': file_content,
                'ContentType': content_type,
                'ContentDisposition': 'inline',
            }
            await s3_client.put_object(**upload_params)
