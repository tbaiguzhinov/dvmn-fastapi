import aioboto3

from env_settings import settings


class MinioService:
    def __init__(self, minio_client: aioboto3.Session.client):
        self.minio_client = minio_client

    async def upload_file(self, file_content: bytes, file_name: str, content_type: str):
        async with self.minio_client as s3_client:
            upload_params = {
                'Bucket': settings.minio.bucket,
                'Key': file_name,
                'Body': file_content,
                'ContentType': content_type,
                'ContentDisposition': 'inline',
            }
            await s3_client.put_object(**upload_params)
