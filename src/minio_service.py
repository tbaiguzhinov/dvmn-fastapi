import aioboto3
from aiobotocore.config import AioConfig


class MinioService:
    def __init__(self):
        self.config = AioConfig(
            max_pool_connections=50,
            connect_timeout=10,
            read_timeout=30,
        )

    async def create_s3_client(self):
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url='http://localhost:9000',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            region_name='us-east-1',
            config=self.config,
        ) as s3_client:
            return s3_client

    async def upload_file(self, file_content: bytes):
        client = await self.create_s3_client()
        async with client as s3_client:
            upload_params = {
                'Bucket': 'my-public-bucket',
                'Key': 'index3.html',
                'Body': file_content,
                'ContentType': 'text/html',
                'ContentDisposition': 'inline',
            }
            await s3_client.put_object(**upload_params)
